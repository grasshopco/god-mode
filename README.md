# Cursor IDE God Mode Template

This repository contains a template for setting up "God Mode" in Cursor IDE, a powerful enhancement that transforms Cursor from a simple AI coding assistant into an autonomous development partner with persistent memory, automated documentation, and advanced AI capabilities.

## What is God Mode?

God Mode is a set of configurations, scripts, and templates that enhance Cursor IDE's AI capabilities by:

1. **Providing Persistent Memory**: The AI maintains context across sessions through structured memory files
2. **Automating Documentation**: Changes are automatically logged and project structure is tracked
3. **Enhancing AI Context**: Specialized notepads provide domain-specific knowledge
4. **Streamlining Workflows**: Templates and scripts automate repetitive tasks
5. **Enabling Advanced Features**: Configuration for autonomous coding, self-review, and continuous improvement
6. **GitHub Integration**: Seamless version control with automatic commits and repository management

## Repository Structure

- `.cursor/`: Cursor IDE configuration files
  - `rules/`: Directory-specific rules for the AI assistant
  - `.cursorrules`: Master rules file with instructions for AI assistance

- `god_mode/`: Resources for AI-assisted development
  - `memory/`: Persistent memory files for the AI assistant
    - `continuity/`: Session continuity summaries for context persistence
  - `templates/`: Templates for various file types
  - `notepads/`: Specialized notepad files for reference
  - `scripts/`: Automation scripts
  - `documentation/`: Project documentation
  - `discussion/`: Discussion notes
  - `prompts_and_thinking_models/`: AI prompts and thinking models
  - `instructions/`: Setup and usage instructions
  - `roadmap/`: Project roadmaps and enhancement plans

- `app/`: Placeholder for your application code

## Getting Started

### Prerequisites

