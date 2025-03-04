#!/bin/bash

# God Mode Shortcut Installer
# This script installs the 'godmode' command globally for easy access

# Set colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Get the directory of this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
GODMODE_COMMAND="$SCRIPT_DIR/godmode"

# Check if 'godmode' command script exists
if [ ! -f "$GODMODE_COMMAND" ]; then
    echo -e "${RED}Error: The 'godmode' command script is missing.${NC}"
    echo -e "Expected location: $GODMODE_COMMAND"
    exit 1
fi

# Make sure the godmode command is executable
chmod +x "$GODMODE_COMMAND"

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
        echo -e "Please manually add an alias for the 'godmode' command to your shell configuration."
        echo -e "For example: alias godmode='$GODMODE_COMMAND'"
        exit 1
        ;;
esac

echo -e "${BLUE}=======================================${NC}"
echo -e "${BLUE}     God Mode Shortcut Installer      ${NC}"
echo -e "${BLUE}=======================================${NC}"
echo
echo -e "This will install the ${CYAN}'godmode'${NC} command for quick access to God Mode."
echo
echo -e "${YELLOW}What is this?${NC}"
echo -e "Instead of typing the full path to access God Mode, you'll be able to"
echo -e "simply type ${CYAN}godmode${NC} from any directory, like: ${CYAN}godmode help${NC} or ${CYAN}godmode c${NC}"
echo
echo -e "${YELLOW}WHICH OPTION SHOULD I CHOOSE?${NC}"
echo -e "Option 2 is STRONGLY RECOMMENDED for most users (especially beginners):"
echo
echo -e "1) FOR ADVANCED USERS ONLY: Create system-wide command"
echo -e "   This adds the command for all users on this computer"
echo -e "   Requires admin password and sudo permissions"
echo
echo -e "2) ${GREEN}★★★ RECOMMENDED CHOICE ★★★${NC}"
echo -e "   Add to your personal profile - easier, safer, and no password needed"
echo -e "   ${GREEN}✓ No admin password required${NC}"
echo -e "   ${GREEN}✓ Works immediately after running 'source $SHELL_CONFIG'${NC}"
echo -e "   ${GREEN}✓ Affects only your user account${NC}"
echo
echo -e "3) Exit without installing"
echo
echo -n "Choose an option (1-3): "
read -r choice

case "$choice" in
    1)
        echo -e "\n${YELLOW}Creating system-wide command...${NC}"
        sudo ln -sf "$GODMODE_COMMAND" /usr/local/bin/godmode
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}Successfully installed 'godmode' command!${NC}"
            echo -e "You can now use ${CYAN}godmode${NC} from any directory to access God Mode."
            echo -e "Try it: ${YELLOW}godmode help${NC}"
        else
            echo -e "${RED}Failed to create system command. Do you have sudo permission?${NC}"
            exit 1
        fi
        ;;
    2)
        echo -e "\n${YELLOW}Adding to your profile at $SHELL_CONFIG...${NC}"
        
        # Check if the alias already exists
        if grep -q "alias godmode=" "$SHELL_CONFIG"; then
            echo -e "${YELLOW}Command 'godmode' already exists in your profile${NC}"
            echo -e "Do you want to update it? (y/n): "
            read -r update_alias
            if [[ "$update_alias" != "y" && "$update_alias" != "Y" ]]; then
                echo -e "${YELLOW}Skipping update.${NC}"
                exit 0
            fi
            # Remove existing alias
            sed -i.bak '/alias godmode=/d' "$SHELL_CONFIG"
        fi
        
        # Add the alias
        echo "" >> "$SHELL_CONFIG"
        echo "# God Mode shortcut" >> "$SHELL_CONFIG"
        echo "alias godmode='$GODMODE_COMMAND'" >> "$SHELL_CONFIG"
        
        echo -e "${GREEN}Successfully added 'godmode' command to your profile!${NC}"
        echo -e "To use it in this terminal window, run: ${YELLOW}source $SHELL_CONFIG${NC}"
        echo -e "Or simply restart your terminal."
        echo -e "Then try: ${CYAN}godmode help${NC}"
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
echo
echo -e "${YELLOW}Quick commands you can try:${NC}"
echo -e "${CYAN}godmode help${NC}   - Show all available commands"
echo -e "${CYAN}godmode c${NC}      - Continue conversation with AI"
echo -e "${CYAN}godmode r${NC}      - Route clipboard content to memory files"
echo -e "${CYAN}godmode customize zeus${NC} - Create a custom 'zeus' command instead of 'godmode'" 