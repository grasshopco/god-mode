#!/usr/bin/env python3
"""
Cursor Watch Script - SQLite Edition

This script watches Cursor's SQLite databases in workspaceStorage to detect changes in 
conversation messages and ensures that assistant responses include the proper tags.

Usage:
    python script_cursor_watch.py

The script will run in the background and periodically check Cursor's databases
for new assistant messages without tags, and log when it finds them.
"""

import os
import sys
import json
import time
import sqlite3
import platform
import re
import subprocess
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
import traceback
from datetime import datetime
import random

# Get the directory of this script
SCRIPT_DIR = Path(os.path.dirname(os.path.abspath(__file__)))

# Define the project root relative to this script
PROJECT_ROOT = SCRIPT_DIR.parent.parent

# Define the God Mode directory
GOD_MODE_DIR = SCRIPT_DIR.parent

# Define the path to the enhance prompt script
ENHANCE_PROMPT_SCRIPT = SCRIPT_DIR / "script_enhance_prompt.py"

# Define the path to the logs directory
LOGS_DIR = GOD_MODE_DIR / "logs"

# Ensure the logs directory exists
os.makedirs(LOGS_DIR, exist_ok=True)

# Define the path to the log file
LOG_FILE = LOGS_DIR / "cursor_watch.log"

# Define paths to the cursor rules files
CURSOR_RULES_FILE = PROJECT_ROOT / ".cursor" / ".cursorrules"
CURSOR_RULES_JSON = PROJECT_ROOT / ".cursor" / "cursorrules.json"

# Check interval in seconds
CHECK_INTERVAL = 5

def ensure_directory_exists(directory):
    """Ensure a directory exists, creating it if necessary."""
    os.makedirs(directory, exist_ok=True)

def get_workspace_storage_paths() -> List[Path]:
    """Get potential workspace storage paths based on the OS."""
    home = Path.home()
    
    if platform.system() == "Windows":
        # Windows
        paths = [
            Path(os.environ.get('APPDATA', '')) / "Cursor" / "User" / "workspaceStorage",
            # WSL compatibility
            Path('/mnt/c/Users') / os.environ.get('USER', '') / 'AppData/Roaming/Cursor/User/workspaceStorage'
        ]
    elif platform.system() == "Darwin":
        # macOS
        paths = [
            home / "Library/Application Support/Cursor/User/workspaceStorage"
        ]
    else:
        # Linux
        paths = [
            home / ".config/Cursor/User/workspaceStorage"
        ]
    
    # Return only paths that exist
    return [p for p in paths if p.exists()]

def log_message(message):
    """Log a message with timestamp."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")
    sys.stdout.flush()  # Ensure output is flushed immediately

def log_error(message):
    """Log an error message with timestamp."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] ERROR: {message}", file=sys.stderr)
    sys.stderr.flush()  # Ensure output is flushed immediately

def log_debug(message):
    """Log a debug message with timestamp (only if debug mode is enabled)."""
    if os.environ.get("DEBUG_MODE", "").lower() in ("1", "true", "yes"):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] DEBUG: {message}")
        sys.stdout.flush()  # Ensure output is flushed immediately

def log_warning(message):
    """Log a warning message with timestamp."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] WARNING: {message}")
    sys.stdout.flush()  # Ensure output is flushed immediately

def log_info(message):
    """Log an info message with timestamp."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] INFO: {message}")
    sys.stdout.flush()  # Ensure output is flushed immediately

def extract_tags_from_text(text):
    """
    Extract tags from text using regex.
    
    Args:
        text (str): The text to extract tags from
        
    Returns:
        list: List of tags found in the text
    """
    # Match patterns like [TAG_NAME] or [TAG_NAME: Value]
    tag_pattern = r'\[(LOG_SUMMARY|LOG_DETAIL|MEMORY_UPDATE|FEATURE_LOG|DOC_UPDATE|MEMORY_[A-Z_]+|MULTI_TAG)(?:\s*:\s*([^\]]+))?\]'
    matches = re.findall(tag_pattern, text)
    return [f"[{tag}{': ' + value if value else ''}]" for tag, value in matches]

