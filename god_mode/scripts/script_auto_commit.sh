#!/bin/bash

# script_auto_commit.sh
# This script processes responses with XML-style tags, updates appropriate files, 
# and auto-commits changes to Git repository

# Set colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get directory of this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
GOD_MODE_DIR="$(dirname "$SCRIPT_DIR")"
PROJECT_DIR="$(dirname "$GOD_MODE_DIR")"

echo -e "${BLUE}=======================================${NC}"
echo -e "${BLUE}     God Mode Response Processor      ${NC}"
echo -e "${BLUE}=======================================${NC}"
echo

# Step 1: Process XML tags in latest response
echo -e "${YELLOW}Processing XML tags in latest response...${NC}"
if [ -f "$SCRIPT_DIR/route" ]; then
    chmod +x "$SCRIPT_DIR/route"
    "$SCRIPT_DIR/route" --clipboard
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ XML tags processed successfully${NC}"
    else
        echo -e "${RED}✗ Error processing XML tags${NC}"
    fi
else
    echo -e "${RED}✗ Error: route script not found${NC}"
fi

# Step 2: Extract and update prompt_enhanced.md
echo -e "${YELLOW}Updating prompt enhancement file...${NC}"
if [ -f "$SCRIPT_DIR/script_enhance_prompt.py" ]; then
    python "$SCRIPT_DIR/script_enhance_prompt.py" --update-from-clipboard
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Prompt enhancement file updated${NC}"
    else
        echo -e "${RED}✗ Error updating prompt enhancement file${NC}"
    fi
else
    echo -e "${RED}✗ Error: script_enhance_prompt.py not found${NC}"
fi

# Step 3: Update roadmap file if needed
echo -e "${YELLOW}Checking for roadmap updates...${NC}"
if [ -f "$SCRIPT_DIR/script_enhance_message_content.py" ]; then
    python "$SCRIPT_DIR/script_enhance_message_content.py" --update-roadmap-from-clipboard
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Roadmap updated successfully${NC}"
    else
        echo -e "${YELLOW}⚠️ No roadmap updates found or error updating roadmap${NC}"
    fi
else
    echo -e "${RED}✗ Error: script_enhance_message_content.py not found${NC}"
fi

# Step 4: Navigate to project directory
cd "$PROJECT_DIR"

# Step 5: Auto-commit changes
echo -e "${YELLOW}Auto-committing changes...${NC}"

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo -e "${YELLOW}Git repository not initialized. Initializing now...${NC}"
    git init
    echo -e "${GREEN}✓ Git repository initialized${NC}"
fi

# Add all changes
git add .

# Create commit with timestamp or custom message
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")
if [ -n "$1" ]; then
    git commit -m "$1"
else
    git commit -m "Auto-commit: $TIMESTAMP"
fi

# Check if commit was successful
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Changes committed successfully!${NC}"
else
    echo -e "${YELLOW}⚠️ No changes to commit or commit failed${NC}"
fi

# Push changes if a remote is configured
if git remote -v | grep -q origin; then
    echo -e "${YELLOW}Pushing changes to remote repository...${NC}"
    git push origin main
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Changes pushed successfully!${NC}"
    else
        echo -e "${RED}✗ Push failed${NC}"
        echo -e "${YELLOW}Try running: git push -u origin main${NC}"
    fi
fi

echo -e "${GREEN}✓ Response processing and auto-commit complete!${NC}"
exit 0 