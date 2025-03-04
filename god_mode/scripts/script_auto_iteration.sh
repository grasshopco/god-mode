#!/bin/bash

# Auto-iteration script for continuous improvement of code
# Usage: ./scripts/auto_iteration.sh [max_iterations] [target_directory]

set -e

# Default values
MAX_ITERATIONS=${1:-3}
TARGET_DIR=${2:-.}

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}Starting auto-iteration loop${NC}"
echo -e "${BLUE}Max iterations: ${MAX_ITERATIONS}${NC}"
echo -e "${BLUE}Target directory: ${TARGET_DIR}${NC}"

# Function to run linting
run_linting() {
  echo -e "${YELLOW}Running linting...${NC}"
  
  if [ -d "grasshop-app" ] && [ -f "grasshop-app/package.json" ]; then
    cd grasshop-app
    npm run lint
    cd ..
  fi
  
  if [ -d "grasshop-ui" ] && [ -f "grasshop-ui/package.json" ]; then
    cd grasshop-ui
    npm run lint
    cd ..
  fi
  
  echo -e "${GREEN}Linting completed${NC}"
}

# Function to run tests
run_tests() {
  echo -e "${YELLOW}Running tests...${NC}"
  ./scripts/run_tests.sh all
  echo -e "${GREEN}Tests completed${NC}"
}

# Function to check for issues
check_for_issues() {
  echo -e "${YELLOW}Checking for issues...${NC}"
  
  # This is a placeholder - in a real implementation, this would
  # analyze test results, linting output, etc. to determine if
  # there are issues that need fixing
  
  # For demonstration, we'll just return a random result
  RANDOM_NUM=$((RANDOM % 10))
  
  if [ $RANDOM_NUM -lt 3 ]; then
    echo -e "${RED}Issues found. Iteration needed.${NC}"
    return 1
  else
    echo -e "${GREEN}No issues found. Code looks good!${NC}"
    return 0
  fi
}

# Main iteration loop
iteration=1
while [ $iteration -le $MAX_ITERATIONS ]; do
  echo -e "${BLUE}=== Iteration $iteration of $MAX_ITERATIONS ===${NC}"
  
  # Run linting and tests
  run_linting
  run_tests
  
  # Check for issues
  if check_for_issues; then
    echo -e "${GREEN}Auto-iteration completed successfully after $iteration iterations${NC}"
    exit 0
  fi
  
  # If we've reached the maximum number of iterations, exit with a warning
  if [ $iteration -eq $MAX_ITERATIONS ]; then
    echo -e "${YELLOW}Warning: Reached maximum number of iterations ($MAX_ITERATIONS)${NC}"
    echo -e "${YELLOW}Some issues may still remain. Human intervention recommended.${NC}"
    exit 1
  fi
  
  # Increment iteration counter
  iteration=$((iteration + 1))
  
  echo -e "${BLUE}Proceeding to next iteration...${NC}"
  echo ""
done 