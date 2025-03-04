#!/usr/bin/env python3
"""
Routing Activity Tracker for God Mode

This script tracks and displays recent message routing activity, showing what content
was routed to which files, with clickable links to open the files at the specific locations.

Usage:
    python script_track_routing.py [--limit N] [--open FILENAME]

Options:
    --limit N       Show only the N most recent routing events (default: 10)
    --open FILENAME Open the specified file in a text editor or IDE
"""

import os
import sys
import json
import argparse
import subprocess
import datetime
from pathlib import Path
import platform
import re

# Get the directory of this script
SCRIPT_DIR = Path(os.path.dirname(os.path.abspath(__file__)))

# Define the project root relative to this script
PROJECT_ROOT = Path(SCRIPT_DIR).parent.parent

# Define the God Mode directory
GOD_MODE_DIR = Path(SCRIPT_DIR).parent

# Define the routing history file
ROUTING_HISTORY_FILE = GOD_MODE_DIR / ".cache" / "routing_history.json"

# Colors for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

def ensure_directory_exists(directory):
    """Ensure a directory exists, creating it if necessary."""
    os.makedirs(directory, exist_ok=True)

def load_routing_history():
    """Load routing history from file."""
    if not ROUTING_HISTORY_FILE.exists():
        return []
    
    try:
        with open(ROUTING_HISTORY_FILE, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"{Colors.RED}Error loading routing history: {e}{Colors.END}")
        return []

def save_routing_history(history):
    """Save routing history to file."""
    ensure_directory_exists(ROUTING_HISTORY_FILE.parent)
    
    try:
        with open(ROUTING_HISTORY_FILE, 'w') as f:
            json.dump(history, f, indent=2)
    except Exception as e:
        print(f"{Colors.RED}Error saving routing history: {e}{Colors.END}")

def add_routing_event(tag, file_path, content, line_number=None):
    """Add a new routing event to the history."""
    history = load_routing_history()
    
    # Create a new event
    event = {
        "timestamp": datetime.datetime.now().isoformat(),
        "tag": tag,
        "file": str(file_path),
        "line_number": line_number,
        "content": content[:500] + ("..." if len(content) > 500 else "")  # Limit content length
    }
    
    # Add to the beginning of the list (most recent first)
    history.insert(0, event)
    
    # Keep only the last 100 events
    history = history[:100]
    
    save_routing_history(history)

def get_file_line_count(file_path):
    """Get the number of lines in a file."""
    try:
        with open(file_path, 'r') as f:
            return sum(1 for _ in f)
    except Exception:
        return 0

def open_file(file_path, line_number=None):
    """Open a file in the default text editor, optionally at a specific line."""
    try:
        file_path = Path(file_path)
        if not file_path.exists():
            print(f"{Colors.RED}Error: File {file_path} does not exist{Colors.END}")
            return False
        
        if platform.system() == "Darwin":  # macOS
            if line_number:
                # Try to open with VS Code first (has good line number support)
                try:
                    subprocess.run(["code", "-g", f"{file_path}:{line_number}"], check=False)
                    return True
                except:
                    pass
                
                # Try to open with cursor IDE if available
                try:
                    subprocess.run(["cursor", "-g", f"{file_path}:{line_number}"], check=False)
                    return True
                except:
                    pass
                
                # Fall back to open command
                subprocess.run(["open", str(file_path)], check=False)
                print(f"{Colors.YELLOW}Opened file, but couldn't navigate to line {line_number}. Please scroll to this line manually.{Colors.END}")
            else:
                subprocess.run(["open", str(file_path)], check=False)
        elif platform.system() == "Windows":
            if line_number:
                try:
                    subprocess.run(["code", "-g", f"{file_path}:{line_number}"], check=False)
                    return True
                except:
                    pass
                
                try:
                    subprocess.run(["cursor", "-g", f"{file_path}:{line_number}"], check=False)
                    return True
                except:
                    pass
                
                # Fall back to notepad
                os.startfile(str(file_path))
                print(f"{Colors.YELLOW}Opened file, but couldn't navigate to line {line_number}. Please scroll to this line manually.{Colors.END}")
            else:
                os.startfile(str(file_path))
        elif platform.system() == "Linux":
            if line_number:
                try:
                    subprocess.run(["code", "-g", f"{file_path}:{line_number}"], check=False)
                    return True
                except:
                    pass
                
                try:
                    subprocess.run(["cursor", "-g", f"{file_path}:{line_number}"], check=False)
                    return True
                except:
                    pass
                
                try:
                    subprocess.run(["xdg-open", str(file_path)], check=False)
                    print(f"{Colors.YELLOW}Opened file, but couldn't navigate to line {line_number}. Please scroll to this line manually.{Colors.END}")
                except:
                    print(f"{Colors.RED}Could not open {file_path}{Colors.END}")
                    return False
            else:
                try:
                    subprocess.run(["xdg-open", str(file_path)], check=False)
                except:
                    print(f"{Colors.RED}Could not open {file_path}{Colors.END}")
                    return False
        else:
            print(f"{Colors.RED}Could not open {file_path}: Unsupported platform {platform.system()}{Colors.END}")
            return False
        
        return True
    except Exception as e:
        print(f"{Colors.RED}Error opening file: {e}{Colors.END}")
        return False

