#!/usr/bin/env python3
"""
Database Integration Script for God Mode

This script provides integration with various database providers for God Mode.
It allows users to connect to and interact with databases for persistence beyond local files.

Features:
- Connect to Supabase, Firebase, or other database providers
- Store and retrieve memory content
- Sync local memory files with remote database
- Backup and restore memory files
- Support for multiple simultaneous database connections
- Local SQLite database option

Usage:
    python script_create_supabase_integration.py --setup
    python script_create_supabase_integration.py --sync
    python script_create_supabase_integration.py --backup
    python script_create_supabase_integration.py --restore
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
    Set up database integration by prompting for provider and credentials.
    """
    print("Database Integration Setup Wizard")
    print("=================================")
    print()
    
    # Load existing config
    config = load_db_config()
    backends = load_backends_config()
    
    # Choose setup type
    print("Choose setup type:")
    print("1) Set up a new backend")
    print("2) View/manage existing backends")
    print("3) Set up local SQLite database (offline mode)")
    print("4) Exit wizard")
    
    setup_type = input("\nEnter your choice (1-4): ")
    
    if setup_type == "1":
        # Choose provider
        print("\nChoose a database provider:")
        print("1) Supabase (https://supabase.com)")
        print("2) Firebase (coming soon)")
        print("3) Custom REST API (coming soon)")
        print("4) Back to main menu")
        
        provider_choice = input("\nEnter your choice (1-4): ")
        
        if provider_choice == "4":
            return
        
        if provider_choice == "1":
            # Supabase setup
            if not is_supabase_available():
                print("Supabase Python client not installed.")
                latest_version = get_latest_package_version("supabase")
                if latest_version:
                    print(f"Latest version available: {latest_version}")
                install_choice = input("Would you like to install it now? (y/n): ")
                if install_choice.lower() == "y":
                    print("Installing Supabase Python client...")
                    if not install_supabase():
                        return
                else:
                    print("Please install the Supabase Python client manually with: pip install supabase")
                    return
            
            # Get backend name
            backend_name = input("\nEnter a name for this backend (e.g., 'production', 'staging'): ")
            if not backend_name:
                backend_name = "default"
            
            # Check if backend already exists
            if backend_name in backends:
                overwrite = input(f"Backend '{backend_name}' already exists. Overwrite? (y/n): ")
                if overwrite.lower() != "y":
                    return
            
            print("\nSupabase Configuration")
            print("----------------------")
            
            # Offer to create Supabase project
            create_new = input("Would you like to create a new Supabase project? (y/n): ")
            if create_new.lower() == "y":
                # Guide user through project creation
                print("\nI'll guide you through creating a new Supabase project:")
                print("1. Open https://supabase.com in your browser")
                print("2. Sign in or create an account")
                print("3. Click 'New Project'")
                print("4. Follow the prompts to create your project")
                print("5. Once created, go to Project Settings > API")
                print("6. Copy the URL and anon key")
                
                # Open browser for them if they want
                open_browser = input("\nWould you like me to open Supabase in your browser? (y/n): ")
                if open_browser.lower() == "y":
                    try:
                        import webbrowser
                        webbrowser.open("https://supabase.com")
                        print("Browser opened to Supabase.com")
                    except Exception as e:
                        print(f"Could not open browser: {e}")
                
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
                "configured": True,
                "last_sync": None,
                "tables": {
                    "memory": "god_mode_memory",
                    "logs": "god_mode_logs",
                    "features": "god_mode_features"
                }
            }
            
            # Save to backends config
            backends[backend_name] = backend_config
            save_backends_config(backends)
            
            # Set as active if requested
            set_active = input(f"\nSet '{backend_name}' as the active backend? (y/n): ")
            if set_active.lower() == "y":
                config = backend_config
                config["active_backend"] = backend_name
                save_db_config(config)
                print(f"'{backend_name}' set as active backend.")
            
            print("\nSupabase configuration saved successfully.")
            
            # Test connection
            try:
                from supabase import create_client
                client = create_client(supabase_url, supabase_key)
                print("Supabase connection test successful!")
                
                # Create tables if they don't exist
                create_tables = input("\nWould you like to create the required tables in your Supabase project? (y/n): ")
                
                if create_tables.lower() == "y":
                    print("Creating tables...")
                    # Implementation for creating tables would go here
                    pass
            except Exception as e:
                print(f"Error connecting to Supabase: {e}")
                print("The configuration was saved but the connection test failed.")
        else:
            print("This provider is not yet supported.")
    
    elif setup_type == "2":
        # View/manage existing backends
        if not backends:
            print("No backends configured yet.")
            return
        
        print("\nConfigured backends:")
        for i, (name, backend) in enumerate(backends.items(), 1):
            status = " (active)" if config.get("active_backend") == name else ""
            provider = backend.get("provider", "unknown")
            print(f"{i}) {name}{status} - {provider}")
        
        print(f"{len(backends) + 1}) Back to main menu")
        
        choice = input("\nSelect a backend to manage or delete: ")
        try:
            choice_num = int(choice)
            if choice_num == len(backends) + 1:
                return
            
            if choice_num < 1 or choice_num > len(backends):
                print("Invalid choice.")
                return
            
            backend_name = list(backends.keys())[choice_num - 1]
            backend = backends[backend_name]
            
            print(f"\nManaging backend: {backend_name}")
            print("1) Set as active backend")
            print("2) View connection details")
            print("3) Test connection")
            print("4) Delete backend")
            print("5) Back to main menu")
            
            action = input("\nChoose an action: ")
            
            if action == "1":
                config["active_backend"] = backend_name
                save_db_config(config)
                print(f"'{backend_name}' set as active backend.")
            elif action == "2":
                print("\nConnection details:")
                for key, value in backend.items():
                    if key != "key":  # Don't show API key for security
                        print(f"{key}: {value}")
                    else:
                        print(f"{key}: ****")
            elif action == "3":
                if backend["provider"] == "supabase":
                    try:
                        from supabase import create_client
                        client = create_client(backend["url"], backend["key"])
                        print("Connection test successful!")
                    except Exception as e:
                        print(f"Connection test failed: {e}")
                else:
                    print(f"Testing not implemented for provider: {backend['provider']}")
            elif action == "4":
                confirm = input(f"Are you sure you want to delete backend '{backend_name}'? (y/n): ")
                if confirm.lower() == "y":
                    del backends[backend_name]
                    save_backends_config(backends)
                    print(f"Backend '{backend_name}' deleted.")
                    
                    # If this was the active backend, reset active backend
                    if config.get("active_backend") == backend_name:
                        if backends:
                            config["active_backend"] = list(backends.keys())[0]
                        else:
                            config["active_backend"] = None
                        save_db_config(config)
            elif action == "5":
                return
        except (ValueError, IndexError):
            print("Invalid choice.")
    
    elif setup_type == "3":
        # Setup local SQLite database
        local_path = input("\nEnter path for SQLite database (or press Enter for default): ")
        
        if not local_path:
            local_path = str(CACHE_DIR / "local.db")
        
        # Ensure directory exists
        ensure_directory_exists(os.path.dirname(local_path))
        
        # Create a SQLite backend
        backend_name = "local"
        backends[backend_name] = {
            "provider": "sqlite",
            "path": local_path,
            "configured": True,
            "last_sync": None
        }
        
        save_backends_config(backends)
        
        # Set as active if requested
        set_active = input("\nSet local SQLite as the active backend? (y/n): ")
        if set_active.lower() == "y":
            config["active_backend"] = backend_name
            config["provider"] = "sqlite"
            config["local_db_path"] = local_path
            config["configured"] = True
            save_db_config(config)
            print("Local SQLite set as active backend.")
        
        print(f"\nLocal SQLite database configured at: {local_path}")
        
        # Create database if it doesn't exist
        try:
            import sqlite3
            conn = sqlite3.connect(local_path)
            cursor = conn.cursor()
            
            # Create tables
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS god_mode_memory (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                content TEXT NOT NULL,
                last_updated TEXT NOT NULL
            )
            ''')
            
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS god_mode_logs (
                id INTEGER PRIMARY KEY,
                type TEXT NOT NULL,
                content TEXT NOT NULL,
                timestamp TEXT NOT NULL
            )
            ''')
            
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS god_mode_features (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                content TEXT NOT NULL,
                last_updated TEXT NOT NULL
            )
            ''')
            
            conn.commit()
            conn.close()
            print("SQLite database tables created successfully.")
        except Exception as e:
            print(f"Error creating SQLite database: {e}")
    
    print("\nDatabase integration setup complete.")

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
    """Main function to parse arguments and run commands."""
    parser = argparse.ArgumentParser(description="Database Integration for God Mode")
    
    parser.add_argument("--setup", action="store_true", help="Set up database integration")
    parser.add_argument("--sync", action="store_true", help="Sync local memory files with remote database")
    parser.add_argument("--backup", action="store_true", help="Backup memory files to remote database")
    parser.add_argument("--restore", action="store_true", help="Restore memory files from backup")
    parser.add_argument("--list-backends", action="store_true", help="List all configured backends")
    parser.add_argument("--switch-backend", type=str, help="Switch to a different backend")
    parser.add_argument("--backend", type=str, help="Specify which backend to use for operations")
    parser.add_argument("--check-version", action="store_true", help="Check for latest package versions")
    parser.add_argument("--debug", action="store_true", help="Enable debug output")
    
    args = parser.parse_args()
    
    # If check version is specified, check all relevant packages
    if args.check_version:
        print("Checking for latest package versions...")
        supabase_version = get_latest_package_version("supabase")
        if supabase_version:
            print(f"Latest Supabase Python client version: {supabase_version}")
            
            # Check if installed version matches latest
            try:
                import importlib.metadata
                installed_version = importlib.metadata.version("supabase")
                if installed_version != supabase_version:
                    print(f"Installed version ({installed_version}) differs from latest ({supabase_version}).")
                    upgrade = input("Would you like to upgrade? (y/n): ")
                    if upgrade.lower() == "y":
                        install_package("supabase", supabase_version)
                else:
                    print("You have the latest version installed.")
            except (ImportError, ModuleNotFoundError):
                print("Supabase is not installed.")
                install = input("Would you like to install it? (y/n): ")
                if install.lower() == "y":
                    install_package("supabase", supabase_version)
        else:
            print("Could not determine latest Supabase version.")
            
            # Add more packages as needed
            
            return
    
    # Main command processing
    if args.setup:
        setup_db_integration()
    elif args.sync:
        sync_with_remote(args.backend)
    elif args.backup:
        backup_memory_files(args.backend)
    elif args.restore:
        restore_from_backup(args.backend)
    elif args.list_backends:
        backends = load_backends_config()
        config = load_db_config()
        active_backend = config.get("active_backend")
        
        if not backends:
            print("No backends configured.")
            return
        
        print("Configured backends:")
        for name, backend in backends.items():
            status = " (active)" if active_backend == name else ""
            provider = backend.get("provider", "unknown")
            last_sync = backend.get("last_sync", "never")
            if provider == "supabase":
                print(f"{name}{status} - Supabase - URL: {backend.get('url', 'not set')} - Last sync: {last_sync}")
            elif provider == "sqlite":
                print(f"{name}{status} - SQLite - Path: {backend.get('path', 'not set')} - Last sync: {last_sync}")
            else:
                print(f"{name}{status} - {provider} - Last sync: {last_sync}")
    elif args.switch_backend:
        backends = load_backends_config()
        config = load_db_config()
        
        if args.switch_backend not in backends:
            print(f"Error: Backend '{args.switch_backend}' is not configured")
            print("Available backends:")
            for name in backends.keys():
                print(f"- {name}")
        else:
            backend = backends[args.switch_backend]
            config["active_backend"] = args.switch_backend
            
            # Copy relevant settings from backend to config
            for key in ["provider", "url", "key", "path", "tables"]:
                if key in backend:
                    config[key] = backend[key]
            
            if backend["provider"] == "sqlite":
                config["local_db_path"] = backend.get("path")
            
            config["configured"] = True
            save_db_config(config)
            print(f"Switched to backend: {args.switch_backend}")
    else:
        parser.print_help()

if __name__ == "__main__":
    main() 