#!/usr/bin/env python3
"""
Enhanced CLI Menu Generator for God Mode

This script creates an enhanced version of the god_mode_remote.sh script with:
1. Better organization with categories and submenus
2. Session continuity options
3. Roadmap generation options
4. System verification integration
5. Auto-commit integration
6. Troubleshooting helpers
"""

import os
import sys
from pathlib import Path
import shutil
import datetime
import re

# Get the directory of this script
SCRIPT_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
GOD_MODE_DIR = SCRIPT_DIR.parent
PROJECT_ROOT = GOD_MODE_DIR.parent

# Source and destination files
SOURCE_REMOTE = PROJECT_ROOT / "god_mode_remote.sh"
ENHANCED_REMOTE = PROJECT_ROOT / "god_mode_remote_enhanced.sh"

# Check if source exists
if not SOURCE_REMOTE.exists():
    print(f"Error: Source file {SOURCE_REMOTE} not found")
    sys.exit(1)

def read_file(file_path):
    """Read a file and return its contents"""
    with open(file_path, 'r') as f:
        return f.read()

def write_file(file_path, content):
    """Write content to a file"""
    with open(file_path, 'w') as f:
        f.write(content)

def backup_file(file_path):
    """Create a backup of a file"""
    backup_path = file_path.with_suffix(f"{file_path.suffix}.bak")
    shutil.copy2(file_path, backup_path)
    print(f"Created backup at {backup_path}")

