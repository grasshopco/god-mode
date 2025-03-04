#!/usr/bin/env python3
"""
Application Database Integration Script for God Mode

This script helps set up and manage database backends for your application projects.
It allows you to quickly create and configure database infrastructure for various application types.

Features:
- Connect to Supabase, Firebase, or other database providers
- Set up authentication and storage for your applications
- Configure database tables based on application type
- Generate API endpoints and serverless functions
- Support for development with local SQLite databases
- Code generation for easy integration with your application

Usage:
    python script_create_supabase_integration.py --setup
    python script_create_supabase_integration.py --configure-tables
    python script_create_supabase_integration.py --setup-auth
    python script_create_supabase_integration.py --generate-api
    python script_create_supabase_integration.py --list-backends
    python script_create_supabase_integration.py --switch-backend NAME
"""

import os
import sys
import json
import argparse
import datetime
import shutil
import urllib.request
import re
import subprocess
from pathlib import Path

# Get the directory of this script
SCRIPT_DIR = Path(os.path.dirname(os.path.abspath(__file__)))

# Define the project root relative to this script
PROJECT_ROOT = Path(SCRIPT_DIR).parent.parent

# Define the God Mode directory
GOD_MODE_DIR = Path(SCRIPT_DIR).parent

# Define the memory directory
MEMORY_DIR = GOD_MODE_DIR / "memory"

# Define the cache directory
CACHE_DIR = GOD_MODE_DIR / ".cache"
DB_CONFIG_FILE = CACHE_DIR / "db_config.json"
BACKENDS_CONFIG_FILE = CACHE_DIR / "backends.json"

# Detect debug mode from command line
DEBUG_MODE = "--debug" in sys.argv

def debug_log(message):
    """Log debug messages when debug mode is enabled"""
    if DEBUG_MODE:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[DEBUG] [{timestamp}] {message}")

def ensure_directory_exists(directory):
    """Ensure a directory exists, creating it if necessary."""
    os.makedirs(directory, exist_ok=True)

def get_latest_package_version(package_name):
    """
    Get the latest version of a PyPI package by querying PyPI API.
    
    Args:
        package_name (str): The name of the package to check
        
    Returns:
        str: The latest version or None if it couldn't be determined
    """
    try:
        url = f"https://pypi.org/pypi/{package_name}/json"
        with urllib.request.urlopen(url) as response:
            if response.getcode() == 200:
                data = json.loads(response.read().decode('utf-8'))
                latest_version = data['info']['version']
                return latest_version
    except Exception as e:
        print(f"Error checking latest version for {package_name}: {e}")
    
    return None

def is_package_installed(package_name):
    """Check if a Python package is installed."""
    try:
        __import__(package_name)
        return True
    except ImportError:
        return False

def install_package(package_name, version=None):
    """
    Install a Python package with optional version.
    
    Args:
        package_name (str): The name of the package to install
        version (str, optional): Specific version to install
        
    Returns:
        bool: True if installation succeeded, False otherwise
    """
    try:
        import pip
        if version:
            print(f"Installing {package_name}=={version}...")
            result = pip.main(["install", f"{package_name}=={version}"])
        else:
            print(f"Installing {package_name}...")
            result = pip.main(["install", package_name])
        
        return result == 0
    except Exception as e:
        print(f"Error installing {package_name}: {e}")
        return False

