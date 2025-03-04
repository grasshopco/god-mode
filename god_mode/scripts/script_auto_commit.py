#!/usr/bin/env python3
"""
Auto Commit Script for God Mode
Automatically commits changes to memory files and other tracked files at the end of a conversation.
"""

import os
import sys
import time
import subprocess
import re
import json
from datetime import datetime
from pathlib import Path

# Add the parent directory to the sys path for importing helper modules
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

# Import helper modules if available
try:
    from utils.logger import log_info, log_error, log_debug, log_warning
except ImportError:
    def log_info(message): print(f"[INFO] {message}")
    def log_error(message): print(f"[ERROR] {message}")
    def log_debug(message): print(f"[DEBUG] {message}")
    def log_warning(message): print(f"[WARNING] {message}")

def git_is_available():
    """
    Check if Git is available.
    
    Returns:
        bool: True if Git is available, False otherwise
    """
    try:
        result = subprocess.run(["git", "--version"], capture_output=True, text=True)
        return result.returncode == 0
    except:
        return False

def is_git_repository(path):
    """
    Check if the specified path is a Git repository.
    
    Args:
        path (str): Path to check
        
    Returns:
        bool: True if it's a Git repository, False otherwise
    """
    try:
        result = subprocess.run(["git", "status"], cwd=path, capture_output=True, text=True)
        return result.returncode == 0
    except:
        return False

def get_uncommitted_changes(repo_path):
    """
    Get a list of uncommitted changes in the repository.
    
    Args:
        repo_path (str): Path to the repository
        
    Returns:
        list: List of files with uncommitted changes
    """
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"], 
            cwd=repo_path, 
            capture_output=True, 
            text=True
        )
        
        if result.returncode == 0:
            files = []
            for line in result.stdout.splitlines():
                status = line[:2]
                file_path = line[3:].strip()
                files.append((status, file_path))
            return files
        return []
    except Exception as e:
        log_error(f"Error checking uncommitted changes: {e}")
        return []

def auto_commit(repo_path, commit_message=None):
    """
    Automatically commit changes to the repository.
    
    Args:
        repo_path (str): Path to the repository
        commit_message (str, optional): Commit message. Defaults to a generated message.
        
    Returns:
        bool: True if the commit was successful, False otherwise
    """
    if not git_is_available():
        log_error("Git is not available. Cannot auto-commit.")
        return False
    
    if not is_git_repository(repo_path):
        log_error(f"{repo_path} is not a Git repository. Cannot auto-commit.")
        return False
    
    # Check for uncommitted changes
    changes = get_uncommitted_changes(repo_path)
    if not changes:
        log_info("No changes to commit.")
        return True
    
    # Generate default commit message if not provided
    if not commit_message:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        files_changed = [f[1] for f in changes]
        memory_files = [f for f in files_changed if "memory" in f]
        other_files = [f for f in files_changed if "memory" not in f]
        
        parts = []
        if memory_files:
            parts.append(f"Update memory: {', '.join(memory_files)}")
        if other_files:
            parts.append(f"Update files: {', '.join(other_files)}")
        
        commit_message = f"Auto-commit: {' | '.join(parts)} ({timestamp})"
    
    # Add all changed files
    try:
        # First add all memory files
        memory_files = [f[1] for f in changes if "memory" in f[1]]
        if memory_files:
            for file in memory_files:
                log_debug(f"Adding memory file: {file}")
                subprocess.run(["git", "add", file], cwd=repo_path, check=True)
        
        # Then add all other files
        other_files = [f[1] for f in changes if "memory" not in f[1]]
        if other_files:
            for file in other_files:
                log_debug(f"Adding file: {file}")
                subprocess.run(["git", "add", file], cwd=repo_path, check=True)
        
        # Commit the changes
        log_info(f"Committing with message: {commit_message}")
        result = subprocess.run(
            ["git", "commit", "-m", commit_message],
            cwd=repo_path,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            log_info(f"Auto-commit successful: {result.stdout.strip()}")
            return True
        else:
            log_error(f"Auto-commit failed: {result.stderr.strip()}")
            return False
    except Exception as e:
        log_error(f"Error during auto-commit: {e}")
        return False

def register_end_of_conversation_hook(repo_path):
    """
    Register a hook that will be called at the end of a conversation to auto-commit changes.
    
    Args:
        repo_path (str): Path to the repository
    """
    log_info("Registering end-of-conversation hook for auto-commit")
    
    # TODO: Implement proper hook registration
    # Currently, this would need to be called manually or by another script
    pass

def main():
    """
    Main function to run the auto-commit script.
    
    Returns:
        int: 0 for success, 1 for failure
    """
    # Get the path to the God Mode project
    god_mode_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    
    # Check command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "--register-hook":
            register_end_of_conversation_hook(god_mode_path)
            return 0
        elif sys.argv[1] == "--help" or sys.argv[1] == "-h":
            print("Usage:")
            print("  script_auto_commit.py [--register-hook | --force | --message 'Commit message']")
            print("  --register-hook: Register a hook to auto-commit at the end of a conversation")
            print("  --force: Force commit even if no memory files have changed")
            print("  --message 'Commit message': Specify a custom commit message")
            return 0
        elif sys.argv[1] == "--message" and len(sys.argv) > 2:
            message = sys.argv[2]
            success = auto_commit(god_mode_path, message)
            return 0 if success else 1
    
    # Default behavior: auto-commit if there are changes
    success = auto_commit(god_mode_path)
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main()) 