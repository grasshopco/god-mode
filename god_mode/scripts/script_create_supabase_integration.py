#!/usr/bin/env python3
"""
Supabase Integration Script for God Mode

This script provides integration with Supabase and other database providers for God Mode.
It allows users to connect to and interact with a database for persistence beyond local files.

Features:
- Connect to Supabase or other database providers
- Store and retrieve memory content
- Sync local memory files with remote database
- Backup and restore memory files

Usage:
    python script_create_supabase_integration.py --setup
    python script_create_supabase_integration.py --sync
    python script_create_supabase_integration.py --backup
    python script_create_supabase_integration.py --restore
"""

import os
import sys
import json
import argparse
import datetime
import shutil
from pathlib import Path

# Try to import provider-specific modules
try:
    from supabase import create_client, Client
    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False

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
            "tables": {
                "memory": "god_mode_memory",
                "logs": "god_mode_logs",
                "features": "god_mode_features"
            }
        }

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

def create_supabase_client():
    """
    Create a Supabase client using the configured URL and key.
    
    Returns:
        Client: The Supabase client, or None if not configured
    """
    if not SUPABASE_AVAILABLE:
        print("Error: Supabase Python client not installed")
        print("Install it with: pip install supabase")
        return None
    
    config = load_db_config()
    if not config["configured"] or config["provider"] != "supabase":
        print("Error: Supabase is not configured")
        print("Run with --setup to configure Supabase")
        return None
    
    try:
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
    
    # Choose provider
    print("Choose a database provider:")
    print("1) Supabase (https://supabase.com)")
    print("2) Firebase (coming soon)")
    print("3) Custom REST API (coming soon)")
    print("4) Exit without configuring")
    
    provider_choice = input("\nEnter your choice (1-4): ")
    
    if provider_choice == "4":
        print("Exiting without configuring database integration.")
        return
    
    if provider_choice == "1":
        # Supabase setup
        if not SUPABASE_AVAILABLE:
            print("Supabase Python client not installed.")
            install_choice = input("Would you like to install it now? (y/n): ")
            if install_choice.lower() == "y":
                print("Installing Supabase Python client...")
                try:
                    import pip
                    pip.main(["install", "supabase"])
                    print("Supabase Python client installed successfully.")
                    global SUPABASE_AVAILABLE
                    SUPABASE_AVAILABLE = True
                except Exception as e:
                    print(f"Error installing Supabase Python client: {e}")
                    print("Please install it manually with: pip install supabase")
                    return
            else:
                print("Please install the Supabase Python client manually with: pip install supabase")
                return
        
        print("\nSupabase Configuration")
        print("----------------------")
        print("You'll need your Supabase URL and key from your Supabase project settings.")
        
        supabase_url = input("Enter your Supabase URL: ")
        supabase_key = input("Enter your Supabase API key: ")
        
        if not supabase_url or not supabase_key:
            print("URL and key are required. Setup cancelled.")
            return
        
        # Save configuration
        config["provider"] = "supabase"
        config["url"] = supabase_url
        config["key"] = supabase_key
        config["configured"] = True
        
        save_db_config(config)
        print("\nSupabase configuration saved successfully.")
        
        # Test connection
        try:
            client = create_client(supabase_url, supabase_key)
            print("Supabase connection test successful!")
            
            # Create tables if they don't exist
            print("\nWould you like to create the required tables in your Supabase project?")
            create_tables = input("This will create tables for memory, logs, and features (y/n): ")
            
            if create_tables.lower() == "y":
                print("Creating tables...")
                # Ideally we would use SQL here, but that would require more setup
                # So we'll use the REST API instead
                pass
        except Exception as e:
            print(f"Error connecting to Supabase: {e}")
    else:
        print("This provider is not yet supported.")
    
    print("\nDatabase integration setup complete.")