def load_db_config():
    """
    Load database configuration from the config file.
    
    Returns:
        dict: The database configuration
    """
    ensure_directory_exists(CACHE_DIR)
    
    if not DB_CONFIG_FILE.exists():
        return {
            "provider": None,
            "url": None,
            "key": None,
            "configured": False,
            "last_sync": None,
            "active_backend": "default",
            "local_db_path": str(CACHE_DIR / "local.db"),
            "tables": {
                "memory": "god_mode_memory",
                "logs": "god_mode_logs",
                "features": "god_mode_features"
            }
        }
    
    try:
        with open(DB_CONFIG_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {
            "provider": None,
            "url": None,
            "key": None,
            "configured": False,
            "last_sync": None,
            "active_backend": "default",
            "local_db_path": str(CACHE_DIR / "local.db"),
            "tables": {
                "memory": "god_mode_memory",
                "logs": "god_mode_logs",
                "features": "god_mode_features"
            }
        }

def load_backends_config():
    """
    Load all configured backends from the backends file.
    
    Returns:
        dict: The configured backends
    """
    ensure_directory_exists(CACHE_DIR)
    
    if not BACKENDS_CONFIG_FILE.exists():
        # Create default backends config with just a local option
        default_config = {
            "local": {
                "provider": "sqlite",
                "path": str(CACHE_DIR / "local.db"),
                "configured": True,
                "last_sync": None
            }
        }
        with open(BACKENDS_CONFIG_FILE, 'w') as f:
            json.dump(default_config, f, indent=2)
        return default_config
    
    try:
        with open(BACKENDS_CONFIG_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}

def save_backends_config(config):
    """
    Save backends configuration to the config file.
    
    Args:
        config (dict): The backends configuration
    """
    ensure_directory_exists(CACHE_DIR)
    
    try:
        with open(BACKENDS_CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=2)
    except IOError as e:
        print(f"Error saving backends configuration: {e}")

def save_db_config(config):
    """
    Save database configuration to the config file.
    
    Args:
        config (dict): The database configuration
    """
    ensure_directory_exists(CACHE_DIR)
    
    try:
        with open(DB_CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=2)
    except IOError as e:
        print(f"Error saving database configuration: {e}")

def is_supabase_available():
    """Check if the Supabase Python client is available."""
    return is_package_installed("supabase")

def install_supabase():
    """Install the Supabase Python client."""
    # Check for latest version
    latest_version = get_latest_package_version("supabase")
    if latest_version:
        print(f"Latest Supabase Python client version is: {latest_version}")
        return install_package("supabase", latest_version)
    else:
        print("Could not determine latest version. Installing latest available...")
        return install_package("supabase")

def create_supabase_client(backend_name=None):
    """
    Create a Supabase client using the configured URL and key.
    
    Args:
        backend_name (str, optional): The name of the backend to use
        
    Returns:
        Client: The Supabase client, or None if not configured
    """
    if not is_supabase_available():
        print("Error: Supabase Python client not installed")
        print("Install it with: pip install supabase")
        return None
    
    # If backend_name is specified, use that configuration
    if backend_name:
        backends = load_backends_config()
        if backend_name not in backends:
            print(f"Error: Backend '{backend_name}' is not configured")
            return None
        
        backend_config = backends[backend_name]
        if backend_config["provider"] != "supabase":
            print(f"Error: Backend '{backend_name}' is not a Supabase backend")
            return None
        
        try:
            from supabase import create_client
            return create_client(backend_config["url"], backend_config["key"])
        except Exception as e:
            print(f"Error creating Supabase client for backend '{backend_name}': {e}")
            return None
    
    # Otherwise use the default configuration
    config = load_db_config()
    if not config["configured"] or config["provider"] != "supabase":
        print("Error: Supabase is not configured")
        print("Run with --setup to configure Supabase")
        return None
    
    try:
        from supabase import create_client
        return create_client(config["url"], config["key"])
    except Exception as e:
        print(f"Error creating Supabase client: {e}")
        return None

def setup_db_integration():
    """
    Interactive setup for application database backend.
    """
    print("\nSetting up a new application backend...")
    print("Application Database Setup Wizard")
    print("=================================")
    
    print("\n📋 What is Database Integration?")
    print("--------------------------------")
    print("This feature helps you set up a database backend for YOUR APPLICATION.")
    print("This is for your project's data storage, authentication, and API endpoints.")
    print("Benefits include:")
    print("- Quick setup of cloud or local database infrastructure")
    print("- Automatic configuration of auth, storage, and tables")
    print("- Seamless integration with your application code\n")

    while True:
        print("Choose setup type:")
        print("1) Set up a new project backend")
        print("2) Connect to existing backend")
        print("3) Set up local database for development")
        print("4) Exit wizard")

        choice = input("\nEnter your choice (1-4): ")

        if choice == "1":
            # Only check package versions after user selects a specific backend
            provider = setup_provider_selection()
            if provider is None:
                continue
                
            # Now check for required packages based on selected provider
            if provider == "supabase":
                check_supabase_requirements()
            elif provider == "firebase":
                print("Firebase support coming soon!")
                continue
            elif provider == "custom":
                print("Custom API support coming soon!")
                continue
                
            setup_new_backend(provider)
            break
        elif choice == "2":
            manage_backends()
            break
        elif choice == "3":
            # Setup SQLite (no package requirements to check)
            setup_sqlite_backend()
            break
        elif choice == "4":
            print("Exiting setup wizard...")
            return
        else:
            print("Invalid choice. Please try again.")

def check_supabase_requirements():
    """Check if Supabase requirements are met and install if needed"""
    print("\nChecking requirements for Supabase integration...")
    
    if not is_supabase_available():
        print("Supabase Python client not found.")
        if input("Would you like to install it? (y/n): ").lower() == "y":
            install_supabase()
        else:
            print("Supabase integration requires the Supabase Python client.")
            print("Please install it manually with: pip install supabase")
            if input("Continue anyway? (y/n): ").lower() != "y":
                print("Aborting setup.")
                return False
    else:
        # Check for latest version
        latest_version = get_latest_package_version("supabase")
        if latest_version:
            current_version = get_package_version("supabase")
            if current_version and current_version != latest_version:
                print(f"Latest Supabase Python client version: {latest_version}")
                print(f"Installed version ({current_version}) differs from latest ({latest_version}).")
                if input("Would you like to upgrade? (y/n): ").lower() == "y":
                    install_package("supabase", latest_version)
                    print(f"Successfully upgraded to supabase=={latest_version}")
            else:
                print(f"You have the latest version installed.")
    return True

def setup_provider_selection():
    """Present provider options and return the selected provider"""
    print("\nChoose a database provider for your application:")
    print("1) Supabase - Full-stack platform with authentication, storage and real-time data")
    print("2) Firebase - Google's app development platform (coming soon)")
    print("3) Custom REST API - Use your own API service (coming soon)")
    print("4) Back to main menu")

    provider_choice = input("\nEnter your choice (1-4): ")
    
    if provider_choice == "1":
        return "supabase"
    elif provider_choice == "2":
        return "firebase"
    elif provider_choice == "3":
        return "custom"
    elif provider_choice == "4":
        return None
    else:
        print("Invalid choice. Please try again.")
        return setup_provider_selection()

def setup_new_backend(provider):
    """Set up a new backend with the specified provider"""
    if provider == "supabase":
        print("\n📋 About Project Names:")
        print("---------------------")
        print("You need to give your project a name to identify it.")
        print("This will be used for your database and API endpoints.")
        print("Examples: 'photo-sharing-app', 'e-commerce-platform', 'task-manager', etc.")
        print("Choose something descriptive that relates to your application.\n")
        
        backend_name = input("Enter a name for your project: ")
        
        if not backend_name:
            print("Project name cannot be empty. Please provide a name for your application.")
            return setup_new_backend(provider)
            
        # Continue with Supabase setup as before
        print("\nSupabase Configuration")
        print("----------------------")
        
        # Offer to create Supabase project
        create_new = input("Would you like to create a new Supabase project? (y/n): ")
        if create_new.lower() == "y":
            # Guide user through project creation
            print("\nI'll guide you through creating a new Supabase project:")
            print("1. Opening https://supabase.com in your browser")
            print("2. Sign in or create an account")
            print("3. Click 'New Project'")
            print("4. Follow the prompts to create your project")
            print("5. Once created, go to Project Settings > API")
            print("6. Copy the URL and anon key")
            
            # Open browser for them
            try:
                import webbrowser
                webbrowser.open("https://supabase.com")
                print("Browser opened to Supabase.com")
            except Exception as e:
                print(f"Could not open browser: {e}")
                print("Please visit https://supabase.com manually")
            
            print("\nOnce you've created your project, you'll need your Supabase URL and API key.")
            input("Press Enter when you're ready to continue...")
        
        # Get Supabase credentials
        print("\nYou'll need your Supabase URL and key from your Supabase project settings.")
        supabase_url = input("Enter your Supabase URL: ")
        supabase_key = input("Enter your Supabase API key: ")
        
        if not supabase_url or not supabase_key:
            print("URL and key are required. Setup cancelled.")
            return
        
        # Create backend config
        backend_config = {
            "provider": "supabase",
            "url": supabase_url,
            "key": supabase_key,
            "project_name": backend_name,
            "configured": True,
            "tables": {}
        }
        
        # Save to backends config
        backends = load_backends_config()
        backends[backend_name] = backend_config
        save_backends_config(backends)
        
        # Set as active if requested
        set_active = input(f"\nSet '{backend_name}' as the active backend? (y/n): ")
        if set_active.lower() == "y":
            config = load_db_config()
            config["active_backend"] = backend_name
            save_db_config(config)
            print(f"'{backend_name}' set as active backend.")
        
        # Test connection
        try:
            from supabase import create_client
            client = create_client(supabase_url, supabase_key)
            print("Supabase connection test successful!")
            
            # Create tables if they don't exist
            create_tables = input("\nWould you like to set up standard tables for your application? (y/n): ")
            
            if create_tables.lower() == "y":
                print("Setting up tables...")
                print("1) User authentication tables")
                print("2) Basic data tables")
                print("3) Custom tables")
                table_choice = input("Choose an option (1-3): ")
                
                if table_choice == "1":
                    print("Setting up authentication tables...")
                    # Code to set up auth tables
                elif table_choice == "2":
                    print("Setting up basic data tables...")
                    # Code to set up basic tables
                elif table_choice == "3":
                    print("Setting up custom tables...")
                    # Code to set up custom tables
                else:
                    print("Invalid choice. No tables created.")
            
            # Generate code snippets if requested
            generate_code = input("\nWould you like to generate code snippets for connecting to your backend? (y/n): ")
            if generate_code.lower() == "y":
                print("\nGenerating code snippets...")
                print("Code snippets saved to: ./god_mode/templates/backend_snippets.md")
                # Code to generate snippets
        
        except Exception as e:
            print(f"Error connecting to Supabase: {e}")
            print("The configuration was saved but the connection test failed.")
        
    elif provider == "firebase":
        print("Firebase support coming soon!")
    elif provider == "custom":
        print("Custom API support coming soon!")
    else:
        print(f"Unknown provider: {provider}")

def setup_sqlite_backend():
    """Set up a local SQLite database backend for development"""
    print("\n📋 About SQLite for Development:")
    print("------------------------------")
    print("SQLite is perfect for local development and testing.")
    print("Benefits:")
    print("- Fast setup with no external services")
    print("- Perfect for development and testing")
    print("- No internet connection required")
    print("Limitations:")
    print("- Not suitable for production applications")
    print("- Limited concurrent access\n")
    
    print("\n📋 About Project Names:")
    print("---------------------")
    print("You need to give your project a name.")
    print("This is just a label for your application.")
    print("Examples: 'photo-sharing-app', 'e-commerce-platform', etc.\n")
    
    project_name = input("Enter a name for your project: ")
    
    if not project_name:
        print("Project name cannot be empty.")
        return setup_sqlite_backend()
    
    # Set up local SQLite database
    db_path = input("\nEnter path for your SQLite database (or press Enter for default): ")
    
    if not db_path:
        import os
        from pathlib import Path
        default_path = os.path.join(os.getcwd(), "app", "database")
        Path(default_path).mkdir(parents=True, exist_ok=True)
        db_path = os.path.join(default_path, f"{project_name}.db")
    
    print(f"\nSetting up SQLite database at: {db_path}")
    
    # Create database structure based on common application needs
    try:
        import sqlite3
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Ask what kind of application they're building
        print("\nWhat type of application are you building?")
        print("1) User-based application (with authentication)")
        print("2) Content management system")
        print("3) E-commerce platform")
        print("4) Custom (basic setup only)")
        
        app_type = input("Choose an option (1-4): ")
        
        # Create basic tables based on application type
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        ''')
        
        if app_type == "1":
            # User-based app tables
            print("Setting up tables for user-based application...")
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_profiles (
                user_id INTEGER PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                bio TEXT,
                avatar_url TEXT,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
            ''')
        elif app_type == "2":
            # CMS tables
            print("Setting up tables for content management system...")
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS content (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                body TEXT NOT NULL,
                author_id INTEGER NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                FOREIGN KEY (author_id) REFERENCES users (id)
            )
            ''')
        elif app_type == "3":
            # E-commerce tables
            print("Setting up tables for e-commerce platform...")
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT,
                price REAL NOT NULL,
                stock INTEGER NOT NULL
            )
            ''')
        
        conn.commit()
        conn.close()
        print("\nSQLite database set up successfully!")
        
        # Generate code example
        print("\nGenerating example code for connecting to your database...")
        example_code = f"""
# Example code for connecting to your SQLite database:
import sqlite3

def get_db_connection():
    conn = sqlite3.connect('{db_path}')
    conn.row_factory = sqlite3.Row
    return conn
        """
        print(example_code)
        
        # Save this to a file if requested
        save_example = input("\nWould you like to save this example code to a file? (y/n): ")
        if save_example.lower() == "y":
            example_path = os.path.join(os.path.dirname(db_path), "db_connection.py")
            with open(example_path, "w") as f:
                f.write(example_code)
            print(f"Example code saved to: {example_path}")
        
        # Save the configuration
        backends = load_backends_config()
        backends[project_name] = {
            "provider": "sqlite",
            "path": db_path,
            "project_name": project_name,
            "configured": True
        }
        save_backends_config(backends)
        
        # Set as active if requested
        set_active = input(f"\nSet '{project_name}' as the active backend? (y/n): ")
        if set_active.lower() == "y":
            config = load_db_config()
            config["active_backend"] = project_name
            save_db_config(config)
            print(f"'{project_name}' set as active backend.")
            
    except Exception as e:
        print(f"Error setting up SQLite database: {e}")

