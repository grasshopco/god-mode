#!/bin/bash

# god_mode_remote.sh
# This script controls God Mode in a subdirectory from a parent directory
# allowing users to maintain their workflow context while using God Mode capabilities.

# Set colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Get the directory of this script (parent directory)
PARENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Default target is the GOD_MODE_PROJECT_STARTER_TEMPLATE
DEFAULT_TARGET="GOD_MODE_PROJECT_STARTER_TEMPLATE"

# Check for help flags
if [ "$1" = "--help" ] || [ "$1" = "-h" ]; then
    echo -e "${BLUE}=======================================${NC}"
    echo -e "${BLUE}     God Mode Remote Control Help     ${NC}"
    echo -e "${BLUE}=======================================${NC}"
    echo
    echo -e "Usage: $0 [target_directory]"
    echo
    echo -e "This script allows you to control God Mode from any directory."
    echo -e "If no target directory is specified, it will default to: ${GREEN}$DEFAULT_TARGET${NC}"
    echo
    echo -e "Available options:"
    echo -e "  [target_directory]   The directory containing God Mode to control"
    echo -e "  --help, -h           Display this help message"
    echo
    echo -e "Example:"
    echo -e "  $0                   # Control God Mode in the default directory"
    echo -e "  $0 my_project        # Control God Mode in 'my_project' directory"
    echo
    exit 0
fi

TARGET_DIR="${1:-$DEFAULT_TARGET}"

# Full path to the target directory
FULL_TARGET_PATH="$PARENT_DIR/$TARGET_DIR"

# Check if the target directory exists
if [ ! -d "$FULL_TARGET_PATH" ]; then
    echo -e "${RED}Error: Target directory '$TARGET_DIR' not found in $PARENT_DIR${NC}"
    echo -e "Usage: $0 [target_directory]"
    echo -e "Example: $0 my_project_with_god_mode"
    exit 1
fi

# Check if the target directory has God Mode
if [ ! -d "$FULL_TARGET_PATH/god_mode" ]; then
    echo -e "${RED}Error: The target directory does not contain God Mode (no 'god_mode' folder found)${NC}"
    exit 1
fi

# Function to check if a process is running
is_process_running() {
    pgrep -f "$1" > /dev/null
    return $?
}

# Check God Mode status for display in header
check_god_mode_status_header() {
    local router_running=false
    local watch_running=false
    
    if is_process_running "route --watch"; then
        router_running=true
    fi
    
    if is_process_running "script_cursor_watch.py"; then
        watch_running=true
    fi
    
    echo "Component Status:"
    if $router_running; then
        echo -e "  ${GREEN}● Message Router is RUNNING${NC}"
    else
        echo -e "  ${RED}● Message Router is NOT RUNNING${NC}"
        echo -e "    ${YELLOW}→ Run option 1 to start, or run the dependency installer (option 8)${NC}"
    fi
    
    if $watch_running; then
        echo -e "  ${GREEN}● Cursor Watch is RUNNING${NC}"
    else
        echo -e "  ${RED}● Cursor Watch is NOT RUNNING${NC}"
        echo -e "    ${YELLOW}→ Run option 1 to start${NC}"
    fi
    
    echo
    if $router_running && $watch_running; then
        echo -e "Overall Status: ${GREEN}● FULLY ACTIVE${NC}"
    elif $router_running || $watch_running; then
        echo -e "Overall Status: ${YELLOW}● PARTIALLY ACTIVE${NC}"
    else
        echo -e "Overall Status: ${RED}● NOT ACTIVE${NC}"
    fi
}


