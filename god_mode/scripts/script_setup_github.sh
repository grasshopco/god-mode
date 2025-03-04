#!/bin/bash

# GitHub Repository Setup Script for God Mode
# This script helps set up a GitHub repository for your God Mode project
# Run this script when you're ready to create a remote repository on GitHub

# Set colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
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

# Function to check if git user is configured
check_git_user() {
  local git_name=$(git config --global user.name)
  local git_email=$(git config --global user.email)
  
  if [ -z "$git_name" ] || [ -z "$git_email" ]; then
    echo -e "${YELLOW}Git user is not fully configured.${NC}"
    echo -e "${YELLOW}Let's set up your Git user information:${NC}"
    
    if [ -z "$git_name" ]; then
      echo -e "${YELLOW}Enter your name:${NC}"
      read -r user_name
      git config --global user.name "$user_name"
    fi
    
    if [ -z "$git_email" ]; then
      echo -e "${YELLOW}Enter your email:${NC}"
      read -r user_email
      git config --global user.email "$user_email"
    fi
    
    echo -e "${GREEN}Git user configured:${NC}"
    echo -e "Name: $(git config --global user.name)"
    echo -e "Email: $(git config --global user.email)"
  fi
}

# Function to configure git user with specific values
configure_git_user() {
  echo -e "${BLUE}Configuring Git User Information${NC}"
  echo -e "${BLUE}==============================${NC}"
  
  echo -e "${YELLOW}Current Git configuration:${NC}"
  echo -e "Name: $(git config --global user.name)"
  echo -e "Email: $(git config --global user.email)"
  echo
  
  echo -e "${YELLOW}Would you like to update your Git user information? (y/n)${NC}"
  read -r update_git_user
  
  if [[ "$update_git_user" =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}Enter your name (leave blank to keep current):${NC}"
    read -r user_name
    
    if [ -n "$user_name" ]; then
      git config --global user.name "$user_name"
    fi
    
    echo -e "${YELLOW}Enter your email (leave blank to keep current):${NC}"
    read -r user_email
    
    if [ -n "$user_email" ]; then
      git config --global user.email "$user_email"
    fi
    
    echo -e "${GREEN}Git user updated:${NC}"
    echo -e "Name: $(git config --global user.name)"
    echo -e "Email: $(git config --global user.email)"
  fi
}

# Function to create GitHub repository
create_github_repo() {
  local repo_name="$1"
  local description="$2"
  local visibility="$3"

  # Validate parameters
  if [ -z "$repo_name" ]; then
    repo_name="God-Mode"
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
    echo -e "${YELLOW}Would you like to authenticate now? (y/n)${NC}"
    read -r auth_now
    
    if [[ "$auth_now" =~ ^[Yy]$ ]]; then
      gh auth login
    else
      echo -e "${YELLOW}Please run 'gh auth login' first and then try again.${NC}"
      return 1
    fi
  fi

  # Create the repository
  echo -e "${BLUE}Creating GitHub repository: ${YELLOW}$repo_name${NC}"
  gh repo create "$repo_name" --description "$description" --"$visibility" --source=. --remote=origin --push

  return $?
}

# Function to connect to an existing GitHub repository
connect_to_existing_repo() {
  echo -e "${BLUE}Connect to Existing GitHub Repository${NC}"
  echo -e "${BLUE}=====================================${NC}"
  
  # List existing remotes
  if git remote -v | grep -q "origin"; then
    echo -e "${YELLOW}Current remote repository:${NC}"
    git remote -v
    echo -e "${YELLOW}Do you want to replace it? (y/n)${NC}"
    read -r replace_remote
    if [[ "$replace_remote" =~ ^[Yy]$ ]]; then
      git remote remove origin
    else
      echo -e "${GREEN}Keeping existing remote. Operation canceled.${NC}"
      return 0
    fi
  fi
  
  # Ask for repository URL
  echo -e "${YELLOW}Enter the GitHub repository URL:${NC}"
  echo -e "${CYAN}(e.g., https://github.com/username/repository.git)${NC}"
  read -r repo_url
  
  if [ -z "$repo_url" ]; then
    echo -e "${RED}No repository URL provided. Operation canceled.${NC}"
    return 1
  fi
  
  # Add the remote
  echo -e "${BLUE}Adding remote repository...${NC}"
  git remote add origin "$repo_url"
  
  # Verify the remote was added
  if git remote -v | grep -q "origin"; then
    echo -e "${GREEN}Remote repository added successfully:${NC}"
    git remote -v
    
    # Ask if user wants to push to the repository
    echo -e "${YELLOW}Would you like to push current code to the repository? (y/n)${NC}"
    read -r push_code
    
    if [[ "$push_code" =~ ^[Yy]$ ]]; then
      # Check if the repository is empty
      echo -e "${YELLOW}Is this an empty repository? (y/n)${NC}"
      echo -e "${CYAN}(If not, this may cause conflicts)${NC}"
      read -r is_empty
      
      if [[ "$is_empty" =~ ^[Yy]$ ]]; then
        git push -u origin main || git push -u origin master
      else
        echo -e "${YELLOW}Choose how to handle potential conflicts:${NC}"
        echo -e "1) ${CYAN}Force push (will overwrite remote repository)${NC}"
        echo -e "2) ${CYAN}Fetch and merge (will try to merge remote changes)${NC}"
        echo -e "3) ${CYAN}Cancel (don't push now)${NC}"
        read -r conflict_choice
        
        case "$conflict_choice" in
          1)
            echo -e "${YELLOW}Force pushing to remote repository...${NC}"
            git push -f -u origin main || git push -f -u origin master
            ;;
          2)
            echo -e "${YELLOW}Fetching and merging with remote repository...${NC}"
            git fetch origin
            git merge origin/main || git merge origin/master
            git push -u origin main || git push -u origin master
            ;;
          *)
            echo -e "${YELLOW}Push canceled. You can push manually later.${NC}"
            ;;
        esac
      fi
    fi
    
    return 0
  else
    echo -e "${RED}Failed to add remote repository.${NC}"
    return 1
  fi
}

