#!/bin/bash

# god_mode_remote_fixed.sh
# This is a fixed version of the God Mode remote script with improved error handling
# and more robust path resolution to help diagnose and fix issues

# Set colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Get the directory of this script (should be the God Mode project)
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Log file for this script
LOG_DIR="$SCRIPT_DIR/god_mode/logs"
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/remote_control.log"

# Function to log messages
log_message() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
  echo -e "$1"
}

# Function to check if a directory exists
check_directory() {
  if [ ! -d "$1" ]; then
    log_message "${RED}Error: Directory not found: $1${NC}"
    return 1
  fi
  return 0
}

# Check if the god_mode directory exists
if ! check_directory "$SCRIPT_DIR/god_mode"; then
  log_message "${RED}Error: God Mode not found in this directory. Make sure you're running this from the correct location.${NC}"
  log_message "${YELLOW}Current directory: $SCRIPT_DIR${NC}"
  exit 1
fi

# Check if scripts directory exists
SCRIPTS_DIR="$SCRIPT_DIR/god_mode/scripts"
if ! check_directory "$SCRIPTS_DIR"; then
  log_message "${RED}Error: Scripts directory not found: $SCRIPTS_DIR${NC}"
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

# Function to display the menu
show_menu() {
  # Display current status in header
  check_god_mode_status_header
  echo

  echo -e "${YELLOW}What would you like to do?${NC}"
  echo -e "1) ${CYAN}Start God Mode${NC} - Turn on AI assistant superpowers"
  echo -e "2) ${CYAN}Stop God Mode${NC} - Turn off AI assistant background processes"
  echo -e "3) ${CYAN}View God Mode status${NC} - Check if everything is working correctly"
  echo -e "4) ${CYAN}Route clipboard content${NC} - Process text with [TAG] markers from clipboard"
  echo -e "5) ${CYAN}View recent logs${NC} - See the latest activity and changes"
  echo -e "6) ${CYAN}Update project structure${NC} - Refresh AI's understanding of your code"
  echo -e "7) ${CYAN}Update Cursor rules${NC} - Refresh the AI assistant's instructions"
  echo -e "8) ${CYAN}Install dependencies${NC} - Install required Python packages for God Mode"
  echo -e "9) ${CYAN}Run diagnostic mode${NC} - In-depth troubleshooting for God Mode"
  echo -e "d) ${CYAN}View documentation${NC} - Read guides on using God Mode and tags"
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
  echo -e "${CYAN}9) Run diagnostic mode${NC}"
  echo -e "   Provides detailed troubleshooting information for God Mode."
  echo -e "   Useful if you're having issues with the Message Router or other components."
  echo -e "   This will create a comprehensive diagnostic log file."
  echo
  echo -e "${CYAN}Troubleshooting Tips:${NC}"
  echo -e "• If Message Router shows NOT RUNNING, make sure python packages are installed:"
  echo -e "  Run option 8 (Install dependencies) or run this command:"
  echo -e "  ${GREEN}$SCRIPTS_DIR/script_install_dependencies.sh${NC}"
  echo -e "• If the AI isn't adding [TAG] markers, try updating Cursor rules (option 7)"
  echo -e "• If desktop notifications aren't working, run option 8 to install the plyer package"
  echo -e "• If having persistent issues, run option 9 (Diagnostic mode) to generate detailed logs"
  echo
  echo -e "${CYAN}Documentation:${NC}"
  echo -e "• Tag System Guide: ${GREEN}$SCRIPT_DIR/god_mode/system_documentation/README_TAGS.md${NC}"
  echo -e "  This guide explains all available tags and how to use them effectively."
  echo -e "  To open it: ${YELLOW}open \"$SCRIPT_DIR/god_mode/system_documentation/README_TAGS.md\"${NC}"
  echo
  echo -e "Press Enter to return to the main menu..."
  read -r
}

