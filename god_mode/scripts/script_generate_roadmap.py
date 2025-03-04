#!/usr/bin/env python3
"""
Roadmap Update Generator Script

This script creates a new roadmap file from the template_roadmap_plan_update.md template.
It fills in the current date and time, and places the file in the roadmap directory.

Usage:
    python script_generate_roadmap.py [--title "Title for the roadmap"]
"""

import os
import sys
import argparse
import datetime
from pathlib import Path
import re
import shutil

# Get the directory of this script
SCRIPT_DIR = Path(os.path.dirname(os.path.abspath(__file__)))

# Define paths
PROJECT_ROOT = SCRIPT_DIR.parent.parent
TEMPLATE_DIR = SCRIPT_DIR.parent / "templates"
ROADMAP_DIR = SCRIPT_DIR.parent / "roadmap"
TEMPLATE_FILE = TEMPLATE_DIR / "template_roadmap_plan_update.md"

def ensure_directory_exists(directory):
    """Ensure a directory exists, creating it if necessary."""
    os.makedirs(directory, exist_ok=True)

def get_timestamp():
    """Get current timestamp in YYYY-MM-DD HH:MM UTC format."""
    now_utc = datetime.datetime.now(datetime.timezone.utc)
    return now_utc.strftime("%Y-%m-%d %H:%M UTC")

def get_filename_timestamp():
    """Get a filename-friendly timestamp (YYYYMMDD_HHMMSS)."""
    now_utc = datetime.datetime.now(datetime.timezone.utc)
    return now_utc.strftime("%Y%m%d_%H%M%S")

def generate_roadmap_file(title=None):
    """
    Generate a new roadmap file from the template.
    
    Args:
        title: Optional title for the roadmap file
    
    Returns:
        Path: Path to the generated file
    """
    # Ensure the roadmap directory exists
    ensure_directory_exists(ROADMAP_DIR)
    
    # Generate the filename
    timestamp = get_filename_timestamp()
    title_slug = "_" + re.sub(r'[^a-zA-Z0-9]', '_', title.lower()) if title else ""
    filename = f"roadmap_god_mode{title_slug}_{timestamp}.md"
    output_file = ROADMAP_DIR / filename
    
    # Read the template
    if not TEMPLATE_FILE.exists():
        print(f"Error: Template file not found at {TEMPLATE_FILE}", file=sys.stderr)
        return None
    
    with open(TEMPLATE_FILE, 'r', encoding='utf-8') as f:
        template_content = f.read()
    
    # Replace template variables
    current_time = get_timestamp()
    content = template_content.replace("[CURRENT_DATE_TIME]", current_time)
    
    # Add title if provided
    if title:
        content = content.replace("# God Mode System: Progress Report and Implementation Plan", 
                                 f"# God Mode System: {title}")
    
    # Write the new file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Generated roadmap file: {output_file}")
    return output_file

def main():
    parser = argparse.ArgumentParser(description="Generate a roadmap file from template")
    parser.add_argument("--title", help="Title for the roadmap file", default=None)
    args = parser.parse_args()
    
    output_file = generate_roadmap_file(args.title)
    if output_file:
        print(f"To edit this file, run: cursor {output_file}")
    else:
        print("Failed to generate roadmap file", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main() 