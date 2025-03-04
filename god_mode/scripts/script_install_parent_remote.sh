#!/bin/bash

# script_install_parent_remote.sh
# This script installs the God Mode remote control script in a parent directory.
# It allows controlling God Mode from the parent directory, without changing context.

# Set colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get the directory of this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
GOD_MODE_DIR="$(dirname "$SCRIPT_DIR")"
PROJECT_ROOT="$(dirname "$GOD_MODE_DIR")"
PROJECT_NAME="$(basename "$PROJECT_ROOT")"

# Determine the parent directory
PARENT_DIR="$(dirname "$PROJECT_ROOT")"

echo -e "${BLUE}=======================================${NC}"
echo -e "${BLUE}  God Mode Parent Remote Installation  ${NC}"
echo -e "${BLUE}=======================================${NC}"
echo

# Confirm with the user
echo -e "This will install a God Mode remote control script in the parent directory:"
echo -e "  Parent directory: ${GREEN}$PARENT_DIR${NC}"
echo -e "  Project directory: ${GREEN}$PROJECT_ROOT${NC}"
echo -e "  Project name: ${GREEN}$PROJECT_NAME${NC}"
echo
echo -e "The remote script will allow you to control God Mode in $PROJECT_NAME"
echo -e "from the parent directory, without changing your Cursor IDE context."
echo
echo -n "Do you want to proceed? (y/n): "
read -r answer

if [[ ! "$answer" =~ ^[Yy]$ ]]; then
    echo -e "${RED}Installation aborted.${NC}"
    exit 0
fi

echo
echo -e "${YELLOW}Installing God Mode remote control script...${NC}"

# Check if the template file exists
TEMPLATE_FILE="$GOD_MODE_DIR/templates/template_parent_remote_script.sh"
if [ ! -f "$TEMPLATE_FILE" ]; then
    echo -e "${RED}Error: Template file not found at $TEMPLATE_FILE${NC}"
    exit 1
fi

# Copy the template to the parent directory
REMOTE_SCRIPT="$PARENT_DIR/god_mode_remote.sh"
cp "$TEMPLATE_FILE" "$REMOTE_SCRIPT"

# Make it executable
chmod +x "$REMOTE_SCRIPT"

echo -e "${GREEN}Installation complete!${NC}"
echo
echo -e "You can now control God Mode from the parent directory using:"
echo -e "  ${YELLOW}$PARENT_DIR/god_mode_remote.sh${NC}"
echo
echo -e "This script will automatically target the $PROJECT_NAME project."
echo -e "You can also specify a different project by running:"
echo -e "  ${YELLOW}$PARENT_DIR/god_mode_remote.sh other_project_with_god_mode${NC}"
echo
echo -e "Enjoy using God Mode with your multi-project workflow!" 