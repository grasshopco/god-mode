#!/bin/bash

# script_check_memory_files.sh
# This script checks if all required memory files exist, and creates them from templates if they don't.
# It should be run:
# 1. During initialization
# 2. Every time the remote control script is run
# 3. Whenever memory file integrity needs to be verified

# Set colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Get the directory of this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
GOD_MODE_DIR="$(dirname "$SCRIPT_DIR")"
PROJECT_ROOT="$(dirname "$GOD_MODE_DIR")"

echo -e "${YELLOW}Checking for missing memory files...${NC}"

# Function to create directory if it doesn't exist
create_dir_if_not_exists() {
    if [ ! -d "$1" ]; then
        echo -e "Creating directory: $1"
        mkdir -p "$1"
    fi
}

# Ensure memory directory exists
create_dir_if_not_exists "$GOD_MODE_DIR/memory"

# Function to copy template to memory file if it doesn't exist
copy_template_to_memory() {
    template_file="$GOD_MODE_DIR/templates/$1"
    memory_file="$GOD_MODE_DIR/memory/$2"
    
    if [ -f "$template_file" ] && [ ! -f "$memory_file" ]; then
        echo -e "${GREEN}Creating missing memory file:${NC} $2"
        cp "$template_file" "$memory_file"
        return 0
    elif [ ! -f "$template_file" ]; then
        echo -e "${RED}Warning: Template file $1 not found${NC}"
        return 2
    else
        # File exists, do nothing
        return 1
    fi
}

# Array to track created files
created_files=()

# Basic memory files (essential)
copy_template_to_memory "template_memory_project_structure.md" "memory_project_structure.md"
[ $? -eq 0 ] && created_files+=("memory_project_structure.md")

copy_template_to_memory "template_memory_logs_all.md" "memory_logs_all.md"
[ $? -eq 0 ] && created_files+=("memory_logs_all.md")

copy_template_to_memory "template_memory_logs_detailed.md" "memory_logs_detailed.md"
[ $? -eq 0 ] && created_files+=("memory_logs_detailed.md")

copy_template_to_memory "template_memory_learnings.md" "memory_learnings.md"
[ $? -eq 0 ] && created_files+=("memory_learnings.md")

copy_template_to_memory "template_MEMORY_CURSOR.md" "MEMORY_CURSOR.md"
[ $? -eq 0 ] && created_files+=("MEMORY_CURSOR.md")

# Extended memory files
copy_template_to_memory "template_MEMORY_UPDATES.md" "memory_updates.md"
[ $? -eq 0 ] && created_files+=("memory_updates.md")

copy_template_to_memory "template_MEMORY_REQUIREMENTS.md" "memory_requirements.md"
[ $? -eq 0 ] && created_files+=("memory_requirements.md")

copy_template_to_memory "template_MEMORY_ROADMAP.md" "memory_roadmap.md"
[ $? -eq 0 ] && created_files+=("memory_roadmap.md")

copy_template_to_memory "template_MEMORY_ARCHITECTURE.md" "memory_architecture.md"
[ $? -eq 0 ] && created_files+=("memory_architecture.md")

copy_template_to_memory "template_MEMORY_CONVENTIONS.md" "memory_conventions.md"
[ $? -eq 0 ] && created_files+=("memory_conventions.md")

copy_template_to_memory "template_MEMORY_DEPENDENCIES.md" "memory_dependencies.md"
[ $? -eq 0 ] && created_files+=("memory_dependencies.md")

copy_template_to_memory "template_MEMORY_GLOSSARY.md" "memory_glossary.md"
[ $? -eq 0 ] && created_files+=("memory_glossary.md")

copy_template_to_memory "template_MEMORY_TESTING.md" "memory_testing.md"
[ $? -eq 0 ] && created_files+=("memory_testing.md")

copy_template_to_memory "template_MEMORY_SECURITY.md" "memory_security.md"
[ $? -eq 0 ] && created_files+=("memory_security.md")

