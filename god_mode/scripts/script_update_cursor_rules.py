#!/usr/bin/env python3
"""
Cursor Rules Update Script

This script updates the Cursor rules to ensure the AI includes appropriate markers
in its responses for automatic documentation. It supports both legacy .cursorrules 
text format and modern cursorrules.json format.

Usage:
    python script_update_cursor_rules.py [--force]

The script will update the rules file if it exists, or create it if it doesn't.
Use the --force flag to overwrite existing marker rules.
"""

import os
import sys
import argparse
from pathlib import Path
import re
import json

# Get the directory of this script
SCRIPT_DIR = Path(os.path.dirname(os.path.abspath(__file__)))

# Define the project root relative to this script
PROJECT_ROOT = SCRIPT_DIR.parent.parent

# Define the God Mode directory
GOD_MODE_DIR = SCRIPT_DIR.parent

# Define paths to cursor rules files (both legacy and modern)
CURSOR_RULES_FILE_LEGACY = PROJECT_ROOT / ".cursor" / ".cursorrules"
CURSOR_RULES_FILE_JSON = PROJECT_ROOT / ".cursor" / "cursorrules.json"
CURSOR_CONFIG_FILE = PROJECT_ROOT / ".cursor" / "cursor.json"

# Define marker rule template for legacy text format
MARKER_RULES = """
# Message Router Markers
All comprehensive responses that contain significant code changes, design decisions, 
or insights MUST include markup with appropriate markers for the message router:

1. Include a [LOG_SUMMARY] with a brief description of the changes (1-2 sentences).
2. Include a [LOG_DETAIL] with comprehensive explanation of the changes.
3. Include a [MEMORY_UPDATE] for relevant project context updates that should be remembered.
4. Use [FEATURE_LOG: FeatureName] for specific feature updates.
5. Use [DOC_UPDATE: project/feature/design/data] for documentation updates.
6. Use specific memory markers for specialized updates:
   - [MEMORY_LEARNINGS] - For insights and lessons learned
   - [MEMORY_ARCHITECTURE] - For architecture changes
   - [MEMORY_REQUIREMENTS] - For requirement changes
   - [MEMORY_ROADMAP] - For roadmap updates
   - [MEMORY_CONVENTIONS] - For convention changes
   - [MEMORY_DEPENDENCIES] - For dependency changes
   - [MEMORY_GLOSSARY] - For terminology updates
   - [MEMORY_TESTING] - For testing updates
   - [MEMORY_SECURITY] - For security updates
   - [MEMORY_PERFORMANCE] - For performance updates
   - [MEMORY_ACCESSIBILITY] - For accessibility updates
7. For efficiency, use [MULTI_TAG: TAG1, TAG2, ...] to route the same content to multiple destinations
   without repeating yourself. For example:
   
   [MULTI_TAG: LOG_SUMMARY, FEATURE_LOG: Authentication]
   Implemented JWT authentication with refresh token rotation.

These markers must be formatted exactly as shown (with square brackets) and must be placed
on their own lines, followed by the relevant content. This markup enables automatic 
documentation and persistent memory across sessions.

Example format:
[LOG_SUMMARY]
Brief summary of the changes in 1-2 sentences.

[LOG_DETAIL]
Detailed explanation of changes with markdown formatting.
- What was implemented
- Why it was done this way
- Any alternatives considered

[MEMORY_UPDATE]
Important architectural decisions or context that future sessions should be aware of.

Example with multi-tag:
[MULTI_TAG: MEMORY_UPDATE, MEMORY_ARCHITECTURE]
The system now uses a microservice architecture with service discovery.
"""