# Function to manually trigger an auto-commit
trigger_auto_commit() {
    echo -e "${BLUE}Triggering auto-commit...${NC}"
    
    # Check if auto-commit script exists
    local auto_commit_script=""
    
    # Handle the case when "." is used as the target directory
    if [ "$TARGET_DIR" = "." ]; then
        auto_commit_script="$PARENT_DIR/god_mode/scripts/script_auto_commit.sh"
        # If that doesn't exist, try the default location
        if [ ! -f "$auto_commit_script" ]; then
            auto_commit_script="$PARENT_DIR/GOD_MODE_PROJECT_STARTER_TEMPLATE/god_mode/scripts/script_auto_commit.sh"
        fi
    else
        auto_commit_script="$FULL_TARGET_PATH/god_mode/scripts/script_auto_commit.sh"
    fi
    
    if [ ! -f "$auto_commit_script" ]; then
        echo -e "${RED}Error: Auto-commit script not found at:${NC}"
        echo -e "$auto_commit_script"
        echo
        echo -e "${YELLOW}Please make sure the script exists and try again.${NC}"
        return 1
    fi
    
    # Make the script executable
    chmod +x "$auto_commit_script"
    
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
    local setup_script=""
    
    # Handle the case when "." is used as the target directory
    if [ "$TARGET_DIR" = "." ]; then
        setup_script="$PARENT_DIR/god_mode/scripts/script_setup_github.sh"
        # If that doesn't exist, try the default location
        if [ ! -f "$setup_script" ]; then
            setup_script="$PARENT_DIR/GOD_MODE_PROJECT_STARTER_TEMPLATE/god_mode/scripts/script_setup_github.sh"
        fi
    else
        setup_script="$FULL_TARGET_PATH/god_mode/scripts/script_setup_github.sh"
    fi
    
    if [ ! -f "$setup_script" ]; then
        echo -e "${RED}Error: GitHub setup script not found at:${NC}"
        echo -e "$setup_script"
        echo
        echo -e "${YELLOW}Please make sure the script exists and try again.${NC}"
        return 1
    fi
    
    # Make the script executable
    chmod +x "$setup_script"
    
    # Run the setup script
    "$setup_script"
}

# Function to display the menu
show_menu() {
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
    echo -e "g) ${CYAN}GitHub repository management${NC} - Setup, connect, or switch GitHub repos"
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
}

# Function to display detailed help
show_help() {
    echo -e "${BLUE}=======================================${NC}"
    echo -e "${BLUE}           God Mode Help              ${NC}"
    echo -e "${BLUE}=======================================${NC}"
    echo
    echo -e "${CYAN}1) Start God Mode${NC}"
    echo -e "   This option activates the AI superpowers in your project."
    echo -e "   It starts the Message Router (processes [TAG] markers)"
    echo -e "   and Cursor Watch (enhances AI prompts with context)."
    echo -e "   Use this when you begin working on your project."
    echo
    echo -e "${CYAN}2) Stop God Mode${NC}"
    echo -e "   This turns off the background processes that power God Mode."
    echo -e "   Use this when you're done working or if you need to restart God Mode."
    echo
    echo -e "${CYAN}3) View God Mode status${NC}"
    echo -e "   Checks if the Message Router and Cursor Watch processes are running."
    echo -e "   If either shows as NOT RUNNING, try restarting God Mode (option 1)."
    echo -e "   The Message Router handles [TAG] markers like [LOG_SUMMARY]."
    echo -e "   The Cursor Watch enhances AI with context from your project."
    echo
    echo -e "${CYAN}4) Route clipboard content${NC}"
    echo -e "   Takes text from your clipboard and processes any [TAG] markers."
    echo -e "   Example: If your clipboard has text with [LOG_SUMMARY], it will"
    echo -e "   extract that content and save it to the appropriate file."
    echo -e "   Tags include: [LOG_SUMMARY], [LOG_DETAIL], [MEMORY_UPDATE], etc."
    echo -e "   For a complete guide to tags, see: god_mode/system_documentation/README_TAGS.md"
    echo
    echo -e "${CYAN}5) View recent logs${NC}"
    echo -e "   Shows the most recent activity from God Mode log files."
    echo -e "   Useful for seeing what's been happening in your project."
    echo
    echo -e "${CYAN}6) Update project structure${NC}"
    echo -e "   Scans your project folders and updates the AI's knowledge."
    echo -e "   Run this after adding new files or folders to your project."
    echo
    echo -e "${CYAN}7) Update Cursor rules${NC}"
    echo -e "   Refreshes the instructions that guide how the AI assistant behaves."
    echo -e "   Run this if the AI isn't adding [TAG] markers to its responses."
    echo
    echo -e "${CYAN}8) Install dependencies${NC}"
    echo -e "   Installs required Python packages (pyperclip, plyer) for God Mode."
    echo -e "   Run this if Message Router is not starting or notifications aren't working."
    echo
    echo -e "${CYAN}9) Navigate to target directory${NC}"
    echo -e "   Opens a new terminal window in your project folder."
    echo -e "   Useful if you need to run commands directly in that folder."
    echo
    echo -e "${CYAN}r) View routing activity${NC}"
    echo -e "   Shows what content was recently routed to which files."
    echo -e "   Provides clickable links to open files at the exact line where"
    echo -e "   content was added, so you can quickly verify what was saved where."
    echo -e "   Extremely useful when working with [MULTI_TAG] to see where"
    echo -e "   everything went without having to search manually."
    echo
    echo -e "${CYAN}d) View documentation${NC}"
    echo -e "   Opens helpful guides and documentation about God Mode."
    echo -e "   Includes information on tags, features, and best practices."
    echo
    echo -e "${CYAN}Troubleshooting Tips:${NC}"
    echo -e "• If Message Router shows NOT RUNNING, make sure python packages are installed:"
    echo -e "  Run option 8 (Install dependencies) or run this command:"
    echo -e "  ${GREEN}$FULL_TARGET_PATH/god_mode/scripts/script_install_dependencies.sh${NC}"
    echo -e "• If the AI isn't adding [TAG] markers, try updating Cursor rules (option 7)"
    echo -e "• If desktop notifications aren't working, run option 8 to install the plyer package"
    echo -e "• If having persistent issues, run the file integrity check:"
    echo -e "  ${GREEN}$FULL_TARGET_PATH/god_mode/scripts/script_check_files.sh${NC}"
    echo
    echo -e "${CYAN}Documentation:${NC}"
    echo -e "• Tag System Guide: ${GREEN}$FULL_TARGET_PATH/god_mode/system_documentation/README_TAGS.md${NC}"
    echo -e "  This guide explains all available tags and how to use them effectively."
    echo -e "  To open it: ${YELLOW}open \"$FULL_TARGET_PATH/god_mode/system_documentation/README_TAGS.md\"${NC}"
    echo
    echo -e "Press Enter to return to the main menu..."
    read -r
}

