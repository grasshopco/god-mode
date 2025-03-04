#!/bin/bash

# script_install_dependencies.sh
# This script installs the required Python dependencies for God Mode

# Set colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=======================================${NC}"
echo -e "${BLUE}     God Mode Dependency Installer     ${NC}"
echo -e "${BLUE}=======================================${NC}"
echo

# Function to check if a Python module is installed
check_module() {
    python -c "import $1" 2>/dev/null
    return $?
}

# Function to install a Python module
install_module() {
    local module=$1
    echo -e "${YELLOW}Installing $module...${NC}"
    
    # Try pip3 first, then pip if pip3 fails
    if command -v pip3 &>/dev/null; then
        pip3 install $module
    elif command -v pip &>/dev/null; then
        pip install $module
    else
        echo -e "${RED}Error: Neither pip3 nor pip was found. Please install pip and try again.${NC}"
        return 1
    fi
    
    # Check if installation was successful
    if check_module $module; then
        echo -e "${GREEN}✓ $module installed successfully${NC}"
        return 0
    else
        echo -e "${RED}✗ Failed to install $module${NC}"
        return 1
    fi
}

# Check for pyperclip
if check_module pyperclip; then
    echo -e "${GREEN}✓ pyperclip is already installed${NC}"
else
    echo -e "${YELLOW}pyperclip is not installed. This is required for clipboard access.${NC}"
    install_module pyperclip
fi

# Check for plyer
if check_module plyer; then
    echo -e "${GREEN}✓ plyer is already installed${NC}"
else
    echo -e "${YELLOW}plyer is not installed. This is required for desktop notifications.${NC}"
    install_module plyer
fi

# Check for pyobjus on macOS (required for notifications)
if [[ "$OSTYPE" == "darwin"* ]]; then
    if check_module pyobjus; then
        echo -e "${GREEN}✓ pyobjus is already installed${NC}"
    else
        echo -e "${YELLOW}pyobjus is not installed. This is required for desktop notifications on macOS.${NC}"
        install_module pyobjus
    fi
fi

echo
echo -e "${BLUE}=======================================${NC}"
echo -e "${GREEN}All dependencies have been checked.${NC}"
echo -e "${BLUE}=======================================${NC}"
echo
echo -e "You can now run God Mode with all required dependencies."
echo -e "To start God Mode, use option 1 in the remote control menu."
echo 