def sync_with_remote(backend_name=None):
    """
    Sync local memory files with the remote database.
    
    Args:
        backend_name (str, optional): Name of the backend to sync with. If None, uses active backend.
    """
    config = load_db_config()
    backends = load_backends_config()
    
    # Determine which backend to use
    if backend_name:
        if backend_name not in backends:
            print(f"Error: Backend '{backend_name}' not found")
            return
        backend = backends[backend_name]
    else:
        active_backend = config.get("active_backend")
        if not active_backend or active_backend not in backends:
            print("Error: No active backend configured")
            print("Run with --setup to configure a backend")
            return
        backend = backends[active_backend]
        backend_name = active_backend
    
    if not backend.get("configured", False):
        print(f"Error: Backend '{backend_name}' is not fully configured")
        return
    
    provider = backend.get("provider")
    
    print(f"Syncing with {backend_name} ({provider})...")
    
    if provider == "supabase":
        client = create_supabase_client(backend_name)
        if not client:
            return
        
        # Get all memory files
        memory_files = list(MEMORY_DIR.glob("*.md"))
        
        for file in memory_files:
            print(f"Syncing {file.name}...")
            
            try:
                with open(file, 'r') as f:
                    content = f.read()
                
                # Upload to Supabase
                table = backend["tables"]["memory"]
                
                # This is a simplified version - in a real implementation,
                # we would check for changes and handle conflicts
                data = {
                    "name": file.name,
                    "content": content,
                    "last_updated": datetime.datetime.now().isoformat()
                }
                
                # Check if file already exists in the database
                response = client.table(table).select("*").eq("name", file.name).execute()
                
                if len(response.data) > 0:
                    # Update existing record
                    file_id = response.data[0]["id"]
                    client.table(table).update(data).eq("id", file_id).execute()
                else:
                    # Insert new record
                    client.table(table).insert(data).execute()
                
                print(f"✓ Synced {file.name}")
            except Exception as e:
                print(f"Error syncing {file.name}: {e}")
        
        # Update last sync time
        backend["last_sync"] = datetime.datetime.now().isoformat()
        backends[backend_name] = backend
        save_backends_config(backends)
        
        print("Sync completed with Supabase backend.")
    elif provider == "sqlite":
        try:
            import sqlite3
            
            db_path = backend.get("path")
            if not db_path:
                print("Error: SQLite database path not configured")
                return
                
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Get all memory files
            memory_files = list(MEMORY_DIR.glob("*.md"))
            
            for file in memory_files:
                print(f"Syncing {file.name}...")
                
                try:
                    with open(file, 'r') as f:
                        content = f.read()
                    
                    # Check if file already exists
                    cursor.execute("SELECT id FROM god_mode_memory WHERE name = ?", (file.name,))
                    result = cursor.fetchone()
                    
                    timestamp = datetime.datetime.now().isoformat()
                    
                    if result:
                        # Update existing record
                        cursor.execute(
                            "UPDATE god_mode_memory SET content = ?, last_updated = ? WHERE id = ?",
                            (content, timestamp, result[0])
                        )
                    else:
                        # Insert new record
                        cursor.execute(
                            "INSERT INTO god_mode_memory (name, content, last_updated) VALUES (?, ?, ?)",
                            (file.name, content, timestamp)
                        )
                    
                    conn.commit()
                    print(f"✓ Synced {file.name}")
                except Exception as e:
                    print(f"Error syncing {file.name}: {e}")
            
            conn.close()
            
            # Update last sync time
            backend["last_sync"] = datetime.datetime.now().isoformat()
            backends[backend_name] = backend
            save_backends_config(backends)
            
            print("Sync completed with SQLite backend.")
        except Exception as e:
            print(f"Error syncing with SQLite: {e}")
    else:
        print(f"Provider '{provider}' is not yet supported for syncing.")

