#!/usr/bin/env python3
"""
Feature Log Checker Script

This script checks all feature log files to ensure they follow the proper template structure.
If a feature log doesn't match the template, it will update it to match while preserving existing content.

Usage:
    python script_check_feature_logs.py [--fix]
"""

import os
import sys
import argparse
import re
from pathlib import Path
import datetime
import difflib

# Get the directory of this script
SCRIPT_DIR = Path(os.path.dirname(os.path.abspath(__file__)))

# Define paths
PROJECT_ROOT = SCRIPT_DIR.parent.parent
MEMORY_DIR = SCRIPT_DIR.parent / "memory"
FEATURES_DIR = MEMORY_DIR / "logs" / "features"
TEMPLATE_DIR = SCRIPT_DIR.parent / "templates"
TEMPLATE_FILE = TEMPLATE_DIR / "template_log_feature.md"

def ensure_directory_exists(directory):
    """Ensure a directory exists, creating it if necessary."""
    os.makedirs(directory, exist_ok=True)

def get_timestamp():
    """Get current timestamp in YYYY-MM-DD HH:MM UTC format."""
    now_utc = datetime.datetime.now(datetime.timezone.utc)
    return now_utc.strftime("%Y-%m-%d %H:%M UTC")

def extract_feature_name(filename):
    """Extract the feature name from a feature log filename."""
    match = re.match(r'memory_log_feature_(.+)\.md', filename)
    if match:
        return match.group(1).replace('_', ' ').title()
    return None

def get_template_structure():
    """
    Read the template file and extract its structure.
    
    Returns:
        dict: A dictionary mapping section names to their positions in the template
    """
    if not TEMPLATE_FILE.exists():
        print(f"Error: Template file not found at {TEMPLATE_FILE}", file=sys.stderr)
        return None
    
    with open(TEMPLATE_FILE, 'r', encoding='utf-8') as f:
        template_content = f.read()
    
    # Find all section headers
    sections = {}
    for i, line in enumerate(template_content.split('\n')):
        if line.startswith('## ') or line.startswith('### '):
            sections[line.strip('#').strip()] = i
    
    return {
        'content': template_content,
        'sections': sections
    }

def extract_existing_content(log_content):
    """
    Extract existing content from a feature log file.
    
    Returns:
        dict: A dictionary mapping section names to their content
    """
    sections = {}
    current_section = None
    current_content = []
    
    for line in log_content.split('\n'):
        if line.startswith('## ') or line.startswith('### '):
            # Save the previous section if there was one
            if current_section:
                sections[current_section] = '\n'.join(current_content)
                current_content = []
            
            current_section = line.strip('#').strip()
        elif current_section:
            current_content.append(line)
    
    # Save the last section
    if current_section:
        sections[current_section] = '\n'.join(current_content)
    
    return sections

def check_feature_log(file_path, template, fix=False):
    """
    Check if a feature log file follows the template structure.
    
    Args:
        file_path: Path to the feature log file
        template: Template structure dictionary
        fix: Whether to fix issues or just report them
        
    Returns:
        bool: True if the file matches the template, False otherwise
    """
    print(f"Checking {file_path.name}...")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        log_content = f.read()
    
    # Extract the feature name
    feature_name = extract_feature_name(file_path.name)
    if not feature_name:
        feature_name = "Unknown Feature"
    
    # Check if the file has the basic structure
    existing_sections = extract_existing_content(log_content)
    template_sections = template['sections']
    
    missing_sections = []
    for section in template_sections:
        if section not in existing_sections:
            missing_sections.append(section)
    
    if not missing_sections:
        print(f"✅ {file_path.name} matches the template structure")
        return True
    
    print(f"❌ {file_path.name} is missing {len(missing_sections)} sections: {', '.join(missing_sections)}")
    
    if not fix:
        return False
    
    # Fix the file
    print(f"Fixing {file_path.name}...")
    
    # Start with the template content
    new_content = template['content']
    
    # Replace [FEATURE_NAME] with the actual feature name
    new_content = new_content.replace('[FEATURE_NAME]', feature_name)
    
    # Replace sections with existing content
    for section, content in existing_sections.items():
        if section in template_sections:
            # Construct a placeholder that we can replace
            placeholder = f"[{section.upper().replace(' ', '_')}]"
            new_content = new_content.replace(placeholder, content.strip())
    
    # Add a note about the file being automatically updated
    update_note = f"\n\n*This file was automatically updated to match the template structure on {get_timestamp()}*"
    new_content += update_note
    
    # Create a backup of the original file
    backup_path = file_path.with_suffix('.bak')
    with open(backup_path, 'w', encoding='utf-8') as f:
        f.write(log_content)
    print(f"Created backup at {backup_path}")
    
    # Write the updated content
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"✅ Fixed {file_path.name}")
    return True

def main():
    parser = argparse.ArgumentParser(description="Check and fix feature log files")
    parser.add_argument("--fix", action="store_true", help="Fix files that don't match the template")
    args = parser.parse_args()
    
    # Ensure the features directory exists
    ensure_directory_exists(FEATURES_DIR)
    
    # Get the template structure
    template = get_template_structure()
    if not template:
        sys.exit(1)
    
    # Check all feature log files
    feature_logs = []
    
    # Check files in the memory directory
    for file in MEMORY_DIR.glob('memory_log_feature_*.md'):
        feature_logs.append(file)
    
    # Check files in the features directory
    for file in FEATURES_DIR.glob('memory_log_feature_*.md'):
        feature_logs.append(file)
    
    if not feature_logs:
        print("No feature log files found")
        return
    
    issues_found = 0
    for file in feature_logs:
        if not check_feature_log(file, template, args.fix):
            issues_found += 1
    
    if issues_found:
        if args.fix:
            print(f"Fixed {issues_found} feature log files")
        else:
            print(f"Found {issues_found} feature log files that don't match the template")
            print("Run with --fix to update them")
    else:
        print("All feature log files match the template")

if __name__ == "__main__":
    main() 