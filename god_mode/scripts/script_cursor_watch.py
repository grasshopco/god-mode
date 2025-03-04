#!/usr/bin/env python3
"""
Cursor Watch Script

This script monitors the Cursor IDE conversation file and automatically enhances
user prompts using the script_enhance_prompt.py script. It creates a more "God-like"
experience by intercepting and enhancing user prompts before they are processed by the AI.

Usage:
    python script_cursor_watch.py

The script will run in the background, monitoring for changes to the Cursor conversation file.
"""

import os
import sys
import time
import json
import subprocess
from pathlib import Path
import re
import glob

# Get the directory of this script
SCRIPT_DIR = Path(os.path.dirname(os.path.abspath(__file__)))

# Define the project root relative to this script
PROJECT_ROOT = Path(SCRIPT_DIR).parent.parent

# Define the God Mode directory
GOD_MODE_DIR = Path(SCRIPT_DIR).parent

# Define the enhance prompt script path
ENHANCE_PROMPT_SCRIPT = SCRIPT_DIR / "script_enhance_prompt.py"

# Define the Cursor conversation file path - default paths to try
CURSOR_DIRS = [
    Path(os.path.expanduser("~/.cursor")),
    Path(os.path.expanduser("~/Library/Application Support/Cursor")),
    Path(os.path.expanduser("~/AppData/Roaming/Cursor")),
    Path(os.path.expanduser("~/.config/Cursor"))
]

# Define known conversation file paths to try first
KNOWN_CONVERSATION_PATHS = [
    "conversations/latest.json",
    "conversations/conversation_latest.json",
    "conversation.json",
    "User/conversation.json"
]

# Define the log file
LOG_FILE = GOD_MODE_DIR / "logs" / "cursor_watch.log"

def ensure_directory_exists(directory):
    """Ensure a directory exists, creating it if necessary."""
    os.makedirs(directory, exist_ok=True)

def log_message(message):
    """Log a message to the log file."""
    ensure_directory_exists(LOG_FILE.parent)
    with open(LOG_FILE, 'a') as f:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        f.write(f"[{timestamp}] {message}\n")
    print(message)

