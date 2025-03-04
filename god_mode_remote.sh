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

# Function to refresh memory at startup
refresh_memory_at_startup() {
    echo -e "${YELLOW}Refreshing memory...${NC}"
    
    # Run critical memory update scripts
    local update_structure="$FULL_TARGET_PATH/god_mode/scripts/script_update_project_structure.py"
    local check_memory="$FULL_TARGET_PATH/god_mode/scripts/script_check_memory_files.sh"
    local check_features="$FULL_TARGET_PATH/god_mode/scripts/script_check_feature_logs.py"
    
    if [ -f "$update_structure" ]; then
        (cd "$FULL_TARGET_PATH" && python "$update_structure")
        echo -e "${GREEN}✓ Updated project structure${NC}"
    fi
    
    if [ -f "$check_memory" ]; then
        chmod +x "$check_memory"
        (cd "$FULL_TARGET_PATH" && "$check_memory")
        echo -e "${GREEN}✓ Checked memory files${NC}"
    fi
    
    if [ -f "$check_features" ]; then
        (cd "$FULL_TARGET_PATH" && python "$check_features" --check)
        echo -e "${GREEN}✓ Checked feature logs${NC}"
    fi
    
    echo -e "${GREEN}Memory refresh complete${NC}"
}

# Call this function at startup
refresh_memory_at_startup

# Function to check if a process is running
is_process_running() {
    pgrep -f "$1" > /dev/null
    return $?
}

# Function to restart the cursor watch process
restart_cursor_watch() {
    echo -e "${BLUE}Restarting Cursor Watch process...${NC}"
    
    # Check if cursor watch is already running
    if pgrep -f "script_cursor_watch.py" >/dev/null; then
        # Get the PID
        local watch_pid=$(pgrep -f "script_cursor_watch.py")
        
        # Kill the process
        echo -e "Stopping existing Cursor Watch process (PID: $watch_pid)..."
        kill -9 $watch_pid 2>/dev/null
        
        # Wait a moment to ensure the process is terminated
        sleep 1
    fi
    
    # Start a new cursor watch process
    local cursor_watch_script="$FULL_TARGET_PATH/god_mode/scripts/script_cursor_watch.py"
    
    if [ ! -f "$cursor_watch_script" ]; then
        echo -e "${RED}Error: Cursor Watch script not found at: $cursor_watch_script${NC}"
        return 1
    fi
    
    echo -e "Starting new Cursor Watch process..."
    chmod +x "$cursor_watch_script"
    nohup python3 "$cursor_watch_script" > "$FULL_TARGET_PATH/god_mode/logs/cursor_watch.log" 2>&1 &
    local new_pid=$!
    
    echo -e "${GREEN}Cursor Watch restarted with PID: $new_pid${NC}"
    return 0
}