# Function to start God Mode
start_god_mode() {
  log_message "${YELLOW}Starting God Mode...${NC}"
  
  # Execute the start script in the target directory
  if [ -f "$SCRIPT_DIR/start_god_mode.sh" ]; then
    # Make it executable if it's not
    chmod +x "$SCRIPT_DIR/start_god_mode.sh"
    
    # Run it
    "$SCRIPT_DIR/start_god_mode.sh"
    
    # Additional check to see if processes are running
    echo
    log_message "${YELLOW}Verifying God Mode processes...${NC}"
    sleep 2  # Give processes time to start
    
    if is_process_running "route --watch"; then
      log_message "Message Router: ${GREEN}RUNNING${NC} ✓"
    else
      log_message "Message Router: ${RED}NOT RUNNING${NC} ✗"
      log_message "${YELLOW}Troubleshooting tip: Run option 8 to install dependencies${NC}"
      log_message "${YELLOW}Command: $SCRIPTS_DIR/script_install_dependencies.sh${NC}"
      
      # Check if the route script exists
      if [ ! -f "$SCRIPTS_DIR/route" ]; then
        log_message "${RED}Error: The 'route' script is missing.${NC}"
        log_message "${YELLOW}This might be why the Message Router isn't starting.${NC}"
        log_message "${YELLOW}Please run option 9 (Diagnostic mode) to diagnose the issue.${NC}"
      fi
    fi
    
    if is_process_running "script_cursor_watch.py"; then
      log_message "Cursor Watch: ${GREEN}RUNNING${NC} ✓"
    else
      log_message "Cursor Watch: ${RED}NOT RUNNING${NC} ✗"
    fi
  else
    log_message "${RED}Error: start_god_mode.sh not found in $SCRIPT_DIR${NC}"
  fi
}

# Function to stop God Mode
stop_god_mode() {
  log_message "${YELLOW}Stopping God Mode processes...${NC}"
  
  # Kill the message router and cursor watch processes
  pkill -f 'route --watch'
  pkill -f 'script_cursor_watch.py'
  
  log_message "${GREEN}God Mode processes stopped.${NC}"
}

# Function to view God Mode status
view_status() {
  log_message "${YELLOW}Checking God Mode status...${NC}"
  
  local router_running=false
  local watch_running=false
  
  if is_process_running "route --watch"; then
    router_running=true
    local router_pid=$(pgrep -f 'route --watch')
    log_message "Message Router: ${GREEN}RUNNING${NC} ✓ (PID: $router_pid)"
    log_message "   This process handles text with [TAG] markers like [LOG_SUMMARY]"
  else
    log_message "Message Router: ${RED}NOT RUNNING${NC} ✗"
    log_message "   ${YELLOW}Not working? Try running option 8 (Install dependencies)${NC}"
    log_message "   This process is needed to handle [TAG] markers in text"
  fi
  
  if is_process_running "script_cursor_watch.py"; then
    watch_running=true
    local watch_pid=$(pgrep -f 'script_cursor_watch.py')
    log_message "Cursor Watch: ${GREEN}RUNNING${NC} ✓ (PID: $watch_pid)"
    log_message "   This process enhances AI prompts with context from your project"
  else
    log_message "Cursor Watch: ${RED}NOT RUNNING${NC} ✗"
    log_message "   This process enhances AI responses with project context"
  fi
  
  if $router_running && $watch_running; then
    log_message "\n${GREEN}God Mode is fully active.${NC} ✓"
    log_message "You can now use all God Mode features!"
  elif $router_running || $watch_running; then
    log_message "\n${YELLOW}God Mode is partially active.${NC} ⚠️"
    log_message "Some features may not work correctly. Try restarting God Mode."
  else
    log_message "\n${RED}God Mode is not active.${NC} ✗"
    log_message "Use option 1 to start God Mode."
  fi
}

