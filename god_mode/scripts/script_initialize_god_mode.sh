#!/bin/bash

# script_initialize_god_mode.sh
# This script initializes the God Mode system by:
# 1. Creating necessary directories
# 2. Copying templates to memory files
# 3. Making scripts executable
# 4. Updating the project structure
# 5. Updating Cursor rules
# 6. Setting up the prompt enhancement system

# Set colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Get the directory of this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
GOD_MODE_DIR="$(dirname "$SCRIPT_DIR")"
PROJECT_ROOT="$(dirname "$GOD_MODE_DIR")"

echo -e "${YELLOW}Initializing God Mode for Cursor IDE...${NC}"
echo -e "Project root: ${PROJECT_ROOT}"
echo -e "God Mode directory: ${GOD_MODE_DIR}"

# Function to create directory if it doesn't exist
create_dir_if_not_exists() {
    if [ ! -d "$1" ]; then
        echo -e "Creating directory: $1"
        mkdir -p "$1"
    fi
}

# Step 1: Create necessary directories
echo -e "\n${YELLOW}Step 1: Creating necessary directories...${NC}"

# Create memory directory
create_dir_if_not_exists "$GOD_MODE_DIR/memory"

# Create documentation directories
create_dir_if_not_exists "$GOD_MODE_DIR/documentation/documentation_project"
create_dir_if_not_exists "$GOD_MODE_DIR/documentation/documentation_feature"
create_dir_if_not_exists "$GOD_MODE_DIR/documentation/documentation_design"
create_dir_if_not_exists "$GOD_MODE_DIR/documentation/documentation_data_model"

# Create discussion directories
create_dir_if_not_exists "$GOD_MODE_DIR/discussion/discussion_project"
create_dir_if_not_exists "$GOD_MODE_DIR/discussion/discussion_feature"
create_dir_if_not_exists "$GOD_MODE_DIR/discussion/discussion_design"
create_dir_if_not_exists "$GOD_MODE_DIR/discussion/discussion_data_model"

# Create logs directory
create_dir_if_not_exists "$GOD_MODE_DIR/logs"

# Create cache directory
create_dir_if_not_exists "$GOD_MODE_DIR/.cache"

# Create cursor config directory
create_dir_if_not_exists "$PROJECT_ROOT/.cursor"

# Create app directory if it doesn't exist
create_dir_if_not_exists "$PROJECT_ROOT/app"

# Step 2: Copy templates to memory files
echo -e "\n${YELLOW}Step 2: Copying templates to memory files...${NC}"

# Function to copy template to memory file if it doesn't exist
copy_template_to_memory() {
    template_file="$GOD_MODE_DIR/templates/$1"
    memory_file="$GOD_MODE_DIR/memory/$2"
    
    if [ -f "$template_file" ] && [ ! -f "$memory_file" ]; then
        echo -e "Copying template $1 to memory file $2"
        cp "$template_file" "$memory_file"
    elif [ ! -f "$template_file" ]; then
        echo -e "${RED}Template file $1 not found${NC}"
    else
        echo -e "Memory file $2 already exists, skipping"
    fi
}

# Copy templates to memory files
copy_template_to_memory "template_memory_project_structure.md" "memory_project_structure.md"
copy_template_to_memory "template_memory_logs_all.md" "memory_logs_all.md"
copy_template_to_memory "template_memory_logs_detailed.md" "memory_logs_detailed.md"
copy_template_to_memory "template_memory_learnings.md" "memory_learnings.md"
copy_template_to_memory "template_MEMORY_CURSOR.md" "MEMORY_CURSOR.md"
copy_template_to_memory "template_MEMORY_UPDATES.md" "memory_updates.md"
copy_template_to_memory "template_MEMORY_REQUIREMENTS.md" "memory_requirements.md"
copy_template_to_memory "template_MEMORY_ROADMAP.md" "memory_roadmap.md"
copy_template_to_memory "template_MEMORY_ARCHITECTURE.md" "memory_architecture.md"
copy_template_to_memory "template_MEMORY_CONVENTIONS.md" "memory_conventions.md"
copy_template_to_memory "template_MEMORY_DEPENDENCIES.md" "memory_dependencies.md"
copy_template_to_memory "template_MEMORY_GLOSSARY.md" "memory_glossary.md"
copy_template_to_memory "template_MEMORY_TESTING.md" "memory_testing.md"
copy_template_to_memory "template_MEMORY_SECURITY.md" "memory_security.md"
copy_template_to_memory "template_MEMORY_PERFORMANCE.md" "memory_performance.md"
copy_template_to_memory "template_MEMORY_ACCESSIBILITY.md" "memory_accessibility.md"

# Step 3: Make scripts executable
echo -e "\n${YELLOW}Step 3: Making scripts executable...${NC}"

# Function to make script executable if it exists
make_executable() {
    script_file="$SCRIPT_DIR/$1"
    
    if [ -f "$script_file" ]; then
        echo -e "Making $1 executable"
        chmod +x "$script_file"
    else
        echo -e "${RED}Script file $1 not found${NC}"
    fi
}

