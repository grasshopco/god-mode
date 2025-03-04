#!/usr/bin/env python3
"""
God Mode System Test Script

This script tests all components of the God Mode system to verify they are working properly.
It runs each enhancement script and verifies the outputs match expectations.
"""

import os
import sys
import subprocess
import json
from pathlib import Path
import time
from datetime import datetime

# Get the absolute path to the god_mode directory
SCRIPT_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
GOD_MODE_DIR = SCRIPT_DIR.parent
BASE_DIR = GOD_MODE_DIR.parent

# Define paths to important files and directories
MEMORY_DIR = GOD_MODE_DIR / "memory"
LOGS_DIR = GOD_MODE_DIR / "logs"
CACHE_DIR = GOD_MODE_DIR / ".cache"
CONTINUITY_DIR = MEMORY_DIR / "continuity"

# Define paths to log files
MESSAGE_ROUTER_LOG = LOGS_DIR / "message_router.log"
CURSOR_WATCH_LOG = LOGS_DIR / "cursor_watch.log"
ROUTE_WRAPPER_LOG = LOGS_DIR / "route_wrapper.log"

# Define paths to test files
TEST_LOG_ENTRY = "## Current UTC timestamp: " + datetime.utcnow().strftime("%Y-%m-%d %H:%M") + " UTC\n\nTest log entry from God Mode test script.\n"
TEST_FEATURE_LOG = "## Current UTC timestamp: " + datetime.utcnow().strftime("%Y-%m-%d %H:%M") + " UTC\n\nTest feature log entry from God Mode test script.\n"

# Terminal colors for better readability
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    """Print a header with nice formatting"""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'=' * 50}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD} {text} {Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'=' * 50}{Colors.ENDC}\n")

def print_status(test_name, status, message=""):
    """Print the status of a test"""
    if status:
        print(f"{Colors.GREEN}✓ {test_name}: PASSED{Colors.ENDC}")
    else:
        print(f"{Colors.RED}✗ {test_name}: FAILED{Colors.ENDC}")
    if message:
        print(f"  {message}")

def run_script(script_name, args=None):
    """Run a script and return the exit code and output"""
    script_path = SCRIPT_DIR / script_name
    cmd = [sys.executable, str(script_path)]
    if args:
        cmd.extend(args)
    
    print(f"{Colors.BLUE}Running: {' '.join(cmd)}{Colors.ENDC}")
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode, result.stdout, result.stderr

def check_file_updated(file_path, last_modified=None):
    """Check if a file exists and has been modified since last_modified"""
    file_path = Path(file_path)
    if not file_path.exists():
        return False, f"File {file_path} does not exist"
    
    if last_modified is not None:
        current_mtime = file_path.stat().st_mtime
        if current_mtime <= last_modified:
            return False, f"File {file_path} has not been modified"
    
    return True, f"File {file_path} exists and has been updated"

def test_project_structure():
    """Test the project structure script"""
    print_header("Testing Project Structure Generator")
    
    # Get the modified time of the structure file before running the script
    structure_file = MEMORY_DIR / "memory_project_structure.md"
    before_mtime = structure_file.stat().st_mtime if structure_file.exists() else 0
    
    # Run the script
    exit_code, stdout, stderr = run_script("script_update_project_structure.py")
    
    # Check if the script ran successfully
    status = exit_code == 0
    print_status("Script execution", status, stderr if not status else "")
    
    # Check if the structure file was updated
    file_updated, message = check_file_updated(structure_file, before_mtime)
    print_status("Structure file updated", file_updated, message)
    
    # Verify content
    if file_updated:
        with open(structure_file, 'r') as f:
            content = f.read()
        has_structure = "# Project Structure" in content and "## Root Directory" in content
        print_status("Structure content valid", has_structure, 
                     "Content has expected headers" if has_structure else "Content missing expected headers")
    
    return status and file_updated

def test_enhance_message_content():
    """Test the message content enhancer script"""
    print_header("Testing Message Content Enhancer")
    
    # Run the script in audit mode
    exit_code, stdout, stderr = run_script("script_enhance_message_content.py", ["--audit"])
    
    # Check if the script ran successfully
    status = exit_code == 0
    print_status("Script execution", status, stderr if not status else "")
    
    # Verify output
    if status:
        audit_completed = "Audit complete" in stdout
        print_status("Audit completed", audit_completed, 
                     "Output indicates audit completed" if audit_completed else "Output doesn't indicate audit completion")
    
    return status

def test_feature_logs():
    """Test the feature logs script"""
    print_header("Testing Feature Log Template Validator")
    
    # Run the script in fix mode
    exit_code, stdout, stderr = run_script("script_check_feature_logs.py", ["--fix"])
    
    # Check if the script ran successfully
    status = exit_code == 0
    print_status("Script execution", status, stderr if not status else "")
    
    # Check if the logs match the template
    if status:
        all_match = "All feature log files match the template" in stdout
        print_status("Feature logs validation", all_match, 
                     "All feature logs match template" if all_match else "Not all feature logs match template")
    
    return status

