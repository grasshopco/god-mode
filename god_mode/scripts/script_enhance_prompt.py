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
import pyperclip
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
    """Get a condensed version of the project structure."""
    structure_file = GOD_MODE_DIR / "memory" / "memory_project_structure.md"
    
    if not structure_file.exists():
        log_debug(f"Project structure file not found at {structure_file}")
        return f"[Project structure file not found at {structure_file}]"
    
    try:
        with open(structure_file, 'r') as f:
            content = f.read()
            
        # Extract just the directory structure part (simplified)
        if "## Directory Structure" in content:
            parts = content.split("## Directory Structure")
            if len(parts) > 1:
                structure_part = parts[1].split("##")[0].strip()
                # Limit to first 1000 chars to avoid overloading the prompt
                if len(structure_part) > 1000:
                    structure_part = structure_part[:1000] + "\n[... truncated ...]"
                return structure_part
            
        # Fall back to a simpler approach if the section isn't found
        lines = content.split("\n")
        # Get first 30 lines
        simplified = "\n".join(lines[:30])
        simplified += "\n[... truncated ...]"
        return simplified
    except Exception as e:
        log_error(f"Error reading project structure: {e}")
        return f"[Error reading project structure: {e}]"

def get_memory_highlights():
    """Get highlights from memory files."""
    memory_dir = GOD_MODE_DIR / "memory"
    
    if not memory_dir.exists() or not memory_dir.is_dir():
        log_debug(f"Memory directory not found at {memory_dir}")
        return f"[Memory directory not found at {memory_dir}]"
    
    try:
        highlights = []
        
        # Try to read the main memory file
        cursor_memory = memory_dir / "MEMORY_CURSOR.md"
        if cursor_memory.exists():
            with open(cursor_memory, 'r') as f:
                content = f.read()
                # Extract 5 random lines that might be meaningful
                lines = [line.strip() for line in content.split("\n") 
                         if line.strip() and not line.startswith("#") and len(line) > 20]
                if lines:
                    import random
                    sample_size = min(5, len(lines))
                    highlights.append("From MEMORY_CURSOR.md:")
                    highlights.extend(random.sample(lines, sample_size))
        
        # Recent learnings
        learnings = memory_dir / "memory_learnings.md"
        if learnings.exists():
            with open(learnings, 'r') as f:
                content = f.read()
                # Try to extract the most recent learning
                if "## " in content:
                    latest_section = content.split("## ")[-1]
                    # Limit to first 300 chars
                    if len(latest_section) > 300:
                        latest_section = latest_section[:300] + "..."
                    highlights.append("\nLatest learning:")
                    highlights.append(latest_section)
        
        return "\n".join(highlights) if highlights else "[No memory highlights found]"
    except Exception as e:
        log_error(f"Error getting memory highlights: {e}")
        return f"[Error getting memory highlights: {e}]"

def get_recent_logs():
    """Get recent log entries."""
    logs_dir = GOD_MODE_DIR / "logs"
    
    if not logs_dir.exists() or not logs_dir.is_dir():
        log_debug(f"Logs directory not found at {logs_dir}")
        return f"[Logs directory not found at {logs_dir}]"
    
    try:
        # Try to read from the all logs file
        all_logs = GOD_MODE_DIR / "memory" / "memory_logs_all.md"
        if all_logs.exists():
            with open(all_logs, 'r') as f:
                content = f.read()
                # Extract the 5 most recent log entries
                lines = content.split("\n")
                
                # Find lines with timestamps (YYYY-MM-DD)
                timestamp_lines = []
                for i, line in enumerate(lines):
                    if re.search(r'\d{4}-\d{2}-\d{2}', line):
                        timestamp_lines.append(i)
                
                # Get the 5 most recent entries
                recent_entries = []
                for i in timestamp_lines[:5]:
                    # Get this line and up to 2 lines after it
                    entry = "\n".join(lines[i:i+3])
                    recent_entries.append(entry)
                
                if recent_entries:
                    return "Recent log entries:\n" + "\n\n".join(recent_entries)
        
        # Fall back to looking for log files
        log_files = list(logs_dir.glob("*.log"))
        if log_files:
            # Get the most recently modified log file
            latest_log = max(log_files, key=os.path.getmtime)
            with open(latest_log, 'r') as f:
                # Get the last 10 lines
                content = f.read().split("\n")[-10:]
                return f"Latest logs from {latest_log.name}:\n" + "\n".join(content)
        
        return "[No recent logs found]"
    except Exception as e:
        log_error(f"Error getting recent logs: {e}")
        return f"[Error getting recent logs: {e}]"

