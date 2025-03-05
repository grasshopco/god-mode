#!/bin/bash

# Run the God Mode MCP server directly for testing

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get the directory of this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is required but not installed.${NC}"
    exit 1
fi

# Path to the MCP server script
MCP_SERVER_SCRIPT="$SCRIPT_DIR/god_mode/scripts/script_mcp_server.py"

# Check if the script exists
if [ ! -f "$MCP_SERVER_SCRIPT" ]; then
    echo -e "${RED}Error: MCP server script not found at $MCP_SERVER_SCRIPT${NC}"
    exit 1
fi

# Make sure the script is executable
chmod +x "$MCP_SERVER_SCRIPT"

echo -e "${BLUE}Starting God Mode MCP Server for testing...${NC}"
echo -e "${YELLOW}This script is intended for testing only.${NC}"
echo -e "${YELLOW}For normal usage, Cursor will run the MCP server automatically.${NC}"
echo -e "${YELLOW}Press Ctrl+C to stop the server.${NC}"
echo

# Run the MCP server in debug mode
python3 "$MCP_SERVER_SCRIPT" --debug

# Handle script termination
echo -e "${BLUE}MCP server stopped.${NC}" 