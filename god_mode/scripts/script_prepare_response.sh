#!/bin/bash

# script_prepare_response.sh
# This script prepares the environment before an AI response by running all necessary checks and fixes

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

# Check if Cursor Watch is running
echo -e "${BLUE}Checking if Cursor Watch is running...${NC}"
if pgrep -f "script_cursor_watch.py" > /dev/null; then
    echo -e "${GREEN}✓ Cursor Watch is running${NC}"
else
    echo -e "${YELLOW}⚠️ Cursor Watch is not running, starting it...${NC}"
    # Navigate to the scripts directory
    cd "$SCRIPT_DIR"
    
    # Start Cursor Watch in the background
    python script_cursor_watch.py > "$GOD_MODE_DIR/logs/cursor_watch.log" 2>&1 &
    
    # Check if it started successfully
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Cursor Watch started successfully${NC}"
    else
        echo -e "${RED}✗ Failed to start Cursor Watch${NC}"
    fi
fi

# Check if Message Router is running
echo -e "${BLUE}Checking if Message Router is running...${NC}"
if pgrep -f "script_message_router.py" > /dev/null; then
    echo -e "${GREEN}✓ Message Router is running${NC}"
else
    echo -e "${YELLOW}⚠️ Message Router is not running, starting it...${NC}"
    # Navigate to the scripts directory
    cd "$SCRIPT_DIR"
    
    # Start Message Router in the background
    ./route --watch > "$GOD_MODE_DIR/logs/message_router.log" 2>&1 &
    
    # Check if it started successfully
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Message Router started successfully${NC}"
    else
        echo -e "${RED}✗ Failed to start Message Router${NC}"
    fi
fi

# Update project structure
echo -e "${BLUE}Updating project structure...${NC}"
cd "$SCRIPT_DIR"
python script_update_project_structure.py
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Project structure updated${NC}"
else
    echo -e "${RED}✗ Failed to update project structure${NC}"
fi

# Verify all memory files exist
echo -e "${BLUE}Checking memory files...${NC}"
cd "$SCRIPT_DIR"
./script_check_files.sh --fix
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Memory files verified${NC}"
else
    echo -e "${RED}✗ Failed to verify memory files${NC}"
fi

# Update Cursor rules
echo -e "${BLUE}Updating Cursor rules...${NC}"
cd "$SCRIPT_DIR"
python script_update_cursor_rules.py --force
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Cursor rules updated${NC}"
else
    echo -e "${RED}✗ Failed to update Cursor rules${NC}"
fi

echo -e "${GREEN}✓ Environment prepared for response${NC}"
echo -e "${YELLOW}Remember to include appropriate XML-style tags in your response:${NC}"
echo -e "- <LOG_SUMMARY>Summary</LOG_SUMMARY>"
echo -e "- <LOG_DETAIL>Details</LOG_DETAIL>"
echo -e "- <MEMORY_UPDATE>Updates</MEMORY_UPDATE>"
echo -e "- <FEATURE: FeatureName>Feature updates</FEATURE: FeatureName>"
echo -e "- <PROMPT_ENHANCEMENT>Analysis of previous interaction</PROMPT_ENHANCEMENT>"
echo -e "- <ROADMAP_UPDATE>Progress and new tasks</ROADMAP_UPDATE>"
echo -e "${YELLOW}Remember to run ./script_auto_commit.sh after your response!${NC}"

exit 0 