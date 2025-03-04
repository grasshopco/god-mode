#!/usr/bin/env python3
"""
Prompt Enhancement Script

This script enhances user prompts with context from memory files, recent discussions,
project structure, and learnings. It creates a more comprehensive prompt that provides
the AI with better context awareness, making responses more accurate and "God-like."

Usage:
    python script_enhance_prompt.py --prompt "Your prompt here"
    python script_enhance_prompt.py --input prompt_file.txt
    python script_enhance_prompt.py --clipboard

The enhanced prompt will be printed to stdout and optionally copied to the clipboard.
"""

import os
import re
import sys
import json
import argparse
from pathlib import Path
import shutil
import subprocess
try:
    import pyperclip
    CLIPBOARD_AVAILABLE = True
except ImportError:
    CLIPBOARD_AVAILABLE = False

# Get the directory of this script
SCRIPT_DIR = Path(os.path.dirname(os.path.abspath(__file__)))

# Define the project root relative to this script
PROJECT_ROOT = Path(SCRIPT_DIR).parent.parent

# Define the God Mode directory
GOD_MODE_DIR = Path(SCRIPT_DIR).parent

# Define memory directories
MEMORY_DIR = GOD_MODE_DIR / "memory"
DISCUSSION_DIR = GOD_MODE_DIR / "discussion"
DOCUMENTATION_DIR = GOD_MODE_DIR / "documentation"
NOTEPADS_DIR = GOD_MODE_DIR / "notepads"

# Define key memory files
MEMORY_CURSOR_FILE = MEMORY_DIR / "MEMORY_CURSOR.md"
MEMORY_LEARNINGS_FILE = MEMORY_DIR / "memory_learnings.md"
MEMORY_LOGS_ALL_FILE = MEMORY_DIR / "memory_logs_all.md"
MEMORY_PROJECT_STRUCTURE_FILE = MEMORY_DIR / "memory_project_structure.md"
MEMORY_ARCHITECTURE_FILE = MEMORY_DIR / "memory_architecture.md"
MEMORY_CONVENTIONS_FILE = MEMORY_DIR / "memory_conventions.md"

# Define cache directory
CACHE_DIR = GOD_MODE_DIR / ".cache"
CONTEXT_CACHE_FILE = CACHE_DIR / "context_cache.json"

def ensure_directory_exists(directory):
    """Ensure a directory exists, creating it if necessary."""
    os.makedirs(directory, exist_ok=True)

def load_file_content(file_path, max_lines=100, recent_only=False):
    """
    Load content from a file.
    
    Args:
        file_path (Path): Path to the file
        max_lines (int): Maximum number of lines to read
        recent_only (bool): If True, read only the most recent entries
        
    Returns:
        str: The file content or empty string if file doesn't exist
    """
    if not file_path.exists():
        return ""
    
    try:
        with open(file_path, 'r') as f:
            if recent_only:
                # Read the entire file but extract only recent entries
                content = f.read()
                # Extract the most recent entries using pattern matching
                # This is a simplified approach - adjust based on your file formats
                entries = re.split(r'#{2,3}\s+\[\d{4}-\d{2}-\d{2}', content)
                if len(entries) > 1:
                    # Return the most recent N entries
                    return ''.join(entries[-min(3, len(entries)):])
                return content
            else:
                # Read the entire file up to max_lines
                lines = []
                for i, line in enumerate(f):
                    if i >= max_lines:
                        lines.append("... (content truncated for brevity) ...")
                        break
                    lines.append(line)
                return ''.join(lines)
    except Exception as e:
        print(f"Error reading {file_path}: {e}", file=sys.stderr)
        return ""

def get_recent_discussion_content():
    """Get content from recent discussions."""
    # Look for discussion files and get the most recent entries
    discussion_files = list(DISCUSSION_DIR.glob('**/*.md'))
    recent_content = []
    
    for file in sorted(discussion_files, key=os.path.getmtime, reverse=True)[:3]:
        content = load_file_content(file, recent_only=True)
        if content:
            recent_content.append(f"From {file.name}:\n{content}\n")
    
    return "\n".join(recent_content)

def get_project_structure():
    """Get a summary of the project structure."""
    content = load_file_content(MEMORY_PROJECT_STRUCTURE_FILE)
    if not content:
        # If project structure file doesn't exist, try to generate it
        try:
            script_path = SCRIPT_DIR / "script_update_project_structure.py"
            if script_path.exists():
                subprocess.run([sys.executable, str(script_path)], check=True)
                content = load_file_content(MEMORY_PROJECT_STRUCTURE_FILE)
        except Exception as e:
            print(f"Error generating project structure: {e}", file=sys.stderr)
    
    return content

