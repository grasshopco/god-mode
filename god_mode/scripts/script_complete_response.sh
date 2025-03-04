#!/bin/bash

# script_complete_response.sh
# This script runs after an AI response is completed to auto-commit changes and verify that tags were used correctly

# Set colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get the script directory and project root
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
GOD_MODE_DIR="$(dirname "$SCRIPT_DIR")"
PROJECT_ROOT="$(dirname "$GOD_MODE_DIR")"

# Check if tags were used in the response
echo -e "${BLUE}Checking routing activity...${NC}"
cd "$SCRIPT_DIR"
python script_track_routing.py
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Response with tags processed${NC}"
else
    echo -e "${YELLOW}⚠️ No routing activity detected. Did you include tags in your response?${NC}"
    echo -e "Remember to include:"
    echo -e "- [LOG_SUMMARY]"
    echo -e "- [LOG_DETAIL]"
    echo -e "- [MEMORY_UPDATE]"
    echo -e "- [FEATURE_LOG: Feature]"
fi

# Auto-commit changes
echo -e "${BLUE}Auto-committing changes...${NC}"
cd "$SCRIPT_DIR"
./script_auto_commit.sh
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Changes committed successfully${NC}"
else
    echo -e "${RED}✗ Failed to commit changes${NC}"
fi

# Verify all components are running
echo -e "${BLUE}Verifying God Mode components...${NC}"
if pgrep -f "script_cursor_watch.py" > /dev/null; then
    echo -e "${GREEN}✓ Cursor Watch is running${NC}"
else
    echo -e "${RED}✗ Cursor Watch is not running${NC}"
fi

if pgrep -f "script_message_router.py" > /dev/null; then
    echo -e "${GREEN}✓ Message Router is running${NC}"
else
    echo -e "${RED}✗ Message Router is not running${NC}"
fi

echo -e "${GREEN}✓ Response completion tasks finished${NC}"

exit 0 