def find_all_workspace_dbs():
    """
    Find all the state.vscdb files in Cursor's workspaceStorage.
    
    Returns:
        list: List of Paths to all workspace database files
    """
    database_files = []
    
    for workspace_path in get_workspace_storage_paths():
        log_message(f"Looking for workspace databases in: {workspace_path}")
        
        if not workspace_path.exists():
            log_message(f"Workspace path does not exist: {workspace_path}")
            continue
            
        # Look for folders that are md5 hashes (hex digits of fixed length)
        try:
            for folder in workspace_path.iterdir():
                if folder.is_dir() and re.match(r'^[0-9a-f]+$', folder.name.lower()):
                    db_file = folder / "state.vscdb"
                    if db_file.exists():
                        database_files.append(db_file)
                        log_message(f"Found database file: {db_file}")
        except Exception as e:
            log_message(f"Error scanning workspace directory {workspace_path}: {e}")
    
    log_message(f"Found {len(database_files)} workspace database files")
    return database_files

def query_cursor_database(db_path):
    """
    Query a Cursor SQLite database for conversation messages.
    
    Args:
        db_path (Path): Path to the database file
        
    Returns:
        list: List of message dictionaries, or empty list if none found or on error
    """
    try:
        # Connect to the database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Try different table names that might contain conversations
        # First check if the conversations table exists
        tables = []
        try:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            log_debug(f"Found tables in {db_path.name}: {', '.join(tables)}")
        except Exception as e:
            log_error(f"Error listing tables in {db_path.name}: {e}")
            conn.close()
            return []
        
        # Try different tables that might contain conversations
        messages = []
        
        # First try conversations table (most common)
        if 'conversations' in tables:
            try:
                cursor.execute("SELECT id, role, content FROM conversations ORDER BY timestamp DESC LIMIT 100")
                rows = cursor.fetchall()
                if rows:
                    for row in rows:
                        messages.append({
                            'id': row[0],
                            'role': row[1],
                            'content': row[2]
                        })
                    log_debug(f"Found {len(messages)} messages in conversations table")
            except Exception as e:
                log_error(f"Error querying conversations table: {e}")
        
        # If no messages yet, try chat_messages table
        if not messages and 'chat_messages' in tables:
            try:
                cursor.execute("SELECT id, role, content FROM chat_messages ORDER BY timestamp DESC LIMIT 100")
                rows = cursor.fetchall()
                if rows:
                    for row in rows:
                        messages.append({
                            'id': row[0],
                            'role': row[1],
                            'content': row[2]
                        })
                    log_debug(f"Found {len(messages)} messages in chat_messages table")
            except Exception as e:
                log_error(f"Error querying chat_messages table: {e}")
        
        # If still no messages, try messages table
        if not messages and 'messages' in tables:
            try:
                cursor.execute("SELECT id, role, content FROM messages ORDER BY timestamp DESC LIMIT 100")
                rows = cursor.fetchall()
                if rows:
                    for row in rows:
                        messages.append({
                            'id': row[0],
                            'role': row[1],
                            'content': row[2]
                        })
                    log_debug(f"Found {len(messages)} messages in messages table")
            except Exception as e:
                log_error(f"Error querying messages table: {e}")
        
        # Close the connection
        conn.close()
        
        # Return the list of messages (might be empty)
        if messages:
            log_debug(f"Returning {len(messages)} messages from {db_path.name}")
        return messages
    
    except Exception as e:
        log_error(f"Error querying database {db_path}: {e}")
        return []

