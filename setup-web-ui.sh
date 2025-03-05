#!/bin/bash

# setup-web-ui.sh
# Sets up and starts the God Mode Web UI

# Set colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get the directory of this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
WEB_UI_DIR="$SCRIPT_DIR/web-ui"

echo -e "${BLUE}Setting up God Mode Web UI...${NC}"

# Check if pnpm is installed
if ! command -v pnpm &> /dev/null; then
    echo -e "${YELLOW}pnpm is not installed. Installing pnpm...${NC}"
    npm install -g pnpm
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ pnpm installed successfully${NC}"
    else
        echo -e "${RED}✗ Failed to install pnpm${NC}"
        echo -e "Please install pnpm manually by running: npm install -g pnpm"
        exit 1
    fi
else
    echo -e "${GREEN}✓ pnpm is already installed${NC}"
fi

# Navigate to web-ui directory
cd "$WEB_UI_DIR"

# Install dependencies
echo -e "${BLUE}Installing dependencies...${NC}"
pnpm install

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Dependencies installed successfully${NC}"
else
    echo -e "${RED}✗ Failed to install dependencies${NC}"
    exit 1
fi

# Install ShadCN UI components
echo -e "${BLUE}Installing ShadCN UI components...${NC}"
if [ -f "./setup-shadcn.sh" ]; then
    chmod +x ./setup-shadcn.sh
    ./setup-shadcn.sh
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ ShadCN UI components installed successfully${NC}"
    else
        echo -e "${YELLOW}⚠️ Some ShadCN UI components may not have installed correctly${NC}"
        echo -e "You can try installing them manually by running: cd $WEB_UI_DIR && ./setup-shadcn.sh"
    fi
else
    echo -e "${RED}✗ setup-shadcn.sh not found${NC}"
    echo -e "ShadCN UI components will not be installed"
fi

# Get local IP address for accessing from other devices
echo -e "${BLUE}Finding your local IP address...${NC}"
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    IP=$(ifconfig | grep "inet " | grep -v 127.0.0.1 | head -n 1 | awk '{print $2}')
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    IP=$(hostname -I | awk '{print $1}')
else
    # Windows or other
    IP="your-local-IP"
fi

# Start development server
echo -e "${GREEN}Starting God Mode Web UI...${NC}"
echo -e "${YELLOW}Access locally at: ${NC}http://localhost:3000"
echo -e "${YELLOW}Access from other devices at: ${NC}http://$IP:3000"
echo -e "${YELLOW}Press Ctrl+C to stop the server${NC}"
echo ""

pnpm dev 