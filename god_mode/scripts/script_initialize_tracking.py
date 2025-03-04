#!/usr/bin/env python3
"""
Initialize Routing Tracking for God Mode

This script initializes the routing tracking system by creating the necessary directory
structure and ensuring the tracking history file exists.

Usage:
    python script_initialize_tracking.py
"""

import os
import sys
import json
from pathlib import Path
import shutil

# Get the directory of this script
SCRIPT_DIR = Path(os.path.dirname(os.path.abspath(__file__)))

# Define the project root relative to this script
PROJECT_ROOT = Path(SCRIPT_DIR).parent.parent

# Define the God Mode directory
GOD_MODE_DIR = Path(SCRIPT_DIR).parent

# Define the routing history file
ROUTING_HISTORY_FILE = GOD_MODE_DIR / ".cache" / "routing_history.json"

def ensure_directory_exists(directory):
    """Ensure a directory exists, creating it if necessary."""
    os.makedirs(directory, exist_ok=True)

def initialize_tracking():
    """Initialize the tracking system."""
    print(f"Initializing routing tracking system...")
    
    # Create the cache directory if it doesn't exist
    cache_dir = GOD_MODE_DIR / ".cache"
    ensure_directory_exists(cache_dir)
    print(f"✅ Cache directory created/verified: {cache_dir}")
    
    # Create the routing history file if it doesn't exist
    if not ROUTING_HISTORY_FILE.exists():
        # Create an empty history file
        with open(ROUTING_HISTORY_FILE, 'w') as f:
            json.dump([], f)
        print(f"✅ Created empty routing history file: {ROUTING_HISTORY_FILE}")
    else:
        print(f"✅ Routing history file already exists: {ROUTING_HISTORY_FILE}")
    
    # Ensure scripts are executable
    track_script = SCRIPT_DIR / "script_track_routing.py"
    if track_script.exists():
        os.chmod(track_script, 0o755)
        print(f"✅ Made tracking script executable: {track_script}")
    else:
        print(f"❌ Tracking script not found: {track_script}")
    
    # Create a link to the tracking module in god_mode/scripts if it doesn't exist
    tracking_module = SCRIPT_DIR / "script_track_routing.py"
    if not tracking_module.exists():
        shutil.copy(track_script, tracking_module)
        print(f"✅ Created tracking module link: {tracking_module}")
    
    print("✅ Tracking system initialized successfully")
    
    return True

def main():
    """Main function."""
    return initialize_tracking()

if __name__ == "__main__":
    sys.exit(0 if main() else 1) 