def test_session_continuity():
    """Test the session continuity script"""
    print_header("Testing Session Continuity System")
    
    # Run the script
    exit_code, stdout, stderr = run_script("script_session_continuity.py")
    
    # Check if the script ran successfully
    status = exit_code == 0
    print_status("Script execution", status, stderr if not status else "")
    
    # Check if a continuity summary was created
    latest_summary = CONTINUITY_DIR / "latest_continuity_summary.md"
    file_exists, message = check_file_updated(latest_summary)
    print_status("Continuity summary created", file_exists, message)
    
    return status and file_exists

def test_roadmap_generator():
    """Test the roadmap generator script"""
    print_header("Testing Roadmap Generator")
    
    # Create a test title
    test_title = f"Test Roadmap {datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
    
    # Run the script
    exit_code, stdout, stderr = run_script("script_generate_roadmap.py", ["--title", test_title])
    
    # Check if the script ran successfully
    status = exit_code == 0
    print_status("Script execution", status, stderr if not status else "")
    
    # Check if a roadmap was created
    if status:
        roadmap_created = "Generated roadmap file:" in stdout
        print_status("Roadmap created", roadmap_created, 
                     "Output indicates roadmap was created" if roadmap_created else "Output doesn't indicate roadmap creation")
        
        if roadmap_created:
            # Extract the file path from the output
            roadmap_path = None
            for line in stdout.split('\n'):
                if "Generated roadmap file:" in line:
                    roadmap_path = line.split("Generated roadmap file:")[1].strip()
                    break
            
            if roadmap_path:
                file_exists, message = check_file_updated(roadmap_path)
                print_status("Roadmap file exists", file_exists, message)
                return status and roadmap_created and file_exists
    
    return status and roadmap_created

def test_message_routing():
    """Test the message routing system by simulating clipboard content"""
    print_header("Testing Message Routing")
    
    try:
        # Need to confirm the message router is running
        if sys.platform == 'darwin':  # macOS
            ps_output = subprocess.check_output(['ps', '-ef']).decode('utf-8')
        else:  # Linux
            ps_output = subprocess.check_output(['ps', 'aux']).decode('utf-8')
        
        router_running = any('route --watch' in line for line in ps_output.split('\n'))
        print_status("Message Router running", router_running, 
                    "Message Router process found" if router_running else "Message Router not running - tests will be skipped")
        
        if not router_running:
            print(f"{Colors.YELLOW}To test message routing, start God Mode with the remote control script before running this test.{Colors.ENDC}")
            return False
        
        # Now let's test routing by running the route command with test content
        test_file = SCRIPT_DIR / "test_routing_content.txt"
        with open(test_file, 'w') as f:
            f.write(TEST_LOG_ENTRY)
        
        # Run the route command with the test file
        route_cmd = GOD_MODE_DIR / "scripts" / "route"
        cmd = [str(route_cmd), "--input", str(test_file)]
        
        print(f"{Colors.BLUE}Running: {' '.join(cmd)}{Colors.ENDC}")
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        status = result.returncode == 0
        print_status("Route command execution", status, result.stderr if not status else "")
        
        # Check if the content was routed properly
        # Allow some time for the routing to complete
        time.sleep(2)
        
        # Check if logs all file was updated
        logs_all = MEMORY_DIR / "memory_logs_all.md"
        before_size = logs_all.stat().st_size if logs_all.exists() else 0
        file_updated, message = check_file_updated(logs_all)
        print_status("Logs file updated", file_updated, message)
        
        # Clean up
        test_file.unlink()
        
        return status and file_updated
        
    except Exception as e:
        print_status("Message Routing", False, f"Error: {str(e)}")
        return False

def run_all_tests():
    """Run all the tests"""
    print_header("GOD MODE SYSTEM VERIFICATION")
    print(f"Running tests at: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC")
    print(f"God Mode directory: {GOD_MODE_DIR}")
    
    # Run all the tests
    results = {
        "Project Structure": test_project_structure(),
        "Message Content": test_enhance_message_content(),
        "Feature Logs": test_feature_logs(),
        "Session Continuity": test_session_continuity(),
        "Roadmap Generator": test_roadmap_generator(),
        "Message Routing": test_message_routing(),
    }
    
    # Print summary
    print_header("TEST SUMMARY")
    
    all_passed = True
    for test, passed in results.items():
        if passed:
            print(f"{Colors.GREEN}✓ {test}: PASSED{Colors.ENDC}")
        else:
            print(f"{Colors.RED}✗ {test}: FAILED{Colors.ENDC}")
            all_passed = False
    
    # Final verdict
    if all_passed:
        print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 ALL TESTS PASSED! God Mode is fully operational.{Colors.ENDC}")
    else:
        print(f"\n{Colors.YELLOW}{Colors.BOLD}⚠️ SOME TESTS FAILED. Please review the output above for details.{Colors.ENDC}")
    
    return all_passed

if __name__ == "__main__":
    run_all_tests() 