# Update check_god_mode_status function to potentially restart cursor watch if it's not running
check_god_mode_status() {
    local verbose=$1
    local router_running=false
    local watch_running=false
    
    # Check if the message router is running
    if pgrep -f "route --watch" >/dev/null; then
        router_running=true
        router_pid=$(pgrep -f "route --watch")
        [ "$verbose" = "true" ] && echo -e "Message Router: ${GREEN}RUNNING${NC} ✓ (PID: $router_pid)"
        [ "$verbose" = "false" ] && echo -e "  ${GREEN}● Message Router is RUNNING${NC}"
    else
        [ "$verbose" = "true" ] && echo -e "Message Router: ${RED}NOT RUNNING${NC} ✗"
        [ "$verbose" = "false" ] && echo -e "  ${RED}● Message Router is NOT RUNNING${NC}"
    fi
    
    # Check if the cursor watch is running
    if pgrep -f "script_cursor_watch.py" >/dev/null; then
        watch_running=true
        watch_pid=$(pgrep -f "script_cursor_watch.py")
        [ "$verbose" = "true" ] && echo -e "Cursor Watch: ${GREEN}RUNNING${NC} ✓ (PID: $watch_pid)"
        [ "$verbose" = "false" ] && echo -e "  ${GREEN}● Cursor Watch is RUNNING${NC}"
    else
        # If cursor watch not running, try to restart it
        if [ "$verbose" = "true" ]; then
            echo -e "Cursor Watch: ${RED}NOT RUNNING${NC} ✗"
            echo -e "${YELLOW}Attempting to restart Cursor Watch...${NC}"
            restart_cursor_watch
            
            # Check again if it's running
            if pgrep -f "script_cursor_watch.py" >/dev/null; then
                watch_running=true
                watch_pid=$(pgrep -f "script_cursor_watch.py")
                echo -e "Cursor Watch: ${GREEN}NOW RUNNING${NC} ✓ (PID: $watch_pid)"
            else
                echo -e "Cursor Watch: ${RED}STILL NOT RUNNING${NC} ✗"
            fi
        else
            # For non-verbose mode
            echo -e "  ${RED}● Cursor Watch is NOT RUNNING${NC}"
            restart_cursor_watch > /dev/null 2>&1
            # Recheck if now running
            if pgrep -f "script_cursor_watch.py" >/dev/null; then 
                watch_running=true
                echo -e "  ${GREEN}● Cursor Watch has been restarted${NC}"
            fi
        fi
    fi
    
    # Determine overall status
    if $router_running && $watch_running; then
        [ "$verbose" = "true" ] && echo -e "\nOverall Status: ${GREEN}FULLY ACTIVE${NC} ✓"
        [ "$verbose" = "false" ] && echo -e "Overall Status: ${GREEN}● FULLY ACTIVE${NC}"
    elif $router_running || $watch_running; then
        [ "$verbose" = "true" ] && echo -e "\nOverall Status: ${YELLOW}PARTIALLY ACTIVE${NC} ⚠️"
        [ "$verbose" = "false" ] && echo -e "Overall Status: ${YELLOW}● PARTIALLY ACTIVE${NC}"
    else
        [ "$verbose" = "true" ] && echo -e "\nOverall Status: ${RED}NOT ACTIVE${NC} ✗"
        [ "$verbose" = "false" ] && echo -e "Overall Status: ${RED}● NOT ACTIVE${NC}"
    fi
    
    return 0
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
    check_god_mode_status "false"
    echo

    echo -e "${BLUE}=======================================${NC}"
    echo -e "${BLUE}     God Mode Remote Control Menu     ${NC}"
    echo -e "${BLUE}=======================================${NC}"
    echo -e "Current target: ${GREEN}$TARGET_DIR${NC}"
    echo
    echo -e "${YELLOW}STATUS & CONTROL:${NC}"
    echo -e "1) ${CYAN}Start God Mode${NC} - Activate AI superpowers in your project"
    echo -e "2) ${CYAN}Stop God Mode${NC} - Turn off God Mode"
    echo -e "3) ${CYAN}View God Mode status${NC} - Check if processes are running"
    echo
    echo -e "${YELLOW}CONTENT & MEMORY:${NC}"
    echo -e "4) ${CYAN}Route clipboard content${NC} - Process [TAG] markers in clipboard"
    echo -e "5) ${CYAN}View recent logs${NC} - See recent activity and insights"
    echo -e "6) ${CYAN}Update project structure${NC} - Refresh AI knowledge of your project"
    echo -e "7) ${CYAN}Enhance prompt${NC} - Add context to your next AI prompt"
    echo -e "8) ${CYAN}Create/update notepad${NC} - Manage notepads for reference info"
    echo -e "c) ${CYAN}Session continuity${NC} - Generate continuity for new chat sessions"
    echo -e "n) ${CYAN}Continue conversation${NC} - Choose from preset questions to continue"
    echo -e "t) ${CYAN}TAG compliance${NC} - View TAG usage metrics and reports"
    echo
    echo -e "${YELLOW}SETTINGS & TOOLS:${NC}"
    echo -e "s) ${CYAN}Notification settings${NC} - Manage notifications and sounds"
    echo -e "i) ${CYAN}Install God Mode shortcut${NC} - Create 'godmode' command (option 2 recommended for beginners)"
    echo -e "b) ${CYAN}Database or Backend integration${NC} - Set up various database backends to sync your memory files."
    echo -e "   Options include:"
    echo -e "   - Cloud backends: Supabase, Firebase (coming soon)"
    echo -e "   - Local backends: SQLite database for offline use"
    echo -e "   - Multiple backends: Configure several and easily switch between them"
    echo -e "   This allows for persistence across machines, data backup, and offline usage."
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
    echo -e "${CYAN}t) TAG compliance${NC}"
    echo -e "   View statistics about TAG usage and check for messages without tags."
    echo -e "   This helps ensure all messages have proper memory routing."
    echo
    echo -e "${CYAN}v) Verify system${NC}"
    echo -e "   Run tests to ensure all God Mode components are working correctly."
    echo -e "   This will check the Message Router, Cursor Watch, and dependencies."
    echo
    echo -e "${CYAN}b) Database or Backend integration${NC}"
    echo -e "   This feature lets you store God Mode memory files in the cloud or locally."
    echo -e "   This is NOT for your application data - it's for God Mode's own memory system!"
    echo -e "   Benefits include syncing across computers and backing up your AI's memory."
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
        echo -e "   ${YELLOW}Not working? Try running option 8 to install dependencies${NC}"
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

# Function to run the tag feedback system
run_tag_feedback() {
    echo -e "${BLUE}=======================================${NC}"
    echo -e "${BLUE}         TAG Compliance System        ${NC}"
    echo -e "${BLUE}=======================================${NC}"
    echo
    
    TAG_FEEDBACK_SCRIPT="$FULL_TARGET_PATH/god_mode/scripts/script_tag_feedback.py"
    
    # Check if the script exists
    if [ ! -f "$TAG_FEEDBACK_SCRIPT" ]; then
        echo -e "${RED}Error: TAG feedback script not found at:${NC}"
        echo -e "${RED}$TAG_FEEDBACK_SCRIPT${NC}"
        echo
        echo -e "Press Enter to continue..."
        read
        return
    fi
    
    # Show sub-menu for tag feedback options
    echo -e "Select a TAG feedback option:"
    echo -e "1) ${CYAN}View compliance report${NC} - See metrics and trends"
    echo -e "2) ${CYAN}Validate a specific file${NC} - Check if a file uses proper TAGs"
    echo -e "3) ${CYAN}Adjust reminder settings${NC} - Manually change enforcement level"
    echo -e "4) ${CYAN}Return to main menu${NC}"
    echo
    echo -n "Enter your choice: "
    read tag_choice
    
    case $tag_choice in
        1)
            # Run the report generation
            echo -e "${YELLOW}Generating TAG compliance report...${NC}"
            echo
            
            # Run the script with --report flag
            python3 "$TAG_FEEDBACK_SCRIPT" --report
            
            echo
            echo -e "${GREEN}Report generated successfully.${NC}"
            ;;
        2)
            # Prompt for file to validate
            echo -e "Enter the relative path of the file to validate (from $TARGET_DIR):"
            read file_path
            
            # Check if the file exists
            full_file_path="$FULL_TARGET_PATH/$file_path"
            if [ ! -f "$full_file_path" ]; then
                echo -e "${RED}Error: File not found at: $full_file_path${NC}"
            else
                echo -e "${YELLOW}Validating file: $file_path${NC}"
                echo
                
                # Run the script with --validate flag
                python3 "$TAG_FEEDBACK_SCRIPT" --validate "$full_file_path"
            fi
            ;;
        3)
            # Define levels
            echo -e "${YELLOW}Adjust TAG reminder settings:${NC}"
            echo -e "1) ${CYAN}Mild${NC} - Occasional gentle reminders"
            echo -e "2) ${CYAN}Normal${NC} - Regular reminders (default)"
            echo -e "3) ${CYAN}Severe${NC} - Strong, frequent reminders"
            echo
            echo -n "Enter your choice (1-3): "
            read level_choice
            
            # Create config directory if it doesn't exist
            CONFIG_DIR="$FULL_TARGET_PATH/god_mode/.cache"
            mkdir -p "$CONFIG_DIR"
            
            # Create or update the config file
            CONFIG_FILE="$CONFIG_DIR/tag_config.json"
            
            case $level_choice in
                1) 
                    level="mild"
                    frequency=0.3
                    ;;
                2) 
                    level="normal"
                    frequency=0.7
                    ;;
                3) 
                    level="severe"
                    frequency=1.0
                    ;;
                *) 
                    echo -e "${RED}Invalid choice. Using default (normal).${NC}"
                    level="normal"
                    frequency=0.7
                    ;;
            esac
            
            # Create JSON content
            json_content="{
  \"reminder_level\": \"$level\",
  \"check_frequency\": $frequency,
  \"last_updated\": \"$(date -u +"%Y-%m-%dT%H:%M:%SZ")\",
  \"compliance_rate\": 0.5,
  \"trend\": \"flat\",
  \"manually_set\": true
}"
            
            # Write to file
            echo "$json_content" > "$CONFIG_FILE"
            
            echo -e "${GREEN}Reminder level set to: $level (frequency: ${frequency}0%)${NC}"
            ;;
        4|*)
            # Return to main menu
            return
            ;;
    esac
    
    echo
    echo -e "Press Enter to continue..."
    read
}