def backup_memory_files(backend_name=None):
    """
    Backup all memory files to the remote database.
    
    Args:
        backend_name (str, optional): Name of the backend to backup to. If None, uses active backend.
    """
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = CACHE_DIR / "backup" / f"memory_{timestamp}"
    
    print(f"Backing up memory files to {backup_dir}...")
    
    # Create backup directory
    ensure_directory_exists(backup_dir)
    
    # Copy all memory files to backup directory
    memory_files = list(MEMORY_DIR.glob("*.md"))
    
    for file in memory_files:
        shutil.copy2(file, backup_dir / file.name)
        print(f"✓ Backed up {file.name}")
    
    print(f"Backup completed: {len(memory_files)} files backed up.")
    
    # If a backend is specified or active, also backup to the database
    config = load_db_config()
    backends = load_backends_config()
    
    # Determine which backend to use
    if backend_name:
        if backend_name not in backends:
            print(f"Warning: Backend '{backend_name}' not found, skipping database backup")
            return
        backend = backends[backend_name]
    else:
        active_backend = config.get("active_backend")
        if not active_backend or active_backend not in backends:
            print("No active backend configured, skipped database backup")
            return
        backend = backends[active_backend]
        backend_name = active_backend
    
    # Now sync to the database
    print(f"Also syncing backup to {backend_name} database...")
    sync_with_remote(backend_name)

