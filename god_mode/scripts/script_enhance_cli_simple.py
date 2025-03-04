#!/usr/bin/env python3

"""
Simple script to update god_mode_remote.sh with Git options.
"""

import os
import re
import sys
from pathlib import Path

# Get script directory and project root
SCRIPT_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = SCRIPT_DIR.parent.parent

# Remote script path
REMOTE_SCRIPT_PATH = PROJECT_ROOT / "god_mode_remote.sh"

def main():
    """Main function to enhance the God Mode CLI."""
    
    print("Enhancing God Mode CLI with Git integration...")
    
    # Check if the remote script exists
    if not os.path.exists(REMOTE_SCRIPT_PATH):
        print(f"Error: Remote script not found at {REMOTE_SCRIPT_PATH}")
        return 1
    
    # Read the remote script
    with open(REMOTE_SCRIPT_PATH, 'r') as f:
        content = f.read()
    
    # Add Git functions before the menu function
    git_functions = """
# Function to manually trigger an auto-commit
trigger_auto_commit() {
    echo -e "${BLUE}Triggering auto-commit...${NC}"
    
    # Check if auto-commit script exists
    local auto_commit_script="$GOD_MODE_DIR/scripts/script_auto_commit.sh"
    if [ ! -f "$auto_commit_script" ]; then
        echo -e "${RED}Error: Auto-commit script not found at $auto_commit_script${NC}"
        return 1
    fi
    
    # Run the auto-commit script
    "$auto_commit_script" "Manual commit via God Mode CLI"
    
    # Check result
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}Auto-commit completed successfully${NC}"
    else
        echo -e "${RED}Auto-commit failed${NC}"
    fi
}

# Function to set up GitHub repository
setup_github_repo() {
    echo -e "${BLUE}Setting up GitHub repository...${NC}"
    
    # Check if setup script exists
    local setup_script="$GOD_MODE_DIR/scripts/script_setup_github.sh"
    if [ ! -f "$setup_script" ]; then
        echo -e "${RED}Error: GitHub setup script not found at $setup_script${NC}"
        return 1
    fi
    
    # Run the setup script
    "$setup_script"
}
"""
    
    # Find the position to insert the Git functions
    pattern = r'# Function to display the menu\nshow_menu\(\) \{'
    match = re.search(pattern, content)
    
    if not match:
        print("Could not find menu function")
        return 1
    
    # Insert the Git functions before the menu function
    insert_position = match.start()
    content = content[:insert_position] + git_functions + content[insert_position:]
    
    # Update the menu options - find the line with "help" option
    menu_pattern = r'(        h\|H\) show_help ;;)'
    menu_match = re.search(menu_pattern, content)
    
    if not menu_match:
        print("Could not find help option in menu")
        return 1
    
    # Add new menu options before the help option
    new_options = """        g|G) setup_github_repo ;;
        a|A) trigger_auto_commit ;;"""
    
    # Replace the help line with new options + help line
    content = content.replace(
        menu_match.group(1),
        new_options + "\n" + menu_match.group(1)
    )
    
    # Update the menu display to include the new options
    menu_display_pattern = r'(    echo -e "d\) \${CYAN}View documentation\${NC} - Read guides on using God Mode and tags")'
    menu_display_match = re.search(menu_display_pattern, content)
    
    if not menu_display_match:
        print("Could not find documentation option in menu display")
        return 1
    
    # Add new menu display options before the documentation option
    new_display_options = """    echo
    echo -e "${YELLOW}VERSION CONTROL:${NC}"
    echo -e "g) ${CYAN}Setup GitHub repository${NC} - Create and connect to a GitHub repository"
    echo -e "a) ${CYAN}Auto-commit changes${NC} - Manually trigger an auto-commit"""
    
    # Replace the documentation line with new display options + documentation line
    content = content.replace(
        menu_display_match.group(1),
        new_display_options + "\n" + menu_display_match.group(1)
    )
    
    # Write the updated content back to the remote script
    with open(REMOTE_SCRIPT_PATH, 'w') as f:
        f.write(content)
    
    print("God Mode CLI has been enhanced with Git integration!")
    return 0

if __name__ == "__main__":
    sys.exit(main()) 