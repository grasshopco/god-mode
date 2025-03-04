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
"""

    return menu

def modify_remote_script():
    """Modify the remote script with the enhanced menu"""
    # Read the source file
    source_content = read_file(SOURCE_REMOTE)
    
    # Create a backup of the source file
    backup_file(SOURCE_REMOTE)
    
    # Split the content at the main execution point
    parts = source_content.split("# Main execution", 1)
    if len(parts) != 2:
        print("Error: Could not find the main execution section in the source file")
        sys.exit(1)
    
    header = parts[0]
    
    # Get enhanced menu content
    enhanced_menu = generate_enhanced_menu()
    
    # Create the enhanced remote script
    enhanced_content = header + "# Main execution\n\n" + enhanced_menu + "\n\n# Start the script\nentry_point\n"
    
    # Write the enhanced content to the destination file
    write_file(ENHANCED_REMOTE, enhanced_content)
    print(f"Enhanced remote script created at {ENHANCED_REMOTE}")
    
    # Make the enhanced remote script executable
    os.chmod(ENHANCED_REMOTE, 0o755)
    print("Made the enhanced remote script executable")

def main():
    """Main function"""
    print("Enhancing the God Mode remote control CLI...")
    modify_remote_script()
    print("\nDone! To use the enhanced CLI, run:")
    print(f"  {ENHANCED_REMOTE}")

if __name__ == "__main__":
    main() 