def generate_enhanced_menu():
    """Generate the enhanced menu content"""
    menu = """
# =====================================
# ======= GOD MODE REMOTE MENU =======
# =====================================

# Main menu function
show_main_menu() {
    clear
    print_header

    echo -e "${BLUE}=======================================${NC}"
    echo -e "${BLUE}       GOD MODE CONTROL CENTER        ${NC}"
    echo -e "${BLUE}=======================================${NC}"
    echo
    
    # System Status Section
    echo -e "${CYAN}=== SYSTEM STATUS ===${NC}"
    echo -e "  ${GREEN}1)${NC} Start God Mode - Turn on AI assistant superpowers"
    echo -e "  ${RED}2)${NC} Stop God Mode - Turn off AI assistant background processes"
    echo -e "  ${BLUE}3)${NC} System Status - Check if everything is working correctly"
    echo -e "  ${BLUE}4)${NC} Run System Verification - Test all components"
    echo
    
    # Memory & Documentation Section
    echo -e "${CYAN}=== MEMORY & DOCUMENTATION ===${NC}"
    echo -e "  ${YELLOW}5)${NC} Memory Management Menu - Session continuity, logs, and memory files"
    echo -e "  ${YELLOW}6)${NC} Project Management Menu - Roadmaps, documentation, and project structure"
    echo -e "  ${YELLOW}7)${NC} Route clipboard content - Process text with message router"
    echo
    
    # Configuration & Tools Section
    echo -e "${CYAN}=== CONFIGURATION & TOOLS ===${NC}"
    echo -e "  ${BLUE}8)${NC} Git Operations Menu - Auto-commit, repository management"
    echo -e "  ${BLUE}9)${NC} Development Tools Menu - Dependency installation, cursor rules"
    echo -e "  ${BLUE}0)${NC} Navigation Menu - Terminal access, directory switching"
    echo
    
    # Help & Exit Section
    echo -e "${CYAN}=== HELP & EXIT ===${NC}"
    echo -e "  ${GREEN}h)${NC} Help - Get detailed information about commands"
    echo -e "  ${RED}q)${NC} Quit - Exit this menu"
    echo
    echo -e "Enter your choice: "
    read -n 1 -r choice
    echo
    
    case $choice in
        1) start_god_mode ;;
        2) stop_god_mode ;;
        3) check_god_mode_status ;;
        4) run_system_verification ;;
        5) show_memory_menu ;;
        6) show_project_menu ;;
        7) process_clipboard ;;
        8) show_git_menu ;;
        9) show_development_menu ;;
        0) show_navigation_menu ;;
        h|H) show_help ;;
        q|Q) echo "Exiting..."; exit 0 ;;
        *) echo -e "${RED}Invalid option. Press Enter to continue.${NC}"; read -r; show_main_menu ;;
    esac
}

# Memory Management Submenu
show_memory_menu() {
    clear
    print_header
    
    echo -e "${BLUE}=======================================${NC}"
    echo -e "${BLUE}       MEMORY MANAGEMENT MENU         ${NC}"
    echo -e "${BLUE}=======================================${NC}"
    echo
    
    echo -e "${CYAN}=== SESSION CONTINUITY ===${NC}"
    echo -e "  ${GREEN}1)${NC} Generate Session Summary - Save current context"
    echo -e "  ${GREEN}2)${NC} Create Restart Prompt - For starting a new session"
    echo -e "  ${GREEN}3)${NC} Copy Latest Continuity Summary to Clipboard"
    echo
    
    echo -e "${CYAN}=== LOGS & MEMORY ===${NC}"
    echo -e "  ${YELLOW}4)${NC} View Recent Logs - Check recent activities"
    echo -e "  ${YELLOW}5)${NC} View Routing History - See where content was routed"
    echo -e "  ${YELLOW}6)${NC} Audit Memory Files - Check for empty log entries"
    echo -e "  ${YELLOW}7)${NC} View Project Memory - See the main MEMORY_CURSOR file"
    echo
    
    echo -e "${CYAN}=== NAVIGATION ===${NC}"
    echo -e "  ${BLUE}b)${NC} Back to Main Menu"
    echo -e "  ${RED}q)${NC} Quit"
    echo
    echo -e "Enter your choice: "
    read -n 1 -r choice
    echo
    
    case $choice in
        1) generate_session_summary ;;
        2) create_restart_prompt ;;
        3) copy_continuity_summary ;;
        4) view_recent_logs ;;
        5) view_routing_history ;;
        6) audit_memory_files ;;
        7) view_project_memory ;;
        b|B) show_main_menu ;;
        q|Q) echo "Exiting..."; exit 0 ;;
        *) echo -e "${RED}Invalid option. Press Enter to continue.${NC}"; read -r; show_memory_menu ;;
    esac
}

# Project Management Submenu
show_project_menu() {
    clear
    print_header
    
    echo -e "${BLUE}=======================================${NC}"
    echo -e "${BLUE}      PROJECT MANAGEMENT MENU         ${NC}"
    echo -e "${BLUE}=======================================${NC}"
    echo
    
    echo -e "${CYAN}=== ROADMAPS & PLANNING ===${NC}"
    echo -e "  ${GREEN}1)${NC} Generate New Roadmap - Create a project roadmap"
    echo -e "  ${GREEN}2)${NC} View Latest Roadmap - See the most recent roadmap"
    echo -e "  ${GREEN}3)${NC} Update Project Structure - Refresh file/folder documentation"
    echo
    
    echo -e "${CYAN}=== DOCUMENTATION ===${NC}"
    echo -e "  ${YELLOW}4)${NC} View README - See project documentation"
    echo -e "  ${YELLOW}5)${NC} View Tag System Documentation - Learn about message tags"
    echo -e "  ${YELLOW}6)${NC} Update Function & Type Documentation"
    echo
    
    echo -e "${CYAN}=== NAVIGATION ===${NC}"
    echo -e "  ${BLUE}b)${NC} Back to Main Menu"
    echo -e "  ${RED}q)${NC} Quit"
    echo
    echo -e "Enter your choice: "
    read -n 1 -r choice
    echo
    
    case $choice in
        1) generate_roadmap ;;
        2) view_latest_roadmap ;;
        3) update_project_structure ;;
        4) view_readme ;;
        5) view_tag_documentation ;;
        6) update_function_types ;;
        b|B) show_main_menu ;;
        q|Q) echo "Exiting..."; exit 0 ;;
        *) echo -e "${RED}Invalid option. Press Enter to continue.${NC}"; read -r; show_project_menu ;;
    esac
}

# Git Operations Submenu
show_git_menu() {
    clear
    print_header
    
    echo -e "${BLUE}=======================================${NC}"
    echo -e "${BLUE}          GIT OPERATIONS MENU         ${NC}"
    echo -e "${BLUE}=======================================${NC}"
    echo
    
    echo -e "${CYAN}=== COMMIT OPERATIONS ===${NC}"
    echo -e "  ${GREEN}1)${NC} Auto-Commit Changes - Commit all changes with auto-message"
    echo -e "  ${GREEN}2)${NC} Commit with Custom Message - Specify your own message"
    echo -e "  ${GREEN}3)${NC} View Git Status - See current repository status"
    echo
    
    echo -e "${CYAN}=== REPOSITORY MANAGEMENT ===${NC}"
    echo -e "  ${YELLOW}4)${NC} Configure Remote Repository - Set up GitHub remote"
    echo -e "  ${YELLOW}5)${NC} Push to Remote - Push commits to GitHub"
    echo -e "  ${YELLOW}6)${NC} View Commit History - See recent commits"
    echo
    
    echo -e "${CYAN}=== NAVIGATION ===${NC}"
    echo -e "  ${BLUE}b)${NC} Back to Main Menu"
    echo -e "  ${RED}q)${NC} Quit"
    echo
    echo -e "Enter your choice: "
    read -n 1 -r choice
    echo
    
    case $choice in
        1) run_auto_commit ;;
        2) run_custom_commit ;;
        3) view_git_status ;;
        4) configure_remote ;;
        5) push_to_remote ;;
        6) view_commit_history ;;
        b|B) show_main_menu ;;
        q|Q) echo "Exiting..."; exit 0 ;;
        *) echo -e "${RED}Invalid option. Press Enter to continue.${NC}"; read -r; show_git_menu ;;
    esac
}

# Development Tools Submenu
show_development_menu() {
    clear
    print_header
    
    echo -e "${BLUE}=======================================${NC}"
    echo -e "${BLUE}      DEVELOPMENT TOOLS MENU          ${NC}"
    echo -e "${BLUE}=======================================${NC}"
    echo
    
    echo -e "${CYAN}=== DEPENDENCIES & CONFIGURATION ===${NC}"
    echo -e "  ${GREEN}1)${NC} Install Dependencies - Set up required packages"
    echo -e "  ${GREEN}2)${NC} Update Cursor Rules - Refresh AI assistant rules"
    echo -e "  ${GREEN}3)${NC} Run Diagnostics - Check for system issues"
    echo
    
    echo -e "${CYAN}=== TROUBLESHOOTING ===${NC}"
    echo -e "  ${YELLOW}4)${NC} Fix Feature Logs - Validate and repair feature logs"
    echo -e "  ${YELLOW}5)${NC} Check Memory Files - Verify memory file integrity"
    echo -e "  ${YELLOW}6)${NC} View Log Files - See debug logs"
    echo
    
    echo -e "${CYAN}=== NAVIGATION ===${NC}"
    echo -e "  ${BLUE}b)${NC} Back to Main Menu"
    echo -e "  ${RED}q)${NC} Quit"
    echo
    echo -e "Enter your choice: "
    read -n 1 -r choice
    echo
    
    case $choice in
        1) install_dependencies ;;
        2) update_cursor_rules ;;
        3) run_diagnostics ;;
        4) fix_feature_logs ;;
        5) check_memory_files ;;
        6) view_log_files ;;
        b|B) show_main_menu ;;
        q|Q) echo "Exiting..."; exit 0 ;;
        *) echo -e "${RED}Invalid option. Press Enter to continue.${NC}"; read -r; show_development_menu ;;
    esac
}

# Navigation Menu
show_navigation_menu() {
    clear
    print_header
    
    echo -e "${BLUE}=======================================${NC}"
    echo -e "${BLUE}           NAVIGATION MENU            ${NC}"
    echo -e "${BLUE}=======================================${NC}"
    echo
    
    echo -e "${CYAN}=== DIRECTORY NAVIGATION ===${NC}"
    echo -e "  ${GREEN}1)${NC} Navigate to Target Directory - Open a new terminal there"
    echo -e "  ${GREEN}2)${NC} Open in Cursor IDE - Launch project in Cursor"
    echo -e "  ${GREEN}3)${NC} Choose a Different Target Directory"
    echo
    
    echo -e "${CYAN}=== FILE OPERATIONS ===${NC}"
    echo -e "  ${YELLOW}4)${NC} List Directory Contents - See files and folders"
    echo -e "  ${YELLOW}5)${NC} Find a File - Search for files by name"
    echo
    
    echo -e "${CYAN}=== NAVIGATION ===${NC}"
    echo -e "  ${BLUE}b)${NC} Back to Main Menu"
    echo -e "  ${RED}q)${NC} Quit"
    echo
    echo -e "Enter your choice: "
    read -n 1 -r choice
    echo
    
    case $choice in
        1) navigate_to_target ;;
        2) open_cursor_ide ;;
        3) choose_different_target ;;
        4) list_directory_contents ;;
        5) find_file ;;
        b|B) show_main_menu ;;
        q|Q) echo "Exiting..."; exit 0 ;;
        *) echo -e "${RED}Invalid option. Press Enter to continue.${NC}"; read -r; show_navigation_menu ;;
    esac
}

# Session Continuity Functions
generate_session_summary() {
    echo -e "${BLUE}Generating session continuity summary...${NC}"
    cd "$FULL_TARGET_PATH" || return
    if python god_mode/scripts/script_session_continuity.py; then
        echo -e "${GREEN}Session summary generated successfully!${NC}"
        echo -e "${YELLOW}To start a new session with this context, choose option 2 from the Memory Menu.${NC}"
    else
        echo -e "${RED}Failed to generate session summary.${NC}"
    fi
    echo -e "${BLUE}Press Enter to continue...${NC}"
    read -r
    show_memory_menu
}

create_restart_prompt() {
    echo -e "${BLUE}Creating restart prompt for a new session...${NC}"
    cd "$FULL_TARGET_PATH" || return
    if python god_mode/scripts/script_session_continuity.py --output "$FULL_TARGET_PATH/god_mode/memory/continuity/restart_prompt.txt"; then
        echo -e "${GREEN}Restart prompt created successfully at:${NC}"
        echo -e "${YELLOW}$FULL_TARGET_PATH/god_mode/memory/continuity/restart_prompt.txt${NC}"
        echo
        echo -e "${BLUE}Would you like to copy this prompt to your clipboard? (y/n)${NC}"
        read -n 1 -r copy_choice
        echo
        if [[ $copy_choice =~ ^[Yy]$ ]]; then
            if command -v pbcopy > /dev/null; then
                # macOS
                cat "$FULL_TARGET_PATH/god_mode/memory/continuity/restart_prompt.txt" | pbcopy
                echo -e "${GREEN}Copied to clipboard! Paste this into your new chat session.${NC}"
            elif command -v xclip > /dev/null; then
                # Linux with xclip
                cat "$FULL_TARGET_PATH/god_mode/memory/continuity/restart_prompt.txt" | xclip -selection clipboard
                echo -e "${GREEN}Copied to clipboard! Paste this into your new chat session.${NC}"
            elif command -v clip > /dev/null; then
                # Windows
                cat "$FULL_TARGET_PATH/god_mode/memory/continuity/restart_prompt.txt" | clip
                echo -e "${GREEN}Copied to clipboard! Paste this into your new chat session.${NC}"
            else
                echo -e "${RED}Could not copy to clipboard. No suitable clipboard command found.${NC}"
                echo -e "${YELLOW}Please manually copy the contents of the file.${NC}"
            fi
        fi
    else
        echo -e "${RED}Failed to create restart prompt.${NC}"
    fi
    echo -e "${BLUE}Press Enter to continue...${NC}"
    read -r
    show_memory_menu
}

copy_continuity_summary() {
    echo -e "${BLUE}Copying latest continuity summary to clipboard...${NC}"
    cd "$FULL_TARGET_PATH" || return
    local summary_file="$FULL_TARGET_PATH/god_mode/memory/continuity/latest_continuity_summary.md"
    
    if [ ! -f "$summary_file" ]; then
        echo -e "${RED}No continuity summary found. Generate one first.${NC}"
    else
        if command -v pbcopy > /dev/null; then
            # macOS
            cat "$summary_file" | pbcopy
            echo -e "${GREEN}Copied to clipboard! Paste this into your new chat session.${NC}"
        elif command -v xclip > /dev/null; then
            # Linux with xclip
            cat "$summary_file" | xclip -selection clipboard
            echo -e "${GREEN}Copied to clipboard! Paste this into your new chat session.${NC}"
        elif command -v clip > /dev/null; then
            # Windows
            cat "$summary_file" | clip
            echo -e "${GREEN}Copied to clipboard! Paste this into your new chat session.${NC}"
        else
            echo -e "${RED}Could not copy to clipboard. No suitable clipboard command found.${NC}"
            echo -e "${YELLOW}Please manually copy the contents of the file:${NC}"
            echo -e "${BLUE}$summary_file${NC}"
        fi
    fi
    echo -e "${BLUE}Press Enter to continue...${NC}"
    read -r
    show_memory_menu
}

# Roadmap Functions
generate_roadmap() {
    echo -e "${BLUE}Generating a new roadmap...${NC}"
    echo -e "${YELLOW}Enter a title for the roadmap (e.g., 'Sprint Planning', 'Feature Roadmap'):${NC}"
    read -r roadmap_title
    
    if [ -z "$roadmap_title" ]; then
        roadmap_title="God Mode Roadmap $(date +%Y%m%d_%H%M%S)"
    fi
    
    cd "$FULL_TARGET_PATH" || return
    if python god_mode/scripts/script_generate_roadmap.py --title "$roadmap_title"; then
        echo -e "${GREEN}Roadmap generated successfully!${NC}"
    else
        echo -e "${RED}Failed to generate roadmap.${NC}"
    fi
    echo -e "${BLUE}Press Enter to continue...${NC}"
    read -r
    show_project_menu
}

view_latest_roadmap() {
    echo -e "${BLUE}Finding the latest roadmap...${NC}"
    cd "$FULL_TARGET_PATH" || return
    
    local roadmap_dir="$FULL_TARGET_PATH/god_mode/roadmap"
    local latest_roadmap=$(find "$roadmap_dir" -name "roadmap_*.md" -type f -printf "%T@ %p\n" 2>/dev/null | sort -nr | head -1 | cut -d' ' -f2-)
    
    if [ -z "$latest_roadmap" ]; then
        echo -e "${RED}No roadmap files found.${NC}"
    else
        echo -e "${GREEN}Latest roadmap: ${YELLOW}$(basename "$latest_roadmap")${NC}"
        echo
        echo -e "${BLUE}Contents:${NC}"
        echo
        cat "$latest_roadmap" | less
    fi
    echo -e "${BLUE}Press Enter to continue...${NC}"
    read -r
    show_project_menu
}

# Git Functions
run_auto_commit() {
    echo -e "${BLUE}Running auto-commit...${NC}"
    cd "$FULL_TARGET_PATH" || return
    if ./god_mode/scripts/script_auto_commit.sh; then
        echo -e "${GREEN}Auto-commit completed successfully!${NC}"
    else
        echo -e "${RED}Auto-commit failed. See error message above.${NC}"
    fi
    echo -e "${BLUE}Press Enter to continue...${NC}"
    read -r
    show_git_menu
}

run_custom_commit() {
    echo -e "${BLUE}Running commit with custom message...${NC}"
    echo -e "${YELLOW}Enter your commit message:${NC}"
    read -r commit_message
    
    if [ -z "$commit_message" ]; then
        echo -e "${RED}Commit message cannot be empty.${NC}"
    else
        cd "$FULL_TARGET_PATH" || return
        if ./god_mode/scripts/script_auto_commit.sh "$commit_message"; then
            echo -e "${GREEN}Commit completed successfully!${NC}"
        else
            echo -e "${RED}Commit failed. See error message above.${NC}"
        fi
    fi
    echo -e "${BLUE}Press Enter to continue...${NC}"
    read -r
    show_git_menu
}

view_git_status() {
    echo -e "${BLUE}Viewing Git status...${NC}"
    cd "$FULL_TARGET_PATH" || return
    git status
    echo -e "${BLUE}Press Enter to continue...${NC}"
    read -r
    show_git_menu
}

configure_remote() {
    echo -e "${BLUE}Configuring Git remote repository...${NC}"
    echo -e "${YELLOW}Enter the URL of your GitHub repository:${NC}"
    read -r repo_url
    
    if [ -z "$repo_url" ]; then
        echo -e "${RED}Repository URL cannot be empty.${NC}"
    else
        cd "$FULL_TARGET_PATH" || return
        echo -e "${BLUE}Checking existing remotes...${NC}"
        if git remote | grep -q "origin"; then
            echo -e "${YELLOW}Remote 'origin' already exists. Do you want to update it? (y/n)${NC}"
            read -n 1 -r update_choice
            echo
            if [[ $update_choice =~ ^[Yy]$ ]]; then
                git remote set-url origin "$repo_url"
                echo -e "${GREEN}Updated remote 'origin' to $repo_url${NC}"
            else
                echo -e "${YELLOW}Remote configuration unchanged.${NC}"
            fi
        else
            git remote add origin "$repo_url"
            echo -e "${GREEN}Added remote 'origin' as $repo_url${NC}"
        fi
    fi
    echo -e "${BLUE}Press Enter to continue...${NC}"
    read -r
    show_git_menu
}

push_to_remote() {
    echo -e "${BLUE}Pushing to remote repository...${NC}"
    cd "$FULL_TARGET_PATH" || return
    
    if ! git remote | grep -q "origin"; then
        echo -e "${RED}No remote repository configured. Configure one first.${NC}"
    else
        echo -e "${BLUE}Pushing to origin/main...${NC}"
        if git push -u origin main; then
            echo -e "${GREEN}Push completed successfully!${NC}"
        else
            echo -e "${RED}Push failed. See error message above.${NC}"
        fi
    fi
    echo -e "${BLUE}Press Enter to continue...${NC}"
    read -r
    show_git_menu
}

view_commit_history() {
    echo -e "${BLUE}Viewing commit history...${NC}"
    cd "$FULL_TARGET_PATH" || return
    git log --oneline --graph --decorate -n 10
    echo -e "${BLUE}Press Enter to continue...${NC}"
    read -r
    show_git_menu
}

# System Verification Function
run_system_verification() {
    echo -e "${BLUE}Running God Mode system verification...${NC}"
    cd "$FULL_TARGET_PATH" || return
    if python god_mode/scripts/script_test_god_mode.py; then
        echo -e "${GREEN}System verification completed!${NC}"
    else
        echo -e "${RED}System verification completed with issues. Review the output above.${NC}"
    fi
    echo -e "${BLUE}Press Enter to continue...${NC}"
    read -r
    show_main_menu
}

# Troubleshooting Functions
audit_memory_files() {
    echo -e "${BLUE}Auditing memory files for empty content...${NC}"
    cd "$FULL_TARGET_PATH" || return
    if python god_mode/scripts/script_enhance_message_content.py --audit; then
        echo -e "${GREEN}Memory file audit completed!${NC}"
    else
        echo -e "${RED}Memory file audit failed. See error message above.${NC}"
    fi
    echo -e "${BLUE}Press Enter to continue...${NC}"
    read -r
    show_memory_menu
}

fix_feature_logs() {
    echo -e "${BLUE}Validating and fixing feature logs...${NC}"
    cd "$FULL_TARGET_PATH" || return
    if python god_mode/scripts/script_check_feature_logs.py --fix; then
        echo -e "${GREEN}Feature log validation and fixing completed!${NC}"
    else
        echo -e "${RED}Feature log validation failed. See error message above.${NC}"
    fi
    echo -e "${BLUE}Press Enter to continue...${NC}"
    read -r
    show_development_menu
}

# Add the main menu trigger to the end of the remote script
entry_point() {
    show_main_menu
}

def add_git_functions():
    """Add Git-related functions to the remote script."""
    
    # Git functions to add
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
    
    # Read the remote script
    with open(REMOTE_SCRIPT_PATH, 'r') as f:
        content = f.read()
    
    # Find the position to insert the Git functions
    # Let's insert them before the show_menu function
    pattern = r'# Function to display the menu\nshow_menu\(\) \{'
    match = re.search(pattern, content)
    
    if not match:
        print("Could not find location to insert Git functions")
        return False
    
    # Insert the Git functions before the show_menu function
    insert_position = match.start()
    new_content = content[:insert_position] + git_functions + content[insert_position:]
    
    # Write the updated content back
    with open(REMOTE_SCRIPT_PATH, 'w') as f:
        f.write(new_content)
    
    return True

def update_menu_display():
    """Update the menu display to include Git options and categories."""
    
    # New organized menu with Git options
    new_menu = """show_menu() {
    # Display current status in header
    check_god_mode_status_header
    echo

    echo -e "${BLUE}======== GOD MODE COMMAND CENTER ========${NC}"
    echo
    echo -e "${YELLOW}SYSTEM MANAGEMENT:${NC}"
    echo -e "1) ${CYAN}Start God Mode${NC} - Turn on AI assistant superpowers"
    echo -e "2) ${CYAN}Stop God Mode${NC} - Turn off AI assistant background processes"
    echo -e "3) ${CYAN}View God Mode status${NC} - Check if everything is working correctly"
    echo -e "8) ${CYAN}Install dependencies${NC} - Install required Python packages for God Mode"
    echo
    echo -e "${YELLOW}CONTENT & MEMORY:${NC}"
    echo -e "4) ${CYAN}Route clipboard content${NC} - Process text with [TAG] markers from clipboard"
    echo -e "5) ${CYAN}View recent logs${NC} - See the latest activity and changes"
    echo -e "6) ${CYAN}Update project structure${NC} - Refresh AI's understanding of your code"
    echo -e "7) ${CYAN}Update Cursor rules${NC} - Refresh the AI assistant's instructions"
    echo -e "r) ${CYAN}View routing activity${NC} - See what content went where with clickable links"
    echo -e "c) ${CYAN}Session continuity${NC} - Generate continuity for new chat sessions"
    echo
    echo -e "${YELLOW}VERSION CONTROL:${NC}"
    echo -e "g) ${CYAN}Setup GitHub repository${NC} - Create and connect to a GitHub repository"
    echo -e "a) ${CYAN}Auto-commit changes${NC} - Manually trigger an auto-commit"
    echo
    echo -e "${YELLOW}NAVIGATION & HELP:${NC}"
    echo -e "9) ${CYAN}Navigate to target directory${NC} - Open a terminal in project folder"
    echo -e "d) ${CYAN}View documentation${NC} - Read guides on using God Mode and tags"
    echo -e "v) ${CYAN}Verify system${NC} - Run tests to ensure everything is working"
    echo -e "h) ${CYAN}Help${NC} - Detailed explanation of all options"
    echo -e "q) ${CYAN}Quit${NC} - Exit this menu"
    echo
    echo -n "Enter your choice: "
}"""
    
    # Read the remote script
    with open(REMOTE_SCRIPT_PATH, 'r') as f:
        content = f.read()
    
    # Find the old menu function
    pattern = r'show_menu\(\) \{.*?\n\}'
    match = re.search(pattern, content, re.DOTALL)
    
    if not match:
        print("Could not find menu function")
        return False
    
    # Replace the old menu with the new one
    new_content = content[:match.start()] + new_menu + content[match.end():]
    
    # Write the updated content back
    with open(REMOTE_SCRIPT_PATH, 'w') as f:
        f.write(new_content)
    
    return True

def update_case_statement():
    """Update the case statement to handle the new menu options."""
    
    # New case entries for Git options
    new_case_entries = """        g|G) setup_github_repo ;;
        a|A) trigger_auto_commit ;;
        c|C) generate_session_continuity ;;
        v|V) verify_system ;;"""
    
    # Read the remote script
    with open(REMOTE_SCRIPT_PATH, 'r') as f:
        content = f.read()
    
    # Find the case statement
    pattern = r'case "\$choice" in.*?esac'
    match = re.search(pattern, content, re.DOTALL)
    
    if not match:
        print("Could not find case statement")
        return False
    
    # Find the position to insert the new case entries
    # We'll insert them before the h|H entry
    help_entry_pattern = r'h\|H\) show_help ;;'
    help_match = re.search(help_entry_pattern, content)
    
    if not help_match:
        print("Could not find help entry in case statement")
        return False
    
    # Insert the new case entries before the help entry
    case_content = content[match.start():match.end()]
    new_case_content = case_content.replace(
        help_match.group(0),
        new_case_entries + "\n        " + help_match.group(0)
    )
    
    # Replace the old case statement with the new one
    new_content = content[:match.start()] + new_case_content + content[match.end():]
    
    # Write the updated content back
    with open(REMOTE_SCRIPT_PATH, 'w') as f:
        f.write(new_content)
    
    return True

def add_system_verification_function():
    """Add the system verification function."""
    
    # System verification function to add
    verification_function = """