# Function to run the continue conversation script
run_continue_conversation() {
    echo -e "${BLUE}=======================================${NC}"
    echo -e "${BLUE}       Continue Conversation          ${NC}"
    echo -e "${BLUE}=======================================${NC}"
    echo
    
    CONTINUE_SCRIPT="$FULL_TARGET_PATH/god_mode/scripts/script_continue_conversation.py"
    
    # Check if the script exists
    if [ ! -f "$CONTINUE_SCRIPT" ]; then
        echo -e "${RED}Error: Continue conversation script not found at:${NC}"
        echo -e "${RED}$CONTINUE_SCRIPT${NC}"
        echo
        echo -e "${YELLOW}Creating the script now...${NC}"
        
        # Create the script directory if it doesn't exist
        mkdir -p "$(dirname "$CONTINUE_SCRIPT")"
        
        # Create a basic version of the script
        cat > "$CONTINUE_SCRIPT" << 'EOF'
#!/usr/bin/env python3
"""
Conversation Continuation Script

This script makes it easy to continue conversations with the AI assistant.
"""
import sys
print("This is a placeholder script. Please update to the full version.")
sys.exit(1)
EOF
        
        chmod +x "$CONTINUE_SCRIPT"
        
        echo -e "${YELLOW}A placeholder script has been created. Please update it to the full version.${NC}"
        echo -e "Press Enter to continue..."
        read
        return
    fi
    
    # Make the script executable
    chmod +x "$CONTINUE_SCRIPT"
    
    # Run the script
    python3 "$CONTINUE_SCRIPT"
    
    echo
    echo -e "Press Enter to continue..."
    read
}

