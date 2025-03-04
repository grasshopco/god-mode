#!/bin/bash

# start_god_mode.sh
# This script helps users start the God Mode system by initializing the necessary 
# components and starting the required background processes.

# Set colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Get the directory of this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
GOD_MODE_DIR="$SCRIPT_DIR/god_mode"
SCRIPTS_DIR="$GOD_MODE_DIR/scripts"

echo -e "${BLUE}=======================================${NC}"
echo -e "${BLUE}  Cursor IDE God Mode Startup Script  ${NC}"
echo -e "${BLUE}=======================================${NC}"
echo

# Check if God Mode is initialized
if [ ! -f "$GOD_MODE_DIR/memory/MEMORY_CURSOR.md" ]; then
    echo -e "${YELLOW}God Mode is not initialized yet. Initializing...${NC}"
    
    # Check if the initialization script exists
    if [ -f "$SCRIPTS_DIR/script_initialize_god_mode.sh" ]; then
        # Make it executable if it's not
        chmod +x "$SCRIPTS_DIR/script_initialize_god_mode.sh"
        
        # Run the initialization script
        "$SCRIPTS_DIR/script_initialize_god_mode.sh"
    else
        echo -e "${RED}Error: Initialization script not found at $SCRIPTS_DIR/script_initialize_god_mode.sh${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}God Mode is already initialized.${NC}"
fi

# Check for required dependencies
check_dependencies

# Ensure the logs directory exists
mkdir -p "$GOD_MODE_DIR/logs"

# Function to check if a process is running
is_process_running() {
    pgrep -f "$1" > /dev/null
    return $?
}

# Function to check if a Python module is installed
check_python_module() {
    if python3 -c "import $1" 2>/dev/null; then
        return 0
    elif python -c "import $1" 2>/dev/null; then
        return 0
    else
        return 1
    fi
}

