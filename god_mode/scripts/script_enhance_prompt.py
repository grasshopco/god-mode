#!/usr/bin/env python3
"""
Prompt Enhancement Script

This script enhances user prompts with context from memory files, recent discussions,
project structure, and learnings. It creates a more comprehensive prompt that provides
the AI with better context awareness, making responses more accurate and "God-like."

It now also includes TAG system reinforcement to ensure consistent TAG usage in AI responses.

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
import datetime
import random
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
MEMORY_TAG_METRICS_FILE = MEMORY_DIR / "memory_tag_metrics.md"

# Define cache directory
CACHE_DIR = GOD_MODE_DIR / ".cache"
CONTEXT_CACHE_FILE = CACHE_DIR / "context_cache.json"
TAG_CONFIG_FILE = CACHE_DIR / "tag_config.json"

# Attempt to import the tag feedback module
try:
    # First, try to import as a module
    sys.path.insert(0, str(SCRIPT_DIR))
    from script_tag_feedback import analyze_compliance, update_tag_config, ensure_metrics_file
    TAG_FEEDBACK_AVAILABLE = True
except ImportError:
    # If that fails, define simplified versions of the functions
    TAG_FEEDBACK_AVAILABLE = False
    
    def analyze_compliance():
        """Simplified version if tag_feedback module is not available"""
        return 0.5, "flat"
    
    def update_tag_config(compliance_rate, trend):
        """Simplified version if tag_feedback module is not available"""
        return {"reminder_level": "normal", "check_frequency": 1.0}
    
    def ensure_metrics_file():
        """Simplified version if tag_feedback module is not available"""
        return False

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
    """Get system context information."""
    system_info = []
    
    # Try to get OS info
    try:
        if os.name == 'posix':
            # Unix/Linux/MacOS
            system_info.append(f"OS: {os.uname().sysname} {os.uname().release}")
        elif os.name == 'nt':
            # Windows
            system_info.append(f"OS: Windows {os.environ.get('OS', 'Unknown')}")
    except:
        system_info.append("OS: Unknown")
    
    # Add Python version
    system_info.append(f"Python: {sys.version.split()[0]}")
    
    return "\n".join(system_info)

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

def check_tag_compliance():
    """
    Check if recent responses have been using TAGs properly
    
    Returns:
        tuple: (compliance_rate, trend, config)
    """
    # Use tag_feedback module if available
    if TAG_FEEDBACK_AVAILABLE:
        compliance_rate, trend = analyze_compliance()
        config = update_tag_config(compliance_rate, trend)
        return compliance_rate, trend, config
    
    # Simplified version if module not available
    # Check if the metrics file exists
    if not MEMORY_TAG_METRICS_FILE.exists():
        return 0.5, "flat", {"reminder_level": "normal", "check_frequency": 1.0}
    
    # Read the last few entries
    try:
        with open(MEMORY_TAG_METRICS_FILE, 'r') as f:
            lines = f.readlines()
        
        # Extract and count compliant entries
        entries = [line for line in lines if "| " in line and " | " in line][-5:]
        if not entries:
            return 0.5, "flat", {"reminder_level": "normal", "check_frequency": 1.0}
        
        compliant_count = sum(1 for entry in entries if "✅" in entry)
        compliance_rate = compliant_count / len(entries)
        
        # Determine reminder level
        if compliance_rate < 0.3:
            reminder_level = "severe"
        elif compliance_rate < 0.7:
            reminder_level = "normal"
        else:
            reminder_level = "mild"
        
        config = {
            "reminder_level": reminder_level,
            "check_frequency": 1.0 if reminder_level == "severe" else 0.7 if reminder_level == "normal" else 0.3
        }
        
        return compliance_rate, "flat", config
    except Exception as e:
        print(f"Error checking tag compliance: {e}")
        return 0.5, "flat", {"reminder_level": "normal", "check_frequency": 1.0}

def get_tag_reminder(reminder_level):
    """
    Get a TAG reminder based on the specified level
    
    Args:
        reminder_level (str): The severity of the reminder ("mild", "normal", "severe")
        
    Returns:
        str: The reminder text
    """
    tag_examples = [
        "[LOG_SUMMARY]\nBrief summary of changes (1-2 sentences).\n",
        "[LOG_DETAIL]\nDetailed explanation of changes:\n- What was changed\n- Why it was necessary\n- How it improves the system\n",
        "[MEMORY_UPDATE]\nKey architectural decisions or context that should be remembered for future work.\n",
        "[FEATURE_LOG: FeatureName]\nFeature-specific updates and progress.\n",
        "[MULTI_TAG: LOG_SUMMARY, MEMORY_ARCHITECTURE]\nContent that should be routed to multiple destinations.\n"
    ]
    
    # Choose an example randomly
    example = random.choice(tag_examples)
    
    if reminder_level == "severe":
        return f"""
⚠️ CRITICAL REMINDER: You MUST use the proper TAG format in your response! ⚠️

Every significant response MUST include at minimum:

[LOG_SUMMARY]
Brief summary (1-2 sentences)

[LOG_DETAIL]
Comprehensive explanation

[MEMORY_UPDATE]
Key architectural decisions

You can also use specialized tags like [FEATURE_LOG: FeatureName] or [MULTI_TAG: TAG1, TAG2, ...].

Example format:
{example}

Without these tags, your response cannot be properly processed by the God Mode system!
"""
    elif reminder_level == "normal":
        return f"""
REMINDER: Please include the required TAGs in your response:

[LOG_SUMMARY] - Brief summary of the changes (1-2 sentences)
[LOG_DETAIL] - Comprehensive explanation
[MEMORY_UPDATE] - Key architectural decisions and context