- [Cursor IDE](https://cursor.sh/) installed
- Basic familiarity with AI-assisted development

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/cursor-god-mode-template.git your-project-name
   cd your-project-name
   ```

2. Initialize the God Mode system:
   ```bash
   cd god_mode/scripts
   chmod +x script_initialize_god_mode.sh
   ./script_initialize_god_mode.sh
   ```

3. Open the project in Cursor IDE:
   ```bash
   cursor .
   ```

### Initial Setup

1. Update the `MEMORY_CURSOR.md` file with your project's specific details
2. Run the project structure update script to generate an accurate map of your codebase:
   ```bash
   python god_mode/scripts/script_update_project_structure.py
   ```

3. Review and customize the templates in `god_mode/templates/` to match your project's needs

## Using God Mode

### Memory System

The memory system consists of several key files:

- `god_mode/memory/MEMORY_CURSOR.md`: Central memory file for project context
- `god_mode/memory/memory_project_structure.md`: Map of the project structure
- `god_mode/memory/memory_logs_all.md`: Summary of all changes
- `god_mode/memory/memory_logs_detailed.md`: Detailed explanations of changes
- `god_mode/memory/memory_learnings.md`: Lessons learned during development

### Notepads

Reference these specialized notepads in your prompts using @ mentions:

- `@notepad_architecture`: System architecture overview
- `@notepad_common_patterns`: Recurring code patterns
- `@notepad_model_roles`: AI model specializations
- `@notepad_self_review_guidelines`: Code review criteria
- `@notepad_ui_guidelines`: UI design principles

Example: "Please create a new component following the patterns in @notepad_common_patterns"

### Automation Scripts

- `script_update_project_structure.py`: Updates the project structure documentation
- `script_message_router.py`: Routes AI outputs to appropriate documentation files
- `script_enhance_message_content.py`: Ensures memory files have meaningful content
- `script_check_feature_logs.py`: Validates and fixes feature logs against template
- `script_session_continuity.py`: Maintains context between chat sessions
- `script_generate_roadmap.py`: Creates comprehensive roadmap documents
- `script_test_god_mode.py`: Verifies all God Mode components are working
- `script_auto_commit.sh`: Automatically commits changes to Git repository
- `script_auto_iteration.sh`: Enables continuous improvement loops
- `script_update_rules.sh`: Updates Cursor rules based on project evolution

### Enhanced Features

#### Automatic Git Integration

God Mode now includes automatic Git repository integration:

```bash
# Run the auto-commit script manually
./god_mode/scripts/script_auto_commit.sh

# With a custom commit message
./god_mode/scripts/script_auto_commit.sh "Your custom commit message"
```

The script will:
- Initialize a Git repository if one doesn't exist
- Automatically generate commit messages based on recent log entries
- Commit all changes to the repository
- Push to remote if configured

#### Session Continuity

God Mode now includes a powerful session continuity system that helps maintain context between chat sessions:

1. Generate a session summary before ending your current session:
   ```bash
   python god_mode/scripts/script_session_continuity.py
   ```

2. When starting a new session, use the generated prompt to provide context:
   ```bash
   python god_mode/scripts/script_session_continuity.py --output restart_prompt.txt
   ```

3. Copy the contents of `restart_prompt.txt` into your new chat session

#### Project Management

Generate roadmap and planning documents:
```bash
python god_mode/scripts/script_generate_roadmap.py --title "Sprint Planning"
```

#### System Verification

Verify all God Mode components are working properly:
```bash
python god_mode/scripts/script_test_god_mode.py
```

This script runs tests on all major components:
- Project structure generator
- Message content enhancer
- Feature log template validator
- Session continuity system
- Roadmap generator
- Message routing system

#### Troubleshooting

If you encounter issues with memory files:
```bash
python god_mode/scripts/script_enhance_message_content.py --audit
```

If feature logs aren't following the template:
```bash
python god_mode/scripts/script_check_feature_logs.py --fix
```

### Message Router

The message router script automatically processes AI outputs and routes them to the appropriate files based on special markers:

```
[LOG_SUMMARY]This is a summary entry

[LOG_DETAIL]
This is a detailed explanation

[MEMORY_UPDATE]
This is an update to the memory

[FEATURE_LOG: FeatureName]
This is a feature-specific log entry

[DOC_UPDATE: DocumentType]
This is a documentation update
```

To use the message router:
```bash
cd god_mode/scripts
./route --clipboard  # Process clipboard content
./route --watch      # Watch clipboard for changes
```

## 🔄 Version Control Integration

God Mode now includes built-in Git integration to help you manage your project's version control:

### Automatic Commits

The system can automatically commit your changes to Git after each significant update. This ensures your work is always saved and tracked.

- **Auto-Commit Script**: Located at `god_mode/scripts/script_auto_commit.sh`
- **Usage**: `./god_mode/scripts/script_auto_commit.sh "Your commit message"`
- **Features**:
  - Automatically detects changes in your project
  - Creates meaningful commit messages based on recent log entries
  - Handles pushing to remote repositories when configured

### GitHub Repository Setup

Setting up a GitHub repository for your God Mode project is now easier than ever with enhanced repository management features:

- **GitHub Management CLI**: Easy-to-use hierarchical menu for all GitHub operations
- **Usage**: Select option 'g' from the main menu or run `./god_mode/scripts/script_setup_github.sh --menu`
- **Features**:
  - Create new GitHub repositories
  - Connect to existing repositories
  - Switch between multiple repositories
  - Configure Git user information
  - Handle repository conflicts intelligently
  - Interactive setup process
  - Manages pushing and merging with remote repositories

### CLI Integration

The God Mode remote control menu now includes a dedicated Version Control section with:

- **GitHub Repository Management**: Setup, connect, or switch GitHub repositories
- **Auto-commit Changes**: Manually trigger an auto-commit

All version control operations are now organized in a hierarchical menu system that makes them easy to find and use, even for beginners.

## Multi-Project Workflow

For developers who work with multiple projects and prefer to maintain their workspace context, God Mode offers a remote control option that allows you to manage God Mode in a project subdirectory without having to switch Cursor IDE contexts.

### Setting Up the Remote Control

1. Install the remote control script in your parent directory:
   ```bash
   cd GOD_MODE_PROJECT_STARTER_TEMPLATE/god_mode/scripts
   ./script_install_parent_remote.sh
   ```

2. This will create a `god_mode_remote.sh` script in your parent directory.

3. Make it executable if needed:
   ```bash
   chmod +x ../../../god_mode_remote.sh
   ```

### Using the Remote Control

From your parent directory, run:
```bash
./god_mode_remote.sh
```

This interactive menu allows you to:
- Start/stop God Mode in your project
- View God Mode status
- Process clipboard content
- View logs
- Update project structure
- Update Cursor rules
- Navigate to the project directory
- Switch between different God Mode projects

You can also specify a different target project:
```bash
./god_mode_remote.sh other_project_with_god_mode
```

### Benefits of the Multi-Project Workflow

- Maintain your Cursor IDE context in the parent directory
- Control God Mode in multiple projects without context switching
- Access God Mode features without changing directories
- Keep chat history intact in your main workspace

## Customization

### Adding New Templates

1. Create a new template file in `god_mode/templates/`
2. Reference it in your prompts using the template name

### Extending God Mode

1. Add new scripts to `god_mode/scripts/`
2. Update the `.cursorrules` file to include new capabilities
3. Create new notepads for specialized knowledge

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- The Cursor IDE team for creating an amazing AI-powered code editor
- The AI community for continuous innovation in developer tools 