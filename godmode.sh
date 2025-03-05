#!/bin/bash

# godmode.sh
# Standalone script for running the God Mode workflow
# Usage: ./godmode.sh "Your message to Cursor AI"

# Set colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get the directory of this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
GOD_MODE_DIR="$SCRIPT_DIR/god_mode"
SCRIPTS_DIR="$GOD_MODE_DIR/scripts"

# Check if message was provided
if [ "$#" -eq 0 ]; then
    echo -e "${RED}Error: No message provided${NC}"
    echo -e "Usage: $0 \"Your message to Cursor AI\""
    exit 1
fi

# Get user's message (combine all arguments)
USER_MESSAGE="$*"

# Create temp file for the message
TEMP_MSG_FILE=$(mktemp)
echo "$USER_MESSAGE" > "$TEMP_MSG_FILE"

# Run prepare response script
echo -e "${BLUE}Running prepare response script...${NC}"
cd "$SCRIPTS_DIR"
./script_prepare_response.sh

# Enhance the prompt
echo -e "${BLUE}Enhancing your prompt...${NC}"
ENHANCED_PROMPT=$(python "$SCRIPTS_DIR/script_enhance_prompt.py" --prompt "$USER_MESSAGE")

# Copy enhanced prompt to clipboard
echo "$ENHANCED_PROMPT" | pbcopy 2>/dev/null || echo "$ENHANCED_PROMPT" | xclip -selection clipboard 2>/dev/null || echo "$ENHANCED_PROMPT" | xsel --clipboard 2>/dev/null

echo -e "\n${GREEN}==================================${NC}"
echo -e "${GREEN}Enhanced prompt copied to clipboard${NC}"
echo -e "${GREEN}==================================${NC}"
echo -e "Please paste this in Cursor IDE, then after receiving the AI response:"
echo -e "1. Select the entire AI response"
echo -e "2. Copy it to the clipboard"
echo -e "3. Run './godmode-process.sh' in your terminal"

# Clean up temp file
rm "$TEMP_MSG_FILE"

# Return to original directory
cd - > /dev/null 