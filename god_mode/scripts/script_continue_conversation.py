#!/usr/bin/env python3
"""
Conversation Continuation Script

This script makes it easy to continue conversations with the AI assistant.
It provides a quick way to send follow-up responses without having to manually
copy and paste questions or navigate to different interfaces.

Usage:
    python script_continue_conversation.py                      # Use preset questions
    python script_continue_conversation.py --custom "Your question" # Ask a custom question
"""

import os
import sys
import json
import argparse
import subprocess
import random
from pathlib import Path

# Get the directory of this script
SCRIPT_DIR = Path(os.path.dirname(os.path.abspath(__file__)))

# Define the project root relative to this script
PROJECT_ROOT = Path(SCRIPT_DIR).parent.parent

# Define the God Mode directory
GOD_MODE_DIR = Path(SCRIPT_DIR).parent

# Define the cache directory
CACHE_DIR = GOD_MODE_DIR / ".cache"
CONVERSATION_CACHE = CACHE_DIR / "conversation_cache.json"

# Define paths
MEMORY_DIR = GOD_MODE_DIR / "memory"
QUESTIONS_FILE = MEMORY_DIR / "memory_continue_questions.md"

# Import enhance_prompt function if available
try:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, script_dir)
    from script_enhance_prompt import enhance_prompt
    ENHANCE_AVAILABLE = True
except ImportError:
    ENHANCE_AVAILABLE = False
    print("Warning: Enhance prompt module not available. Responses will not be enhanced.")
    
    def enhance_prompt(prompt):
        return prompt

def debug_log(message):
    """Print debug message if verbose mode is enabled."""
    if os.environ.get("GOD_MODE_DEBUG") == "1":
        print(f"[DEBUG] {message}")

def ensure_directory_exists(directory):
    """Ensure a directory exists, creating it if necessary."""
    os.makedirs(directory, exist_ok=True)
    