# Function to route clipboard content
route_clipboard() {
  log_message "${YELLOW}Routing clipboard content to God Mode...${NC}"
  
  local route_script="$SCRIPTS_DIR/route"
  
  if [ -f "$route_script" ]; then
    # Make it executable if it's not
    chmod +x "$route_script"
    
    # Run it with the clipboard option
    "$route_script" --clipboard
    
    log_message "\n${GREEN}Tip:${NC} If you don't see desktop notifications, the content may not have any [TAG] markers."
    log_message "Tags include: [LOG_SUMMARY], [LOG_DETAIL], [MEMORY_UPDATE], [FEATURE_LOG: Name], etc."
    log_message "You can also use [MULTI_TAG: TAG1, TAG2, ...] to route content to multiple destinations."
  else
    log_message "${RED}Error: route script not found at $route_script${NC}"
    log_message "${YELLOW}Try running option 9 (Diagnostic mode) to diagnose the issue.${NC}"
  fi
}

# Function to view recent logs
view_logs() {
  local logs_dir="$LOG_DIR"
  
  if [ ! -d "$logs_dir" ]; then
    log_message "${RED}Error: Logs directory not found at $logs_dir${NC}"
    log_message "Creating logs directory..."
    mkdir -p "$logs_dir"
    log_message "${GREEN}Created logs directory at $logs_dir${NC}"
    return
  fi
  
  log_message "${YELLOW}Recent God Mode activity:${NC}"
  
  local found_logs=false
  
  # Check for log files and display the most recent entries
  if [ -f "$logs_dir/message_router.log" ]; then
    log_message "\n${GREEN}Message Router Log (last 10 entries):${NC}"
    tail -n 10 "$logs_dir/message_router.log"
    found_logs=true
  fi
  
  if [ -f "$logs_dir/cursor_watch.log" ]; then
    log_message "\n${GREEN}Cursor Watch Log (last 10 entries):${NC}"
    tail -n 10 "$logs_dir/cursor_watch.log"
    found_logs=true
  fi
  
  if [ -f "$SCRIPT_DIR/god_mode/memory/memory_logs_all.md" ]; then
    log_message "\n${GREEN}Recent Memory Logs (last 10 entries):${NC}"
    tail -n 20 "$SCRIPT_DIR/god_mode/memory/memory_logs_all.md"
    found_logs=true
  fi
  
  if [ -f "$logs_dir/debug_router.log" ]; then
    log_message "\n${GREEN}Debug Log (last 10 entries):${NC}"
    tail -n 10 "$logs_dir/debug_router.log"
    found_logs=true
  fi
  
  if [ "$found_logs" = false ]; then
    log_message "${YELLOW}No log files found yet. Try using God Mode first to generate logs.${NC}"
  fi
}

# Function to update project structure
update_project_structure() {
  log_message "${YELLOW}Updating project structure...${NC}"
  
  local script="$SCRIPTS_DIR/script_update_project_structure.py"
  
  if [ -f "$script" ]; then
    (cd "$SCRIPT_DIR" && python "$script")
    log_message "${GREEN}Project structure updated.${NC}"
    log_message "The AI assistant now has an updated map of your project files and folders."
  else
    log_message "${RED}Error: Update script not found at $script${NC}"
  fi
}

# Function to update Cursor rules
update_cursor_rules() {
  log_message "${YELLOW}Updating Cursor rules...${NC}"
  
  local script="$SCRIPTS_DIR/script_update_cursor_rules.py"
  
  if [ -f "$script" ]; then
    (cd "$SCRIPT_DIR" && python "$script" --force)
    log_message "${GREEN}Cursor rules updated.${NC}"
    log_message "The AI assistant's instructions have been refreshed."
    log_message "This should help with automatic [TAG] markers in AI responses."
  else
    log_message "${RED}Error: Update script not found at $script${NC}"
  fi
}