# Function to start God Mode
start_god_mode() {
    echo -e "${YELLOW}Starting God Mode in $TARGET_DIR...${NC}"
    
    # Execute the start script in the target directory
    if [ -f "$FULL_TARGET_PATH/start_god_mode.sh" ]; then
        # Make it executable if it's not
        chmod +x "$FULL_TARGET_PATH/start_god_mode.sh"
        
        # Run it
        (cd "$FULL_TARGET_PATH" && ./start_god_mode.sh)
        
        # Additional check to see if processes are running
        echo
        echo -e "${YELLOW}Verifying God Mode processes...${NC}"
        sleep 2  # Give processes time to start
        
        if is_process_running "route --watch"; then
            echo -e "Message Router: ${GREEN}RUNNING${NC} ✓"
        else
            echo -e "Message Router: ${RED}NOT RUNNING${NC} ✗"
            echo -e "${YELLOW}Troubleshooting tip: Run option 8 to install dependencies${NC}"
            echo -e "${YELLOW}Command: $FULL_TARGET_PATH/god_mode/scripts/script_install_dependencies.sh${NC}"
        fi
        
        if is_process_running "script_cursor_watch.py"; then
            echo -e "Cursor Watch: ${GREEN}RUNNING${NC} ✓"
        else
            echo -e "Cursor Watch: ${RED}NOT RUNNING${NC} ✗"
        fi
    else
        echo -e "${RED}Error: start_god_mode.sh not found in $TARGET_DIR${NC}"
    fi
}

# Function to stop God Mode
stop_god_mode() {
    echo -e "${YELLOW}Stopping God Mode processes...${NC}"
    
    # Kill the message router and cursor watch processes
    pkill -f 'route --watch'
    pkill -f 'script_cursor_watch.py'
    
    echo -e "${GREEN}God Mode processes stopped.${NC}"
}