Example format:
{example}

These TAGs ensure your response is properly processed by the God Mode system.
"""
    else:  # mild
        return f"""
Note: Remember to use TAGs in your response ([LOG_SUMMARY], [LOG_DETAIL], [MEMORY_UPDATE], etc.).
"""

def generate_predictive_questions(user_query):
    """
    Generate predictive follow-up questions based on the user's query.
    
    Args:
        user_query (str): The user's original query
        
    Returns:
        str: A set of 2-4 predictive questions that might be relevant to the user's current task
    """
    # Common follow-up patterns based on query types
    feature_questions = [
        "Would you like me to implement this feature now?",
        "Should I create tests for this feature as well?",
        "Is there a specific part of this feature you'd like me to focus on first?",
        "Are there any specific requirements or constraints for this implementation?",
        "Would you like to see a sample implementation before proceeding with the full feature?"
    ]
    
    bug_questions = [
        "Would you like me to debug this issue further?",
        "Should I create a fix for this bug?",
        "Would you like to see the root cause analysis in more detail?",
        "Should I suggest ways to prevent similar bugs in the future?",
        "Would you like me to implement additional error handling for this case?"
    ]
    
    explanation_questions = [
        "Would you like me to explain any particular part in more detail?",
        "Would you like to see some code examples to illustrate this concept?",
        "Is there a specific aspect of this explanation that needs clarification?",
        "Would you like me to relate this to another part of your project?",
        "Should I provide alternative approaches or just focus on this one?"
    ]
    
    architectural_questions = [
        "Would you like me to suggest improvements to the current architecture?",
        "Should I create a diagram to illustrate this architecture?",
        "Would you like me to implement this architectural change?",
        "Are there specific performance concerns I should address in this design?",
        "Should we consider how this architecture would scale for future requirements?"
    ]
    
    general_questions = [
        "Is there anything specific about this you'd like me to elaborate on?",
        "Would you like me to continue with the next steps?",
        "Is this approach aligned with what you had in mind?",
        "Would you prefer a different approach to solving this problem?",
        "Do you want me to make any changes to the implementation we discussed?"
    ]
    
    # Determine the type of query
    query_lower = user_query.lower()
    question_pool = general_questions
    
    if any(word in query_lower for word in ["implement", "create", "add", "build", "develop", "feature"]):
        question_pool = feature_questions
    elif any(word in query_lower for word in ["bug", "error", "fix", "issue", "problem", "crash", "exception"]):
        question_pool = bug_questions
    elif any(word in query_lower for word in ["explain", "how", "why", "what is", "understand", "clarify"]):
        question_pool = explanation_questions
    elif any(word in query_lower for word in ["architecture", "design", "structure", "pattern", "organization"]):
        question_pool = architectural_questions
    
    # Randomly select 2-4 questions from the appropriate pool
    num_questions = random.randint(2, 4)
    selected_questions = random.sample(question_pool, min(num_questions, len(question_pool)))
    
    # Format the questions
    return "\n\nPredictive Follow-up Questions:\n" + "\n".join(f"• {q}" for q in selected_questions)

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
    
    # Check TAG compliance and determine if a reminder is needed
    compliance_rate, trend, config = check_tag_compliance()
    should_add_reminder = random.random() < config["check_frequency"]
    
    # Build the enhanced prompt
    enhanced_parts = []
    
    # Add TAG reminder if needed
    if should_add_reminder:
        tag_reminder = get_tag_reminder(config["reminder_level"])
        enhanced_parts.append(tag_reminder)
    
    # Continue with regular enhancement
    enhanced_parts.extend([
        "# ENHANCED CONTEXT FOR USER QUERY\n",
        "## Original User Query\n",
        prompt,
        "\n\n## Project Context\n"
    ])
    
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
    
    # Closing instruction with emphasize on TAGs if compliance is low
    tag_instruction = ""
    if compliance_rate < 0.7:
        tag_instruction = (
            "IMPORTANT: You MUST include the appropriate message router markers in your response:\n"
            "- [LOG_SUMMARY] - Brief summary (1-2 sentences)\n"
            "- [LOG_DETAIL] - Comprehensive explanation\n"
            "- [MEMORY_UPDATE] - Key architectural decisions\n"
            "- Any specialized tags as needed (e.g., [FEATURE_LOG: FeatureName])\n"
            "- Remember the [MULTI_TAG: TAG1, TAG2, ...] format for routing to multiple destinations\n\n"
        )
    
    enhanced_parts.append(
        "\n\n# ACTION INSTRUCTION\n"
        "Use the above context to enhance your response to the user's query.\n"
        "DO NOT mention this additional context explicitly in your response.\n"
        "Respond directly and concisely to the user's query using this additional context implicitly.\n\n"
        f"{tag_instruction}"
        "When your response contains significant information, code changes, or insights, include the appropriate\n"
        "message router markers ([LOG_SUMMARY], [LOG_DETAIL], [MEMORY_UPDATE], etc.) for automatic documentation.\n"
        "\n"
        "IMPORTANT: You must think ahead and be predictive in your responses. Always conclude your response with \n"
        "2-4 relevant follow-up questions that anticipate the user's next needs or potential questions.\n"
        "These questions should help guide the conversation forward and demonstrate that you're thinking\n"
        "several steps ahead of the current request.\n"
        "\n---\n\n"
    )
    
    # The actual query the user will see the AI respond to
    enhanced_parts.append(prompt)
    
    # Add predictive questions to the end of the prompt
    predictive_questions = generate_predictive_questions(prompt)
    enhanced_parts.append(predictive_questions)
    
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