#!/usr/bin/env python3

"""
Debug Router Script for God Mode

This script helps debug issues with the message router by providing detailed
tracing of message processing steps.
"""

import os
import sys
import re
import argparse
import traceback
from pathlib import Path
import datetime
import json

# Get the directory of this script
SCRIPT_DIR = Path(os.path.dirname(os.path.abspath(__file__)))

# Define the log directory relative to this script
LOG_DIR = SCRIPT_DIR.parent / "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Define the path to the log file
LOG_FILE = LOG_DIR / "debug_router.log"

def log_message(message):
    """Log a message with timestamp to both console and file"""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{timestamp}] {message}"
    
    # Print to console
    print(log_line)
    
    # Log to file
    with open(LOG_FILE, 'a') as f:
        f.write(log_line + "\n")

def read_file_safely(filepath):
    """Read a file with detailed error handling"""
    log_message(f"Attempting to read file: {filepath}")
    
    try:
        with open(filepath, 'r') as f:
            content = f.read()
            log_message(f"Successfully read file with {len(content)} characters")
            return content
    except Exception as e:
        log_message(f"Error reading file: {e}")
        log_message(traceback.format_exc())
        return None

def debug_pattern_matching(content):
    """Debug regex pattern matching on content"""
    log_message("Testing pattern matching on content...")
    
    # Define the patterns to test
    patterns = {
        "LOG_SUMMARY": r"\[LOG_SUMMARY\](.*?)(?=\[|\Z)",
        "LOG_DETAIL": r"\[LOG_DETAIL\](.*?)(?=\[|\Z)",
        "MEMORY_UPDATE": r"\[MEMORY_UPDATE\](.*?)(?=\[|\Z)",
        "FEATURE_LOG": r"\[FEATURE_LOG\s*:\s*([^]]+)\](.*?)(?=\[|\Z)",
        "DOC_UPDATE": r"\[DOC_UPDATE\s*:\s*([^]]+)\](.*?)(?=\[|\Z)",
        "MULTI_TAG": r"\[MULTI_TAG\s*:\s*([^]]+)\](.*?)(?=\[|\Z)"
    }
    
    # Test each pattern
    found_matches = False
    for name, pattern in patterns.items():
        log_message(f"Testing pattern: {name}")
        matches = list(re.finditer(pattern, content, re.DOTALL))
        
        if matches:
            found_matches = True
            log_message(f"✅ Found {len(matches)} matches for pattern {name}")
            
            # Log the match groups
            for i, match in enumerate(matches):
                log_message(f"  Match {i+1}:")
                for j, group in enumerate(match.groups()):
                    log_message(f"    Group {j+1}: {repr(group)}")
        else:
            log_message(f"❌ No matches found for pattern {name}")
    
    # If no patterns matched at all
    if not found_matches:
        log_message("⚠️ No pattern matches found in content. Content may not contain any tags.")
        log_message(f"Content preview: {content[:100]}...")
    
    return found_matches

def simulate_routing(content):
    """Simulate the routing process without actually writing to files"""
    log_message("Simulating routing process...")
    
    # Only implementing the FEATURE_LOG pattern for demonstration
    feature_pattern = r"\[FEATURE_LOG\s*:\s*([^]]+)\](.*?)(?=\[|\Z)"
    try:
        for match in re.finditer(feature_pattern, content, re.DOTALL):
            # This is where the "too many values to unpack" error might occur
            log_message(f"Match groups count: {len(match.groups())}")
            
            if len(match.groups()) >= 2:
                feature_name = match.group(1).strip()
                content = match.group(2).strip()
                log_message(f"Would process feature log for: {feature_name}")
                log_message(f"With content: {content[:100]}...")
            else:
                log_message(f"⚠️ Match doesn't have expected number of groups. Groups: {match.groups()}")
    except Exception as e:
        log_message(f"❌ Error simulating routing: {e}")
        log_message(traceback.format_exc())

def main():
    """Main entry point for the debug router script."""
    # Set up command line argument parsing
    parser = argparse.ArgumentParser(description='Debug the message router script.')
    parser.add_argument('--input', type=str, help='Input file to debug')
    parser.add_argument('--content', type=str, help='Content to debug directly')
    
    args = parser.parse_args()
    
    log_message("Starting Message Router Debugger")
    log_message(f"Python version: {sys.version}")
    log_message(f"Script directory: {SCRIPT_DIR}")
    
    content = None
    
    # Get content from file or directly
    if args.input:
        content = read_file_safely(args.input)
    elif args.content:
        content = args.content
        log_message(f"Using provided content: {content[:100]}...")
    else:
        log_message("No input specified. Creating a test message...")
        content = """[FEATURE_LOG: TestFeature]
This is a test feature log entry.

[LOG_SUMMARY]
This is a summary entry.

[MEMORY_UPDATE]
This is a memory update.
"""
        log_message(f"Created test content: {content}")
    
    if content:
        # Test pattern matching
        debug_pattern_matching(content)
        
        # Simulate routing
        simulate_routing(content)
    
    log_message("Debug process completed")

if __name__ == "__main__":
    main() 