# Define God Mode rules for modern JSON format
GOD_MODE_JSON_RULES = {
    "name": "God Mode Content Routing",
    "description": "Route content to specific files based on tags",
    "rules": [
        {
            "name": "Include structured tags in your answers",
            "description": "When providing information that should be saved for future reference, include special tags",
            "prompts": [
                {
                    "rule": """Always include appropriate tags when generating important information. Use exactly one of these tag formats in your responses when appropriate:

1. [LOG_SUMMARY]: Brief, high-level summary of key decisions or insights
2. [LOG_DETAIL]: Detailed technical discussions or explorations
3. [MEMORY_UPDATE]: Important facts to remember for future discussions
4. [REFERENCE: Name]: Technical details that should be saved for reference
5. [FEATURE_LOG: Name]: Notes about a specific feature's implementation
6. [DOCUMENTATION: Path]: Documentation for a specific component
7. [DOC_UPDATE: project/feature/design/data]: Documentation updates for specific areas
8. Use specific memory markers for specialized updates:
   - [MEMORY_LEARNINGS]: For insights and lessons learned
   - [MEMORY_ARCHITECTURE]: For architecture changes
   - [MEMORY_REQUIREMENTS]: For requirement changes
   - [MEMORY_ROADMAP]: For roadmap updates
   - [MEMORY_CONVENTIONS]: For convention changes
   - [MEMORY_DEPENDENCIES]: For dependency changes
   - [MEMORY_GLOSSARY]: For terminology updates
   - [MEMORY_TESTING]: For testing updates
   - [MEMORY_SECURITY]: For security updates
   - [MEMORY_PERFORMANCE]: For performance updates
   - [MEMORY_ACCESSIBILITY]: For accessibility updates
9. [MULTI_TAG: TAG1, TAG2, ...]: Route the same content to multiple tags at once

Example usage: [LOG_SUMMARY] Today we implemented the authentication system using JWT tokens, which will allow us to securely identify users."""
                }
            ]
        }
    ]
}

def ensure_directory_exists(directory):
    """Ensure a directory exists, creating it if necessary."""
    os.makedirs(directory, exist_ok=True)

def read_cursor_rules_legacy():
    """
    Read the existing .cursorrules file.
    
    Returns:
        str: The content of the .cursorrules file, or empty string if it doesn't exist
    """
    if not CURSOR_RULES_FILE_LEGACY.exists():
        return ""
    
    try:
        with open(CURSOR_RULES_FILE_LEGACY, 'r') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading .cursorrules file: {e}", file=sys.stderr)
        return ""

def write_cursor_rules_legacy(content):
    """
    Write content to the .cursorrules file.
    
    Args:
        content (str): The content to write
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Ensure the directory exists
        ensure_directory_exists(CURSOR_RULES_FILE_LEGACY.parent)
        
        # Write the content to the file
        with open(CURSOR_RULES_FILE_LEGACY, 'w') as f:
            f.write(content)
        
        return True
    except Exception as e:
        print(f"Error writing .cursorrules file: {e}", file=sys.stderr)
        return False

def has_marker_rules_legacy(content):
    """
    Check if the content already has marker rules.
    
    Args:
        content (str): The content to check
        
    Returns:
        bool: True if marker rules exist, False otherwise
    """
    patterns = [
        r"Message\s+Router\s+Markers",
        r"\[LOG_SUMMARY\]",
        r"\[LOG_DETAIL\]",
        r"\[MEMORY_UPDATE\]"
    ]
    
    for pattern in patterns:
        if re.search(pattern, content):
            return True
    
    return False

def update_cursor_rules_legacy(force=False):
    """
    Update the .cursorrules file with marker rules.
    
    Args:
        force (bool): Whether to force update even if marker rules already exist
        
    Returns:
        bool: True if successful, False otherwise
    """
    # Read the existing rules
    existing_rules = read_cursor_rules_legacy()
    
    # Check if marker rules already exist
    if has_marker_rules_legacy(existing_rules) and not force:
        print("Marker rules already exist in .cursorrules file.")
        print("Use --force to update them anyway.")
        return True
    
    # Add marker rules
    if existing_rules:
        # Add marker rules after the existing content
        updated_rules = existing_rules + "\n\n" + MARKER_RULES
    else:
        # Create new file with default rules and marker rules
        default_rules = """# Cursor Rules
# These rules guide the AI assistant in the Cursor IDE