# Check for required dependencies
check_dependencies() {
    local missing_deps=()
    
    echo -e "Checking dependencies..."
    
    # Check for pyperclip
    if ! check_python_module "pyperclip"; then
        echo -e "${YELLOW}Warning: pyperclip module not found. This is required for clipboard access.${NC}"
        missing_deps+=("pyperclip")
    fi
    
    # Check for plyer
    if ! check_python_module "plyer"; then
        echo -e "${YELLOW}Warning: plyer module not found. This is required for notifications.${NC}"
        missing_deps+=("plyer")
    fi
    
    # Check for pyobjus on macOS (required for notifications)
    if [[ "$OSTYPE" == "darwin"* ]]; then
        if ! check_python_module "pyobjus"; then
            echo -e "${YELLOW}Warning: pyobjus module not found. This is required for macOS notifications.${NC}"
            missing_deps+=("pyobjus")
        fi
    fi
    
    # If there are missing dependencies, ask to install them
    if [ ${#missing_deps[@]} -gt 0 ]; then
        echo -e "${YELLOW}Some required dependencies are missing.${NC}"
        echo -e "Would you like to install them now? (y/n)"
        read -r install_deps
        
        if [[ $install_deps =~ ^[Yy]$ ]]; then
            echo -e "Installing missing dependencies..."
            if [ -f "$SCRIPTS_DIR/script_install_dependencies.sh" ]; then
                chmod +x "$SCRIPTS_DIR/script_install_dependencies.sh"
                "$SCRIPTS_DIR/script_install_dependencies.sh"
            else
                # Fallback if the script doesn't exist
                for dep in "${missing_deps[@]}"; do
                    echo -e "Installing $dep..."
                    pip install "$dep" || pip3 install "$dep"
                done
            fi
        else
            echo -e "${YELLOW}Warning: Some features may not work without the required dependencies.${NC}"
            echo -e "You can install them later with: $SCRIPTS_DIR/script_install_dependencies.sh"
        fi
    fi
}

# Start the necessary background processes
echo
echo -e "${YELLOW}Starting God Mode background processes...${NC}"

# 1. Start the message router in watch mode
if is_process_running "route --watch"; then
    echo -e "Message router is already running."
else
    echo -e "Starting message router in watch mode..."
    nohup "$SCRIPTS_DIR/route" --watch > "$GOD_MODE_DIR/logs/message_router.log" 2>&1 &
    ROUTER_PID=$!
    echo -e "Message router started with PID $ROUTER_PID"
fi

# 2. Start the cursor watch script
if is_process_running "script_cursor_watch.py"; then
    echo -e "Cursor watch script is already running."
else
    echo -e "Starting cursor watch script..."
    nohup python "$SCRIPTS_DIR/script_cursor_watch.py" > "$GOD_MODE_DIR/logs/cursor_watch.log" 2>&1 &
    WATCH_PID=$!
    echo -e "Cursor watch script started with PID $WATCH_PID"
fi

# 3. Update the project structure
echo -e "Updating project structure..."
python "$SCRIPTS_DIR/script_update_project_structure.py"

# 3.5. Update functions and types maps
echo -e "Updating functions and types maps..."
python "$SCRIPTS_DIR/script_update_functions_and_types.py"

# 4. Update cursor rules
echo -e "Updating Cursor rules..."
python "$SCRIPTS_DIR/script_update_cursor_rules.py"

echo
echo -e "${GREEN}God Mode is now active!${NC}"
echo -e "The following components are running:"
echo -e "  - Message Router (PID ${ROUTER_PID:-Unknown})"
echo -e "  - Cursor Watch (PID ${WATCH_PID:-Unknown})"
echo
echo -e "${YELLOW}You can start using Cursor IDE with God Mode capabilities.${NC}"
echo -e "Your messages will automatically be enhanced with context from:"
echo -e "  - Project memory files"
echo -e "  - Recent changes and discussions"
echo -e "  - Project structure and architecture"
echo
echo -e "AI responses will include markers for automatic documentation."
echo -e "Example markers: [LOG_SUMMARY], [LOG_DETAIL], [MEMORY_UPDATE], etc."
echo
echo -e "${YELLOW}To stop God Mode:${NC}"
echo -e "Run: killall -f 'route --watch' 'script_cursor_watch.py'"
echo
echo -e "${BLUE}=======================================${NC}"
echo -e "${BLUE}       God Mode is now active         ${NC}"
echo -e "${BLUE}=======================================${NC}"

# Add directory navigation help
echo
echo -e "${CYAN}================= DIRECTORY NAVIGATION =================${NC}"
echo -e "${YELLOW}Current directory:${NC} $(pwd)"
echo -e "${YELLOW}Navigation commands:${NC}"
echo -e "  ${GREEN}cd ..${NC}                - Move up one directory level"
echo -e "  ${GREEN}cd [directory_name]${NC}  - Move into a specific directory"
echo -e "  ${GREEN}cd ~${NC}                 - Return to your home directory"
echo -e "  ${GREEN}pwd${NC}                  - Show current directory path"
echo -e "  ${GREEN}ls${NC}                   - List files in current directory"
echo -e "${CYAN}=========================================================${NC}"
echo

# Add remote control info
echo -e "${CYAN}================= REMOTE CONTROL =================${NC}"
echo -e "${YELLOW}To control God Mode from any directory:${NC}"
echo -e "  ${GREEN}./god_mode_remote.sh${NC}  - Run from parent directory"
echo -e "This allows you to start/stop/manage God Mode without changing your context."
echo -e "${CYAN}====================================================${NC}"
echo

# Open Cursor IDE if it's installed
if command -v cursor &> /dev/null; then
    echo
    echo -e "${CYAN}================= PROJECT WORKFLOW CHOICE =================${NC}"
    echo -e "${YELLOW}Would you like to open this project in Cursor IDE now?${NC}"
    echo -e "  ${GREEN}Y${NC} - Yes, open this project directly in Cursor IDE"
    echo -e "      (Choose this if you're working primarily in this project)"
    echo -e "  ${RED}N${NC} - No, I'll manage Cursor separately"
    echo -e "      (Choose this for multi-project workflows or if Cursor is already open)"
    echo -e "${CYAN}=========================================================${NC}"
    echo -ne "Your choice (y/n): "
    read -r answer
    if [[ "$answer" =~ ^[Yy]$ ]]; then
        cursor "$SCRIPT_DIR"
    else
        echo -e "${YELLOW}You can continue using God Mode in your existing workflow.${NC}"
        echo -e "${GREEN}Common next steps:${NC}"
        echo -e "1. To move up to parent directory:       ${CYAN}cd ..${NC}"
        echo -e "2. To control God Mode from parent dir:  ${CYAN}cd .. && ./god_mode_remote.sh${NC}"
        echo -e "3. To control God Mode from this dir:    ${CYAN}./god_mode_remote.sh${NC} (symlink available)"
        echo -e "4. To view quick-start guide:           ${CYAN}open README_QUICKSTART.md${NC}"
    fi
fi 