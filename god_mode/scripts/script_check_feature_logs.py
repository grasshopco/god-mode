#!/usr/bin/env python3
"""
Feature Log Checker Script

This script checks all feature log files to ensure they follow the proper template structure.
If a feature log doesn't match the template, it will update it to match while preserving existing content.

Key features:
1. Validates all feature logs against the template structure
2. Fixes non-compliant logs by preserving content but updating structure
3. Updates roadmap files to mark relevant tasks as completed
4. Generates detailed summaries of changes

Usage:
    python script_check_feature_logs.py [--fix] [--check-only] [--update-roadmap]
"""

import os
import sys
import argparse
import re
from pathlib import Path
import datetime
import difflib
import subprocess

# Get the directory of this script
SCRIPT_DIR = Path(os.path.dirname(os.path.abspath(__file__)))

# Define paths
PROJECT_ROOT = SCRIPT_DIR.parent.parent
MEMORY_DIR = SCRIPT_DIR.parent / "memory"
FEATURES_DIR = MEMORY_DIR / "logs" / "features"
TEMPLATE_DIR = SCRIPT_DIR.parent / "templates"
TEMPLATE_FILE = TEMPLATE_DIR / "template_log_feature.md"
ROADMAP_DIR = SCRIPT_DIR.parent / "roadmap"

def ensure_directory_exists(directory):
    """Ensure a directory exists, creating it if necessary."""
    os.makedirs(directory, exist_ok=True)

def get_timestamp():
    """Get current timestamp in YYYY-MM-DD HH:MM UTC format."""
    now_utc = datetime.datetime.now(datetime.timezone.utc)
    return now_utc.strftime("%Y-%m-%d %H:%M UTC")

