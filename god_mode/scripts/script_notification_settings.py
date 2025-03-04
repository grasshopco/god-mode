#!/usr/bin/env python3
"""
Notification Settings Script

This script allows users to manage notification settings for God Mode.
Users can enable/disable desktop notifications and sound effects.

Usage:
    python script_notification_settings.py --list
    python script_notification_settings.py --toggle-sound
    python script_notification_settings.py --toggle-notifications
    python script_notification_settings.py --enable-all
    python script_notification_settings.py --disable-all
    python script_notification_settings.py --test
"""

import os
import sys
import json
import argparse
from pathlib import Path

# Get the directory of this script
SCRIPT_DIR = Path(os.path.dirname(os.path.abspath(__file__)))

# Define paths
PROJECT_ROOT = SCRIPT_DIR.parent.parent
GOD_MODE_DIR = SCRIPT_DIR.parent
CACHE_DIR = GOD_MODE_DIR / ".cache"
CONFIG_FILE = CACHE_DIR / "notification_config.json"

# Try to import from the message router for consistency
try:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, script_dir)
    from script_message_router import (
        toggle_notification_settings, 
        get_notification_settings,
        send_notification,
        ensure_directory_exists
    )
    IMPORTED = True
except ImportError:
    IMPORTED = False
    
    # Fallback implementations if import fails
    def ensure_directory_exists(directory):
        """Ensure a directory exists, creating it if necessary."""
        os.makedirs(directory, exist_ok=True)

    def get_notification_settings():
        """
        Get the current notification settings.
        
        Returns:
            dict: The current notification settings
        """
        # Default settings
        settings = {
            "sound_enabled": True,
            "notifications_enabled": True
        }
        
        if CONFIG_FILE.exists():
            try:
                with open(CONFIG_FILE, 'r') as f:
                    settings.update(json.load(f))
            except (json.JSONDecodeError, IOError):
                pass
        
        return settings

    def toggle_notification_settings(sound_enabled=None, notifications_enabled=None):
        """
        Toggle notification settings.
        
        Args:
            sound_enabled (bool, optional): Whether to enable sound effects
            notifications_enabled (bool, optional): Whether to enable desktop notifications
            
        Returns:
            dict: The current notification settings
        """
        ensure_directory_exists(CACHE_DIR)
        
        # Load current settings
        settings = get_notification_settings()
        
        # Update settings if provided
        if sound_enabled is not None:
            settings["sound_enabled"] = sound_enabled
        
        if notifications_enabled is not None:
            settings["notifications_enabled"] = notifications_enabled
        
        # Save settings
        try:
            with open(CONFIG_FILE, 'w') as f:
                json.dump(settings, f, indent=2)
        except IOError as e:
            print(f"Error: Failed to save notification settings: {e}")
        
        return settings

    def send_notification(title, message):
        """Simple fallback to print notifications if import fails."""
        print(f"\n[NOTIFICATION] {title}: {message}")
        # Try to play a sound on macOS
        if sys.platform == 'darwin':
            try:
                import subprocess
                subprocess.run(['afplay', '/System/Library/Sounds/Purr.aiff'], 
                              stderr=subprocess.DEVNULL,
                              stdout=subprocess.DEVNULL)
            except:
                pass

def list_settings():
    """List current notification settings."""
    settings = get_notification_settings()
    
    print("\nGod Mode Notification Settings")
    print("=============================")
    print(f"Desktop Notifications: {'ENABLED' if settings.get('notifications_enabled', True) else 'DISABLED'}")
    print(f"Sound Effects: {'ENABLED' if settings.get('sound_enabled', True) else 'DISABLED'}")
    
    # Show which implementation is being used
    if IMPORTED:
        print("\nUsing settings from main script_message_router.py")
    else:
        print("\nUsing built-in settings module (script_message_router.py not found)")
    
    # Show the config file location
    print(f"\nConfig file: {CONFIG_FILE}")
    
    return settings

def test_notifications():
    """Test notifications with current settings."""
    settings = get_notification_settings()
    
    # Show current settings
    print("Current settings:")
    print(f"Desktop Notifications: {'ENABLED' if settings.get('notifications_enabled', True) else 'DISABLED'}")
    print(f"Sound Effects: {'ENABLED' if settings.get('sound_enabled', True) else 'DISABLED'}")
    
    # Send a test notification
    print("\nSending test notification...")
    send_notification("God Mode Test", "This is a test notification with the current settings")
    
    print("Test completed.")
    print("If you didn't see a desktop notification or hear a sound, check your system's notification settings.")
    print("You may need to grant Cursor or Terminal permission to send notifications.")

def main():
    """Main function to parse arguments and manage notification settings."""
    parser = argparse.ArgumentParser(description='Manage God Mode notification settings.')
    parser.add_argument('--list', action='store_true', help='List current notification settings')
    parser.add_argument('--toggle-sound', action='store_true', help='Toggle sound effects')
    parser.add_argument('--toggle-notifications', action='store_true', help='Toggle desktop notifications')
    parser.add_argument('--enable-all', action='store_true', help='Enable all notifications')
    parser.add_argument('--disable-all', action='store_true', help='Disable all notifications')
    parser.add_argument('--test', action='store_true', help='Test notifications with current settings')
    
    args = parser.parse_args()
    
    # Default to listing settings if no arguments are provided
    if len(sys.argv) == 1:
        list_settings()
        print("\nUse --help for more options.")
        return 0
    
    # Handle arguments
    if args.list:
        list_settings()
    
    if args.toggle_sound:
        settings = get_notification_settings()
        new_settings = toggle_notification_settings(sound_enabled=not settings.get('sound_enabled', True))
        print(f"Sound effects {'ENABLED' if new_settings.get('sound_enabled', True) else 'DISABLED'}")
    
    if args.toggle_notifications:
        settings = get_notification_settings()
        new_settings = toggle_notification_settings(
            notifications_enabled=not settings.get('notifications_enabled', True))
        print(f"Desktop notifications {'ENABLED' if new_settings.get('notifications_enabled', True) else 'DISABLED'}")
    
    if args.enable_all:
        toggle_notification_settings(sound_enabled=True, notifications_enabled=True)
        print("All notifications ENABLED")
    
    if args.disable_all:
        toggle_notification_settings(sound_enabled=False, notifications_enabled=False)
        print("All notifications DISABLED")
    
    if args.test:
        test_notifications()
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 