#!/bin/bash

# setup-shadcn.sh
# Installs ALL ShadCN UI components for the God Mode Web UI

# Set colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get the directory of this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Change to the web-ui directory (critical for shadcn to work properly)
cd "$SCRIPT_DIR"

echo -e "${BLUE}Installing ALL ShadCN UI components...${NC}"
echo -e "${YELLOW}Note: ShadCN UI is not a traditional package!${NC}"
echo -e "${YELLOW}It copies component source code directly into your project.${NC}"

# Verify components.json exists (required for shadcn)
if [ ! -f "./components.json" ]; then
    echo -e "${RED}Error: components.json not found!${NC}"
    echo -e "${YELLOW}Creating components.json configuration...${NC}"
    
    # Create components.json with proper configuration
    cat > ./components.json << EOF
{
  "\$schema": "https://ui.shadcn.com/schema.json",
  "style": "default",
  "rsc": true,
  "tsx": true,
  "tailwind": {
    "config": "tailwind.config.js",
    "css": "app/globals.css",
    "baseColor": "slate",
    "cssVariables": true
  },
  "aliases": {
    "components": "@/components",
    "utils": "@/lib/utils"
  }
}
EOF
fi

# Check for lib/utils.ts (required by shadcn)
if [ ! -d "./lib" ]; then
    echo -e "${YELLOW}Creating lib directory...${NC}"
    mkdir -p ./lib
fi

if [ ! -f "./lib/utils.ts" ]; then
    echo -e "${YELLOW}Creating utils.ts (required by shadcn)...${NC}"
    
    # Create utils.ts
    cat > ./lib/utils.ts << EOF
import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"
 
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
EOF
fi

# Update globals.css file with required CSS variables
echo -e "${YELLOW}Updating globals.css with required CSS variables...${NC}"
cat > ./app/globals.css << EOF
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 222.2 84% 4.9%;
    --card: 0 0% 100%;
    --card-foreground: 222.2 84% 4.9%;
    --popover: 0 0% 100%;
    --popover-foreground: 222.2 84% 4.9%;
    --primary: 222.2 47.4% 11.2%;
    --primary-foreground: 210 40% 98%;
    --secondary: 210 40% 96.1%;
    --secondary-foreground: 222.2 47.4% 11.2%;
    --muted: 210 40% 96.1%;
    --muted-foreground: 215.4 16.3% 46.9%;
    --accent: 210 40% 96.1%;
    --accent-foreground: 222.2 47.4% 11.2%;
    --destructive: 0 84.2% 60.2%;
    --destructive-foreground: 210 40% 98%;
    --border: 214.3 31.8% 91.4%;
    --input: 214.3 31.8% 91.4%;
    --ring: 222.2 84% 4.9%;
    --radius: 0.5rem;
  }
 
  .dark {
    --background: 222.2 84% 4.9%;
    --foreground: 210 40% 98%;
    --card: 222.2 84% 4.9%;
    --card-foreground: 210 40% 98%;
    --popover: 222.2 84% 4.9%;
    --popover-foreground: 210 40% 98%;
    --primary: 210 40% 98%;
    --primary-foreground: 222.2 47.4% 11.2%;
    --secondary: 217.2 32.6% 17.5%;
    --secondary-foreground: 210 40% 98%;
    --muted: 217.2 32.6% 17.5%;
    --muted-foreground: 215 20.2% 65.1%;
    --accent: 217.2 32.6% 17.5%;
    --accent-foreground: 210 40% 98%;
    --destructive: 0 62.8% 30.6%;
    --destructive-foreground: 210 40% 98%;
    --border: 217.2 32.6% 17.5%;
    --input: 217.2 32.6% 17.5%;
    --ring: 212.7 26.8% 83.9%;
  }
}

/* Custom scrollbar for webkit browsers */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: rgba(0, 0, 0, 0.1);
  border-radius: 8px;
}

::-webkit-scrollbar-thumb {
  background: rgba(0, 0, 0, 0.2);
  border-radius: 8px;
}

::-webkit-scrollbar-thumb:hover {
  background: rgba(0, 0, 0, 0.3);
}
EOF

# Create components directory if it doesn't exist
mkdir -p "$SCRIPT_DIR/components/ui"

# Install sonner for toast notifications
echo -e "${YELLOW}Installing sonner package for toast notifications...${NC}"
pnpm add sonner || npm install sonner

# Essential UI components to install
COMPONENTS=(
  "button"
  "card" 
  "select"
  "form"
  "input"
  "checkbox"
  "textarea"
  "sonner"    # Modern toast notifications
  "alert"
  "dialog"
  "popover"
  "dropdown-menu"
  "label"     # Essential for forms
)

# Additional components that might be useful
ADDITIONAL_COMPONENTS=(
  "badge"
  "separator"
  "switch"
  "tooltip"
  "tabs"
  "accordion"
  "avatar"
  "sheet"
  "progress"
)

# Install essential components
echo -e "${BLUE}Installing essential UI components...${NC}"
for component in "${COMPONENTS[@]}"; do
  echo -e "${YELLOW}Installing ${component} component...${NC}"
  npx shadcn@latest add $component -y || echo -e "${RED}Failed to install ${component}, continuing...${NC}"
done

# Ask if user wants to install additional components
echo -e "${BLUE}Essential components installed. Install additional components? (y/n)${NC}"
read -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
  for component in "${ADDITIONAL_COMPONENTS[@]}"; do
    echo -e "${YELLOW}Installing ${component} component...${NC}"
    npx shadcn@latest add $component -y || echo -e "${RED}Failed to install ${component}, continuing...${NC}"
  done
fi

# Check if components were successfully installed
if [ -f "$SCRIPT_DIR/components/ui/button.tsx" ]; then
    echo -e "${GREEN}✓ ShadCN UI components installed successfully!${NC}"
    echo -e "${BLUE}You can now import components from '@/components/ui'${NC}"
    echo -e "${YELLOW}Example: import { Button } from '@/components/ui/button'${NC}"
else
    echo -e "${RED}⚠️ Components may not have installed correctly.${NC}"
    echo -e "${YELLOW}Try running this script again or manually install components with:${NC}"
    echo -e "cd $SCRIPT_DIR && npx shadcn@latest add button"
fi 