# General Guidelines
Try to be helpful and informative. Provide context and explanation when appropriate.
Prioritize writing correct, efficient, and maintainable code.
When showing examples, ensure they are correct and follow best practices.
"""
        updated_rules = default_rules + "\n\n" + MARKER_RULES
    
    # Write the updated rules
    success = write_cursor_rules_legacy(updated_rules)
    
    if success:
        print(f"✅ Successfully updated legacy .cursorrules file at {CURSOR_RULES_FILE_LEGACY}")
    else:
        print(f"❌ Failed to update legacy .cursorrules file.")
    
    return success

def update_cursor_rules_json(force=False):
    """
    Update or create the cursorrules.json file.
    
    Args:
        force (bool): Whether to force update even if rule file already exists
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Ensure the directory exists
        ensure_directory_exists(CURSOR_RULES_FILE_JSON.parent)
        
        # Check if file exists and if we should update it
        if CURSOR_RULES_FILE_JSON.exists() and not force:
            # Read existing rules
            with open(CURSOR_RULES_FILE_JSON, 'r') as f:
                existing_rules = json.load(f)
            
            # Check if God Mode rule already exists
            has_god_mode_rule = False
            for rule in existing_rules.get('rules', []):
                if "God Mode" in rule.get('name', ''):
                    has_god_mode_rule = True
                    break
            
            if has_god_mode_rule:
                print(f"✅ JSON rules file already contains God Mode rules.")
                return True
            
            # Add our rule to existing rules
            existing_rules['rules'] = existing_rules.get('rules', []) + GOD_MODE_JSON_RULES['rules']
            rules_to_write = existing_rules
        else:
            # Create new file or force overwrite
            rules_to_write = GOD_MODE_JSON_RULES
        
        # Write the rules
        with open(CURSOR_RULES_FILE_JSON, 'w') as f:
            json.dump(rules_to_write, f, indent=2)
        
        print(f"✅ Successfully updated JSON rules file at {CURSOR_RULES_FILE_JSON}")
        return True
        
    except Exception as e:
        print(f"❌ Error updating cursorrules.json: {e}", file=sys.stderr)
        return False

def update_cursor_config_json():
    """
    Update the cursor.json config file to set enhanced mode.
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        config = {}
        if CURSOR_CONFIG_FILE.exists():
            with open(CURSOR_CONFIG_FILE, 'r') as f:
                config = json.load(f)
        
        # Set enhanced mode
        config["alwaysProvideRequestedFiles"] = True
        config["enhancedContextEnabled"] = True
        
        # Ensure the directory exists
        ensure_directory_exists(CURSOR_CONFIG_FILE.parent)
        
        # Write the updated config
        with open(CURSOR_CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"✅ Successfully updated cursor.json config file at {CURSOR_CONFIG_FILE}")
        return True
    except Exception as e:
        print(f"❌ Error updating cursor.json config file: {e}", file=sys.stderr)
        return False

def main():
    """Main function to parse arguments and update cursor rules."""
    parser = argparse.ArgumentParser(description='Update Cursor rules for message router markers.')
    parser.add_argument('--force', action='store_true', help='Force update even if marker rules already exist')
    args = parser.parse_args()
    
    print(f"\n🔮 Updating God Mode Cursor rules...")
    print(f"Project root: {PROJECT_ROOT}")
    
    # Update modern JSON rules (preferred by newer Cursor versions)
    json_success = update_cursor_rules_json(args.force)
    
    # Also update legacy text rules for backwards compatibility
    legacy_success = update_cursor_rules_legacy(args.force)
    
    # Update cursor config
    config_success = update_cursor_config_json()
    
    if json_success and config_success:
        print("\n✅ God Mode Cursor rules updated successfully!")
        print("The AI assistant will now be prompted to include [TAG] markers in its responses.")
        print("Examples of tags: [LOG_SUMMARY], [MEMORY_UPDATE], [DOCUMENTATION: Path], etc.")
        print("You can also use [MULTI_TAG: TAG1, TAG2, ...] to route content to multiple destinations.")
    else:
        print("\n⚠️ Some updates may not have been applied successfully.")
        print("Check the error messages above for details.")
    
    return 0 if (json_success or legacy_success) and config_success else 1

if __name__ == "__main__":
    sys.exit(main()) 