def get_recent_changes():
    """Get a summary of recent changes from the logs."""
    content = load_file_content(MEMORY_LOGS_ALL_FILE, recent_only=True)
    return content

def get_system_context():
    """Get information about the user's system."""
    system_info = {
        "os": os.name,
        "platform": sys.platform,
        "python_version": sys.version,
    }
    
    return f"System Context: {json.dumps(system_info)}"

def should_include_file(file_name, user_query):
    """
    Determine if a file should be included in context based on the user query.
    This uses simple keyword matching - more sophisticated methods could be used.
    """
    # Define keywords that indicate relevance for each file
    file_keywords = {
        "memory_architecture.md": ["architecture", "design", "structure", "system", "components"],
        "memory_conventions.md": ["convention", "standard", "rule", "guideline", "pattern", "naming"],
        "memory_requirements.md": ["requirement", "specification", "need", "must", "should"],
        "memory_roadmap.md": ["roadmap", "plan", "future", "milestone", "release"],
        "memory_security.md": ["security", "auth", "authentication", "authorization", "encrypt"],
        "memory_performance.md": ["performance", "optimize", "speed", "efficient", "fast"],
        "memory_accessibility.md": ["accessibility", "a11y", "wcag", "aria", "screen reader"],
        "memory_testing.md": ["test", "unit test", "integration test", "e2e", "testing"],
        "memory_dependencies.md": ["dependency", "package", "library", "external", "import"],
        "memory_glossary.md": ["term", "definition", "glossary", "vocabulary", "meaning"],
    }
    
    # Normalize query for matching
    query_lower = user_query.lower()
    
    # Get keywords for the file
    keywords = file_keywords.get(os.path.basename(file_name), [])
    
    # Check if any keyword is in the query
    for keyword in keywords:
        if keyword.lower() in query_lower:
            return True
    
    return False

def get_specialized_memory_content(user_query):
    """
    Get content from specialized memory files based on the user query.
    Only includes relevant files to avoid context overload.
    """
    specialized_memory_files = list(MEMORY_DIR.glob('memory_*.md'))
    specialized_memory_files = [f for f in specialized_memory_files 
                                if f.name != "memory_logs_all.md" 
                                and f.name != "memory_logs_detailed.md"
                                and f.name != "memory_project_structure.md"]
    
    relevant_content = []
    
    for file in specialized_memory_files:
        if should_include_file(file, user_query):
            content = load_file_content(file, max_lines=50)
            if content:
                # Include a brief summary rather than the whole file
                first_lines = '\n'.join(content.split('\n')[:5])
                relevant_content.append(f"From {file.name}:\n{first_lines}\n...(content available)")
    
    return "\n".join(relevant_content)

def get_notepad_references(user_query):
    """
    Get references to relevant notepads based on the user query.
    """
    if not NOTEPADS_DIR.exists():
        return ""
    
    notepad_files = list(NOTEPADS_DIR.glob('notepad_*.md'))
    if not notepad_files:
        return ""
    
    # Map notepads to keywords
    notepad_keywords = {
        "notepad_ui_guidelines.md": ["ui", "interface", "design", "component", "style", "css"],
        "notepad_architecture.md": ["architecture", "structure", "system", "design pattern"],
        "notepad_common_patterns.md": ["pattern", "common", "standard", "reuse", "component"],
        "notepad_model_roles.md": ["model", "ai", "role", "claude", "gpt", "llm"],
        "notepad_self_review_guidelines.md": ["review", "code review", "quality", "test", "check"],
    }
    
    # Normalize query for matching
    query_lower = user_query.lower()
    
    # Find relevant notepads
    relevant_notepads = []
    for file in notepad_files:
        file_keywords = notepad_keywords.get(file.name, [])
        for keyword in file_keywords:
            if keyword.lower() in query_lower:
                relevant_notepads.append(f"@{file.stem}")
                break
    
    if relevant_notepads:
        return "Relevant notepads: " + ", ".join(relevant_notepads)
    return ""