def extract_conversations_from_chat_data(chat_data):
    """
    Extract conversations from the chat data.
    
    Args:
        chat_data (dict): Chat data from querying the database
        
    Returns:
        list: List of conversation objects with user and assistant messages
    """
    conversations = []
    
    # Extract from aiService.prompts
    if 'aiService.prompts' in chat_data:
        try:
            prompts_data = chat_data['aiService.prompts']
            if isinstance(prompts_data, list):
                log_message(f"Found {len(prompts_data)} prompts in aiService.prompts")
                for prompt in prompts_data:
                    if 'messages' in prompt and isinstance(prompt['messages'], list):
                        conversations.append(prompt)
        except Exception as e:
            log_message(f"Error extracting from aiService.prompts: {e}")
    
    # Extract from aichat.chatdata
    if 'workbench.panel.aichat.view.aichat.chatdata' in chat_data:
        try:
            chat_data_obj = chat_data['workbench.panel.aichat.view.aichat.chatdata']
            if isinstance(chat_data_obj, dict) and 'chats' in chat_data_obj:
                chats = chat_data_obj['chats']
                if isinstance(chats, list):
                    log_message(f"Found {len(chats)} chats in aichat.chatdata")
                    for chat in chats:
                        if 'messages' in chat and isinstance(chat['messages'], list):
                            conversations.append(chat)
        except Exception as e:
            log_message(f"Error extracting from aichat.chatdata: {e}")
    
    return conversations

def get_message_content(message):
    """
    Get content from a message object with error handling.
    
    Args:
        message (dict): The message object
        
    Returns:
        str: The content of the message
    """
    if not isinstance(message, dict):
        return ""
    
    return message.get('content', '')

def get_last_assistant_message(conversation):
    """
    Get the last assistant message from a conversation.
    
    Args:
        conversation (dict): The conversation object
        
    Returns:
        dict: The last assistant message
    """
    if not conversation or 'messages' not in conversation:
        return None
    
    messages = conversation['messages']
    if not isinstance(messages, list) or not messages:
        return None
    
    # Look for the last assistant message
    for message in reversed(messages):
        if isinstance(message, dict) and message.get('role') == 'assistant':
            return message
    
    return None

def check_for_messages_without_tags(db_path, conversation, last_check_time):
    """
    Check for assistant messages that don't have tags.
    
    Args:
        db_path (Path): Path to the database
        conversation (dict): The conversation object
        last_check_time (float): Timestamp of the last check
        
    Returns:
        list: List of messages that need tags
    """
    if not conversation or 'messages' not in conversation:
        return []
    
    messages = conversation['messages']
    if not isinstance(messages, list) or not messages:
        return []
    
    messages_without_tags = []
    
    # Look for assistant messages that need tags
    for i, message in enumerate(messages):
        if not isinstance(message, dict) or message.get('role') != 'assistant':
            continue
        
        # Skip messages we've already checked
        message_time = message.get('timestamp', 0) / 1000 if isinstance(message.get('timestamp'), (int, float)) else 0
        if message_time < last_check_time and message_time > 0:
            continue
        
        content = get_message_content(message)
        if not content:
            continue
        
        # Check if the message has tags
        existing_tags = extract_tags_from_text(content)
        if existing_tags:
            log_message(f"Found message with tags: {', '.join(existing_tags)}")
            continue
        
        # If no tags, add to the list
        messages_without_tags.append(message)
    
    return messages_without_tags

def get_ai_rules_from_file():
    """
    Get AI rules from the cursorrules file.
    
    Returns:
        str: The AI rules
    """
    try:
        # First try JSON format
        if CURSOR_RULES_JSON.exists():
            with open(CURSOR_RULES_JSON, 'r') as f:
                data = json.load(f)
                if isinstance(data, dict) and 'rules' in data:
                    return data['rules']
        
        # Fall back to text format
        if CURSOR_RULES_FILE.exists():
            with open(CURSOR_RULES_FILE, 'r') as f:
                return f.read()
        
        return ""
    except Exception as e:
        log_message(f"Error reading cursor rules: {e}")
        return ""

def enhance_user_prompt(user_prompt):
    """
    Enhance the user prompt with relevant context from the project.
    This function uses the enhance_prompt.py script to add context.
    
    Args:
        user_prompt (str): The user's prompt
        
    Returns:
        str: The enhanced prompt
    """
    # For now, this is a placeholder
    # We'll implement the actual enhancement logic later
    context = "I'll reference project context and memory files in my response."
    return f"{context}\n\n{user_prompt}"