def is_valid_conversation_file(file_path):
    """
    Check if a file is a valid Cursor conversation file.
    
    Args:
        file_path (Path): Path to the file to check
        
    Returns:
        bool: True if the file is a valid conversation file, False otherwise
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
                # Check if this looks like a conversation file - must have messages array
                if isinstance(data, dict):
                    # If it has a messages array, it's definitely a conversation file
                    if 'messages' in data and isinstance(data['messages'], list):
                        log_message(f"Found valid conversation file with messages array: {file_path}")
                        return True
                    # If it has conversation-like keys, it might be a conversation file
                    if any(key in data for key in ['conversation', 'chat', 'history', 'prompt', 'response']):
                        log_message(f"Found possible conversation file with conversation keys: {file_path}")
                        return True
                    # If it's a small JSON file, take a closer look
                    file_size = os.path.getsize(file_path)
                    if file_size < 10000 and len(data) < 50:  # Small file with few keys
                        log_message(f"Small JSON file might be relevant: {file_path}")
                        return True
                return False
            except json.JSONDecodeError:
                # Try a more lenient approach - check if it contains conversation keywords
                f.seek(0)
                content = f.read(1000)  # Read just the first 1000 chars
                if any(keyword in content.lower() for keyword in ['message', 'chat', 'conversation', 'user', 'assistant', 'ai', 'prompt']):
                    log_message(f"File contains conversation keywords but isn't valid JSON: {file_path}")
                    return False
                return False
    except Exception as e:
        log_message(f"Error checking conversation file {file_path}: {e}")
        return False

def find_cursor_conversation_file():
    """
    Find the Cursor conversation file.
    This function tries different possible locations based on the OS.
    
    Returns:
        Path: Path to the Cursor conversation file, or None if not found
    """
    # 1. Try known specific locations first (faster)
    log_message("Trying known conversation file locations first...")
    for cursor_dir in CURSOR_DIRS:
        if not cursor_dir.exists():
            continue
            
        for known_path in KNOWN_CONVERSATION_PATHS:
            conv_path = cursor_dir / known_path
            if conv_path.exists():
                log_message(f"Found conversation file at known location: {conv_path}")
                if is_valid_conversation_file(conv_path):
                    return conv_path
    
    # 2. Search for recently modified JSON files in cursor directories
    log_message("Searching for recently modified JSON files...")
    recent_json_files = []
    
    for cursor_dir in CURSOR_DIRS:
        if not cursor_dir.exists():
            continue
            
        # Find all .json files and sort by modification time (newest first)
        for root, _, files in os.walk(cursor_dir):
            for file in files:
                if file.endswith('.json'):
                    file_path = Path(root) / file
                    try:
                        mtime = os.path.getmtime(file_path)
                        recent_json_files.append((file_path, mtime))
                    except:
                        pass
    
    # Sort by modification time, newest first
    recent_json_files.sort(key=lambda x: x[1], reverse=True)
    
    # Take the 10 most recently modified files for detailed examination
    candidates = recent_json_files[:10]
    log_message(f"Found {len(candidates)} potential conversation files to check")
    
    for file_path, mtime in candidates:
        # Skip files in certain directories
        if any(x in str(file_path) for x in ['node_modules', 'extensions']):
            continue
            
        # Check size - conversation files are typically not huge
        try:
            size = os.path.getsize(file_path)
            if size > 5000000:  # Skip files > 5MB
                continue
                
            if is_valid_conversation_file(file_path):
                log_message(f"Found valid conversation file: {file_path}")
                return file_path
        except:
            pass
    
    # 3. As a fallback, look for any file with "conversation" in the name
    log_message("Fallback: looking for files with 'conversation' in the name...")
    for cursor_dir in CURSOR_DIRS:
        if not cursor_dir.exists():
            continue
            
        for root, _, files in os.walk(cursor_dir):
            for file in files:
                if 'conversation' in file.lower() and file.endswith('.json'):
                    file_path = Path(root) / file
                    if is_valid_conversation_file(file_path):
                        log_message(f"Found conversation file by name: {file_path}")
                        return file_path
    
    log_message("Could not find any Cursor conversation files")
    return None

def enhance_user_prompt(prompt):
    """
    Enhance a user prompt using the script_enhance_prompt.py script.
    
    Args:
        prompt (str): The user's original prompt
        
    Returns:
        str: The enhanced prompt, or the original prompt if enhancement fails
    """
    try:
        # Create a temporary file for the prompt
        temp_file = GOD_MODE_DIR / ".cache" / "temp_prompt.txt"
        ensure_directory_exists(temp_file.parent)
        
        with open(temp_file, 'w') as f:
            f.write(prompt)
        
        # Call the enhance_prompt script
        result = subprocess.run(
            [sys.executable, str(ENHANCE_PROMPT_SCRIPT), "--input", str(temp_file)],
            capture_output=True,
            text=True,
            check=True
        )
        
        # Extract the enhanced prompt
        enhanced_prompt = result.stdout.strip()
        
        # Only return if we got a valid result
        if enhanced_prompt:
            log_message(f"Successfully enhanced prompt of length {len(prompt)} to {len(enhanced_prompt)}")
            return enhanced_prompt
    except Exception as e:
        log_message(f"Error enhancing prompt: {e}")
    
    # Return the original prompt if enhancement fails
    return prompt

def watch_cursor_conversation():
    """
    Watch the Cursor conversation file for changes and enhance user prompts.
    """
    log_message("Starting Cursor conversation watch...")
    
    # Continuously try to find the conversation file - sometimes it changes
    while True:
        # Find the Cursor conversation file
        conversation_file = find_cursor_conversation_file()
        if not conversation_file:
            log_message("Error: Could not find Cursor conversation file. Will retry in 10 seconds.")
            time.sleep(10)
            continue
        
        log_message(f"Watching Cursor conversation file: {conversation_file}")
        
        # Track the last modification time and content
        last_mtime = 0
        last_content = None
        file_missing_count = 0
        
        # Watch the current conversation file until it disappears or we're interrupted
        while True:
            try:
                # Check if the file still exists
                if not conversation_file.exists():
                    file_missing_count += 1
                    if file_missing_count > 3:
                        log_message(f"Conversation file no longer exists: {conversation_file}")
                        break  # Break inner loop to find a new file
                    time.sleep(1)
                    continue
                
                file_missing_count = 0  # Reset counter if file exists
                
                # Check if the file has been modified
                current_mtime = os.path.getmtime(conversation_file)
                if current_mtime != last_mtime:
                    # Read the conversation file
                    try:
                        with open(conversation_file, 'r', encoding='utf-8') as f:
                            content = f.read()
                        
                        # Only process if the content has changed
                        if content != last_content:
                            last_content = content
                            last_mtime = current_mtime
                            
                            try:
                                # Parse the conversation JSON
                                conversation = json.loads(content)
                                
                                # Handle different conversation formats
                                messages = None
                                if isinstance(conversation, dict):
                                    if 'messages' in conversation:
                                        messages = conversation.get('messages', [])
                                    elif 'conversation' in conversation:
                                        messages = conversation.get('conversation', {}).get('messages', [])
                                
                                if not messages or not isinstance(messages, list):
                                    log_message(f"No valid messages array found in {conversation_file}")
                                    time.sleep(2)
                                    continue
                                    
                                # Check if the most recent message is from the user
                                if messages and any(msg.get('role') == 'user' for msg in messages):
                                    # Find the most recent user message
                                    for i in range(len(messages) - 1, -1, -1):
                                        if messages[i].get('role') == 'user' and not messages[i].get('enhanced'):
                                            # Get the user prompt
                                            user_prompt = messages[i].get('content', '')
                                            
                                            # Enhance the user prompt
                                            enhanced_prompt = enhance_user_prompt(user_prompt)
                                            
                                            # Update the conversation file if the prompt was enhanced
                                            if enhanced_prompt != user_prompt:
                                                # Mark as enhanced to avoid re-enhancing
                                                messages[i]['enhanced'] = True
                                                messages[i]['original_content'] = user_prompt
                                                messages[i]['content'] = enhanced_prompt
                                                
                                                # Write the updated conversation back to the file
                                                with open(conversation_file, 'w', encoding='utf-8') as f:
                                                    json.dump(conversation, f, indent=2)
                                                
                                                log_message("Updated Cursor conversation with enhanced prompt.")
                                            break
                            except json.JSONDecodeError as e:
                                log_message(f"Error parsing conversation JSON: {e}")
                                time.sleep(2)
                    except Exception as e:
                        log_message(f"Error reading conversation file: {e}")
                
                # Sleep for a short time to avoid busy waiting
                time.sleep(0.5)
            
            except KeyboardInterrupt:
                log_message("Cursor watch script stopped by user.")
                return 0
            except Exception as e:
                log_message(f"Error watching Cursor conversation: {e}")
                # Sleep a bit longer after an error to avoid spamming logs
                time.sleep(5)
                # Break inner loop to find a new file if we've had persistent errors
                if "No such file or directory" in str(e):
                    break

def main():
    """Main function to run the script."""
    log_message("Starting Cursor watch script...")
    
    # Check if the enhance prompt script exists
    if not ENHANCE_PROMPT_SCRIPT.exists():
        log_message(f"Error: Could not find enhance prompt script at {ENHANCE_PROMPT_SCRIPT}")
        return 1
    
    # Run the watch function
    return watch_cursor_conversation()

if __name__ == "__main__":
    sys.exit(main()) 