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
    Interactive setup for database integration.
    """
    print("\nSetting up a new database backend...")
    print("Database Integration Setup Wizard")
    print("=================================")
    
    print("\n📋 What is Database Integration?")
    print("--------------------------------")
    print("This feature allows you to store your God Mode memory files (.md files) in a database.")
    print("This is NOT for your application data, but for God Mode's own memory system.")
    print("Benefits include:")
    print("- Synchronize your God Mode memory across multiple computers")
    print("- Back up your AI's memory to prevent data loss")
    print("- Work offline with local storage options\n")

    while True:
        print("Choose setup type:")
        print("1) Set up a new backend")
        print("2) View/manage existing backends")
        print("3) Set up local SQLite database (offline mode)")
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
    print("\nChoose a database provider:")
    print("1) Supabase - Cloud database with free tier (recommended for syncing across devices)")
    print("2) Firebase - Cloud database by Google (coming soon)")
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
        print("\n📋 About Backend Names:")
        print("---------------------")
        print("You need to give this connection profile a name to identify it.")
        print("This is NOT your project name, but a label for this specific connection.")
        print("Examples: 'work', 'personal', 'macbook', 'home-pc', etc.")
        print("If you're not sure, 'main' or 'default' works fine.\n")
        
        backend_name = input("Enter a name for this connection profile: ")
        
        if not backend_name:
            print("Backend name cannot be empty. Using 'default'.")
            backend_name = "default"
            
        # Continue with Supabase setup as before
        # ... existing supabase setup code ...
        
    elif provider == "firebase":
        print("Firebase support coming soon!")
    elif provider == "custom":
        print("Custom API support coming soon!")
    else:
        print(f"Unknown provider: {provider}")

def setup_sqlite_backend():
    """Set up a local SQLite database backend"""
    print("\n📋 About SQLite Backend:")
    print("----------------------")
    print("SQLite is a file-based database stored on your computer.")
    print("Benefits:")
    print("- Works completely offline")
    print("- No account registration needed")
    print("- Perfect for single-device usage")
    print("Limitations:")
    print("- Cannot sync across multiple devices without manual file transfer")
    print("- No automatic cloud backup\n")
    
    print("\n📋 About Backend Names:")
    print("---------------------")
    print("You need to give this connection profile a name to identify it.")
    print("This is just a label for this specific connection.")
    print("Examples: 'local', 'offline', 'laptop', etc.")
    print("If you're not sure, 'local' works fine.\n")
    
    backend_name = input("Enter a name for this connection profile: ")
    
    if not backend_name:
        print("Backend name cannot be empty. Using 'local'.")
        backend_name = "local"
    
    # Continue with SQLite setup as before
    # ... existing sqlite setup code ...

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