def get_detailed_timestamp():
    """Get detailed timestamp in YYYY-MM-DD HH:MM:SS format."""
    now_utc = datetime.datetime.now(datetime.timezone.utc)
    return now_utc.strftime("%Y-%m-%d %H:%M:%S")

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
        str: The template structure
    """
    if not TEMPLATE_FILE.exists():
        print(f"Error: Template file not found at {TEMPLATE_FILE}")
        return None
    
    try:
        with open(TEMPLATE_FILE, 'r') as f:
            template = f.read()
        
        # Replace placeholders with feature-specific values
        template = template.replace('[FEATURE_NAME]', '{feature_name}')
        template = template.replace('[YYYY-MM-DD HH:MM:SS]', '{timestamp}')
        
        return template
    except Exception as e:
        print(f"Error reading template file: {e}")
        return None

def extract_existing_content(log_content):
    """
    Extract existing content from a feature log while preserving structure.
    
    Args:
        log_content (str): The content of the log file
        
    Returns:
        dict: Extracted content sections
    """
    content_sections = {}
    
    # Extract Summary of Changes section
    summary_match = re.search(r'## Summary of Changes\s*\n(.*?)(?=\n##|\Z)', log_content, re.DOTALL)
    if summary_match:
        content_sections['summary'] = summary_match.group(1).strip()
    
    # Extract Detailed Changes section
    detailed_match = re.search(r'## Detailed Changes\s*\n(.*?)(?=\n## Feature Overview|\Z)', log_content, re.DOTALL)
    if detailed_match:
        content_sections['detailed'] = detailed_match.group(1).strip()
    
    # Extract Feature Overview section
    overview_match = re.search(r'## Feature Overview\s*\n(.*?)(?=\n---|\Z)', log_content, re.DOTALL)
    if overview_match:
        content_sections['overview'] = overview_match.group(1).strip()
    
    return content_sections

def find_latest_roadmap_file():
    """
    Find the most recently created or updated roadmap file.
    
    Returns:
        Path: Path to the most recent roadmap file, or None if none found
    """
    # Ensure roadmap directory exists
    ensure_directory_exists(ROADMAP_DIR)
    
    # List all roadmap files
    roadmap_files = list(ROADMAP_DIR.glob("roadmap_god_mode*.md"))
    
    if not roadmap_files:
        return None
    
    # Sort by modification time (most recent first)
    roadmap_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
    
    return roadmap_files[0]

def update_roadmap_task(task_name="Fix Feature Log Compliance"):
    """
    Update the roadmap file to mark a task as completed.
    
    Args:
        task_name (str): The name of the task to mark as completed
        
    Returns:
        bool: True if successful, False otherwise
    """
    # Attempt to use the enhance_message_content script if available
    update_script = SCRIPT_DIR / "script_enhance_message_content.py"
    if update_script.exists():
        try:
            timestamp = get_timestamp()
            cmd = [sys.executable, str(update_script), "--update-roadmap", task_name, 
                   "--notes", f"Completed by script_check_feature_logs.py at {timestamp}"]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"Updated roadmap for task '{task_name}'")
                return True
            else:
                print(f"Failed to update roadmap: {result.stderr}")
                return False
        except Exception as e:
            print(f"Error calling roadmap update script: {e}")
            return False
    
    # If the script doesn't exist, use a direct approach
    roadmap_file = find_latest_roadmap_file()
    if not roadmap_file:
        print("No roadmap file found")
        return False
    
    try:
        with open(roadmap_file, 'r') as f:
            lines = f.readlines()
        
        # Find the task and mark it as completed
        task_found = False
        for i, line in enumerate(lines):
            if task_name.lower() in line.lower() and "[ ]" in line:
                lines[i] = line.replace("[ ]", "[x]")
                timestamp = get_timestamp()
                completion_note = f"  - **Completed**: {timestamp} - Fixed by script_check_feature_logs.py\n"
                lines.insert(i + 1, completion_note)
                task_found = True
                break
        
        if not task_found:
            print(f"Task '{task_name}' not found in roadmap")
            return False
        
        with open(roadmap_file, 'w') as f:
            f.writelines(lines)
        
        print(f"Updated roadmap file: {roadmap_file}")
        return True
        
    except Exception as e:
        print(f"Error updating roadmap file: {e}")
        return False

def check_feature_log(file_path, template, fix=False):
    """
    Check if a feature log file follows the template and fix it if needed.
    
    Args:
        file_path (Path): Path to the feature log file
        template (str): The template structure
        fix (bool): Whether to fix the file if it doesn't match the template
        
    Returns:
        tuple: (needs_fix, was_fixed, error_message)
    """
    if not file_path.exists():
        return True, False, f"File not found: {file_path}"
    
    # Read the file
    try:
        with open(file_path, 'r') as f:
            content = f.read()
    except Exception as e:
        return True, False, f"Error reading file: {e}"
    
    # Extract the feature name from the filename
    feature_name = extract_feature_name(file_path.name)
    if not feature_name:
        return True, False, f"Could not extract feature name from filename: {file_path.name}"
    
    # Check for required sections
    required_sections = [
        "# Feature Log:",
        "## Summary of Changes",
        "## Detailed Changes",
        "## Feature Overview",
    ]
    
    # Check if all required sections are present
    needs_fix = False
    missing_sections = []
    
    for section in required_sections:
        if section not in content:
            needs_fix = True
            missing_sections.append(section)
    
    # Check if the file is using the template structure
    if "[YYYY-MM-DD HH:MM:SS]" in content or "Brief description" in content:
        needs_fix = True
    
    if not needs_fix:
        return False, False, "File follows template structure"
    
    if not fix:
        missing_str = ", ".join(missing_sections) if missing_sections else "Template placeholders still present"
        return True, False, f"File does not follow template structure: {missing_str}"
    
    # Fix the file
    try:
        # Extract existing content
        existing_sections = extract_existing_content(content)
        
        # Create a timestamp for the update
        timestamp = get_detailed_timestamp()
        
        # Create a basic structure if no existing content
        if not existing_sections:
            existing_sections = {
                'summary': f"- [{timestamp}] **Initial Setup** - Feature log created and structured according to template",
                'detailed': f"### [{timestamp}] Initial Setup\n\n#### Implementation Details\n\nThis feature log has been restructured to follow the standard template format.",
                'overview': f"### Purpose\n\nThe {feature_name} feature provides functionality for the God Mode system.\n\n### Technical Design\n\nDetailed technical design will be added as the feature evolves."
            }
        else:
            # If there's existing content but it has template placeholders, add a proper entry
            if "[YYYY-MM-DD HH:MM:SS]" in content:
                # Replace placeholders with real content
                entry = f"- [{timestamp}] **Initial Setup** - Feature log created and structured according to template"
                if 'summary' in existing_sections:
                    existing_sections['summary'] = existing_sections['summary'].replace("[YYYY-MM-DD HH:MM:SS] **Initial Implementation** - Brief description of initial implementation", entry)
                else:
                    existing_sections['summary'] = entry
        
        # Format the template with extracted content and feature name
        updated_content = template.format(
            feature_name=feature_name,
            timestamp=timestamp
        )
        
        # Replace template sections with existing content
        if 'summary' in existing_sections:
            updated_content = updated_content.replace("- {timestamp} **Initial Implementation** - Brief description of initial implementation\n- {timestamp} **Added functionality X** - Brief description of functionality X added\n- {timestamp} **Fixed bug Y** - Brief description of bug Y fixed\n- {timestamp} **Refactored component Z** - Brief description of component Z refactored", existing_sections['summary'])
        
        if 'detailed' in existing_sections:
            # Replace the entire Detailed Changes section after the heading
            detailed_section_start = updated_content.find("## Detailed Changes")
            detailed_section_end = updated_content.find("## Feature Overview")
            
            if detailed_section_start != -1 and detailed_section_end != -1:
                section_header = updated_content[detailed_section_start:detailed_section_start + len("## Detailed Changes")]
                updated_content = updated_content[:detailed_section_start] + section_header + "\n\n" + existing_sections['detailed'] + "\n\n" + updated_content[detailed_section_end:]
        
        if 'overview' in existing_sections:
            # Replace the entire Feature Overview section after the heading
            overview_section_start = updated_content.find("## Feature Overview")
            overview_section_end = updated_content.find("---\n\n*This log")
            
            if overview_section_start != -1 and overview_section_end != -1:
                section_header = updated_content[overview_section_start:overview_section_start + len("## Feature Overview")]
                updated_content = updated_content[:overview_section_start] + section_header + "\n\n" + existing_sections['overview'] + "\n\n" + updated_content[overview_section_end:]
        
        # Add a note that the file was updated to match the template
        updated_content += f"\n*This file was automatically updated to match the template structure on {get_timestamp()}*\n"
        
        # Compare original with updated content
        if content == updated_content:
            return False, False, "No changes needed"
        
        # Get a diff for the log
        diff = difflib.unified_diff(
            content.splitlines(),
            updated_content.splitlines(),
            fromfile=file_path.name,
            tofile=f"{file_path.name} (updated)",
            lineterm=''
        )
        
        # Write the updated content
        with open(file_path, 'w') as f:
            f.write(updated_content)
        
        # Create a backup if it doesn't exist
        backup_path = file_path.with_suffix('.bak')
        if not backup_path.exists():
            with open(backup_path, 'w') as f:
                f.write(content)
        
        return True, True, f"File updated to match template structure. Changes:\n" + "\n".join(diff)
    
    except Exception as e:
        return True, False, f"Error fixing file: {e}"

def process_all_feature_logs(fix=False, check_only=False, update_roadmap=False):
    """
    Process all feature log files to ensure they follow the template.
    
    Args:
        fix (bool): Whether to fix files that don't match the template
        check_only (bool): Only check files, don't print detailed results
        update_roadmap (bool): Whether to update the roadmap with results
        
    Returns:
        tuple: (total_files, files_needing_fix, files_fixed)
    """
    # Ensure directories exist
    ensure_directory_exists(MEMORY_DIR)
    ensure_directory_exists(FEATURES_DIR)
    
    # Get the template structure
    template = get_template_structure()
    if not template:
        print("Error: Could not get template structure")
        return 0, 0, 0
    
    # Get all feature log files
    feature_files = list(MEMORY_DIR.glob("memory_log_feature_*.md"))
    
    if not feature_files:
        print("No feature log files found")
        return 0, 0, 0
    
    total_files = len(feature_files)
    files_needing_fix = 0
    files_fixed = 0
    
    print(f"Checking {total_files} feature log files...")
    
    for file_path in feature_files:
        feature_name = extract_feature_name(file_path.name) or "Unknown"
        
        needs_fix, was_fixed, message = check_feature_log(file_path, template, fix)
        
        if needs_fix:
            files_needing_fix += 1
            
            if was_fixed:
                files_fixed += 1
                if not check_only:
                    print(f"✅ Fixed: {file_path.name} ({feature_name})")
                    print(f"  {message.split('Changes:')[0]}")
            else:
                if not check_only:
                    print(f"❌ Needs fix: {file_path.name} ({feature_name})")
                    print(f"  {message}")
        else:
            if not check_only:
                print(f"✓ OK: {file_path.name} ({feature_name})")
    
    # Update roadmap if requested and files were fixed
    if update_roadmap and files_fixed > 0:
        update_roadmap_task("Fix Feature Log Compliance")
    
    return total_files, files_needing_fix, files_fixed

def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(description='Feature Log Checker')
    parser.add_argument('--fix', action='store_true', help='Fix feature logs that don\'t match the template')
    parser.add_argument('--check-only', action='store_true', help='Only check files, don\'t print detailed results')
    parser.add_argument('--update-roadmap', action='store_true', help='Update roadmap with results')
    
    args = parser.parse_args()
    
    total_files, files_needing_fix, files_fixed = process_all_feature_logs(
        fix=args.fix,
        check_only=args.check_only,
        update_roadmap=args.update_roadmap
    )
    
    print(f"\nSummary:")
    print(f"  Total feature log files: {total_files}")
    print(f"  Files needing fix: {files_needing_fix}")
    
    if args.fix:
        print(f"  Files fixed: {files_fixed}")
        
        if files_fixed > 0 and files_fixed == files_needing_fix:
            print("\n✅ All feature log files have been fixed and now follow the template structure!")
        elif files_fixed > 0:
            print(f"\n⚠️ {files_fixed} of {files_needing_fix} files were fixed. Some files could not be fixed automatically.")
        else:
            print("\n❌ No files were fixed. See error messages above for details.")
    else:
        if files_needing_fix == 0:
            print("\n✅ All feature log files follow the template structure!")
        else:
            print(f"\n⚠️ {files_needing_fix} files need to be fixed. Run with --fix to fix them.")
    
    # Return appropriate exit code
    if files_needing_fix == 0 or (args.fix and files_fixed == files_needing_fix):
        return 0
    else:
        return 1

if __name__ == "__main__":
    sys.exit(main()) 