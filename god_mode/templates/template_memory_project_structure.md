# Project Structure

This document maps the entire project codebase, providing descriptions of directories and key files to help navigate the project.

## Root Directory

- `app/`: Main application code
- `.cursor/`: Cursor IDE configuration
  - `rules/`: Directory-specific rules for the AI assistant
  - `.cursorrules`: Master rules file with instructions for AI assistance
- `god_mode/`: Resources for AI-assisted development
  - `memory/`: Directory containing memory files for the AI assistant
    - `memory_project_structure.md`: Map of all folders and files with descriptions (this file)
    - `memory_logs_all.md`: Master log file with summarized entries of all AI changes
    - `memory_logs_detailed.md`: Detailed logs with comprehensive explanations of changes
    - `MEMORY_CURSOR.md`: Central file for recording architectural decisions and coding guidelines
    - `memory_learnings.md`: File for tracking lessons learned and insights
  - `templates/`: Directory containing templates for various file types
  - `notepads/`: Directory containing specialized notepad files for reference
  - `scripts/`: Directory containing automation scripts
    - `utils/`: Utility scripts used by other scripts
  - `documentation/`: Directory containing project documentation
  - `discussion/`: Directory containing discussion notes
  - `prompts_and_thinking_models/`: Directory containing AI prompts and thinking models
  - `instructions/`: Directory containing setup and usage instructions
  - `issues/`: Directory for tracking project issues
  - `project_setup/`: Directory containing project setup scripts and configuration

## Development Workflow

### Key Files for Development

- `.cursor/rules/*.mdc`: AI assistant rules for specific file types
- `.cursor/.cursorrules`: Master rules file with instructions for AI assistance
- `god_mode/memory/MEMORY_CURSOR.md`: Project memory for AI context
- `god_mode/memory/memory_project_structure.md`: This file, for navigation
- `god_mode/notepads/`: Reference documentation
- `god_mode/scripts/`: Automation scripts

### Logging System

- `god_mode/memory/memory_logs_all.md`: Summary logs
- `god_mode/memory/memory_logs_detailed.md`: Detailed logs
- `god_mode/memory/memory_log_feature_*.md`: Feature-specific logs

---

*This document will be continuously updated as the project evolves. The AI assistant will maintain it to ensure it accurately reflects the current state of the codebase.* 