# Function to verify all God Mode components
verify_system() {
    echo -e "${BLUE}Verifying God Mode System Components...${NC}"
    
    # Check if verification script exists
    local verify_script="$GOD_MODE_DIR/scripts/script_verify_system.sh"
    if [ ! -f "$verify_script" ]; then
        echo -e "${YELLOW}Creating verification script...${NC}"
        # Create the verification script if it doesn't exist
        cat > "$verify_script" << 'EOF'
#!/bin/bash

# System Verification Script for God Mode
# This script tests all components of the God Mode system to ensure they're working properly

# Set colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get the script directory and project root
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
GOD_MODE_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

# Change to the project root directory
cd "$PROJECT_ROOT" || { echo -e "${RED}Error: Could not navigate to project root directory${NC}"; exit 1; }

# Function to print test result
print_result() {
    local test_name="$1"
    local status="$2"
    local padding=$(printf '%*s' $((40 - ${#test_name})) "")
    
    case "$status" in
        "PASS") echo -e "$test_name $padding [ ${GREEN}PASS${NC} ]" ;;
        "FAIL") echo -e "$test_name $padding [ ${RED}FAIL${NC} ]" ;;
        "WARN") echo -e "$test_name $padding [ ${YELLOW}WARN${NC} ]" ;;
        *) echo -e "$test_name $padding [ ${YELLOW}UNKNOWN${NC} ]" ;;
    esac
}

# Function to test file existence
test_file_exists() {
    local file_path="$1"
    local file_name="$2"
    
    if [ -f "$file_path" ]; then
        print_result "$file_name" "PASS"
        return 0
    else
        print_result "$file_name" "FAIL"
        echo -e "  ${RED}File not found: $file_path${NC}"
        return 1
    fi
}

# Function to test script execution
test_script_execution() {
    local script_path="$1"
    local script_name="$2"
    local test_args="$3"
    
    if [ ! -f "$script_path" ]; then
        print_result "$script_name" "FAIL"
        echo -e "  ${RED}Script not found: $script_path${NC}"
        return 1
    fi
    
    if [ ! -x "$script_path" ]; then
        chmod +x "$script_path"
        echo -e "  ${YELLOW}Made script executable: $script_path${NC}"
    fi
    
    # Execute the script with test arguments
    "$script_path" $test_args &> /dev/null
    local exit_code=$?
    
    if [ $exit_code -eq 0 ]; then
        print_result "$script_name" "PASS"
        return 0
    else
        print_result "$script_name" "FAIL"
        echo -e "  ${RED}Script failed with exit code: $exit_code${NC}"
        return 1
    fi
}

# Function to test the message router
test_message_router() {
    local router_script="$GOD_MODE_DIR/scripts/route"
    local test_file="$SCRIPT_DIR/test_message.txt"
    
    # Create a test message file
    echo -e "[LOG_SUMMARY]\nTest message for router verification." > "$test_file"
    
    # Test the router script
    if [ ! -f "$router_script" ]; then
        print_result "Message Router" "FAIL"
        echo -e "  ${RED}Router script not found: $router_script${NC}"
        return 1
    fi
    
    if [ ! -x "$router_script" ]; then
        chmod +x "$router_script"
        echo -e "  ${YELLOW}Made router script executable: $router_script${NC}"
    fi
    
    # Execute the router with the test file
    "$router_script" --input "$test_file" &> /dev/null
    local exit_code=$?
    
    # Clean up the test file
    rm -f "$test_file"
    
    if [ $exit_code -eq 0 ]; then
        print_result "Message Router" "PASS"
        return 0
    else
        print_result "Message Router" "FAIL"
        echo -e "  ${RED}Router failed to process test message${NC}"
        return 1
    fi
}

# Function to check if a process is running
check_process_running() {
    local process_name="$1"
    local search_pattern="$2"
    
    if pgrep -f "$search_pattern" &> /dev/null; then
        print_result "$process_name Process" "PASS"
        return 0
    else
        print_result "$process_name Process" "FAIL"
        echo -e "  ${RED}Process not running: $process_name${NC}"
        return 1
    fi
}

# Function to test memory file integrity
test_memory_file() {
    local file_path="$1"
    local file_name="$2"
    
    if [ ! -f "$file_path" ]; then
        print_result "$file_name" "FAIL"
        echo -e "  ${RED}Memory file not found: $file_path${NC}"
        return 1
    fi
    
    # Check if the file has content
    if [ -s "$file_path" ]; then
        print_result "$file_name" "PASS"
        return 0
    else
        print_result "$file_name" "WARN"
        echo -e "  ${YELLOW}Memory file exists but is empty: $file_path${NC}"
        return 0
    fi
}

# Main testing sequence
echo -e "${BLUE}God Mode System Verification${NC}"
echo -e "${BLUE}==========================${NC}"
echo

echo -e "${YELLOW}Core Component Tests:${NC}"
test_file_exists "$GOD_MODE_DIR/scripts/script_auto_commit.sh" "Auto-Commit Script"
test_file_exists "$GOD_MODE_DIR/scripts/script_setup_github.sh" "GitHub Setup Script"
test_file_exists "$GOD_MODE_DIR/scripts/route" "Message Router Script"
test_file_exists "$GOD_MODE_DIR/scripts/script_session_continuity.py" "Session Continuity Script"
test_file_exists "$GOD_MODE_DIR/scripts/script_enhance_message_content.py" "Message Enhancer Script"

echo
echo -e "${YELLOW}Process Tests:${NC}"
check_process_running "Message Router" "script_message_router.py"
check_process_running "Cursor Watch" "script_cursor_watch.py"

echo
echo -e "${YELLOW}Functionality Tests:${NC}"
test_message_router
test_script_execution "$GOD_MODE_DIR/scripts/script_update_project_structure.py" "Project Structure Update" "--quiet"
test_script_execution "$GOD_MODE_DIR/scripts/script_check_feature_logs.py" "Feature Log Validator" "--check-only"
test_script_execution "$GOD_MODE_DIR/scripts/script_auto_commit.sh" "Auto-Commit" "--dry-run"

echo
echo -e "${YELLOW}Memory File Tests:${NC}"
test_memory_file "$GOD_MODE_DIR/memory/memory_logs_all.md" "Summary Logs"
test_memory_file "$GOD_MODE_DIR/memory/memory_logs_detailed.md" "Detailed Logs"
test_memory_file "$GOD_MODE_DIR/memory/MEMORY_CURSOR.md" "Memory Cursor"
test_memory_file "$GOD_MODE_DIR/memory/memory_project_structure.md" "Project Structure"

echo
echo -e "${BLUE}System Verification Complete${NC}"
EOF
        chmod +x "$verify_script"
    fi
    
    # Run the verification script
    "$verify_script"
}

