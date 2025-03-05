#!/bin/bash

# godmode-process.sh
# Standalone script for processing AI responses in the God Mode workflow
# Usage: ./godmode-process.sh

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

echo -e "${BLUE}Processing AI response...${NC}"

# Run auto commit script to process the response
cd "$SCRIPTS_DIR"
./script_auto_commit.sh

echo -e "\n${GREEN}Response processed successfully!${NC}"
echo -e "Any XML-tagged content in the response has been routed to the appropriate memory files."
echo -e "The next time you use godmode.sh, this information will be included in the enhanced prompt."

# Return to original directory
cd - > /dev/null 