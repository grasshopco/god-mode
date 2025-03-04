#!/bin/bash

# god_mode_remote.sh
# This script controls God Mode in a subdirectory from a parent directory
# allowing users to maintain their workflow context while using God Mode capabilities.

# Set colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get the directory of this script (parent directory)
PARENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Default target is the GOD_MODE_PROJECT_STARTER_TEMPLATE
DEFAULT_TARGET="GOD_MODE_PROJECT_STARTER_TEMPLATE"
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

# Display header
echo -e "${BLUE}=======================================${NC}"
echo -e "${BLUE}    God Mode Remote Control Script    ${NC}"
echo -e "${BLUE}=======================================${NC}"
echo
echo -e "Parent directory: ${GREEN}$PARENT_DIR${NC}"
echo -e "Target directory: ${GREEN}$TARGET_DIR${NC}"
echo

# Function to display the menu
show_menu() {
    echo -e "${YELLOW}What would you like to do?${NC}"
    echo "1) Start God Mode in $TARGET_DIR"
    echo "2) Stop God Mode in $TARGET_DIR"
    echo "3) View God Mode status"
    echo "4) Route clipboard content to God Mode"
    echo "5) View recent logs"
    echo "6) Update project structure"
    echo "7) Update Cursor rules"
    echo "8) Navigate to target directory"
    echo "9) Choose a different target directory"
    echo "q) Quit"
    echo
    echo -n "Enter your choice: "
}

# Function to check if a process is running
is_process_running() {
    pgrep -f "$1" > /dev/null
    return $?
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
        echo -e "Message Router: ${GREEN}RUNNING${NC} (PID: $router_pid)"
    else
        echo -e "Message Router: ${RED}NOT RUNNING${NC}"
    fi
    
    if is_process_running "script_cursor_watch.py"; then
        watch_running=true
        local watch_pid=$(pgrep -f 'script_cursor_watch.py')
        echo -e "Cursor Watch: ${GREEN}RUNNING${NC} (PID: $watch_pid)"
    else
        echo -e "Cursor Watch: ${RED}NOT RUNNING${NC}"
    fi
    
    if $router_running && $watch_running; then
        echo -e "\n${GREEN}God Mode is fully active.${NC}"
    elif $router_running || $watch_running; then
        echo -e "\n${YELLOW}God Mode is partially active.${NC}"
    else
        echo -e "\n${RED}God Mode is not active.${NC}"
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
    else
        echo -e "${RED}Error: route script not found at $route_script${NC}"
    fi
}

# Function to view recent logs
view_logs() {
    local logs_dir="$FULL_TARGET_PATH/god_mode/logs"
    
    if [ ! -d "$logs_dir" ]; then
        echo -e "${RED}Error: Logs directory not found at $logs_dir${NC}"
        return
    fi
    
    echo -e "${YELLOW}Recent God Mode activity:${NC}"
    
    # Check for log files and display the most recent entries
    if [ -f "$logs_dir/message_router.log" ]; then
        echo -e "\n${GREEN}Message Router Log (last 10 entries):${NC}"
        tail -n 10 "$logs_dir/message_router.log"
    fi
    
    if [ -f "$logs_dir/cursor_watch.log" ]; then
        echo -e "\n${GREEN}Cursor Watch Log (last 10 entries):${NC}"
        tail -n 10 "$logs_dir/cursor_watch.log"
    fi
    
    if [ -f "$FULL_TARGET_PATH/god_mode/memory/memory_logs_all.md" ]; then
        echo -e "\n${GREEN}Recent Memory Logs (last 10 entries):${NC}"
        tail -n 20 "$FULL_TARGET_PATH/god_mode/memory/memory_logs_all.md"
    fi
}

# Function to update project structure
update_structure() {
    echo -e "${YELLOW}Updating project structure...${NC}"
    
    local script="$FULL_TARGET_PATH/god_mode/scripts/script_update_project_structure.py"
    
    if [ -f "$script" ]; then
        (cd "$FULL_TARGET_PATH" && python "$script")
        echo -e "${GREEN}Project structure updated.${NC}"
    else
        echo -e "${RED}Error: Update script not found at $script${NC}"
    fi
}

# Function to update Cursor rules
update_cursor_rules() {
    echo -e "${YELLOW}Updating Cursor rules...${NC}"
    
    local script="$FULL_TARGET_PATH/god_mode/scripts/script_update_cursor_rules.py"
    
    if [ -f "$script" ]; then
        (cd "$FULL_TARGET_PATH" && python "$script")
        echo -e "${GREEN}Cursor rules updated.${NC}"
    else
        echo -e "${RED}Error: Update script not found at $script${NC}"
    fi
}

# Function to navigate to the target directory
navigate_to_target() {
    echo -e "${YELLOW}Opening target directory in a new terminal...${NC}"
    
    # Open a new terminal window in the target directory
    open -a Terminal "$FULL_TARGET_PATH"
    
    echo -e "${GREEN}New terminal opened at $TARGET_DIR${NC}"
}

# Function to choose a different target directory
choose_target() {
    echo -e "${YELLOW}Available directories with potential God Mode:${NC}"
    
    # List subdirectories that might have God Mode
    local i=1
    local dirs=()
    
    for dir in "$PARENT_DIR"/*/; do
        if [ -d "${dir}god_mode" ] || [ -f "${dir}start_god_mode.sh" ]; then
            dir_name=$(basename "$dir")
            dirs+=("$dir_name")
            echo "$i) $dir_name"
            ((i++))
        fi
    done
    
    if [ ${#dirs[@]} -eq 0 ]; then
        echo -e "${RED}No directories with God Mode found.${NC}"
        return
    fi
    
    echo -n "Choose a directory (1-${#dirs[@]}): "
    read -r choice
    
    if [[ $choice =~ ^[0-9]+$ ]] && [ "$choice" -ge 1 ] && [ "$choice" -le "${#dirs[@]}" ]; then
        TARGET_DIR="${dirs[$((choice-1))]}"
        FULL_TARGET_PATH="$PARENT_DIR/$TARGET_DIR"
        echo -e "${GREEN}Now controlling God Mode in: $TARGET_DIR${NC}"
    else
        echo -e "${RED}Invalid choice.${NC}"
    fi
}

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
        8) navigate_to_target ;;
        9) choose_target ;;
        q|Q) echo -e "${GREEN}Goodbye!${NC}"; exit 0 ;;
        *) echo -e "${RED}Invalid choice. Please try again.${NC}" ;;
    esac
    
    # Pause to let the user read the output
    echo
    echo -n "Press Enter to continue..."
    read -r
done 