# Function to view God Mode status
view_status() {
    echo -e "${YELLOW}Checking God Mode status...${NC}"
    
    local router_running=false
    local watch_running=false
    
    if is_process_running "route --watch"; then
        router_running=true
        local router_pid=$(pgrep -f 'route --watch')
        echo -e "Message Router: ${GREEN}RUNNING${NC} ✓ (PID: $router_pid)"
        echo -e "   This process handles text with [TAG] markers like [LOG_SUMMARY]"
    else
        echo -e "Message Router: ${RED}NOT RUNNING${NC} ✗"
        echo -e "   ${YELLOW}Not working? Try running option 8 (Install dependencies)${NC}"
        echo -e "   This process is needed to handle [TAG] markers in text"
    fi
    
    if is_process_running "script_cursor_watch.py"; then
        watch_running=true
        local watch_pid=$(pgrep -f 'script_cursor_watch.py')
        echo -e "Cursor Watch: ${GREEN}RUNNING${NC} ✓ (PID: $watch_pid)"
        echo -e "   This process enhances AI prompts with context from your project"
    else
        echo -e "Cursor Watch: ${RED}NOT RUNNING${NC} ✗"
        echo -e "   This process enhances AI responses with project context"
    fi
    
    if $router_running && $watch_running; then
        echo -e "\n${GREEN}God Mode is fully active.${NC} ✓"
        echo -e "You can now use all God Mode features!"
    elif $router_running || $watch_running; then
        echo -e "\n${YELLOW}God Mode is partially active.${NC} ⚠️"
        echo -e "Some features may not work correctly. Try restarting God Mode."
    else
        echo -e "\n${RED}God Mode is not active.${NC} ✗"
        echo -e "Use option 1 to start God Mode."
    fi
}

# Function to route clipboard content
route_clipboard() {
    echo -e "${YELLOW}Routing clipboard content to God Mode...${NC}"
    
    local route_script="$FULL_TARGET_PATH/god_mode/scripts/route"
    
    if [ -f "$route_script" ]; then
        # Make it executable if it's not
        chmod +x "$route_script"
        
        # Run it with the clipboard option
        "$route_script" --clipboard
        
        echo -e "\n${GREEN}Tip:${NC} If you don't see desktop notifications, the content may not have any [TAG] markers."
        echo -e "Tags include: [LOG_SUMMARY], [LOG_DETAIL], [MEMORY_UPDATE], [FEATURE_LOG: Name], etc."
        echo -e "You can also use [MULTI_TAG: TAG1, TAG2, ...] to route content to multiple destinations."
    else
        echo -e "${RED}Error: route script not found at $route_script${NC}"
        echo -e "${YELLOW}Try running the file integrity check:${NC}"
        echo -e "${YELLOW}$FULL_TARGET_PATH/god_mode/scripts/script_check_files.sh${NC}"
    fi
}

# Function to view recent logs
view_logs() {
    local logs_dir="$FULL_TARGET_PATH/god_mode/logs"
    
    if [ ! -d "$logs_dir" ]; then
        echo -e "${RED}Error: Logs directory not found at $logs_dir${NC}"
        echo -e "Creating logs directory..."
        mkdir -p "$logs_dir"
        echo -e "${GREEN}Created logs directory at $logs_dir${NC}"
        return
    fi
    
    echo -e "${YELLOW}Recent God Mode activity:${NC}"
    
    local found_logs=false
    
    # Check for log files and display the most recent entries
    if [ -f "$logs_dir/message_router.log" ]; then
        echo -e "\n${GREEN}Message Router Log (last 10 entries):${NC}"
        tail -n 10 "$logs_dir/message_router.log"
        found_logs=true
    fi
    
    if [ -f "$logs_dir/cursor_watch.log" ]; then
        echo -e "\n${GREEN}Cursor Watch Log (last 10 entries):${NC}"
        tail -n 10 "$logs_dir/cursor_watch.log"
        found_logs=true
    fi
    
    if [ -f "$FULL_TARGET_PATH/god_mode/memory/memory_logs_all.md" ]; then
        echo -e "\n${GREEN}Recent Memory Logs (last 10 entries):${NC}"
        tail -n 20 "$FULL_TARGET_PATH/god_mode/memory/memory_logs_all.md"
        found_logs=true
    fi
    
    if [ -f "$logs_dir/debug_router.log" ]; then
        echo -e "\n${GREEN}Debug Log (last 10 entries):${NC}"
        tail -n 10 "$logs_dir/debug_router.log"
        found_logs=true
    fi
    
    if [ "$found_logs" = false ]; then
        echo -e "${YELLOW}No log files found yet. Try using God Mode first to generate logs.${NC}"
    fi
}

