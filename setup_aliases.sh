#!/bin/bash

# setup_aliases.sh
# Sets up simple aliases for godmode commands

# Set colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get the directory of this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Determine which shell the user is using
SHELL_TYPE=$(basename "$SHELL")

# Set the appropriate profile file
if [ "$SHELL_TYPE" = "bash" ]; then
    PROFILE_FILE="$HOME/.bashrc"
elif [ "$SHELL_TYPE" = "zsh" ]; then
    PROFILE_FILE="$HOME/.zshrc"
else
    echo -e "${RED}Unsupported shell: $SHELL_TYPE${NC}"
    echo -e "Please manually add the aliases to your shell profile."
    exit 1
fi

echo -e "${BLUE}Setting up godmode aliases in $PROFILE_FILE...${NC}"

# Check if aliases already exist
if grep -q "alias gm=" "$PROFILE_FILE"; then
    echo -e "${YELLOW}gm alias already exists, updating...${NC}"
    sed -i '' '/alias gm=/d' "$PROFILE_FILE" 2>/dev/null || sed -i '/alias gm=/d' "$PROFILE_FILE"
fi

if grep -q "alias gmp=" "$PROFILE_FILE"; then
    echo -e "${YELLOW}gmp alias already exists, updating...${NC}"
    sed -i '' '/alias gmp=/d' "$PROFILE_FILE" 2>/dev/null || sed -i '/alias gmp=/d' "$PROFILE_FILE"
fi

# Function to handle arguments without quotes
GM_FUNCTION="
# God Mode simple command - run without quotes!
gm() {
    \"$SCRIPT_DIR/godmode.sh\" \"\$*\"
}
"

GMP_FUNCTION="
# God Mode process - run after getting AI response
gmp() {
    \"$SCRIPT_DIR/godmode-process.sh\"
}
"

# Add the aliases to the profile file
echo "$GM_FUNCTION" >> "$PROFILE_FILE"
echo "$GMP_FUNCTION" >> "$PROFILE_FILE"

echo -e "${GREEN}✓ Aliases have been set up successfully!${NC}"
echo -e "To use the new aliases, either:"
echo -e "1. Restart your terminal, or"
echo -e "2. Run: source $PROFILE_FILE"
echo -e ""
echo -e "${BLUE}Usage:${NC}"
echo -e "  ${GREEN}gm How do I implement a search feature?${NC}"
echo -e "  ${YELLOW}^ No quotes needed!${NC}"
echo -e ""
echo -e "After getting the AI response:"
echo -e "  ${GREEN}gmp${NC}"
echo -e ""
echo -e "${YELLOW}Would you like to source the profile now? (y/n)${NC}"
read -r answer
if [[ "$answer" == "y" || "$answer" == "Y" ]]; then
    source "$PROFILE_FILE"
    echo -e "${GREEN}Profile sourced. You can now use gm and gmp commands!${NC}"
fi 