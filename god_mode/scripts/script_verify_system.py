#!/usr/bin/env python3
"""
System Verification Script for God Mode
Checks the status and functionality of all God Mode components.
"""

import os
import sys
import time
import json
import subprocess
import re
import platform
import psutil
from pathlib import Path

# Add the parent directory to the sys path for importing helper modules
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

# Import helper modules if available
try:
    from utils.logger import log
except ImportError:
    def log(message, level="INFO"):
        print(f"[{level}] {message}")

# Define color codes for terminal output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"

def print_status(component, status, details=""):
    """
    Print the status of a component with color coding.
    
    Args:
        component (str): Name of the component
        status (str): Status of the component (PASS, FAIL, WARNING)
        details (str): Additional details about the status
    """
    status_color = {
        "PASS": GREEN,
        "FAIL": RED,
        "WARNING": YELLOW,
        "INFO": BLUE
    }.get(status, RESET)
    
    print(f"{status_color}[{status}]{RESET} {component}: {details}")

def check_process_running(process_name):
    """
    Check if a process is running.
    
    Args:
        process_name (str): Name of the process to check
        
    Returns:
        tuple: (is_running, pid or None)
    """
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if process_name in ' '.join(proc.info['cmdline'] or []):
                return True, proc.info['pid']
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False, None

def check_file_exists(file_path, component_name):
    """
    Check if a file exists and report status.
    
    Args:
        file_path (str): Path to the file
        component_name (str): Name of the component for reporting
        
    Returns:
        bool: True if the file exists, False otherwise
    """
    if os.path.exists(file_path):
        print_status(component_name, "PASS", f"File exists at {file_path}")
        return True
    else:
        print_status(component_name, "FAIL", f"File missing: {file_path}")
        return False

def verify_cursor_watch():
    """
    Verify cursor_watch script status and functionality.
    
    Returns:
        bool: True if cursor_watch is running correctly, False otherwise
    """
    print("\n=== Verifying Cursor Watch ===")
    
    # Check if the script exists
    script_path = os.path.join(current_dir, "script_cursor_watch.py")
    script_exists = check_file_exists(script_path, "Cursor Watch Script")
    
    # Check if the process is running
    is_running, pid = check_process_running("script_cursor_watch.py")
    if is_running:
        print_status("Cursor Watch Process", "PASS", f"Running with PID {pid}")
    else:
        print_status("Cursor Watch Process", "FAIL", "Not running")
    
    # Check if the script is using SQLite (look for imports)
    if script_exists:
        with open(script_path, 'r') as f:
            content = f.read()
            if "sqlite3" in content:
                print_status("Cursor Watch Implementation", "PASS", "Using SQLite implementation")
            else:
                print_status("Cursor Watch Implementation", "WARNING", "Not using SQLite implementation")
    
    return is_running and script_exists

def verify_message_router():
    """
    Verify message_router script status and functionality.
    
    Returns:
        bool: True if message_router is configured correctly, False otherwise
    """
    print("\n=== Verifying Message Router ===")
    
    # Check if the script exists
    script_path = os.path.join(current_dir, "script_message_router.py")
    script_exists = check_file_exists(script_path, "Message Router Script")
    
    # Check if the function for tag validation exists
    if script_exists:
        with open(script_path, 'r') as f:
            content = f.read()
            if "def should_add_tags_to_message" in content:
                print_status("Tag Detection Function", "PASS", "should_add_tags_to_message function exists")
            else:
                print_status("Tag Detection Function", "FAIL", "should_add_tags_to_message function missing")
            
            # Check validate_message implementation
            if "def validate_message" in content and "too many values to unpack" not in content:
                print_status("Message Validation", "PASS", "validate_message function exists and appears correct")
            else:
                print_status("Message Validation", "WARNING", "validate_message function may have issues")
    
    return script_exists

def verify_cursor_rules():
    """
    Verify cursor rules are properly set up.
    
    Returns:
        bool: True if cursor rules are set up correctly, False otherwise
    """
    print("\n=== Verifying Cursor Rules ===")
    
    # Find cursor rules file
    home_dir = str(Path.home())
    cursor_dirs = [
        os.path.join(home_dir, ".cursor", "cursor_rules.json"),
        os.path.join(home_dir, "Library", "Application Support", "Cursor", "cursor_rules.json")
    ]
    
    rules_file = None
    for path in cursor_dirs:
        if os.path.exists(path):
            rules_file = path
            break
    
    if not rules_file:
        print_status("Cursor Rules File", "FAIL", "Could not find cursor_rules.json")
        return False
    
    print_status("Cursor Rules File", "PASS", f"Found at {rules_file}")
    
    # Check if the file contains tagging rules
    try:
        with open(rules_file, 'r') as f:
            content = f.read()
            rules = json.loads(content)
            if isinstance(rules, list):
                tag_rules = [rule for rule in rules if "tags" in str(rule)]
                if tag_rules:
                    print_status("Tagging Rules", "PASS", f"Found {len(tag_rules)} tagging rules")
                    return True
                else:
                    print_status("Tagging Rules", "FAIL", "No tagging rules found in cursor_rules.json")
            else:
                print_status("Cursor Rules Format", "WARNING", "Unexpected format in cursor_rules.json")
    except (json.JSONDecodeError, IOError) as e:
        print_status("Cursor Rules Parsing", "FAIL", f"Error parsing cursor_rules.json: {str(e)}")
    
    return False

