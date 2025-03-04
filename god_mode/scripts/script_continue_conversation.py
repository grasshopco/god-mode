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

def main():
    """Main function for the conversation continuation script."""
    parser = argparse.ArgumentParser(description='Continue a conversation with the AI assistant.')
    parser.add_argument('--custom', help='Custom question to ask')
    parser.add_argument('--update', action='store_true', help='Update the preset questions from the most recent response')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
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
        
    # Determine the question to ask
    question = None
    if args.custom:
        question = args.custom
    else:
        question = display_preset_menu()
        
    if not question:
        print("No question selected. Exiting.")
        return 1
    elif question == "QUIT":
        print("Goodbye!")
        return 0
        
    # Enhance the prompt if possible
    if ENHANCE_AVAILABLE:
        enhanced_question = enhance_prompt(question)
    else:
        enhanced_question = question
        
    # For debug mode, just print the question
    if args.debug:
        print(f"Question: {question}")
        print(f"Enhanced question: {enhanced_question}")
        return 0
        
    # Send the question to the AI assistant
    # This would typically involve interacting with an API or UI
    # For now, we'll save it to a file that can be picked up by other scripts
    
    query_file = CACHE_DIR / "continue_query.txt"
    try:
        with open(query_file, 'w') as f:
            f.write(enhanced_question)
        print(f"Question ready: {question}")
        print("Your question has been prepared for the AI assistant.")
        
        # Optional: Try to send directly to a terminal or API
        # This part would depend on the specific setup
        try:
            # For example, you might try to pipe to a command-line API
            # subprocess.run(["some_cli_tool", "--query", query_file])
            pass
        except Exception as e:
            if args.debug:
                print(f"Failed to send directly: {e}")
    except Exception as e:
        print(f"Error saving question: {e}")
        return 1
        
    # Update the cache with this question
    cache = load_cache()
    if question not in cache["previous_questions"]:
        cache["previous_questions"].append(question)
        # Keep only the last 20 questions
        cache["previous_questions"] = cache["previous_questions"][-20:]
    cache["last_question"] = question
    save_cache(cache)
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 