# Function to generate session continuity
generate_session_continuity() {
    echo -e "${BLUE}Generating session continuity summary...${NC}"
    
    # Check if session continuity script exists
    local continuity_script="$GOD_MODE_DIR/scripts/script_session_continuity.py"
    if [ ! -f "$continuity_script" ]; then
        echo -e "${RED}Error: Session continuity script not found at $continuity_script${NC}"
        return 1
    fi
    
    # Run the session continuity script
    python "$continuity_script"
    
    # Check result
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}Session continuity summary generated${NC}"
        
        # Copy restart prompt to clipboard
        local restart_file="$GOD_MODE_DIR/.cache/restart_prompt.txt"
        if [ -f "$restart_file" ]; then
            if command -v pbcopy &> /dev/null; then
                # macOS
                cat "$restart_file" | pbcopy
                echo -e "${GREEN}Restart prompt copied to clipboard!${NC}"
            elif command -v xclip &> /dev/null; then
                # Linux with xclip
                cat "$restart_file" | xclip -selection clipboard
                echo -e "${GREEN}Restart prompt copied to clipboard!${NC}"
            elif command -v clip.exe &> /dev/null; then
                # Windows
                cat "$restart_file" | clip.exe
                echo -e "${GREEN}Restart prompt copied to clipboard!${NC}"
            else
                echo -e "${YELLOW}Could not copy to clipboard. Restart prompt is at: $restart_file${NC}"
            fi
            
            echo -e "${BLUE}To start a new session with context:${NC}"
            echo -e "1. ${YELLOW}Open a new chat window in Cursor${NC}"
            echo -e "2. ${YELLOW}Paste the copied prompt or the content from: $restart_file${NC}"
        else
            echo -e "${YELLOW}Restart prompt file not found${NC}"
        fi
    else
        echo -e "${RED}Failed to generate session continuity${NC}"
    fi
}
"""
    
    # Read the remote script
    with open(REMOTE_SCRIPT_PATH, 'r') as f:
        content = f.read()
    
    # Find the position to insert the functions
    # We'll insert them before the show_menu function
    pattern = r'# Function to display the menu\nshow_menu\(\) \{'
    match = re.search(pattern, content)
    
    if not match:
        print("Could not find location to insert functions")
        return False
    
    # Insert the functions before the show_menu function
    insert_position = match.start()
    new_content = content[:insert_position] + verification_function + content[insert_position:]
    
    # Write the updated content back
    with open(REMOTE_SCRIPT_PATH, 'w') as f:
        f.write(new_content)
    
    return True

def main():
    """Main function to enhance the God Mode CLI."""
    
    print("Enhancing God Mode CLI with Git integration...")
    
    # Check if the remote script exists
    if not os.path.exists(REMOTE_SCRIPT_PATH):
        print(f"Error: Remote script not found at {REMOTE_SCRIPT_PATH}")
        return 1
    
    # Add Git functions
    if not add_git_functions():
        print("Failed to add Git functions")
        return 1
    
    # Add system verification function
    if not add_system_verification_function():
        print("Failed to add system verification function")
        return 1
    
    # Update menu display
    if not update_menu_display():
        print("Failed to update menu display")
        return 1
    
    # Update case statement
    if not update_case_statement():
        print("Failed to update case statement")
        return 1
    
    print("God Mode CLI has been enhanced with Git integration")
    return 0

if __name__ == "__main__":
    sys.exit(main()) 