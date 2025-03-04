#!/bin/bash

# Script to run tests for the Grasshop project
# Usage: ./scripts/run_tests.sh [app|ui|all]

set -e

# Default to running all tests
TEST_TARGET=${1:-all}

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Running tests for: ${TEST_TARGET}${NC}"

# Function to run tests for grasshop-app
run_app_tests() {
  echo -e "${YELLOW}Running Grasshop App tests...${NC}"
  cd grasshop-app
  
  if [ -f "package.json" ]; then
    npm test
  else
    echo -e "${RED}Error: package.json not found in grasshop-app directory${NC}"
    exit 1
  fi
  
  cd ..
  echo -e "${GREEN}Grasshop App tests completed${NC}"
}

# Function to run tests for grasshop-ui
run_ui_tests() {
  echo -e "${YELLOW}Running Grasshop UI tests...${NC}"
  cd grasshop-ui
  
  if [ -f "package.json" ]; then
    npm test
  else
    echo -e "${RED}Error: package.json not found in grasshop-ui directory${NC}"
    exit 1
  fi
  
  cd ..
  echo -e "${GREEN}Grasshop UI tests completed${NC}"
}

# Run tests based on target
case $TEST_TARGET in
  app)
    run_app_tests
    ;;
  ui)
    run_ui_tests
    ;;
  all)
    run_app_tests
    run_ui_tests
    ;;
  *)
    echo -e "${RED}Invalid target: ${TEST_TARGET}${NC}"
    echo "Usage: ./scripts/run_tests.sh [app|ui|all]"
    exit 1
    ;;
esac

echo -e "${GREEN}All tests completed successfully${NC}" 