# Function to manage notification settings
manage_notification_settings() {
    echo -e "${BLUE}=======================================${NC}"
    echo -e "${BLUE}     Notification Settings           ${NC}"
    echo -e "${BLUE}=======================================${NC}"
    echo
    
    local notification_script="$FULL_TARGET_PATH/god_mode/scripts/script_notification_settings.py"
    
    # Check if the script exists
    if [ ! -f "$notification_script" ]; then
        echo -e "${RED}Error: Notification settings script not found at:${NC}"
        echo -e "${RED}$notification_script${NC}"
        echo
        echo -e "${YELLOW}Please make sure the script exists and try again.${NC}"
        echo
        echo -e "Press Enter to continue..."
        read
        return
    fi
    
    # Make the script executable
    chmod +x "$notification_script"
    
    # Display current settings
    echo -e "${YELLOW}Current notification settings:${NC}"
    python3 "$notification_script" --list
    
    # Show sub-menu for notification settings
    echo
    echo -e "Notification Settings Options:"
    echo -e "1) ${CYAN}Toggle desktop notifications${NC} (enable/disable)"
    echo -e "2) ${CYAN}Toggle sound effects${NC} (enable/disable)"
    echo -e "3) ${CYAN}Enable all notifications${NC}"
    echo -e "4) ${CYAN}Disable all notifications${NC}"
    echo -e "5) ${CYAN}Test notifications${NC}"
    echo -e "6) ${CYAN}Return to main menu${NC}"
    echo
    echo -n "Enter your choice: "
    read notification_choice
    
    case $notification_choice in
        1)
            echo -e "\n${YELLOW}Toggling desktop notifications...${NC}"
            python3 "$notification_script" --toggle-notifications
            ;;
        2)
            echo -e "\n${YELLOW}Toggling sound effects...${NC}"
            python3 "$notification_script" --toggle-sound
            ;;
        3)
            echo -e "\n${YELLOW}Enabling all notifications...${NC}"
            python3 "$notification_script" --enable-all
            ;;
        4)
            echo -e "\n${YELLOW}Disabling all notifications...${NC}"
            python3 "$notification_script" --disable-all
            ;;
        5)
            echo -e "\n${YELLOW}Testing notifications...${NC}"
            python3 "$notification_script" --test
            ;;
        6|*)
            # Return to main menu
            return
            ;;
    esac
    
    echo
    echo -e "Press Enter to continue..."
    read
}

# Function to install the 'godmode' shortcut command
install_godmode_shortcut() {
    echo -e "${BLUE}=======================================${NC}"
    echo -e "${BLUE}     Install 'godmode' Shortcut Command  ${NC}"
    echo -e "${BLUE}=======================================${NC}"
    echo
    
    local install_script="$FULL_TARGET_PATH/install_shortcut.sh"
    
    # Check if the install script exists
    if [ ! -f "$install_script" ]; then
        echo -e "${RED}Error: Shortcut installation script not found at:${NC}"
        echo -e "${RED}$install_script${NC}"
        echo
        echo -e "${YELLOW}Please make sure the installation script exists.${NC}"
        echo -e "The install_shortcut.sh file should be in the root of your God Mode project."
        echo
        echo -e "Press Enter to continue..."
        read
        return
    fi
    
    # Make the script executable
    chmod +x "$install_script"
    
    # Run the installation script
    "$install_script"
    
    echo
    echo -e "Press Enter to continue..."
    read
}

