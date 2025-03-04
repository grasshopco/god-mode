#!/usr/bin/env python3
"""
Test script to verify access to Cursor's SQLite databases.
"""

import os
import sys
import sqlite3
import platform
import json
from pathlib import Path

def get_workspace_storage_paths():
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

def find_all_workspace_dbs():
    """
    Find all the state.vscdb files in Cursor's workspaceStorage.
    
    Returns:
        list: List of Paths to all workspace database files
    """
    database_files = []
    
    for workspace_path in get_workspace_storage_paths():
        print(f"Looking for workspace databases in: {workspace_path}")
        
        if not workspace_path.exists():
            print(f"Workspace path does not exist: {workspace_path}")
            continue
        
        # Look for folders that are md5 hashes (hex digits of fixed length)
        try:
            for folder in workspace_path.iterdir():
                if folder.is_dir():
                    db_file = folder / "state.vscdb"
                    if db_file.exists():
                        database_files.append(db_file)
                        print(f"Found database file: {db_file}")
        except Exception as e:
            print(f"Error scanning workspace directory {workspace_path}: {e}")
    
    print(f"Found {len(database_files)} workspace database files")
    return database_files

def query_database(db_path):
    """
    Query a SQLite database to extract chat data.
    
    Args:
        db_path (Path): Path to the SQLite database
        
    Returns:
        dict: Dictionary of chat data with keys for different types of chat data
    """
    try:
        # Connect to the database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # List all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(f"Tables in {db_path.name}:")
        for table in tables:
            print(f"  - {table[0]}")
        
        # Query the database for chat data
        cursor.execute("""
        SELECT rowid, [key], value FROM ItemTable 
        WHERE [key] IN ('aiService.prompts', 'workbench.panel.aichat.view.aichat.chatdata')
        """)
        
        results = cursor.fetchall()
        conn.close()
        
        if not results:
            print(f"No chat data found in {db_path.name}")
            return {}
        
        print(f"Found {len(results)} chat data entries in {db_path.name}")
        
        # Process results
        chat_data = {}
        for _, key, value in results:
            if value:
                try:
                    chat_data[key] = json.loads(value)
                    print(f"Successfully parsed JSON from key '{key}'")
                except json.JSONDecodeError:
                    print(f"Failed to parse JSON from key '{key}'")
        
        return chat_data
    except sqlite3.Error as e:
        print(f"SQLite error in {db_path}: {e}")
        return {}
    except Exception as e:
        print(f"Error querying database {db_path}: {e}")
        return {}

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
                print(f"Found {len(prompts_data)} prompts in aiService.prompts")
                for i, prompt in enumerate(prompts_data):
                    if 'messages' in prompt and isinstance(prompt['messages'], list):
                        print(f"Prompt {i+1} has {len(prompt['messages'])} messages")
                        conversations.append(prompt)
        except Exception as e:
            print(f"Error extracting from aiService.prompts: {e}")
    
    # Extract from aichat.chatdata
    if 'workbench.panel.aichat.view.aichat.chatdata' in chat_data:
        try:
            chat_data_obj = chat_data['workbench.panel.aichat.view.aichat.chatdata']
            if isinstance(chat_data_obj, dict) and 'chats' in chat_data_obj:
                chats = chat_data_obj['chats']
                if isinstance(chats, list):
                    print(f"Found {len(chats)} chats in aichat.chatdata")
                    for i, chat in enumerate(chats):
                        if 'messages' in chat and isinstance(chat['messages'], list):
                            print(f"Chat {i+1} has {len(chat['messages'])} messages")
                            conversations.append(chat)
        except Exception as e:
            print(f"Error extracting from aichat.chatdata: {e}")
    
    return conversations

def main():
    print("Testing Cursor SQLite Database Access")
    
    # Find all workspace databases
    db_files = find_all_workspace_dbs()
    
    if not db_files:
        print("No database files found!")
        return 1
    
    # Check each database for chat data
    for db_path in db_files:
        print(f"\nAnalyzing database: {db_path}")
        
        # Query the database
        chat_data = query_database(db_path)
        
        # Extract conversations
        if chat_data:
            conversations = extract_conversations_from_chat_data(chat_data)
            print(f"Found {len(conversations)} conversations in {db_path}")
            
            # Print sample of each conversation
            for i, conversation in enumerate(conversations):
                if 'messages' in conversation and isinstance(conversation['messages'], list) and conversation['messages']:
                    print(f"\nConversation {i+1}:")
                    messages = conversation['messages']
                    print(f"Total messages: {len(messages)}")
                    
                    # Print some sample messages
                    for j, message in enumerate(messages[:3]):
                        if isinstance(message, dict):
                            role = message.get('role', 'unknown')
                            content = message.get('content', '')
                            if content:
                                print(f"  Message {j+1} ({role}): {content[:100]}...")
                    
                    if len(messages) > 3:
                        print(f"  ...and {len(messages) - 3} more messages")
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 