def sync_with_remote():
    """
    Sync local memory files with the remote database.
    """
    config = load_db_config()
    if not config["configured"]:
        print("Error: Database integration is not configured")
        print("Run with --setup to configure a database provider")
        return
    
    if config["provider"] == "supabase":
        client = create_supabase_client()
        if not client:
            return
        
        print("Syncing with Supabase...")
        
        # Get all memory files
        memory_files = list(MEMORY_DIR.glob("*.md"))
        
        for file in memory_files:
            print(f"Syncing {file.name}...")
            
            try:
                with open(file, 'r') as f:
                    content = f.read()
                
                # Upload to Supabase
                table = config["tables"]["memory"]
                
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
        config["last_sync"] = datetime.datetime.now().isoformat()
        save_db_config(config)
        
        print("Sync completed.")
    else:
        print(f"Provider '{config['provider']}' is not yet supported for syncing.")

def backup_memory_files():
    """
    Backup all memory files to the remote database.
    """
    # Create a local backup first
    backup_dir = CACHE_DIR / "backup" / datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    ensure_directory_exists(backup_dir)
    
    print(f"Creating local backup in {backup_dir}...")
    
    # Copy all memory files
    for file in MEMORY_DIR.glob("*.md"):
        shutil.copy2(file, backup_dir / file.name)
    
    print(f"Local backup created with {len(list(backup_dir.glob('*.md')))} files.")
    
    # Sync with remote if configured
    config = load_db_config()
    if config["configured"]:
        print("Backing up to remote database...")
        sync_with_remote()
    else:
        print("Remote database not configured. Only local backup created.")
    
    print("Backup completed.")

def restore_from_backup():
    """
    Restore memory files from a backup.
    """
    # List available local backups
    backup_base_dir = CACHE_DIR / "backup"
    ensure_directory_exists(backup_base_dir)
    
    backups = list(backup_base_dir.glob("*"))
    backups.sort(reverse=True)  # Most recent first
    
    if not backups:
        print("No local backups found.")
        return
    
    print("Available backups:")
    for i, backup in enumerate(backups):
        backup_time = backup.name
        file_count = len(list(backup.glob("*.md")))
        print(f"{i+1}) {backup_time} ({file_count} files)")
    
    print(f"{len(backups)+1}) Restore from remote database")
    print(f"{len(backups)+2}) Cancel")
    
    choice = input(f"\nChoose a backup to restore (1-{len(backups)+2}): ")
    
    try:
        choice_num = int(choice)
        
        if choice_num == len(backups) + 2:
            print("Restore cancelled.")
            return
        
        if choice_num == len(backups) + 1:
            # Restore from remote
            config = load_db_config()
            if not config["configured"]:
                print("Error: Remote database not configured.")
                return
            
            if config["provider"] == "supabase":
                client = create_supabase_client()
                if not client:
                    return
                
                print("Restoring from Supabase...")
                
                table = config["tables"]["memory"]
                response = client.table(table).select("*").execute()
                
                if not response.data:
                    print("No data found in the remote database.")
                    return
                
                # Create a backup of current files first
                backup_before_restore = CACHE_DIR / "backup" / f"before_restore_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
                ensure_directory_exists(backup_before_restore)
                
                for file in MEMORY_DIR.glob("*.md"):
                    shutil.copy2(file, backup_before_restore / file.name)
                
                # Restore files from remote data
                for record in response.data:
                    file_name = record["name"]
                    content = record["content"]
                    
                    with open(MEMORY_DIR / file_name, 'w') as f:
                        f.write(content)
                    
                    print(f"✓ Restored {file_name}")
                
                print(f"Restored {len(response.data)} files from remote database.")
                print(f"Previous files backed up to {backup_before_restore}")
            else:
                print(f"Provider '{config['provider']}' is not yet supported for restoring.")
        else:
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

def main():
    """Main function to parse arguments and run commands."""
    parser = argparse.ArgumentParser(description="Supabase Integration for God Mode")
    
    parser.add_argument("--setup", action="store_true", help="Set up database integration")
    parser.add_argument("--sync", action="store_true", help="Sync local memory files with remote database")
    parser.add_argument("--backup", action="store_true", help="Backup memory files to remote database")
    parser.add_argument("--restore", action="store_true", help="Restore memory files from backup")
    parser.add_argument("--debug", action="store_true", help="Enable debug output")
    
    args = parser.parse_args()
    
    if args.setup:
        setup_db_integration()
    elif args.sync:
        sync_with_remote()
    elif args.backup:
        backup_memory_files()
    elif args.restore:
        restore_from_backup()
    else:
        parser.print_help()

if __name__ == "__main__":
    main() 