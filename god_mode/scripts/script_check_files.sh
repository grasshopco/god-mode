#!/bin/bash

# script_check_files.sh
# This script checks for essential files and creates any that are missing

# Set colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get the scripts directory (where this script is located)
SCRIPTS_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Get the god_mode directory (parent of scripts)
GOD_MODE_DIR="$(dirname "$SCRIPTS_DIR")"

# Get the project root directory (parent of god_mode)
PROJECT_ROOT="$(dirname "$GOD_MODE_DIR")"

echo -e "${BLUE}=======================================${NC}"
echo -e "${BLUE}     God Mode File Integrity Check     ${NC}"
echo -e "${BLUE}=======================================${NC}"
echo

# Check if a file exists
check_file() {
    if [ ! -f "$1" ]; then
        echo -e "${RED}✗ Missing: $1${NC}"
        return 1
    else
        echo -e "${GREEN}✓ Found: $1${NC}"
        return 0
    fi
}

# Create route script if it's missing
create_route_script() {
    local route_script="$SCRIPTS_DIR/route"
    if [ ! -f "$route_script" ]; then
        echo -e "${YELLOW}Creating missing route script...${NC}"
        cat > "$route_script" << 'EOF'
#!/bin/bash

# route - Wrapper script for the Message Router
# This script provides a simple interface to the message router functionality

# Set colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get the script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Ensure log directory exists
LOG_DIR="$SCRIPT_DIR/../logs"
mkdir -p "$LOG_DIR"

# Log file for this script
LOG_FILE="$LOG_DIR/route_wrapper.log"

# Function to log messages
log_message() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
  echo -e "$1"
}

# Function to check if a Python module is installed
check_python_module() {
  python3 -c "import $1" 2>/dev/null || python -c "import $1" 2>/dev/null
  return $?
}

# Function to try multiple Python interpreters
run_with_python() {
  # Try python3 first, then python as fallback
  if command -v python3 &>/dev/null; then
    log_message "${YELLOW}Running with python3...${NC}"
    python3 "$@"
    return $?
  elif command -v python &>/dev/null; then
    log_message "${YELLOW}Running with python...${NC}"
    python "$@"
    return $?
  else
    log_message "${RED}Error: No Python interpreter found${NC}"
    return 1
  fi
}

# Check for the message router script
MESSAGE_ROUTER="$SCRIPT_DIR/script_message_router.py"
if [ ! -f "$MESSAGE_ROUTER" ]; then
  log_message "${RED}Error: Message router script not found at $MESSAGE_ROUTER${NC}"
  exit 1
fi

# Check for required Python modules
check_dependencies() {
  log_message "${BLUE}Checking dependencies...${NC}"
  
  missing_deps=()
  
  if ! check_python_module "pyperclip"; then
    missing_deps+=("pyperclip")
  else
    log_message "${GREEN}✓ pyperclip is installed${NC}"
  fi
  
  if ! check_python_module "plyer"; then
    missing_deps+=("plyer")
  else
    log_message "${GREEN}✓ plyer is installed${NC}"
  fi
  
  if [ ${#missing_deps[@]} -gt 0 ]; then
    log_message "${RED}Missing dependencies: ${missing_deps[*]}${NC}"
    log_message "${YELLOW}Install them with: pip install ${missing_deps[*]}${NC}"
    log_message "${YELLOW}Or run: $SCRIPT_DIR/script_install_dependencies.sh${NC}"
    
    # Check if dependency installer exists and offer to run it
    if [ -f "$SCRIPT_DIR/script_install_dependencies.sh" ]; then
      read -p "Would you like to run the dependency installer now? (y/n) " -n 1 -r
      echo
      if [[ $REPLY =~ ^[Yy]$ ]]; then
        chmod +x "$SCRIPT_DIR/script_install_dependencies.sh"
        "$SCRIPT_DIR/script_install_dependencies.sh"
        # Check if installation was successful
        if ! check_python_module "pyperclip" || ! check_python_module "plyer"; then
          log_message "${RED}Some dependencies are still missing. Please install them manually.${NC}"
          exit 1
        fi
      else
        exit 1
      fi
    else
      exit 1
    fi
  fi
  
  log_message "${GREEN}All dependencies are installed${NC}"
}

# Parse command line arguments
case "$1" in
  --input)
    if [ -z "$2" ]; then
      log_message "${RED}Error: Input file not specified${NC}"
      echo "Usage: $0 --input <file>"
      exit 1
    fi
    
    check_dependencies
    log_message "${BLUE}Reading from file: $2${NC}"
    run_with_python "$MESSAGE_ROUTER" --input "$2" --debug
    exit $?
    ;;
    
  --clipboard)
    check_dependencies
    log_message "${BLUE}Reading from clipboard...${NC}"
    run_with_python "$MESSAGE_ROUTER" --clipboard --debug
    exit $?
    ;;
    
  --watch)
    check_dependencies
    log_message "${BLUE}Starting clipboard watch mode...${NC}"
    INTERVAL="2.0"
    if [ -n "$2" ] && [[ "$2" =~ ^[0-9]+(\.[0-9]+)?$ ]]; then
      INTERVAL="$2"
    fi
    
    # Run in background if requested
    if [ "$3" == "--background" ]; then
      log_message "${YELLOW}Running in background mode${NC}"
      run_with_python "$MESSAGE_ROUTER" --watch --interval "$INTERVAL" --debug > "$LOG_DIR/message_router.log" 2>&1 &
      PID=$!
      echo $PID > "$LOG_DIR/message_router.pid"
      log_message "${GREEN}Message router started with PID $PID${NC}"
      log_message "${YELLOW}View logs at: $LOG_DIR/message_router.log${NC}"
    else
      # Run in foreground
      run_with_python "$MESSAGE_ROUTER" --watch --interval "$INTERVAL" --debug
    fi
    exit $?
    ;;
    
  --debug)
    # Run the debug script if it exists
    DEBUG_SCRIPT="$SCRIPT_DIR/script_debug_router.py"
    if [ -f "$DEBUG_SCRIPT" ]; then
      log_message "${BLUE}Running diagnostic mode...${NC}"
      run_with_python "$DEBUG_SCRIPT"
      log_message "${YELLOW}Debug logs saved to: $LOG_DIR/debug_router.log${NC}"
    else
      log_message "${RED}Debug script not found at $DEBUG_SCRIPT${NC}"
      log_message "${BLUE}Running message router in debug mode instead...${NC}"
      run_with_python "$MESSAGE_ROUTER" --watch --debug
    fi
    exit $?
    ;;
    
  --help|-h)
    echo "Usage: $0 [OPTIONS]"
    echo
    echo "Options:"
    echo "  --input <file>   Read and process content from a file"
    echo "  --clipboard      Read and process content from clipboard"
    echo "  --watch [interval] [--background]"
    echo "                   Watch clipboard for changes (default interval: 2.0s)"
    echo "  --debug          Run in diagnostic mode with extensive logging"
    echo "  --help, -h       Show this help message"
    echo
    echo "Examples:"
    echo "  $0 --watch                 # Watch clipboard with 2s interval"
    echo "  $0 --watch 5.0             # Watch clipboard with 5s interval"
    echo "  $0 --watch 2.0 --background # Run in background mode"
    exit 0
    ;;
    
  *)
    echo "Usage: $0 [--input <file>|--clipboard|--watch|--debug|--help]"
    echo "Run '$0 --help' for more information"
    exit 1
    ;;