def load_cache():
    """Load the context cache if it exists."""
    if not CONTEXT_CACHE_FILE.exists():
        return {}
    
    try:
        with open(CONTEXT_CACHE_FILE, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading cache: {e}", file=sys.stderr)
        return {}

def save_cache(cache):
    """Save the context cache."""
    ensure_directory_exists(CACHE_DIR)
    
    try:
        with open(CONTEXT_CACHE_FILE, 'w') as f:
            json.dump(cache, f, indent=2)
    except Exception as e:
        print(f"Error saving cache: {e}", file=sys.stderr)

def enhance_prompt(prompt):
    """
    Enhance a user prompt with relevant context.
    
    Args:
        prompt (str): The user's original prompt
        
    Returns:
        str: The enhanced prompt with context
    """
    # Load cache to avoid redundant context
    cache = load_cache()
    
    # Build the enhanced prompt
    enhanced_parts = [
        "# ENHANCED CONTEXT FOR USER QUERY\n",
        "## Original User Query\n",
        prompt,
        "\n\n## Project Context\n"
    ]
    
    # Add core memory content
    cursor_memory = load_file_content(MEMORY_CURSOR_FILE)
    if cursor_memory:
        enhanced_parts.append("### Core Project Memory\n")
        enhanced_parts.append(cursor_memory)
    
    # Add specialized memory content based on the query
    specialized_memory = get_specialized_memory_content(prompt)
    if specialized_memory:
        enhanced_parts.append("\n### Specialized Memory Files\n")
        enhanced_parts.append(specialized_memory)
    
    # Add recent changes
    recent_changes = get_recent_changes()
    if recent_changes:
        enhanced_parts.append("\n### Recent Changes\n")
        enhanced_parts.append(recent_changes)
    
    # Add recent discussion content
    recent_discussion = get_recent_discussion_content()
    if recent_discussion:
        enhanced_parts.append("\n### Recent Discussions\n")
        enhanced_parts.append(recent_discussion)
    
    # Add project structure summary
    if "structure" in prompt.lower() or "files" in prompt.lower() or "folders" in prompt.lower():
        project_structure = get_project_structure()
        if project_structure:
            enhanced_parts.append("\n### Project Structure\n")
            enhanced_parts.append(project_structure)
    
    # Add notepad references
    notepad_refs = get_notepad_references(prompt)
    if notepad_refs:
        enhanced_parts.append("\n### Relevant References\n")
        enhanced_parts.append(notepad_refs)
    
    # Add system context if relevant
    if "system" in prompt.lower() or "environment" in prompt.lower():
        enhanced_parts.append("\n### System Information\n")
        enhanced_parts.append(get_system_context())
    
    # Closing instruction
    enhanced_parts.append(
        "\n\n# ACTION INSTRUCTION\n"
        "Use the above context to enhance your response to the user's query.\n"
        "DO NOT mention this additional context explicitly in your response.\n"
        "Respond directly and concisely to the user's query using this additional context implicitly.\n\n"
        "When your response contains significant information, code changes, or insights, include the appropriate\n"
        "message router markers ([LOG_SUMMARY], [LOG_DETAIL], [MEMORY_UPDATE], etc.) for automatic documentation.\n"
        "\n---\n\n"
    )
    
    # The actual query the user will see the AI respond to
    enhanced_parts.append(prompt)
    
    # Update cache with this context
    cache["last_enhanced_prompt"] = "\n".join(enhanced_parts)
    save_cache(cache)
    
    return "\n".join(enhanced_parts)

def main():
    """Main function to parse arguments and enhance prompts."""
    parser = argparse.ArgumentParser(description='Enhance user prompts with relevant context.')
    
    # Create a mutually exclusive group for input sources
    input_group = parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument('--prompt', help='The prompt to enhance')
    input_group.add_argument('--input', help='Input file containing the prompt')
    input_group.add_argument('--clipboard', action='store_true', help='Read the prompt from clipboard')
    
    # Output options
    parser.add_argument('--copy', action='store_true', 
                        help='Copy the enhanced prompt to clipboard')
    parser.add_argument('--output', help='Output file for the enhanced prompt')
    
    args = parser.parse_args()
    
    # Get the prompt from the appropriate source
    if args.prompt:
        prompt = args.prompt
    elif args.input:
        try:
            with open(args.input, 'r') as f:
                prompt = f.read()
        except Exception as e:
            print(f"Error reading input file: {e}", file=sys.stderr)
            return 1
    elif args.clipboard:
        if not CLIPBOARD_AVAILABLE:
            print("Clipboard functionality requires pyperclip. Install with: pip install pyperclip", 
                  file=sys.stderr)
            return 1
        prompt = pyperclip.paste()
    
    # Enhance the prompt
    enhanced_prompt = enhance_prompt(prompt)
    
    # Output the enhanced prompt
    if args.output:
        try:
            with open(args.output, 'w') as f:
                f.write(enhanced_prompt)
            print(f"Enhanced prompt written to {args.output}")
        except Exception as e:
            print(f"Error writing to output file: {e}", file=sys.stderr)
            return 1
    else:
        print(enhanced_prompt)
    
    # Copy to clipboard if requested
    if args.copy:
        if not CLIPBOARD_AVAILABLE:
            print("Clipboard functionality requires pyperclip. Install with: pip install pyperclip", 
                  file=sys.stderr)
            return 1
        pyperclip.copy(enhanced_prompt)
        print("Enhanced prompt copied to clipboard.")
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 