# Function to update project structure
update_structure() {
    echo -e "${YELLOW}Updating project structure...${NC}"
    
    local script="$FULL_TARGET_PATH/god_mode/scripts/script_update_project_structure.py"
    
    if [ -f "$script" ]; then
        (cd "$FULL_TARGET_PATH" && python "$script")
        echo -e "${GREEN}Project structure updated.${NC}"
        echo -e "The AI assistant now has an updated map of your project files and folders."
    else
        echo -e "${RED}Error: Update script not found at $script${NC}"
    fi
}

# Function to update Cursor rules
update_cursor_rules() {
    echo -e "${YELLOW}Updating Cursor rules...${NC}"
    
    local script="$FULL_TARGET_PATH/god_mode/scripts/script_update_cursor_rules.py"
    
    if [ -f "$script" ]; then
        (cd "$FULL_TARGET_PATH" && python "$script" --force)
        echo -e "${GREEN}Cursor rules updated.${NC}"
        echo -e "The AI assistant's instructions have been refreshed."
        echo -e "This should help with automatic [TAG] markers in AI responses."
    else
        echo -e "${RED}Error: Update script not found at $script${NC}"
    fi
}

# Function to install dependencies
install_dependencies() {
    echo -e "${BLUE}=======================================${NC}"
    echo -e "${BLUE}     Installing God Mode Dependencies  ${NC}"
    echo -e "${BLUE}=======================================${NC}"
    echo
    
    local script="$FULL_TARGET_PATH/god_mode/scripts/script_install_dependencies.sh"
    
    if [ -f "$script" ]; then
        # Make it executable if it's not
        chmod +x "$script"
        
        # Run it
        echo -e "${YELLOW}Running dependency installer...${NC}"
        "$script"
        
        if [ $? -eq 0 ]; then
            echo -e "\n${GREEN}✓ Dependencies installed successfully${NC}"
            echo -e "${YELLOW}You should now be able to start God Mode with option 1${NC}"
        else
            echo -e "\n${RED}✗ There was a problem installing dependencies${NC}"
            echo -e "${YELLOW}Try running the script manually:${NC}"
            echo -e "  cd \"$FULL_TARGET_PATH/god_mode/scripts\" && ./script_install_dependencies.sh"
        fi
    else
        echo -e "${RED}Error: Dependency installer script not found at:${NC}"
        echo -e "$script"
        echo
        echo -e "${YELLOW}Try installing dependencies manually:${NC}"
        echo -e "  pip install pyperclip plyer"
    fi
}

# Function to navigate to the target directory
navigate_to_target() {
    echo -e "${YELLOW}Opening target directory in a new terminal...${NC}"
    
    # Open a new terminal window in the target directory
    open -a Terminal "$FULL_TARGET_PATH"
    
    echo -e "${GREEN}New terminal opened at $TARGET_DIR${NC}"
}

# Function to view readme files
view_readme() {
    echo -e "${YELLOW}Available Documentation:${NC}"
    echo -e "1) Tag System Guide - Learn how to use [TAG] markers"
    echo -e "2) God Mode Overview - Understand how God Mode works"
    echo -e "3) Back to main menu"
    echo
    echo -n "Which document would you like to view? "
    read -r doc_choice
    
    case "$doc_choice" in
        1)
            local readme_path="$FULL_TARGET_PATH/god_mode/system_documentation/README_TAGS.md"
            if [ -f "$readme_path" ]; then
                # Try to open with the default application first
                open "$readme_path" 2>/dev/null || {
                    # If that fails, show content in terminal
                    echo -e "\n${GREEN}=== TAG SYSTEM GUIDE ===${NC}\n"
                    cat "$readme_path"
                    echo
                }
            else
                echo -e "${RED}Error: Tag guide not found at $readme_path${NC}"
            fi
            ;;
        2)
            local readme_path="$FULL_TARGET_PATH/README.md"
            if [ -f "$readme_path" ]; then
                # Try to open with the default application first
                open "$readme_path" 2>/dev/null || {
                    # If that fails, show content in terminal
                    echo -e "\n${GREEN}=== GOD MODE OVERVIEW ===${NC}\n"
                    cat "$readme_path"
                    echo
                }
            else
                echo -e "${RED}Error: Overview not found at $readme_path${NC}"
            fi
            ;;
        3|*)
            # Just return to main menu
            return
            ;;
    esac
}

