# God Mode Quickstart Guide

This quickstart guide will help you set up and start using God Mode with your Cursor IDE for enhanced AI-assisted development capabilities.

## Initial Setup

1. Open this project in Cursor IDE:
   ```bash
   cursor /path/to/project
   ```

2. Run the God Mode initialization script:
   ```bash
   bash start_god_mode.sh
   ```

3. This will:
   - Set up the necessary directory structure
   - Create required memory files
   - Configure Cursor with enhanced rules
   - Start memory/logging systems

## Key Components

### Memory System
God Mode maintains a persistent memory system through various specialized files:
- `memory/MEMORY_CURSOR.md`: Core memory file for project context
- `memory/memory_project_structure.md`: Map of the project structure
- `memory/memory_functions.md`: Documentation of all functions in the codebase
- `memory/memory_types.md`: Documentation of all types in the codebase
- Various specialized memory files (architecture, requirements, learnings, etc.)

### Logging System
Track all changes and decisions with the comprehensive logging system:
- `memory/memory_logs_all.md`: Brief summary of all changes
- `memory/memory_logs_detailed.md`: Detailed explanations of changes
- `memory/logs/features/`: Feature-specific logs with comprehensive information

### Documentation System
Create and maintain documentation with specialized templates:
- `templates/`: Templates for various documentation types
- `documentation/`: Project documentation organized by domain

### Enhanced Scripts
Use these scripts to enhance your God Mode experience:

#### Core Functionality
- `scripts/script_update_project_structure.py`: Update the project structure map with file descriptions
- `scripts/script_update_functions_and_types.py`: Update the functions and types documentation
- `scripts/script_message_router.py`: Route tagged message content to appropriate files

#### Enhanced Quality
- `scripts/script_enhance_message_content.py`: Ensure log entries have meaningful content
- `scripts/script_check_feature_logs.py`: Validate and fix feature logs against template

#### Project Management
- `scripts/script_generate_roadmap.py`: Generate roadmap files from template
- `scripts/script_session_continuity.py`: Maintain continuity between chat sessions

## Using God Mode

### In Your Conversations
Include special tags in your AI responses to route information to the right files:

```
[LOG_SUMMARY]
Brief summary of changes (1-2 sentences)

[LOG_DETAIL]
Detailed explanation of changes with reasons and approach

[MEMORY_UPDATE]
Important information to remember for future sessions
```

For specialized memory types, use tags like:
```
[MEMORY_ARCHITECTURE]
Architecture decisions and patterns

[MEMORY_LEARNINGS]
Lessons learned and insights
```

### Session Management
To maintain continuity between chat sessions:

1. Generate a session summary before ending your current session:
   ```bash
   python god_mode/scripts/script_session_continuity.py
   ```

2. When starting a new session, use the generated prompt to provide context:
   ```bash
   python god_mode/scripts/script_session_continuity.py --output restart_prompt.txt
   ```

3. Copy the contents of `restart_prompt.txt` into your new chat session

### Project Management
Generate roadmap and planning documents:

```bash
python god_mode/scripts/script_generate_roadmap.py --title "Sprint Planning"
```

## Troubleshooting

If you encounter issues with empty log entries:
```bash
python god_mode/scripts/script_enhance_message_content.py --audit
```

If feature logs aren't following the template:
```bash
python god_mode/scripts/script_check_feature_logs.py --fix
```

If project structure lacks file descriptions:
```bash
python god_mode/scripts/script_update_project_structure.py
```

## Advanced Usage

For advanced usage, including remote control and CI integration, see the full README.md file.

## Essential Commands for Beginners

### Directory Navigation
```bash
# Move up one directory level (to parent)
cd ..

# Move into a specific directory
cd directory_name

# Show current directory
pwd

# List files in current directory
ls
```

### Running God Mode
```bash
# Start God Mode (run from God Mode project directory)
./start_god_mode.sh

# Control God Mode remotely (run from parent directory)
./god_mode_remote.sh
```

### If You Get Lost
If you find yourself in the wrong directory or are unsure where you are:

1. Run `pwd` to see your current location
2. Navigate to the parent directory with `cd ..`
3. Run `ls` to see available files and directories
4. Use `./god_mode_remote.sh` from the parent directory to control God Mode

### Common Issues
- **"Command not found"**: Make sure you're in the correct directory
- **"Permission denied"**: Run `chmod +x filename.sh` to make scripts executable
- **Message Router not working**: Install dependencies with `pip install pyperclip plyer`

### Manually Restart Message Router
If you need to manually restart the Message Router:
```bash
# Navigate to the scripts directory
cd god_mode/scripts

# Run the route script in watch mode
./route --watch
```

### Getting Help
If you need more detailed information:
1. Check the main README.md for comprehensive documentation
2. Look in the god_mode/system_documentation/ folder for system guides
3. Use the `h` option in the remote control menu for help with specific features 