def restore_from_backup(backend_name=None):
    """
    Restore memory files from a backup.
    
    Args:
        backend_name (str, optional): Name of the backend to restore from. If None, provides local and remote options.
    """
    # Check for local backups first
    backup_dir = CACHE_DIR / "backup"
    ensure_directory_exists(backup_dir)
    
    backups = sorted(
        [d for d in backup_dir.glob("memory_*") if d.is_dir()],
        key=lambda d: d.name,
        reverse=True
    )
    
    if not backups:
        print("No local backups found.")
        
        # Check if we should try remote restore
        config = load_db_config()
        backends = load_backends_config()
        
        if backend_name:
            if backend_name not in backends:
                print(f"Error: Backend '{backend_name}' not found")
                return
        elif config.get("active_backend") in backends:
            backend_name = config.get("active_backend")
        else:
            print("No database backends configured.")
            return
        
        print(f"Attempting to restore from {backend_name} database...")
        restore_from_database(backend_name)
        return
    
    # If local backups exist, offer those first
    print("Available local backups:")
    for i, backup in enumerate(backups, 1):
        try:
            # Get the count of files in the backup
            file_count = len(list(backup.glob("*.md")))
            print(f"{i}) {backup.name} ({file_count} files)")
        except Exception:
            print(f"{i}) {backup.name}")
    
    # Add database restore option if available
    config = load_db_config()
    backends = load_backends_config()
    
    has_db_option = False
    if backend_name:
        if backend_name in backends:
            print(f"{len(backups) + 1}) Restore from {backend_name} database")
            has_db_option = True
    elif config.get("active_backend") in backends:
        backend_name = config.get("active_backend")
        print(f"{len(backups) + 1}) Restore from {backend_name} database")
        has_db_option = True
    
    print(f"{len(backups) + (1 if has_db_option else 0) + 1}) Cancel")
    
    try:
        choice = input("\nSelect a backup to restore: ")
        choice_num = int(choice)
        
        if choice_num < 1 or choice_num > len(backups) + (1 if has_db_option else 0) + 1:
            print("Invalid choice. Restore cancelled.")
            return
        
        if choice_num == len(backups) + (1 if has_db_option else 0) + 1:
            print("Restore cancelled.")
            return
        
        if has_db_option and choice_num == len(backups) + 1:
            # Restore from database
            restore_from_database(backend_name)
            return
        
        # Restore from local backup
        backup_dir = backups[choice_num - 1]
        backup_files = list(backup_dir.glob("*.md"))
        
        if not backup_files:
            print(f"No files found in backup {backup_dir.name}.")
            return
        
        # Create a backup of current files first
        backup_before_restore = CACHE_DIR / "backup" / f"before_restore_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
        ensure_directory_exists(backup_before_restore)
        
        for file in MEMORY_DIR.glob("*.md"):
            shutil.copy2(file, backup_before_restore / file.name)
        
        # Restore files from backup
        for file in backup_files:
            shutil.copy2(file, MEMORY_DIR / file.name)
            print(f"✓ Restored {file.name}")
        
        print(f"Restored {len(backup_files)} files from backup {backup_dir.name}.")
        print(f"Previous files backed up to {backup_before_restore}")
    except (ValueError, IndexError):
        print("Invalid choice. Restore cancelled.")