# Function to switch between GitHub repositories
switch_github_repo() {
  echo -e "${BLUE}Switch GitHub Repository${NC}"
  echo -e "${BLUE}=======================${NC}"
  
  # List existing remotes
  echo -e "${YELLOW}Current remote repositories:${NC}"
  git remote -v
  
  echo -e "${YELLOW}What would you like to do?${NC}"
  echo -e "1) ${CYAN}Change 'origin' to a different repository${NC}"
  echo -e "2) ${CYAN}Add an additional remote repository${NC}"
  echo -e "3) ${CYAN}Remove a remote repository${NC}"
  echo -e "4) ${CYAN}Cancel${NC}"
  read -r switch_choice
  
  case "$switch_choice" in
    1)
      # Change origin remote
      echo -e "${YELLOW}Enter the new GitHub repository URL for 'origin':${NC}"
      read -r new_url
      
      if [ -z "$new_url" ]; then
        echo -e "${RED}No repository URL provided. Operation canceled.${NC}"
        return 1
      fi
      
      git remote remove origin
      git remote add origin "$new_url"
      echo -e "${GREEN}Origin updated to: $new_url${NC}"
      ;;
    2)
      # Add a new remote
      echo -e "${YELLOW}Enter the name for the new remote:${NC}"
      read -r remote_name
      
      echo -e "${YELLOW}Enter the GitHub repository URL for '$remote_name':${NC}"
      read -r remote_url
      
      if [ -z "$remote_name" ] || [ -z "$remote_url" ]; then
        echo -e "${RED}Incomplete information provided. Operation canceled.${NC}"
        return 1
      fi
      
      git remote add "$remote_name" "$remote_url"
      echo -e "${GREEN}Added remote '$remote_name' pointing to: $remote_url${NC}"
      ;;
    3)
      # Remove a remote
      echo -e "${YELLOW}Enter the name of the remote to remove:${NC}"
      read -r remove_name
      
      if [ -z "$remove_name" ]; then
        echo -e "${RED}No remote name provided. Operation canceled.${NC}"
        return 1
      fi
      
      git remote remove "$remove_name"
      echo -e "${GREEN}Removed remote: $remove_name${NC}"
      ;;
    *)
      echo -e "${YELLOW}Operation canceled.${NC}"
      return 0
      ;;
  esac
  
  # Show updated remotes
  echo -e "${YELLOW}Updated remote repositories:${NC}"
  git remote -v
  
  return 0
}

# Show GitHub menu
show_github_menu() {
  echo -e "${BLUE}GitHub Repository Management${NC}"
  echo -e "${BLUE}============================${NC}"
  echo
  echo -e "${YELLOW}What would you like to do?${NC}"
  echo -e "1) ${CYAN}Create a new GitHub repository${NC}"
  echo -e "2) ${CYAN}Connect to an existing GitHub repository${NC}"
  echo -e "3) ${CYAN}Switch GitHub repositories${NC}"
  echo -e "4) ${CYAN}Configure Git user information${NC}"
  echo -e "5) ${CYAN}Back to main menu${NC}"
  echo
  echo -n "Enter your choice: "
  read -r github_choice
  
  case "$github_choice" in
    1)
      # Create a new GitHub repository
      echo -e "${BLUE}Let's set up your GitHub repository.${NC}"
      echo -e "${YELLOW}Repository name (default: God-Mode):${NC}"
      read -r repo_name
      echo -e "${YELLOW}Description (default: An advanced Cursor IDE enhancement system):${NC}"
      read -r description
      echo -e "${YELLOW}Visibility (public/private, default: public):${NC}"
      read -r visibility
      
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
      fi
      ;;
    2)
      # Connect to an existing repository
      connect_to_existing_repo
      ;;
    3)
      # Switch GitHub repositories
      switch_github_repo
      ;;
    4)
      # Configure Git user
      configure_git_user
      ;;
    5|*)
      # Back to main menu
      echo -e "${YELLOW}Returning to main menu.${NC}"
      return 0
      ;;
  esac
  
  echo
  echo -n "Press Enter to continue..."
  read
  
  # Show GitHub menu again
  show_github_menu
}

# Main execution
if [ "$1" = "--menu" ]; then
  # Show GitHub menu
  show_github_menu
  exit 0
fi

echo -e "${BLUE}GitHub Repository Setup for God Mode${NC}"
echo -e "${BLUE}===============================${NC}"

# Check if git is installed
if ! command -v git &> /dev/null; then
  echo -e "${RED}Error: Git is not installed or not in PATH${NC}"
  exit 1
fi

# Check git user configuration
check_git_user

# Check GitHub CLI
if ! check_gh_cli; then
  echo -e "${YELLOW}You can set up the GitHub repository manually with:${NC}"
  echo -e "${YELLOW}  1. Create a new repository on github.com${NC}"
  echo -e "${YELLOW}  2. Run: git remote add origin <repository-url>${NC}"
  echo -e "${YELLOW}  3. Run: git push -u origin main${NC}"
  exit 1
fi

# Show GitHub menu
show_github_menu

exit 0 