#!/bin/bash

# God Mode Shortcut Installer
# This script installs the 'god' command globally for easy access

# Set colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get the directory of this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
GOD_COMMAND="$SCRIPT_DIR/god"

# Check if 'god' command script exists
if [ ! -f "$GOD_COMMAND" ]; then
    echo -e "${RED}Error: The 'god' command script is missing.${NC}"
    echo -e "Expected location: $GOD_COMMAND"
    exit 1
fi

# Make sure the god command is executable
chmod +x "$GOD_COMMAND"

# Determine the user's shell
USER_SHELL="$(basename "$SHELL")"
SHELL_CONFIG=""

case "$USER_SHELL" in
    bash)
        SHELL_CONFIG="$HOME/.bashrc"
        if [[ "$OSTYPE" == "darwin"* ]]; then
            # macOS may use .bash_profile instead
            if [ -f "$HOME/.bash_profile" ]; then
                SHELL_CONFIG="$HOME/.bash_profile"
            fi
        fi
        ;;
    zsh)
        SHELL_CONFIG="$HOME/.zshrc"
        ;;
    *)
        echo -e "${YELLOW}Warning: Unsupported shell ($USER_SHELL).${NC}"
        echo -e "Please manually add an alias for the 'god' command to your shell configuration."
        echo -e "For example: alias god='$GOD_COMMAND'"
        exit 1
        ;;
esac

echo -e "${BLUE}=======================================${NC}"
echo -e "${BLUE}     God Mode Shortcut Installer      ${NC}"
echo -e "${BLUE}=======================================${NC}"
echo
echo -e "This will install the 'god' command for quick access to God Mode."
echo -e "Installation options:"
echo -e "1) ${GREEN}Create symlink in /usr/local/bin${NC} (requires sudo)"
echo -e "2) ${GREEN}Add alias to $SHELL_CONFIG${NC}"
echo -e "3) ${GREEN}Exit without installing${NC}"
echo
echo -n "Choose an option (1-3): "
read -r choice

case "$choice" in
    1)
        echo -e "\n${YELLOW}Creating symlink in /usr/local/bin...${NC}"
        sudo ln -sf "$GOD_COMMAND" /usr/local/bin/god
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}Successfully installed 'god' command!${NC}"
            echo -e "You can now use 'god' from any directory to access God Mode."
            echo -e "Try it: ${YELLOW}god help${NC}"
        else
            echo -e "${RED}Failed to create symlink. Do you have sudo permission?${NC}"
            exit 1
        fi
        ;;
    2)
        echo -e "\n${YELLOW}Adding alias to $SHELL_CONFIG...${NC}"
        
        # Check if the alias already exists
        if grep -q "alias god=" "$SHELL_CONFIG"; then
            echo -e "${YELLOW}Alias for 'god' already exists in $SHELL_CONFIG${NC}"
            echo -e "Do you want to update it? (y/n): "
            read -r update_alias
            if [[ "$update_alias" != "y" && "$update_alias" != "Y" ]]; then
                echo -e "${YELLOW}Skipping alias update.${NC}"
                exit 0
            fi
            # Remove existing alias
            sed -i.bak '/alias god=/d' "$SHELL_CONFIG"
        fi
        
        # Add the alias
        echo "" >> "$SHELL_CONFIG"
        echo "# God Mode shortcut" >> "$SHELL_CONFIG"
        echo "alias god='$GOD_COMMAND'" >> "$SHELL_CONFIG"
        
        echo -e "${GREEN}Successfully added 'god' alias to $SHELL_CONFIG!${NC}"
        echo -e "To use it in the current terminal, run: ${YELLOW}source $SHELL_CONFIG${NC}"
        echo -e "Or restart your terminal."
        echo -e "Then try: ${YELLOW}god help${NC}"
        ;;
    3|*)
        echo -e "\n${YELLOW}Exiting without installing the shortcut.${NC}"
        echo -e "You can still use God Mode through the full path:"
        echo -e "${YELLOW}$SCRIPT_DIR/god_mode_remote.sh${NC}"
        exit 0
        ;;
esac

echo
echo -e "${BLUE}Installation complete!${NC}"
echo -e "For help on using the 'god' command, type: ${YELLOW}god help${NC}" 