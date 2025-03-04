#!/usr/bin/env python3
"""
Prompt Enhancement Script

This script enhances user prompts with relevant context from the project,
including project structure, memory files, and recent logs.
"""

import os
import sys
import re
import json
import argparse
import sqlite3
import time
from pathlib import Path
from datetime import datetime

# Add the parent directory to sys.path for importing helper modules
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

# Get the God Mode directory
GOD_MODE_DIR = Path(parent_dir)
PROJECT_ROOT = GOD_MODE_DIR.parent

# Define logging functions
def log_message(message, level="INFO"):
    """Log a message with timestamp and level."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [{level}] {message}")
    sys.stdout.flush()

def log_debug(message):
    """Log a debug message."""
    if os.environ.get("DEBUG_MODE", "").lower() in ("1", "true", "yes"):
        log_message(message, "DEBUG")

def log_error(message):
    """Log an error message."""
    log_message(message, "ERROR")

def log_info(message):
    """Log an info message."""
    log_message(message, "INFO")

def log_warning(message):
    """Log a warning message."""
    log_message(message, "WARNING")

def get_project_structure():
    """
    Get a summary of the project structure.
    
    Returns:
        str: A brief summary of the project structure
    """
    try:
        # Get the project structure from the memory file
        structure_file = GOD_MODE_DIR / "memory" / "memory_project_structure.md"
        if structure_file.exists():
            with open(structure_file, 'r') as f:
                content = f.read()
                
                # Extract just the top-level directories and some key files
                summary_lines = []
                for line in content.splitlines():
                    if '📁' in line and '/' not in line.split('📁')[1]:
                        summary_lines.append(line.strip())
                    elif '📄' in line and line.count('/') <= 1:
                        summary_lines.append(line.strip())
                
                # Limit to 15 lines max
                if len(summary_lines) > 15:
                    summary_lines = summary_lines[:12] + ["..."] + summary_lines[-2:]
                
                return "## Project Structure Summary\n" + "\n".join(summary_lines)
        return ""
    except Exception as e:
        log_error(f"Error getting project structure: {e}")
        return ""

def get_memory_highlights():
    """
    Get highlights from memory files.
    
    Returns:
        str: A summary of key information from memory files
    """
    try:
        memory_dir = GOD_MODE_DIR / "memory"
        
        if not memory_dir.exists():
            return ""
        
        # List of important memory files
        memory_files = [
            "MEMORY_CURSOR.md",
            "memory_architecture.md",
            "memory_conventions.md",
            "memory_requirements.md",
            "memory_logs_all.md"
        ]
        
        highlights = []
        
        for file_name in memory_files:
            file_path = memory_dir / file_name
            if file_path.exists():
                with open(file_path, 'r') as f:
                    content = f.read()
                    # Get the title and a brief excerpt
                    title = file_name.replace('.md', '').replace('_', ' ').title()
                    
                    # Extract the most recent entry if possible
                    entry_matches = re.findall(r'##\s.*?\n(.*?)(?=##|\Z)', content, re.DOTALL)
                    if entry_matches:
                        latest_entry = entry_matches[-1].strip()
                        # Truncate long entries
                        if len(latest_entry) > 200:
                            latest_entry = latest_entry[:197] + "..."
                        highlights.append(f"### {title}\n{latest_entry}")
        
        if highlights:
            return "## Memory Highlights\n" + "\n\n".join(highlights)
        return ""
    except Exception as e:
        log_error(f"Error getting memory highlights: {e}")
        return ""

def get_recent_logs():
    """
    Get recent logs for context.
    
    Returns:
        str: Recent log entries
    """
    try:
        log_file = GOD_MODE_DIR / "memory" / "memory_logs_all.md"
        
        if not log_file.exists():
            return ""
        
        with open(log_file, 'r') as f:
            content = f.read()
            
            # Extract the most recent few log entries
            entry_matches = re.findall(r'##\s.*?\n(.*?)(?=##|\Z)', content, re.DOTALL)
            if entry_matches:
                # Get the 3 most recent entries
                recent_entries = entry_matches[-3:]
                
                logs = []
                for entry in recent_entries:
                    # Truncate long entries
                    if len(entry) > 150:
                        entry = entry[:147] + "..."
                    logs.append(entry.strip())
                
                return "## Recent Activity\n" + "\n\n".join(logs)
        return ""
    except Exception as e:
        log_error(f"Error getting recent logs: {e}")
        return ""

def enhance_prompt(user_prompt):
    """
    Enhance a user prompt with relevant context.
    
    Args:
        user_prompt (str): The original user prompt
        
    Returns:
        str: The enhanced prompt with added context
    """
    # Don't enhance very short prompts or those that seem like commands
    if len(user_prompt) < 20 or user_prompt.startswith('/'):
        log_info("Not enhancing short prompt or command")
        return user_prompt
    
    # Collect context
    context_parts = []
    
    project_structure = get_project_structure()
    if project_structure:
        context_parts.append(project_structure)
    
    memory_highlights = get_memory_highlights()
    if memory_highlights:
        context_parts.append(memory_highlights)
    
    recent_logs = get_recent_logs()
    if recent_logs:
        context_parts.append(recent_logs)
    
    # If no context was collected, just return the original prompt
    if not context_parts:
        log_info("No context available for enhancement")
        return user_prompt
    
    # Build the enhanced prompt
    context = "\n\n".join(context_parts)
    
    # Save the context to a file for debugging
    try:
        with open(GOD_MODE_DIR / ".cache" / "last_prompt_context.md", 'w') as f:
            f.write(context)
    except Exception as e:
        log_error(f"Error saving context: {e}")
    
    log_info(f"Enhanced prompt with {len(context_parts)} context sections")
    
    return f"{context}\n\n{user_prompt}"

def main():
    """
    Main function to parse arguments and enhance prompts.
    """
    parser = argparse.ArgumentParser(description='Enhance user prompts with context from the project.')
    parser.add_argument('--message', type=str, help='The message to enhance')
    parser.add_argument('--message-id', type=str, help='The ID of the message to enhance (for database lookup)')
    args = parser.parse_args()
    
    if args.message:
        # Enhance the provided message
        enhanced_prompt = enhance_prompt(args.message)
        print(enhanced_prompt)
    elif args.message_id:
        # This would look up the message in the database and update it directly
        # Currently a placeholder for future implementation
        log_warning(f"Direct database update not implemented. ID: {args.message_id}")
    else:
        log_error("No message provided to enhance. Use --message or --message-id")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 