#!/bin/bash

# GitHub Repository Setup Script for God Mode
# This script helps set up a GitHub repository for your God Mode project
# Run this script when you're ready to create a remote repository on GitHub

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

# Function to check GitHub CLI availability
check_gh_cli() {
  if ! command -v gh &> /dev/null; then
    echo -e "${YELLOW}GitHub CLI (gh) is not installed.${NC}"
    echo -e "${YELLOW}Would you like to install it? (y/n)${NC}"
    read -r install_gh
    if [[ "$install_gh" =~ ^[Yy]$ ]]; then
      echo -e "${BLUE}Installing GitHub CLI...${NC}"
      if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        brew install gh
      elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
        echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
        sudo apt update
        sudo apt install gh
      else
        echo -e "${RED}Unsupported operating system. Please install GitHub CLI manually:${NC}"
        echo -e "${YELLOW}https://github.com/cli/cli#installation${NC}"
        return 1
      fi
    else
      echo -e "${YELLOW}Please install GitHub CLI manually and run this script again.${NC}"
      return 1
    fi
  fi
  return 0
}

# Function to create GitHub repository
create_github_repo() {
  local repo_name="$1"
  local description="$2"
  local visibility="$3"

  # Validate parameters
  if [ -z "$repo_name" ]; then
    repo_name="GOD_MODE_PROJECT_STARTER_TEMPLATE"
  fi
  
  if [ -z "$description" ]; then
    description="An advanced Cursor IDE enhancement system with memory, automation, and context management."
  fi

  if [ -z "$visibility" ]; then
    visibility="public"
  fi

  # Check if GitHub CLI is authenticated
  gh auth status &> /dev/null
  if [ $? -ne 0 ]; then
    echo -e "${YELLOW}You are not authenticated with GitHub CLI.${NC}"
    echo -e "${YELLOW}Please run 'gh auth login' first.${NC}"
    return 1
  fi

  # Create the repository
  echo -e "${BLUE}Creating GitHub repository: ${YELLOW}$repo_name${NC}"
  gh repo create "$repo_name" --description "$description" --"$visibility" --source=. --remote=origin --push

  return $?
}

# Main execution
echo -e "${BLUE}GitHub Repository Setup for God Mode${NC}"
echo -e "${BLUE}===============================${NC}"

# Check if git is installed
if ! command -v git &> /dev/null; then
  echo -e "${RED}Error: Git is not installed or not in PATH${NC}"
  exit 1
fi

# Check if already has a remote
if git remote -v | grep -q "origin"; then
  echo -e "${YELLOW}Remote repository already configured:${NC}"
  git remote -v
  echo -e "${YELLOW}Do you want to replace it? (y/n)${NC}"
  read -r replace_remote
  if [[ "$replace_remote" =~ ^[Yy]$ ]]; then
    git remote remove origin
  else
    echo -e "${GREEN}Keeping existing remote. Setup complete!${NC}"
    exit 0
  fi
fi

# Check GitHub CLI
if ! check_gh_cli; then
  echo -e "${YELLOW}You can set up the GitHub repository manually with:${NC}"
  echo -e "${YELLOW}  1. Create a new repository on github.com${NC}"
  echo -e "${YELLOW}  2. Run: git remote add origin <repository-url>${NC}"
  echo -e "${YELLOW}  3. Run: git push -u origin main${NC}"
  exit 1
fi

# Get repository details
echo -e "${BLUE}Let's set up your GitHub repository.${NC}"
echo -e "${YELLOW}Repository name (default: GOD_MODE_PROJECT_STARTER_TEMPLATE):${NC}"
read -r repo_name
echo -e "${YELLOW}Description (default: An advanced Cursor IDE enhancement system):${NC}"
read -r description
echo -e "${YELLOW}Visibility (public/private, default: public):${NC}"
read -r visibility

# Create the repository
if create_github_repo "$repo_name" "$description" "$visibility"; then
  echo -e "${GREEN}Repository created and connected successfully!${NC}"
  
  # Run auto-commit to push changes
  "$SCRIPT_DIR/script_auto_commit.sh" "Initial setup with GitHub repository"
  
  echo -e "${GREEN}All set! Your God Mode system is now on GitHub.${NC}"
else
  echo -e "${RED}Failed to create GitHub repository.${NC}"
  echo -e "${YELLOW}You can try again later or set up manually:${NC}"
  echo -e "${YELLOW}  1. Create a new repository on github.com${NC}"
  echo -e "${YELLOW}  2. Run: git remote add origin <repository-url>${NC}"
  echo -e "${YELLOW}  3. Run: git push -u origin main${NC}"
  exit 1
fi

exit 0 