# Make scripts executable
make_executable "script_update_project_structure.py"
make_executable "script_message_router.py"
make_executable "script_auto_iteration.sh"
make_executable "script_update_rules.sh"
make_executable "script_get_utc_time.py"
make_executable "script_get_utc_time.sh"
make_executable "script_run_tests.sh"
make_executable "route"
make_executable "script_enhance_prompt.py"
make_executable "script_cursor_watch.py"
make_executable "script_update_cursor_rules.py"
make_executable "script_update_functions_and_types.py"
make_executable "script_analyze_patterns.py"

# Make utils scripts executable
if [ -d "$SCRIPT_DIR/utils" ]; then
    for script in "$SCRIPT_DIR/utils"/*.py; do
        if [ -f "$script" ]; then
            echo -e "Making $(basename "$script") executable"
            chmod +x "$script"
        fi
    done
fi

# Step 4: Update the project structure
echo -e "\n${YELLOW}Step 4: Updating project structure...${NC}"

if [ -f "$SCRIPT_DIR/script_update_project_structure.py" ]; then
    echo -e "Running script_update_project_structure.py"
    python "$SCRIPT_DIR/script_update_project_structure.py"
else
    echo -e "${RED}script_update_project_structure.py not found, skipping project structure update${NC}"
fi

# Step 4.5: Update the functions and types maps
echo -e "\n${YELLOW}Step 4.5: Updating functions and types maps...${NC}"

if [ -f "$SCRIPT_DIR/script_update_functions_and_types.py" ]; then
    echo -e "Running script_update_functions_and_types.py"
    python "$SCRIPT_DIR/script_update_functions_and_types.py"
else
    echo -e "${RED}script_update_functions_and_types.py not found, skipping functions and types mapping${NC}"
fi

# Step 5: Update Cursor rules
echo -e "\n${YELLOW}Step 5: Updating Cursor rules...${NC}"

if [ -f "$SCRIPT_DIR/script_update_cursor_rules.py" ]; then
    echo -e "Running script_update_cursor_rules.py"
    python "$SCRIPT_DIR/script_update_cursor_rules.py"
else
    echo -e "${RED}script_update_cursor_rules.py not found, skipping Cursor rules update${NC}"
fi

# Step 6: Create a sample log entry
echo -e "\n${YELLOW}Step 6: Creating a sample log entry...${NC}"

if [ -f "$SCRIPT_DIR/script_message_router.py" ]; then
    echo -e "Creating sample log entry using script_message_router.py"
    
    # Create a temporary message file
    temp_message_file=$(mktemp)
    
    # Write sample message to temporary file
    cat > "$temp_message_file" << EOF
God Mode initialization complete.

[LOG_SUMMARY]Initialized God Mode system with memory files, documentation structure, and executable scripts

[LOG_DETAIL]
# God Mode Initialization

Completed the following setup steps:
- Created necessary directories for memory, documentation, discussion, and logs
- Copied templates to memory files
- Made scripts executable
- Updated project structure documentation
- Updated Cursor rules for message routing
- Set up prompt enhancement system

The system is now ready for AI-assisted development with persistent memory, automated documentation, and enhanced prompts.

[MEMORY_UPDATE]
God Mode has been initialized for this project. The memory system is active and will maintain context across sessions. The message router will automatically route messages to the appropriate files based on markers.

[FEATURE_LOG: GodMode]
Initial setup of God Mode completed with the following features:
- Memory system with specialized memory files
- Message router for automatic documentation
- Prompt enhancement for better context awareness
- Cursor rules for consistent AI responses

[DOC_UPDATE: project]
## God Mode

This project uses the God Mode enhancement for Cursor IDE, providing:
- Persistent memory across sessions
- Automated documentation
- Enhanced AI context
- Streamlined workflows
- Predictive capabilities
EOF
    
    # Process the message
    python "$SCRIPT_DIR/script_message_router.py" --input "$temp_message_file"
    
    # Remove the temporary file
    rm "$temp_message_file"
else
    echo -e "${RED}script_message_router.py not found, skipping sample log entry${NC}"
fi

# Step 7: Instructions for starting the Cursor watch script
echo -e "\n${YELLOW}Step 7: Instructions for running the Cursor watch script...${NC}"

echo -e "To automatically enhance your prompts in Cursor IDE, run:"
echo -e "  cd $SCRIPT_DIR"
echo -e "  python script_cursor_watch.py"
echo -e "This will monitor your Cursor conversations and enhance prompts with relevant context."

# Step 8: Create godmode command function
echo -e "\n${YELLOW}Step 8: Setting up godmode command function...${NC}"

# Determine the user's shell profile file
SHELL_TYPE=$(basename "$SHELL")
case "$SHELL_TYPE" in
  "bash")
    PROFILE_FILE="$HOME/.bashrc"
    ;;
  "zsh")
    PROFILE_FILE="$HOME/.zshrc"
    ;;
  *)
    echo -e "${RED}Unsupported shell type: $SHELL_TYPE. Please manually add the godmode function to your shell profile.${NC}"
    PROFILE_FILE=""
    ;;
esac

if [ -n "$PROFILE_FILE" ]; then
    echo -e "Adding godmode function to $PROFILE_FILE"
    
    # Check if the function already exists
    if grep -q "function godmode" "$PROFILE_FILE"; then
        echo -e "${YELLOW}godmode function already exists in $PROFILE_FILE. Updating...${NC}"
        # Remove the existing function
        sed -i '' '/function godmode/,/}/d' "$PROFILE_FILE" 2>/dev/null || sed -i '/function godmode/,/}/d' "$PROFILE_FILE"
    fi
    
    # Add the function to the profile file
    cat >> "$PROFILE_FILE" << 'EOL'

# God Mode function for Cursor IDE
function godmode() {
    # Store the current directory
    CURRENT_DIR=$(pwd)
    
    # Get script directory dynamically based on this function's location
    GODMODE_FUNC_LINE=$(grep -n "function godmode" "$HOME/.zshrc" 2>/dev/null || grep -n "function godmode" "$HOME/.bashrc")
    GODMODE_PROJECT_ROOT=$(echo "$GODMODE_FUNC_LINE" | grep -o "GOD_MODE_PROJECT_STARTER_TEMPLATE")
    
    if [ -z "$GODMODE_PROJECT_ROOT" ]; then
        echo "Error: Cannot determine God Mode project location"
        return 1
    fi
    
    # Construct paths
    for dir in $(find $HOME -type d -name "GOD_MODE_PROJECT_STARTER_TEMPLATE" 2>/dev/null); do
        if [ -d "$dir/god_mode/scripts" ]; then
            SCRIPT_DIR="$dir/god_mode/scripts"
            GOD_MODE_DIR="$dir/god_mode"
            PROJECT_ROOT="$dir"
            break
        fi
    done
    
    if [ -z "$SCRIPT_DIR" ]; then
        echo "Error: God Mode scripts directory not found"
        return 1
    fi
    
    # Check if a message was provided
    if [ "$#" -eq 0 ]; then
        echo "Usage: godmode \"Your message to Cursor AI\""
        return 1
    fi
    
    # Get user's message
    USER_MESSAGE="$*"
    
    # Create temp file for the message
    TEMP_MSG_FILE=$(mktemp)
    echo "$USER_MESSAGE" > "$TEMP_MSG_FILE"
    
    # Run prepare response script
    cd "$SCRIPT_DIR"
    ./script_prepare_response.sh
    
    # Enhance the prompt
    ENHANCED_PROMPT=$(python "$SCRIPT_DIR/script_enhance_prompt.py" "$USER_MESSAGE")
    
    # Copy enhanced prompt to clipboard
    echo "$ENHANCED_PROMPT" | pbcopy 2>/dev/null || echo "$ENHANCED_PROMPT" | xclip -selection clipboard 2>/dev/null || echo "$ENHANCED_PROMPT" | xsel --clipboard 2>/dev/null
    
    echo "==================================="
    echo "Enhanced prompt copied to clipboard"
    echo "==================================="
    echo "Please paste this in Cursor IDE, then after receiving the AI response:"
    echo "1. Select the entire AI response"
    echo "2. Copy it to the clipboard"
    echo "3. Run 'godmode-process' in your terminal"
    
    # Return to the original directory
    cd "$CURRENT_DIR"
}

# Process God Mode response
function godmode-process() {
    # Store the current directory
    CURRENT_DIR=$(pwd)
    
    # Find God Mode scripts directory
    for dir in $(find $HOME -type d -name "GOD_MODE_PROJECT_STARTER_TEMPLATE" 2>/dev/null); do
        if [ -d "$dir/god_mode/scripts" ]; then
            SCRIPT_DIR="$dir/god_mode/scripts"
            break
        fi
    done
    
    if [ -z "$SCRIPT_DIR" ]; then
        echo "Error: God Mode scripts directory not found"
        return 1
    fi
    
    # Run auto commit script to process the response
    cd "$SCRIPT_DIR"
    ./script_auto_commit.sh
    
    # Return to the original directory
    cd "$CURRENT_DIR"
}
EOL

    # Source the profile file to make the function available immediately
    echo -e "Sourcing $PROFILE_FILE to make the godmode function available"
    source "$PROFILE_FILE"
    
    echo -e "${GREEN}✓ godmode function has been added to your shell profile${NC}"
    echo -e "Usage:"
    echo -e "  godmode \"Your message to Cursor AI\"     # Enhance and send a message"
    echo -e "  godmode-process                         # Process AI response"
else
    echo -e "${RED}Could not determine shell profile file. Please manually add the godmode function to your shell profile.${NC}"
fi

echo -e "\n${GREEN}God Mode installation and setup complete!${NC}"
echo -e "You can now use 'godmode' to interact with Cursor AI with enhanced context and proper formatting."
echo -e "After receiving an AI response, use 'godmode-process' to process the response and update all memory files."
echo -e "\nEnjoy your enhanced AI coding experience!" 