# Function to view recent routing activity
view_routing_activity() {
    echo -e "${YELLOW}Recent Message Routing Activity:${NC}"
    
    local script="$FULL_TARGET_PATH/god_mode/scripts/script_track_routing.py"
    
    if [ -f "$script" ]; then
        # Make it executable if it's not
        chmod +x "$script"
        
        # Run the script
        (cd "$FULL_TARGET_PATH" && python "$script")
        
        echo -e "\n${GREEN}To open a specific file, you can run:${NC}"
        echo -e "cd \"$FULL_TARGET_PATH\" && python god_mode/scripts/script_track_routing.py --open <number>"
    else
        echo -e "${RED}Error: Routing tracker script not found at $script${NC}"
        echo -e "${YELLOW}This feature requires the latest version of God Mode.${NC}"
    fi
}

# Function to manage GitHub repository
manage_github_repo() {
    # Call the GitHub setup script with menu option
    local setup_script=""
    
    # Handle the case when "." is used as the target directory
    if [ "$TARGET_DIR" = "." ]; then
        setup_script="$PARENT_DIR/god_mode/scripts/script_setup_github.sh"
        # If that doesn't exist, try the default location
        if [ ! -f "$setup_script" ]; then
            setup_script="$PARENT_DIR/GOD_MODE_PROJECT_STARTER_TEMPLATE/god_mode/scripts/script_setup_github.sh"
        fi
    else
        setup_script="$FULL_TARGET_PATH/god_mode/scripts/script_setup_github.sh"
    fi
    
    # Check if the setup script exists
    if [ ! -f "$setup_script" ]; then
        echo -e "${RED}Error: GitHub setup script not found at:${NC}"
        echo -e "$setup_script"
        echo
        echo -e "${YELLOW}Please make sure the script exists and try again.${NC}"
        echo -e "${YELLOW}You can try running the script directly:${NC}"
        echo -e "${YELLOW}cd GOD_MODE_PROJECT_STARTER_TEMPLATE/god_mode/scripts && ./script_setup_github.sh${NC}"
        return 1
    fi
    
    # Make the script executable
    chmod +x "$setup_script"
    
    # Run the script
    "$setup_script" --menu
}

# Display header with a welcome message
echo -e "${BLUE}=======================================${NC}"
echo -e "${BLUE}     God Mode Remote Control         ${NC}"
echo -e "${BLUE}=======================================${NC}"
echo
echo -e "Parent directory: ${GREEN}$PARENT_DIR${NC}"
echo -e "Target directory: ${GREEN}$TARGET_DIR${NC}"
echo

# Main loop
while true; do
    echo
    show_menu
    read -r choice
    echo
    
    case "$choice" in
        1) start_god_mode ;;
        2) stop_god_mode ;;
        3) view_status ;;
        4) route_clipboard ;;
        5) view_logs ;;
        6) update_structure ;;
        7) update_cursor_rules ;;
        8) install_dependencies ;;
        9) navigate_to_target ;;
        g|G) manage_github_repo ;;
        a|A) trigger_auto_commit ;;
        r|R) view_routing_activity ;;
        d|D) view_readme ;;
        h|H) show_help ;;
        q|Q) echo -e "${GREEN}Goodbye!${NC}"; exit 0 ;;
        c|C) echo -e "${YELLOW}Session continuity feature is not implemented yet.${NC}" ;;
        v|V) echo -e "${YELLOW}System verification feature is not implemented yet.${NC}" ;;
        *) echo -e "${RED}Invalid choice. Please try again.${NC}" ;;
    esac
    
    # Pause to let the user read the output
    echo
    echo -n "Press Enter to continue..."
    read -r
done 