def format_relative_time(timestamp_str):
    """Format a timestamp as a relative time (e.g., '2 minutes ago')."""
    try:
        timestamp = datetime.datetime.fromisoformat(timestamp_str)
        now = datetime.datetime.now()
        diff = now - timestamp
        
        if diff.days > 0:
            if diff.days == 1:
                return "yesterday"
            else:
                return f"{diff.days} days ago"
        elif diff.seconds >= 3600:
            hours = diff.seconds // 3600
            if hours == 1:
                return "1 hour ago"
            else:
                return f"{hours} hours ago"
        elif diff.seconds >= 60:
            minutes = diff.seconds // 60
            if minutes == 1:
                return "1 minute ago"
            else:
                return f"{minutes} minutes ago"
        else:
            if diff.seconds == 1:
                return "1 second ago"
            else:
                return f"{diff.seconds} seconds ago"
    except:
        return "unknown time"

def truncate_path(path, max_length=50):
    """Truncate a path to a reasonable length for display."""
    path_str = str(path)
    if len(path_str) <= max_length:
        return path_str
    
    # Split the path
    parts = Path(path_str).parts
    
    # Keep the first and last parts, and abbreviate the middle
    if len(parts) <= 2:
        return path_str
    
    first = parts[0]
    last_parts = parts[-2:]
    
    return f"{first}/.../{'/'.join(last_parts)}"

def display_routing_history(limit=10):
    """Display recent routing history."""
    history = load_routing_history()
    
    if not history:
        print(f"{Colors.YELLOW}No routing history found.{Colors.END}")
        return
    
    print(f"\n{Colors.BOLD}{Colors.HEADER}Recent Routing Activity{Colors.END}\n")
    
    for i, event in enumerate(history[:limit]):
        timestamp = event.get("timestamp", "")
        tag = event.get("tag", "")
        file_path = event.get("file", "")
        content = event.get("content", "")
        line_number = event.get("line_number")
        
        relative_time = format_relative_time(timestamp)
        truncated_path = truncate_path(file_path)
        
        print(f"{Colors.BOLD}{i+1}. [{relative_time}] {Colors.CYAN}{tag}{Colors.END}")
        print(f"   {Colors.GREEN}→ {truncated_path}{Colors.END}" + (f" (line {line_number})" if line_number else ""))
        
        # Format content for display
        content_lines = content.split("\n")
        formatted_content = "\n      ".join(content_lines[:5])
        if len(content_lines) > 5:
            formatted_content += f"\n      {Colors.YELLOW}... ({len(content_lines) - 5} more lines){Colors.END}"
        
        print(f"   {Colors.BOLD}Content:{Colors.END}")
        print(f"      {formatted_content}")
        
        # Add clickable command
        print(f"   {Colors.BOLD}To open this file:{Colors.END} {Colors.BLUE}script_track_routing.py --open {i+1}{Colors.END}")
        print()

def main():
    """Main function to parse arguments and display or open files."""
    parser = argparse.ArgumentParser(description="Track and display message routing activity.")
    parser.add_argument("--limit", type=int, default=10, help="Number of recent routing events to display")
    parser.add_argument("--open", type=str, help="Open the specified file (number or path)")
    
    args = parser.parse_args()
    
    # If open argument is specified, open the file
    if args.open:
        try:
            # Check if it's a number (index)
            if args.open.isdigit():
                index = int(args.open) - 1
                history = load_routing_history()
                
                if 0 <= index < len(history):
                    event = history[index]
                    file_path = event.get("file", "")
                    line_number = event.get("line_number")
                    
                    if file_path:
                        print(f"{Colors.GREEN}Opening {file_path}" + (f" at line {line_number}" if line_number else "") + f"{Colors.END}")
                        open_file(file_path, line_number)
                    else:
                        print(f"{Colors.RED}No file path found for event {index+1}{Colors.END}")
                else:
                    print(f"{Colors.RED}Invalid event index: {args.open}{Colors.END}")
            else:
                # Assume it's a file path
                open_file(args.open)
        except Exception as e:
            print(f"{Colors.RED}Error opening file: {e}{Colors.END}")
    else:
        # Display routing history
        display_routing_history(args.limit)

if __name__ == "__main__":
    main() 