def verify_memory_files():
    """
    Verify memory files exist and are accessible.
    
    Returns:
        bool: True if memory files are set up correctly, False otherwise
    """
    print("\n=== Verifying Memory Files ===")
    
    memory_dir = os.path.join(parent_dir, "memory")
    if not os.path.exists(memory_dir):
        print_status("Memory Directory", "FAIL", f"Directory missing: {memory_dir}")
        return False
    
    print_status("Memory Directory", "PASS", f"Exists at {memory_dir}")
    
    # Check key memory files
    memory_files = ["feature_log.md", "log_summary.md", "memory_updates.md"]
    all_exist = True
    
    for file in memory_files:
        file_path = os.path.join(memory_dir, file)
        if not os.path.exists(file_path):
            print_status(f"Memory File: {file}", "FAIL", "File missing")
            all_exist = False
        else:
            print_status(f"Memory File: {file}", "PASS", "File exists")
    
    return all_exist

def verify_auto_commit():
    """
    Verify the auto-commit functionality.
    
    Returns:
        bool: True if auto-commit is set up correctly, False otherwise
    """
    print("\n=== Verifying Auto-Commit ===")
    
    # Check if the script exists
    script_path = os.path.join(current_dir, "script_auto_commit.py")
    script_exists = check_file_exists(script_path, "Auto-Commit Script")
    
    # Check if Git is available
    try:
        result = subprocess.run(["git", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print_status("Git Installation", "PASS", f"Git is installed: {result.stdout.strip()}")
        else:
            print_status("Git Installation", "FAIL", "Git is not installed or not in PATH")
            return False
    except Exception as e:
        print_status("Git Installation", "FAIL", f"Error checking Git: {str(e)}")
        return False
    
    # Check if script is properly implemented
    if script_exists:
        with open(script_path, 'r') as f:
            content = f.read()
            if "def auto_commit" in content and "git add" in content and "git commit" in content:
                print_status("Auto-Commit Implementation", "PASS", "auto_commit function properly implemented")
            else:
                print_status("Auto-Commit Implementation", "WARNING", "auto_commit function may be incomplete")
    
    # Check for Git repository
    try:
        result = subprocess.run(["git", "status"], cwd=parent_dir, capture_output=True, text=True)
        if result.returncode == 0:
            print_status("Git Repository", "PASS", "Git repository exists and is accessible")
        else:
            print_status("Git Repository", "FAIL", "Not a Git repository or Git repository is inaccessible")
            return False
    except Exception as e:
        print_status("Git Repository", "FAIL", f"Error checking Git repository: {str(e)}")
        return False
    
    return script_exists

def run_verification():
    """
    Run all verification checks and print a summary.
    
    Returns:
        int: 0 if all checks pass, 1 if any check fails
    """
    print(f"{BLUE}===== God Mode System Verification ====={RESET}")
    print(f"{BLUE}Started at: {time.strftime('%Y-%m-%d %H:%M:%S')}{RESET}")
    print(f"{BLUE}System: {platform.system()} {platform.release()}{RESET}")
    print(f"{BLUE}======================================={RESET}\n")
    
    # Run all verification checks
    cursor_watch_ok = verify_cursor_watch()
    message_router_ok = verify_message_router()
    cursor_rules_ok = verify_cursor_rules()
    memory_files_ok = verify_memory_files()
    auto_commit_ok = verify_auto_commit()
    
    # Print summary
    print(f"\n{BLUE}===== Verification Summary ====={RESET}")
    
    summary = {
        "Cursor Watch": cursor_watch_ok,
        "Message Router": message_router_ok,
        "Cursor Rules": cursor_rules_ok,
        "Memory Files": memory_files_ok,
        "Auto-Commit": auto_commit_ok
    }
    
    for component, status in summary.items():
        status_text = f"{GREEN}PASS{RESET}" if status else f"{RED}FAIL{RESET}"
        print(f"{component}: {status_text}")
    
    # Overall status
    all_pass = all(summary.values())
    overall_status = f"{GREEN}PASS{RESET}" if all_pass else f"{RED}FAIL{RESET}"
    print(f"\nOverall Status: {overall_status}")
    
    if not all_pass:
        print(f"\n{YELLOW}Recommendations:{RESET}")
        if not cursor_watch_ok:
            print("- Restart cursor_watch script with: python3 god_mode/scripts/script_cursor_watch.py")
        if not message_router_ok:
            print("- Check message_router script for errors and restart it")
        if not cursor_rules_ok:
            print("- Update cursor_rules.json with proper tagging rules")
        if not memory_files_ok:
            print("- Create missing memory files")
        if not auto_commit_ok:
            print("- Fix auto-commit script and ensure Git is properly configured")
    
    print(f"\n{BLUE}=============================={RESET}")
    
    return 0 if all_pass else 1

if __name__ == "__main__":
    sys.exit(run_verification()) 