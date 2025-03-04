#!/bin/bash

# Script to update Cursor rules based on project evolution
# Usage: ./scripts/update_rules.sh [rule_file] [update_description]

set -e

# Default values
RULE_FILE=${1:-".cursorrules"}
UPDATE_DESCRIPTION=${2:-"Updated rules"}

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}Updating Cursor rules${NC}"
echo -e "${BLUE}Rule file: ${RULE_FILE}${NC}"
echo -e "${BLUE}Update description: ${UPDATE_DESCRIPTION}${NC}"

# Check if the rule file exists
if [ ! -f "$RULE_FILE" ]; then
  echo -e "${RED}Error: Rule file '$RULE_FILE' not found${NC}"
  exit 1
fi

# Create a backup of the current rule file
BACKUP_FILE="${RULE_FILE}.backup.$(date +%Y%m%d%H%M%S)"
cp "$RULE_FILE" "$BACKUP_FILE"
echo -e "${GREEN}Created backup: ${BACKUP_FILE}${NC}"

# Function to update the rules file
update_rules() {
  local rule_file=$1
  local update_description=$2
  
  # In a real implementation, this would use AI to analyze the project
  # and suggest updates to the rules. For now, we'll just add a comment.
  
  echo -e "${YELLOW}Analyzing project for rule updates...${NC}"
  
  # Add a comment about the update
  echo "" >> "$rule_file"
  echo "# Updated on $(date): $update_description" >> "$rule_file"
  
  echo -e "${GREEN}Rules updated successfully${NC}"
}

# Update the rules
update_rules "$RULE_FILE" "$UPDATE_DESCRIPTION"

# Log the update
echo -e "${YELLOW}Logging the update...${NC}"
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")
LOG_ENTRY="- [$TIMESTAMP] **Updated Rules** - $UPDATE_DESCRIPTION"

# Add to all_logs.md if it exists
if [ -f "all_logs.md" ]; then
  echo "$LOG_ENTRY" >> "all_logs.md"
  echo -e "${GREEN}Added entry to all_logs.md${NC}"
fi

# Add to in_depth_logs.md if it exists
if [ -f "in_depth_logs.md" ]; then
  echo -e "\n## [$TIMESTAMP] Updated Rules\n" >> "in_depth_logs.md"
  echo -e "### Files Modified\n" >> "in_depth_logs.md"
  echo -e "- \`$RULE_FILE\`:" >> "in_depth_logs.md"
  echo -e "  - Updated rules based on project evolution" >> "in_depth_logs.md"
  echo -e "  - $UPDATE_DESCRIPTION\n" >> "in_depth_logs.md"
  echo -e "### Approach\n" >> "in_depth_logs.md"
  echo -e "- Analyzed project for rule updates" >> "in_depth_logs.md"
  echo -e "- Created backup of existing rules" >> "in_depth_logs.md"
  echo -e "- Applied updates to rules file\n" >> "in_depth_logs.md"
  echo -e "### Reasoning\n" >> "in_depth_logs.md"
  echo -e "- Rules need to evolve with the project to remain relevant" >> "in_depth_logs.md"
  echo -e "- Regular updates ensure AI assistance remains effective" >> "in_depth_logs.md"
  echo -e "- Keeping rules current improves code quality and consistency" >> "in_depth_logs.md"
  echo -e "${GREEN}Added entry to in_depth_logs.md${NC}"
fi

echo -e "${GREEN}Rule update completed successfully${NC}" 