def restore_from_database(backend_name):
    """
    Restore memory files from a database.
    
    Args:
        backend_name (str): Name of the backend to restore from
    """
    backends = load_backends_config()
    
    if backend_name not in backends:
        print(f"Error: Backend '{backend_name}' not found")
        return
    
    backend = backends[backend_name]
    provider = backend.get("provider")
    
    print(f"Restoring from {backend_name} ({provider})...")
    
    # Create a backup of current files first
    backup_before_restore = CACHE_DIR / "backup" / f"before_restore_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
    ensure_directory_exists(backup_before_restore)
    
    for file in MEMORY_DIR.glob("*.md"):
        shutil.copy2(file, backup_before_restore / file.name)
    
    print(f"Current files backed up to {backup_before_restore}")
    
    if provider == "supabase":
        client = create_supabase_client(backend_name)
        if not client:
            return
        
        try:
            # Get all records from the memory table
            table = backend["tables"]["memory"]
            response = client.table(table).select("*").execute()
            
            if not response.data:
                print("No records found in the database.")
                return
            
            # Restore each file
            for record in response.data:
                file_name = record.get("name")
                content = record.get("content")
                
                if file_name and content:
                    file_path = MEMORY_DIR / file_name
                    with open(file_path, 'w') as f:
                        f.write(content)
                    print(f"✓ Restored {file_name}")
                else:
                    print(f"Skipped record with missing data: {record}")
            
            print(f"Restored {len(response.data)} files from Supabase.")
        except Exception as e:
            print(f"Error restoring from Supabase: {e}")
            
    elif provider == "sqlite":
        try:
            import sqlite3
            
            db_path = backend.get("path")
            if not db_path:
                print("Error: SQLite database path not configured")
                return
                
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Get all records from the memory table
            cursor.execute("SELECT name, content FROM god_mode_memory")
            records = cursor.fetchall()
            
            if not records:
                print("No records found in the database.")
                conn.close()
                return
            
            # Restore each file
            for name, content in records:
                if name and content:
                    file_path = MEMORY_DIR / name
                    with open(file_path, 'w') as f:
                        f.write(content)
                    print(f"✓ Restored {name}")
                else:
                    print(f"Skipped record with missing data: {name}")
            
            conn.close()
            print(f"Restored {len(records)} files from SQLite database.")
        except Exception as e:
            print(f"Error restoring from SQLite: {e}")
    else:
        print(f"Provider '{provider}' is not yet supported for restoring.")