# Function to install dependencies
install_dependencies() {
  log_message "${BLUE}=======================================${NC}"
  log_message "${BLUE}     Installing God Mode Dependencies  ${NC}"
  log_message "${BLUE}=======================================${NC}"
  log_message ""
  
  local script="$SCRIPTS_DIR/script_install_dependencies.sh"
  
  if [ -f "$script" ]; then
    # Make it executable if it's not
    chmod +x "$script"
    
    # Run it
    log_message "${YELLOW}Running dependency installer...${NC}"
    "$script"
    
    if [ $? -eq 0 ]; then
      log_message "\n${GREEN}✓ Dependencies installed successfully${NC}"
      log_message "${YELLOW}You should now be able to start God Mode with option 1${NC}"
    else
      log_message "\n${RED}✗ There was a problem installing dependencies${NC}"
      log_message "${YELLOW}Try running the script manually:${NC}"
      log_message "  cd \"$SCRIPTS_DIR\" && ./script_install_dependencies.sh"
    fi
  else
    log_message "${RED}Error: Dependency installer script not found at:${NC}"
    log_message "$script"
    log_message ""
    log_message "${YELLOW}Try installing dependencies manually:${NC}"
    log_message "  pip install pyperclip plyer"
  fi
}

# Function to run diagnostic mode
run_diagnostic_mode() {
  log_message "${BLUE}=======================================${NC}"
  log_message "${BLUE}     Running God Mode Diagnostics      ${NC}"
  log_message "${BLUE}=======================================${NC}"
  log_message ""
  
  # Ensure the debug script exists
  local debug_script="$SCRIPTS_DIR/script_debug_router.py"
  
  if [ ! -f "$debug_script" ]; then
    log_message "${RED}Error: Debug script not found at: $debug_script${NC}"
    log_message "${YELLOW}Creating a basic diagnostic report instead...${NC}"
    
    # Create a basic diagnostic report
    local diag_report="$LOG_DIR/diagnostic_report.log"
    
    echo "=================================" > "$diag_report"
    echo "     God Mode Diagnostic Report     " >> "$diag_report"
    echo "=================================" >> "$diag_report"
    echo "" >> "$diag_report"
    echo "Generated: $(date)" >> "$diag_report"
    echo "" >> "$diag_report"
    
    echo "SYSTEM INFORMATION:" >> "$diag_report"
    echo "OS: $(uname -a)" >> "$diag_report"
    echo "Python: $(which python || which python3)" >> "$diag_report"
    if command -v python3 &>/dev/null; then
      echo "Python version: $(python3 --version 2>&1)" >> "$diag_report"
    elif command -v python &>/dev/null; then
      echo "Python version: $(python --version 2>&1)" >> "$diag_report"
    else
      echo "Python not found" >> "$diag_report"
    fi
    echo "" >> "$diag_report"
    
    echo "DIRECTORY CHECK:" >> "$diag_report"
    echo "Script directory: $SCRIPT_DIR" >> "$diag_report"
    echo "Scripts directory: $SCRIPTS_DIR" >> "$diag_report"
    echo "Log directory: $LOG_DIR" >> "$diag_report"
    echo "" >> "$diag_report"
    
    echo "FILES CHECK:" >> "$diag_report"
    echo "Route script: $([ -f "$SCRIPTS_DIR/route" ] && echo "✓ Exists" || echo "✗ Missing")" >> "$diag_report"
    echo "Message router: $([ -f "$SCRIPTS_DIR/script_message_router.py" ] && echo "✓ Exists" || echo "✗ Missing")" >> "$diag_report"
    echo "Cursor watch: $([ -f "$SCRIPTS_DIR/script_cursor_watch.py" ] && echo "✓ Exists" || echo "✗ Missing")" >> "$diag_report"
    echo "Dependencies installer: $([ -f "$SCRIPTS_DIR/script_install_dependencies.sh" ] && echo "✓ Exists" || echo "✗ Missing")" >> "$diag_report"
    echo "" >> "$diag_report"
    
    echo "PROCESS STATUS:" >> "$diag_report"
    echo "Message Router: $(pgrep -f 'route --watch' > /dev/null && echo "✓ Running" || echo "✗ Not running")" >> "$diag_report"
    echo "Cursor Watch: $(pgrep -f 'script_cursor_watch.py' > /dev/null && echo "✓ Running" || echo "✗ Not running")" >> "$diag_report"
    echo "" >> "$diag_report"
    
    log_message "${GREEN}Basic diagnostic report created at:${NC} $diag_report"
    log_message "${YELLOW}Please check this file for information about your God Mode setup.${NC}"
    return
  fi
  
  # Make the script executable
  chmod +x "$debug_script"
  
  # Run the diagnostic script
  log_message "${YELLOW}Running comprehensive diagnostics...${NC}"
  (cd "$SCRIPTS_DIR" && python "$debug_script")
  
  # Check if the diagnostic log was created
  local debug_log="$LOG_DIR/debug_router.log"
  if [ -f "$debug_log" ]; then
    log_message "${GREEN}Diagnostics complete!${NC}"
    log_message "${YELLOW}Detailed diagnostic log created at:${NC} $debug_log"
    log_message "${YELLOW}Please check this file for comprehensive information about any issues.${NC}"
  else
    log_message "${RED}Error: Diagnostic log was not created.${NC}"
    log_message "${YELLOW}The diagnostic script may have encountered an error.${NC}"
  fi
}