copy_template_to_memory "template_MEMORY_PERFORMANCE.md" "memory_performance.md"
[ $? -eq 0 ] && created_files+=("memory_performance.md")

copy_template_to_memory "template_MEMORY_ACCESSIBILITY.md" "memory_accessibility.md"
[ $? -eq 0 ] && created_files+=("memory_accessibility.md")

# Now create any notepads from templates if they don't exist
create_dir_if_not_exists "$GOD_MODE_DIR/notepads"

# Function to copy template to notepad file if it doesn't exist
copy_template_to_notepad() {
    template_file="$GOD_MODE_DIR/templates/$1"
    notepad_file="$GOD_MODE_DIR/notepads/$2"
    
    if [ -f "$template_file" ] && [ ! -f "$notepad_file" ]; then
        echo -e "${GREEN}Creating missing notepad file:${NC} $2"
        cp "$template_file" "$notepad_file"
        return 0
    elif [ ! -f "$template_file" ]; then
        echo -e "${RED}Warning: Template file $1 not found${NC}"
        return 2
    else
        # File exists, do nothing
        return 1
    fi
}

# Copy notepad templates
copy_template_to_notepad "template_notepad_architecture.md" "notepad_architecture.md"
[ $? -eq 0 ] && created_files+=("notepads/notepad_architecture.md")

copy_template_to_notepad "template_notepad_common_patterns.md" "notepad_common_patterns.md"
[ $? -eq 0 ] && created_files+=("notepads/notepad_common_patterns.md")

copy_template_to_notepad "template_notepad_model_roles.md" "notepad_model_roles.md"
[ $? -eq 0 ] && created_files+=("notepads/notepad_model_roles.md")

copy_template_to_notepad "template_notepad_self_review_guidelines.md" "notepad_self_review_guidelines.md"
[ $? -eq 0 ] && created_files+=("notepads/notepad_self_review_guidelines.md")

copy_template_to_notepad "template_notepad_ui_guidelines.md" "notepad_ui_guidelines.md"
[ $? -eq 0 ] && created_files+=("notepads/notepad_ui_guidelines.md")

# Check if we created any new files
if [ ${#created_files[@]} -eq 0 ]; then
    echo -e "${GREEN}All memory files exist.${NC}"
else
    echo -e "${GREEN}Created ${#created_files[@]} missing memory files:${NC}"
    for file in "${created_files[@]}"; do
        echo -e "  - $file"
    done
    
    # Update project structure if needed
    if [ -f "$SCRIPT_DIR/script_update_project_structure.py" ]; then
        echo -e "\n${YELLOW}Updating project structure to include new files...${NC}"
        python "$SCRIPT_DIR/script_update_project_structure.py"
    fi
fi

# Check for system_documentation folder and ensure it has required files
create_dir_if_not_exists "$GOD_MODE_DIR/system_documentation"

# Copy any project documentation files to system_documentation if they exist and haven't been copied yet
if [ -f "$GOD_MODE_DIR/documentation/documentation_project/documentation_message_router_usage.md" ] && [ ! -f "$GOD_MODE_DIR/system_documentation/documentation_message_router_usage.md" ]; then
    echo -e "${GREEN}Moving message router usage documentation to system_documentation${NC}"
    cp "$GOD_MODE_DIR/documentation/documentation_project/documentation_message_router_usage.md" "$GOD_MODE_DIR/system_documentation/"
fi

if [ -f "$GOD_MODE_DIR/documentation/documentation_project/documentation_multi_tag_feature.md" ] && [ ! -f "$GOD_MODE_DIR/system_documentation/documentation_multi_tag_feature.md" ]; then
    echo -e "${GREEN}Moving multi-tag feature documentation to system_documentation${NC}"
    cp "$GOD_MODE_DIR/documentation/documentation_project/documentation_multi_tag_feature.md" "$GOD_MODE_DIR/system_documentation/"
fi

echo -e "${GREEN}Memory file check complete.${NC}" 