def should_add_tags_to_message(message):
    """
    Determines if a message should have tags based on its content.
    
    Args:
        message (str): The message to check
        
    Returns:
        bool: True if the message should have tags, False otherwise
    """
    # If message is empty, no tags needed
    if not message or len(message.strip()) == 0:
        log_debug("Message is empty, no tags needed")
        return False
    
    # Check if message already has tags
    tag_pattern = r'\[(LOG_SUMMARY|LOG_DETAIL|MEMORY_UPDATE|FEATURE_LOG|DOC_UPDATE|MEMORY_[A-Z_]+|MULTI_TAG)(?:\s*:\s*([^\]]+))?\]'
    if re.search(tag_pattern, message):
        log_debug("Message already has tags")
        return False  # Already has tags
    
    # Check if message is substantial enough to need tags (more than 200 chars)
    substantial_content = len(message) > 200
    
    # Check for indicators that this is a substantive response
    has_code_blocks = '```' in message
    has_bullet_points = re.search(r'^\s*[-*]\s+', message, re.MULTILINE) is not None
    has_numbered_lists = re.search(r'^\s*\d+\.\s+', message, re.MULTILINE) is not None
    has_headers = re.search(r'^\s*#{1,6}\s+', message, re.MULTILINE) is not None
    has_substantive_formatting = has_code_blocks or has_bullet_points or has_numbered_lists or has_headers
    
    # Return True if the message is substantial or has substantive formatting
    result = substantial_content or has_substantive_formatting
    
    if result:
        log_debug(f"Message should have tags (length: {len(message)}, has_code_blocks: {has_code_blocks}, has_bullet_points: {has_bullet_points})")
    else:
        log_debug(f"Message doesn't need tags (length: {len(message)})")
    
    return result

def check_message_has_tags(message_content, message_id):
    """
    Check if a message has the required tags, log if tags are missing.
    
    Args:
        message_content (str): The content of the message to check
        message_id (str): The ID of the message for reference
        
    Returns:
        bool: True if the message has tags or doesn't need them, False if tags are missing
    """
    # Define tag detection pattern
    tag_pattern = r'\[(LOG_SUMMARY|LOG_DETAIL|MEMORY_UPDATE|FEATURE_LOG|DOC_UPDATE|MEMORY_[A-Z_]+|MULTI_TAG)(?:\s*:\s*([^\]]+))?\]'
    
    # Check if message has tags
    has_tags = re.search(tag_pattern, message_content) is not None
    
    # If no tags found, check if this message should have tags
    if not has_tags and should_add_tags_to_message(message_content):
        log_warning(f"Message {message_id[:8]} is missing required tags")
        log_debug(f"Message content (first 100 chars): {message_content[:100]}...")
        # Get file path to message_router script
        message_router_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "script_message_router.py")
        log_debug(f"To fix, run: python3 {message_router_path} --validate-message")
        return False
    
    return True