# Function to run system verification
run_system_verification() {
    echo -e "${BLUE}Running system verification...${NC}"
    
    local verify_script="$FULL_TARGET_PATH/god_mode/scripts/script_verify_system.py"
    
    if [ ! -f "$verify_script" ]; then
        echo -e "${RED}Error: System verification script not found at: $verify_script${NC}"
        return 1
    fi
    
    echo -e "${CYAN}Checking the status of all God Mode components...${NC}"
    python3 "$verify_script"
    
    local exit_code=$?
    if [ $exit_code -eq 0 ]; then
        echo -e "${GREEN}All systems operational!${NC}"
    else
        echo -e "${YELLOW}Some components need attention. Please follow the recommendations above.${NC}"
    fi
    
    return $exit_code
}

# Function to setup Database/Backend integration
setup_database_integration() {
    clear
    echo "======================================="
    echo "     Database Integration Setup       "
    echo "======================================="
    echo
    echo "This feature lets you store God Mode memory files in the cloud or locally."
    echo "This is NOT for your application data - it's for God Mode's own memory system!"
    echo "Benefits include syncing across computers and backing up your AI's memory."
    echo
    
    local integration_script="$FULL_TARGET_PATH/god_mode/scripts/script_create_supabase_integration.py"
    
    # Check if the script exists
    if [ ! -f "$integration_script" ]; then
        echo -e "${RED}Error: Database integration script not found at:${NC}"
        echo -e "${RED}$integration_script${NC}"
        echo
        echo -e "${YELLOW}Please make sure the script exists and try again.${NC}"
        echo
        echo -e "Press Enter to continue..."
        read
        return
    fi
    
    # Make the script executable
    chmod +x "$integration_script"
    
    # First check for latest versions
    echo -e "${YELLOW}Checking for latest package versions...${NC}"
    python3 "$integration_script" --check-version
    
    # Show main database options
    echo -e "\nDatabase Integration Options:"
    echo -e "1) ${CYAN}Setup a new database backend${NC} - Connect to Supabase, SQLite, or other services"
    echo -e "2) ${CYAN}Manage existing backends${NC} - View, switch, or delete configured connections"
    echo -e "3) ${CYAN}Sync with current backend${NC} - Update memory files in cloud from local files"
    echo -e "4) ${CYAN}Backup to current backend${NC} - Create a complete backup of your memory files"
    echo -e "5) ${CYAN}Restore from backup${NC} - Replace local memory files with backed up versions"
    echo -e "6) ${CYAN}Return to main menu${NC}"
    echo
    echo -n "Enter your choice: "
    read db_choice
    
    case $db_choice in
        1)
            echo -e "\n${YELLOW}Setting up a new database backend...${NC}"
            python3 "$integration_script" --setup
            ;;
        2)
            echo -e "\n${YELLOW}Managing existing backends...${NC}"
            python3 "$integration_script" --list-backends
            
            # Ask if they want to switch backends
            echo -e "\nWould you like to switch to a different backend? (y/n): "
            read switch_choice
            
            if [ "$switch_choice" = "y" ]; then
                echo -e "\nEnter the name of the backend to switch to: "
                read backend_name
                python3 "$integration_script" --switch-backend "$backend_name"
            fi
            ;;
        3)
            echo -e "\n${YELLOW}Syncing with current backend...${NC}"
            python3 "$integration_script" --sync
            ;;
        4)
            echo -e "\n${YELLOW}Backing up to current backend...${NC}"
            python3 "$integration_script" --backup
            ;;
        5)
            echo -e "\n${YELLOW}Restoring from backup...${NC}"
            python3 "$integration_script" --restore
            ;;
        6)
            echo -e "\n${YELLOW}Returning to main menu...${NC}"
            ;;
        *)
            echo -e "\n${RED}Invalid choice. Returning to main menu.${NC}"
            ;;
    esac
}

# Function to verify God Mode is running
verify_god_mode() {
    echo -e "${BLUE}Verifying God Mode processes...${NC}"
    check_god_mode_status "true"
    
    echo -e "\nPress Enter to continue..."
    read -r
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
    read -n 1 choice
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
        v|V) run_system_verification ;;
        t|T) run_tag_feedback ;;
        n|N) run_continue_conversation ;;
        s|S) manage_notification_settings ;;
        i|I) install_godmode_shortcut ;;
        b|B)
            setup_database_integration 
            ;;
        *) echo -e "${RED}Invalid choice. Please try again.${NC}" ;;
    esac
    
    # Pause to let the user read the output
    echo
    echo -n "Press Enter to continue..."
    read -r
done 