def load_cache():
    """Load the conversation cache file or create it if it doesn't exist."""
    ensure_directory_exists(CACHE_DIR)
    
    if not CONVERSATION_CACHE.exists():
        return {
            "previous_questions": [],
            "last_question": "",
            "preset_questions": []
        }
    
    try:
        with open(CONVERSATION_CACHE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error loading cache: {e}")
        return {
            "previous_questions": [],
            "last_question": "",
            "preset_questions": []
        }

def save_cache(cache):
    """Save the conversation cache to file."""
    ensure_directory_exists(CACHE_DIR)
    
    try:
        with open(CONVERSATION_CACHE, 'w') as f:
            json.dump(cache, f, indent=2)
    except IOError as e:
        print(f"Error saving cache: {e}")

def update_preset_questions(response_content):
    """
    Extract potential preset questions from an AI response.
    Looks for lines that end with a question mark or start with bullet points.
    """
    questions = []
    lines = response_content.split('\n')
    
    for line in lines:
        line = line.strip()
        # Skip empty lines
        if not line:
            continue
            
        # Look for lines that have question marks
        if line.endswith('?'):
            # Clean up bullet points and other markers
            clean_line = line.lstrip('•-*># ').strip()
            if len(clean_line) > 10:  # Ignore very short questions
                questions.append(clean_line)
                
        # Look for bullet points followed by questions
        elif line.startswith('•') or line.startswith('-') or line.startswith('*'):
            if '?' in line:
                clean_line = line.lstrip('•-*># ').strip()
                if len(clean_line) > 10:  # Ignore very short questions
                    questions.append(clean_line)
    
    # Get the most recent questions (up to 5)
    return questions[-5:] if questions else []

def find_most_recent_response():
    """
    Try to find the most recent AI response in the clipboard or a temporary file.
    """
    # First, check if we can get the clipboard content
    try:
        import pyperclip
        content = pyperclip.paste()
        if content and len(content) > 50:  # Arbitrary minimum length
            return content
    except (ImportError, Exception) as e:
        print(f"Unable to access clipboard: {e}")
    
    # Check for temporary response files
    tmp_dir = CACHE_DIR / "responses"
    ensure_directory_exists(tmp_dir)
    
    try:
        # Get the most recent file in the tmp directory
        files = list(tmp_dir.glob("*.txt"))
        if files:
            most_recent = max(files, key=os.path.getmtime)
            with open(most_recent, 'r') as f:
                content = f.read()
                if content:
                    return content
    except Exception as e:
        print(f"Error reading response files: {e}")
    
    return None

def process_response_for_questions():
    """Process the most recent response to extract preset questions."""
    response = find_most_recent_response()
    if not response:
        print("Could not find a recent response. No preset questions available.")
        return []
        
    # Extract questions from the response
    questions = update_preset_questions(response)
    
    # Update the cache with these questions
    cache = load_cache()
    cache["preset_questions"] = questions
    save_cache(cache)
    
    return questions

def display_preset_menu():
    """Display the menu of preset questions."""
    cache = load_cache()
    preset_questions = cache.get("preset_questions", [])
    
    # If there are no preset questions, try to process the last response
    if not preset_questions:
        preset_questions = process_response_for_questions()
        
    if not preset_questions:
        print("No preset questions available. Please use --custom to ask a question.")
        return None
        
    print("\nChoose a question to ask:")
    for i, question in enumerate(preset_questions, 1):
        print(f"{i}. {question}")
    print("C. Enter a custom question")
    print("Q. Quit")
    
    choice = input("\nEnter your choice: ")
    
    if choice.lower() == 'q':
        return "QUIT"
    elif choice.lower() == 'c':
        custom = input("\nEnter your question: ")
        return custom if custom else None
    else:
        try:
            index = int(choice) - 1
            if 0 <= index < len(preset_questions):
                return preset_questions[index]
            else:
                print("Invalid choice.")
                return None
        except ValueError:
            print("Invalid choice.")
            return None

def save_question(question):
    """Save a question to the questions file."""
    ensure_directory_exists(MEMORY_DIR)
    
    # Create the file if it doesn't exist
    if not QUESTIONS_FILE.exists():
        with open(QUESTIONS_FILE, 'w') as f:
            f.write("# Continuation Questions\n\n")
            f.write("This file contains questions that can be used to continue the conversation.\n\n")
    
    # Append the question if it's not already in the file
    with open(QUESTIONS_FILE, 'r') as f:
        content = f.read()
    
    if question not in content:
        with open(QUESTIONS_FILE, 'a') as f:
            f.write(f"- {question}\n")

def get_questions():
    """Get a list of predefined questions from the questions file."""
    if not QUESTIONS_FILE.exists():
        return []
    
    questions = []
    with open(QUESTIONS_FILE, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith('- '):
                questions.append(line[2:])
    
    return questions

def extract_questions_from_file(file_path):
    """Extract questions from a file containing an AI response."""
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Look for questions at the end of the response
        lines = content.split('\n')
        questions = []
        
        # Look for lines ending with ? near the end of the content
        for line in lines[-10:]:  # Check the last 10 lines
            line = line.strip()
            if line.endswith('?') and len(line) > 10:  # Reasonably long questions
                questions.append(line)
                save_question(line)
        
        return questions
    except Exception as e:
        debug_log(f"Error extracting questions: {e}")
        return []

def scan_for_questions():
    """Scan recent AI responses for questions and save them."""
    logs_dir = GOD_MODE_DIR / "logs"
    ai_responses_dir = GOD_MODE_DIR / "responses"
    
    # Scan directories if they exist
    for directory in [logs_dir, ai_responses_dir]:
        if directory.exists():
            for file in directory.glob("*.md"):
                extract_questions_from_file(file)

def continue_conversation(custom_question=None):
    """Continue the conversation with a preset or custom question."""
    questions = get_questions()
    
    if custom_question:
        print(f"Using custom question: {custom_question}")
        return custom_question
    
    if not questions:
        print("No preset questions available. Please use --custom to ask a question.")
        return None
    
    # Display questions with numbers
    print("Select a question to continue the conversation:")
    for i, question in enumerate(questions, 1):
        print(f"{i}) {question}")
    print("0) Exit without selecting")
    
    # Get user selection
    try:
        choice = int(input("\nEnter your choice (0-{0}): ".format(len(questions))))
        if choice == 0:
            print("No question selected. Exiting.")
            return None
        if 1 <= choice <= len(questions):
            selected_question = questions[choice-1]
            print(f"\nSelected: {selected_question}")
            return selected_question
        else:
            print("Invalid choice. Exiting.")
            return None
    except ValueError:
        print("Invalid input. Exiting.")
        return None

def main():
    """Main function for the conversation continuation script."""
    parser = argparse.ArgumentParser(description='Continue a conversation with the AI assistant.')
    parser.add_argument('--custom', help='Custom question to ask')
    parser.add_argument('--update', action='store_true', help='Update the preset questions from the most recent response')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    parser.add_argument('--scan', action='store_true', help='Scan for questions in recent responses')
    parser.add_argument('--add', type=str, help='Add a question to the list')
    args = parser.parse_args()
    
    if args.update:
        questions = process_response_for_questions()
        if questions:
            print("Updated preset questions:")
            for i, q in enumerate(questions, 1):
                print(f"{i}. {q}")
        else:
            print("No questions found in the most recent response.")
        return 0
        
    # Ensure the memory directory exists
    ensure_directory_exists(MEMORY_DIR)
    
    # Handle the add question option
    if args.add:
        save_question(args.add)
        print(f"Added question: {args.add}")
        return 0
    
    # Handle the scan option
    if args.scan:
        scan_for_questions()
        print("Scanned for questions in recent responses")
        return 0
    
    # Continue the conversation
    selected_question = continue_conversation(args.custom)
    
    if selected_question:
        # Here you would typically send this to Cursor or copy to clipboard
        print(f"\nContinuing conversation with: {selected_question}")
        
        # Copy to clipboard if possible
        try:
            import pyperclip
            pyperclip.copy(selected_question)
            print("Question copied to clipboard! Paste it into your AI conversation.")
        except ImportError:
            print("pyperclip module not found. Install it to enable clipboard functionality.")
            print("You can manually copy the question above.")
    
    return 0 if selected_question else 1

if __name__ == "__main__":
    sys.exit(main()) 