# Function to view readme files
view_readme() {
  log_message "${YELLOW}Available Documentation:${NC}"
  log_message "1) Tag System Guide - Learn how to use [TAG] markers"
  log_message "2) God Mode Overview - Understand how God Mode works"
  log_message "3) Back to main menu"
  echo
  echo -n "Which document would you like to view? "
  read -r doc_choice
  
  case "$doc_choice" in
    1)
      local readme_path="$SCRIPT_DIR/god_mode/system_documentation/README_TAGS.md"
      if [ -f "$readme_path" ]; then
        # Try to open with the default application first
        open "$readme_path" 2>/dev/null || {
          # If that fails, show content in terminal
          log_message "\n${GREEN}=== TAG SYSTEM GUIDE ===${NC}\n"
          cat "$readme_path"
          echo
        }
      else
        log_message "${RED}Error: Tag guide not found at $readme_path${NC}"
      fi
      ;;
    2)
      local readme_path="$SCRIPT_DIR/README.md"
      if [ -f "$readme_path" ]; then
        # Try to open with the default application first
        open "$readme_path" 2>/dev/null || {
          # If that fails, show content in terminal
          log_message "\n${GREEN}=== GOD MODE OVERVIEW ===${NC}\n"
          cat "$readme_path"
          echo
        }
      else
        log_message "${RED}Error: Overview not found at $readme_path${NC}"
      fi
      ;;
    3|*)
      # Just return to main menu
      return
      ;;
  esac
}

# Create a parent directory symlink for the remote script
create_parent_symlink() {
  local parent_dir="$(dirname "$SCRIPT_DIR")"
  local parent_remote="$parent_dir/god_mode_remote.sh"
  
  if [ ! -f "$parent_remote" ] && [ ! -L "$parent_remote" ]; then
    log_message "${YELLOW}Creating symlink in parent directory for easier access...${NC}"
    ln -s "$SCRIPT_DIR/god_mode_remote_fixed.sh" "$parent_remote" 2>/dev/null
    
    if [ $? -eq 0 ]; then
      log_message "${GREEN}✓ Created symlink at: $parent_remote${NC}"
      log_message "${YELLOW}You can now run './god_mode_remote.sh' from $parent_dir${NC}"
    else
      log_message "${RED}Failed to create symlink in parent directory${NC}"
    fi
  fi
}

# Main logic
log_message "${BLUE}=======================================${NC}"
log_message "${BLUE}       God Mode Remote Control        ${NC}"
log_message "${BLUE}      (Fixed Diagnostic Version)      ${NC}"
log_message "${BLUE}=======================================${NC}"
log_message ""
log_message "${YELLOW}Working directory: $SCRIPT_DIR${NC}"

# Try to create parent symlink
create_parent_symlink

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
    6) update_project_structure ;;
    7) update_cursor_rules ;;
    8) install_dependencies ;;
    9) run_diagnostic_mode ;;
    d|D) view_readme ;;
    h|H) show_help ;;
    q|Q) log_message "${GREEN}Goodbye!${NC}"; exit 0 ;;
    *) log_message "${RED}Invalid choice. Please try again.${NC}" ;;
  esac
  
  # Pause to let the user read the output
  echo
  echo -n "Press Enter to continue..."
  read -r
done 