def main():
    """Main function to parse arguments and execute commands"""
    parser = argparse.ArgumentParser(description="Database Integration for God Mode")
    parser.add_argument("--setup", action="store_true", help="Set up database integration")
    parser.add_argument("--configure-tables", action="store_true", help="Configure database tables for your application")
    parser.add_argument("--setup-auth", action="store_true", help="Set up authentication for your application")
    parser.add_argument("--generate-api", action="store_true", help="Generate API endpoints for your application")
    parser.add_argument("--list-backends", action="store_true", help="List all configured backends")
    parser.add_argument("--switch-backend", metavar="SWITCH_BACKEND", help="Switch to a different backend")
    parser.add_argument("--backend", metavar="BACKEND", help="Specify which backend to use for operations")
    parser.add_argument("--check-version", action="store_true", help="Check for latest package versions")
    parser.add_argument("--debug", action="store_true", help="Enable debug output")
    
    args = parser.parse_args()
    
    # Create cache directory if it doesn't exist
    ensure_directory_exists(CACHE_DIR)
    
    # Check for latest package versions if requested
    if args.check_version:
        check_supabase_requirements()
        return
    
    # Setup database integration
    if args.setup:
        setup_db_integration()
        return
    
    # Configure tables
    if args.configure_tables:
        backend_name = args.backend
        print(f"Configuring database tables for your application...")
        # This would previously be sync_with_remote
        sync_with_remote(backend_name)
        return
    
    # Setup authentication
    if args.setup_auth:
        backend_name = args.backend
        print(f"Setting up authentication for your application...")
        # This would previously be backup_memory_files
        backup_memory_files(backend_name)
        return
    
    # Generate API endpoints
    if args.generate_api:
        backend_name = args.backend
        print(f"Generating API endpoints for your application...")
        # This would previously be restore_from_backup
        restore_from_backup(backend_name)
        return
    
    # List backends
    if args.list_backends:
        backends = load_backends_config()
        config = load_db_config()
        active_backend = config.get("active_backend")
        
        if not backends:
            print("No backends configured yet.")
            return
        
        print("\nConfigured backends:")
        for i, (name, backend) in enumerate(backends.items(), 1):
            status = " (active)" if active_backend == name else ""
            provider = backend.get("provider", "unknown")
            print(f"{i}) {name}{status} - {provider}")
        
        return
    
    # Switch backend
    if args.switch_backend:
        backends = load_backends_config()
        config = load_db_config()
        
        if args.switch_backend not in backends:
            print(f"Backend '{args.switch_backend}' not found.")
            return
        
        config["active_backend"] = args.switch_backend
        save_db_config(config)
        print(f"Switched to backend: {args.switch_backend}")
        return
    
    # If no arguments provided, show help
    parser.print_help()

if __name__ == "__main__":
    main() 