esac
EOF
        chmod +x "$route_script"
        echo -e "${GREEN}✓ Created route script at: $route_script${NC}"
    fi
}

# Create a symlink to the remote script if needed
create_remote_symlink() {
    local parent_dir="$(dirname "$PROJECT_ROOT")"
    local remote_script="$parent_dir/god_mode_remote.sh"
    
    if [ ! -f "$remote_script" ] && [ ! -L "$remote_script" ]; then
        echo -e "${YELLOW}Creating symlink to remote script in parent directory...${NC}"
        ln -s "$PROJECT_ROOT/god_mode_remote.sh" "$remote_script" 2>/dev/null
        
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}✓ Created symlink at: $remote_script${NC}"
        else
            echo -e "${RED}✗ Failed to create symlink${NC}"
        fi
    else
        echo -e "${GREEN}✓ Remote script symlink exists: $remote_script${NC}"
    fi
}

# Main function to check all files
check_all_files() {
    # Check critical files
    echo -e "Checking critical files..."
    check_file "$SCRIPTS_DIR/script_message_router.py" || echo -e "${RED}⚠️ Message router script is missing! This is a serious issue.${NC}"
    check_file "$SCRIPTS_DIR/route" || create_route_script
    check_file "$SCRIPTS_DIR/script_debug_router.py" || echo -e "${YELLOW}Debug script is missing, but not critical.${NC}"
    check_file "$SCRIPTS_DIR/script_install_dependencies.sh" || echo -e "${YELLOW}Dependencies installer is missing, but not critical.${NC}"
    check_file "$PROJECT_ROOT/god_mode_remote.sh" || echo -e "${RED}Remote script is missing!${NC}"
    
    # Create required directories
    echo -e "\nChecking required directories..."
    if [ ! -d "$GOD_MODE_DIR/logs" ]; then
        echo -e "${YELLOW}Creating logs directory...${NC}"
        mkdir -p "$GOD_MODE_DIR/logs"
        echo -e "${GREEN}✓ Created logs directory at: $GOD_MODE_DIR/logs${NC}"
    else
        echo -e "${GREEN}✓ Found logs directory: $GOD_MODE_DIR/logs${NC}"
    fi
    
    if [ ! -d "$GOD_MODE_DIR/memory" ]; then
        echo -e "${YELLOW}Creating memory directory...${NC}"
        mkdir -p "$GOD_MODE_DIR/memory"
        echo -e "${GREEN}✓ Created memory directory at: $GOD_MODE_DIR/memory${NC}"
    else
        echo -e "${GREEN}✓ Found memory directory: $GOD_MODE_DIR/memory${NC}"
    fi
    
    if [ ! -d "$GOD_MODE_DIR/system_documentation" ]; then
        echo -e "${YELLOW}Creating system_documentation directory...${NC}"
        mkdir -p "$GOD_MODE_DIR/system_documentation"
        echo -e "${GREEN}✓ Created system_documentation directory at: $GOD_MODE_DIR/system_documentation${NC}"
    else
        echo -e "${GREEN}✓ Found system_documentation directory: $GOD_MODE_DIR/system_documentation${NC}"
    fi
    
    # Check symlinks
    echo -e "\nChecking symlinks..."
    create_remote_symlink
    
    # Make all scripts executable
    echo -e "\nMaking all scripts executable..."
    chmod +x "$SCRIPTS_DIR"/*.py "$SCRIPTS_DIR"/*.sh "$PROJECT_ROOT"/*.sh 2>/dev/null
    echo -e "${GREEN}✓ Made scripts executable${NC}"
    
    echo
    echo -e "${GREEN}File integrity check complete!${NC}"
}

# Run the main function
check_all_files 