def enhance_prompt(user_prompt):
    """Enhance a user prompt with relevant context."""
    log_info(f"Enhancing prompt: {user_prompt[:50]}{'...' if len(user_prompt) > 50 else ''}")
    
    # Get context information
    project_structure = get_project_structure()
    memory_highlights = get_memory_highlights()
    recent_logs = get_recent_logs()
    
    # Build the enhanced prompt
    separator = "\n\n" + "=" * 40 + "\n\n"
    enhanced_prompt = f"""
{user_prompt}

{separator}
CONTEXT: You're working on a project with the following structure:

{project_structure}

{separator}
MEMORY HIGHLIGHTS:

{memory_highlights}

{separator}
RECENT ACTIVITY:

{recent_logs}
"""
    
    log_info("Prompt enhanced with project context")
    return enhanced_prompt

def extract_prompt_enhancement_from_clipboard():
    """Extract PROMPT_ENHANCEMENT content from clipboard."""
    try:
        # Get clipboard content
        clipboard_content = pyperclip.paste()
        
        # Extract content between PROMPT_ENHANCEMENT tags
        pattern = r'<PROMPT_ENHANCEMENT>(.*?)</PROMPT_ENHANCEMENT>'
        match = re.search(pattern, clipboard_content, re.DOTALL)
        
        if match:
            enhancement_content = match.group(1).strip()
            log_info("Successfully extracted PROMPT_ENHANCEMENT content from clipboard")
            return enhancement_content
        else:
            log_warning("No PROMPT_ENHANCEMENT tags found in clipboard")
            return None
    except Exception as e:
        log_error(f"Error extracting PROMPT_ENHANCEMENT from clipboard: {e}")
        return None

def update_prompt_enhanced_file(enhancement_content):
    """Update the prompt_enhanced.md file with new content."""
    if not enhancement_content:
        log_warning("No enhancement content provided")
        return False
    
    prompt_enhanced_file = GOD_MODE_DIR / "memory" / "prompt_enhanced.md"
    last_message_file = GOD_MODE_DIR / "memory" / ".last_user_message"
    
    try:
        # Get the last user message if available
        user_message = ""
        if last_message_file.exists():
            try:
                with open(last_message_file, 'r') as f:
                    user_message = f.read().strip()
            except Exception as e:
                log_warning(f"Could not read last user message: {e}")
        
        # Create file if it doesn't exist
        if not prompt_enhanced_file.exists():
            prompt_enhanced_file.parent.mkdir(parents=True, exist_ok=True)
            with open(prompt_enhanced_file, 'w') as f:
                f.write("# Enhanced Prompts History\n\n## Current Enhanced Prompt\n\n*Last Updated: Never*\n\n[No enhanced prompts yet]\n\n## Version History\n\n")
        
        # Read existing content
        with open(prompt_enhanced_file, 'r') as f:
            existing_content = f.read()
        
        # Current timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Update current enhanced prompt
        current_section = f"## Current Enhanced Prompt\n\n*Last Updated: {timestamp}*\n\n{enhancement_content}"
        
        # Add to version history with user message
        version_entry = f"### Version {int(time.time())} - {timestamp}\n\n"
        if user_message:
            version_entry += f"**User's Message:**\n```\n{user_message}\n```\n\n"
        version_entry += f"**Enhanced Prompt:**\n{enhancement_content}"
        
        # Find where to insert the version
        if "## Version History" in existing_content:
            parts = existing_content.split("## Version History")
            new_content = parts[0].split("## Current Enhanced Prompt")[0] + current_section + "\n\n## Version History\n\n" + version_entry + "\n\n" + parts[1].strip()
        else:
            new_content = existing_content.split("## Current Enhanced Prompt")[0] + current_section + "\n\n## Version History\n\n" + version_entry
        
        # Write updated content
        with open(prompt_enhanced_file, 'w') as f:
            f.write(new_content)
        
        log_info(f"Successfully updated {prompt_enhanced_file}")
        return True
    
    except Exception as e:
        log_error(f"Error updating prompt_enhanced.md: {e}")
        return False

def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(description='Enhance user prompts with project context')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--prompt', help='User prompt to enhance')
    group.add_argument('--update-from-clipboard', action='store_true', help='Extract PROMPT_ENHANCEMENT from clipboard and update prompt_enhanced.md')
    
    args = parser.parse_args()
    
    if args.prompt:
        enhanced = enhance_prompt(args.prompt)
        print("\nEnhanced prompt:")
        print(enhanced)
        try:
            pyperclip.copy(enhanced)
            print("\nThe enhanced prompt has been copied to your clipboard!")
        except Exception as e:
            log_error(f"Error copying to clipboard: {e}")
            print("\nError copying to clipboard. Please manually copy the enhanced prompt.")
    
    elif args.update_from_clipboard:
        enhancement_content = extract_prompt_enhancement_from_clipboard()
        if enhancement_content:
            success = update_prompt_enhanced_file(enhancement_content)
            if success:
                print("Successfully updated prompt enhancement file!")
                return 0
            else:
                print("Failed to update prompt enhancement file.")
                return 1
        else:
            print("No PROMPT_ENHANCEMENT content found in clipboard.")
            return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 