def watch_cursor_databases():
    """
    Main function to watch Cursor SQLite databases for changes and ensure proper tagging.
    """
    log_message("Starting cursor_watch (SQLite edition)")
    log_message(f"Looking for SQLite databases in: {get_cursor_db_paths()}")
    
    # Find all SQLite databases
    db_files = find_cursor_db_files()
    if not db_files:
        log_warning("No Cursor SQLite databases found.")
        log_message("Please make sure Cursor is installed correctly.")
        return 1
    
    log_message(f"Found {len(db_files)} Cursor SQLite database files.")
    
    # Keep track of the latest messages we've seen
    seen_message_ids = set()
    
    # Run the prompt enhancement script if available
    prompt_enhancement_script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "script_enhance_prompt.py")
    if os.path.exists(prompt_enhancement_script):
        log_message("Found prompt enhancement script. Will apply to conversations.")
    else:
        log_warning("Prompt enhancement script not found. Conversations will not be enhanced.")
    
    # Main watch loop
    while True:
        try:
            new_messages_found = False
            
            # Check each database for new messages
            for db_file in db_files:
                log_debug(f"Checking database: {db_file}")
                
                try:
                    messages = query_cursor_database(db_file)
                    
                    if not messages:
                        log_debug(f"No messages found in {db_file}")
                        continue
                    
                    # Process new assistant messages only
                    for msg in messages:
                        try:
                            msg_id = msg.get('id', '')
                            if not msg_id:
                                continue
                                
                            msg_role = msg.get('role', '')
                            msg_content = msg.get('content', '')
                            
                            # Skip messages we've already seen
                            if msg_id in seen_message_ids:
                                continue
                            
                            # Add to seen messages
                            seen_message_ids.add(msg_id)
                            new_messages_found = True
                            
                            # Only check assistant messages for tags
                            if msg_role == 'assistant':
                                log_debug(f"Found new assistant message: {msg_id[:8] if len(msg_id) > 8 else msg_id}")
                                
                                # Check if message has required tags
                                check_message_has_tags(msg_content, msg_id)
                                
                            # For user messages, apply prompt enhancement if available
                            elif msg_role == 'user' and os.path.exists(prompt_enhancement_script):
                                log_debug(f"Found new user message: {msg_id[:8] if len(msg_id) > 8 else msg_id}")
                                
                                # Try to enhance the prompt
                                try:
                                    # This is a placeholder - implement actual prompt enhancement
                                    # In a real implementation, you would modify the database or 
                                    # call an external script to enhance the prompt
                                    log_message(f"Would enhance prompt for message {msg_id[:8]}")
                                    
                                    # Example of how to call the prompt enhancement script:
                                    # subprocess.run([sys.executable, prompt_enhancement_script, "--message", msg_id])
                                except Exception as e:
                                    log_error(f"Error enhancing prompt: {e}")
                        except Exception as e:
                            log_error(f"Error processing message: {e}")
                except Exception as e:
                    log_error(f"Error querying database {db_file}: {e}")
            
            # Check for new database files periodically
            if not new_messages_found:
                # Refresh the database list occasionally
                if random.random() < 0.05:  # ~5% chance each check when idle
                    new_db_files = find_cursor_db_files()
                    if set(new_db_files) != set(db_files):
                        log_message(f"Found updated database list: {len(new_db_files)} files")
                        db_files = new_db_files
                
                time.sleep(5)  # Check every 5 seconds when idle
            else:
                time.sleep(1)  # Brief pause when actively processing
            
        except KeyboardInterrupt:
            log_message("Cursor watch stopped by user.")
            return 0
        except Exception as e:
            log_error(f"Error watching Cursor databases: {e}")
            traceback.print_exc()
            log_message("Will attempt to continue in 10 seconds...")
            time.sleep(10)  # Back off on errors
    
    return 0

def main():
    """Main function to run the script."""
    log_message("Starting Cursor watch script...")
    
    # Check if the enhance prompt script exists
    if not ENHANCE_PROMPT_SCRIPT.exists():
        log_message(f"Warning: Could not find enhance prompt script at {ENHANCE_PROMPT_SCRIPT}")
        log_message("Continuing without prompt enhancement...")
    
    # Check if any Cursor workspaceStorage paths exist
    workspace_paths = get_workspace_storage_paths()
    if not workspace_paths:
        log_message("Error: Could not find any Cursor workspaceStorage directories.")
        log_message("Looked in:")
        if platform.system() == "Windows":
            log_message("  %APPDATA%\\Cursor\\User\\workspaceStorage")
            log_message("  /mnt/c/Users/$USER/AppData/Roaming/Cursor/User/workspaceStorage (WSL)")
        elif platform.system() == "Darwin":
            log_message("  ~/Library/Application Support/Cursor/User/workspaceStorage")
        else:
            log_message("  ~/.config/Cursor/User/workspaceStorage")
        return 1
    
    # Check if the cursor rules file exists
    if not CURSOR_RULES_FILE.exists() and not CURSOR_RULES_JSON.exists():
        log_message("Warning: Could not find cursor rules files.")
        log_message("This may affect the script's ability to check for proper tagging.")
    
    # Run the watch function
    return watch_cursor_databases()

if __name__ == "__main__":
    sys.exit(main()) 