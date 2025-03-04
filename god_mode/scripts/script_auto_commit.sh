#!/bin/bash

# Auto Commit Script for God Mode
# This script automatically commits changes to the Git repository
# It can be triggered after each AI response or at specified intervals

# Set colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get the script directory and project root
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

# Change to the project root directory
cd "$PROJECT_ROOT" || { echo -e "${RED}Error: Could not navigate to project root directory${NC}"; exit 1; }

# Function to check if there are any changes to commit
has_changes() {
  git status --porcelain | grep -q "."
  return $?
}

# Function to generate commit message
generate_commit_message() {
  # Default commit message
  local message="Auto-commit: God Mode updates"
  
  # If a commit message is provided as an argument, use that instead
  if [ -n "$1" ]; then
    message="$1"
  else
    # Get the most recent log entry to use as a commit message
    local logs_file="$PROJECT_ROOT/god_mode/memory/memory_logs_all.md"
    if [ -f "$logs_file" ]; then
      # Extract the most recent log entry (first non-empty line after a timestamp)
      local recent_log=$(grep -A 3 "UTC" "$logs_file" | grep -v "UTC" | grep -v "^$" | head -n 1)
      if [ -n "$recent_log" ]; then
        message="Auto-commit: $recent_log"
      fi
    fi
  fi
  
  echo "$message"
}

# Main execution
echo -e "${BLUE}Running God Mode auto-commit...${NC}"

# Check if git is installed
if ! command -v git &> /dev/null; then
  echo -e "${RED}Error: Git is not installed or not in PATH${NC}"
  exit 1
fi

# Check if we're in a git repository
if [ ! -d .git ]; then
  echo -e "${YELLOW}Warning: Not in a Git repository, initializing...${NC}"
  git init
  git branch -m main
  echo -e "${GREEN}Git repository initialized with 'main' branch${NC}"
fi

# Check for changes
if ! has_changes; then
  echo -e "${YELLOW}No changes to commit${NC}"
  exit 0
fi

# Add all changes
echo -e "${BLUE}Adding changes to staging area...${NC}"
git add .

# Generate commit message
commit_message=$(generate_commit_message "$1")

# Commit the changes
echo -e "${BLUE}Committing changes with message: ${YELLOW}$commit_message${NC}"
git commit -m "$commit_message"

# Check if commit was successful
if [ $? -eq 0 ]; then
  echo -e "${GREEN}Changes committed successfully${NC}"
  
  # Attempt to push if remote is configured (will fail silently if no remote)
  if git remote -v | grep -q "origin"; then
    echo -e "${BLUE}Pushing changes to remote repository...${NC}"
    git push origin main || {
      echo -e "${YELLOW}Could not push to remote repository. You may need to set up a remote with:${NC}"
      echo -e "${YELLOW}  git remote add origin <repository-url>${NC}"
      echo -e "${YELLOW}  git push -u origin main${NC}"
    }
  else
    echo -e "${YELLOW}No remote repository configured. To add one, use:${NC}"
    echo -e "${YELLOW}  git remote add origin <repository-url>${NC}"
    echo -e "${YELLOW}  git push -u origin main${NC}"
  fi
else
  echo -e "${RED}Failed to commit changes${NC}"
  exit 1
fi

exit 0 