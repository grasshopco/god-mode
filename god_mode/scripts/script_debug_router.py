#!/usr/bin/env python3

"""
Debug utility for God Mode Message Router

This script runs the message router with enhanced error handling and diagnostics.
It captures detailed information about errors and the environment to help diagnose issues.

Usage:
    python script_debug_router.py
"""

import os
import sys
import traceback
import platform
import time
import subprocess
from pathlib import Path
import importlib.util

# Set up diagnostic log file
LOG_DIR = Path(__file__).parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / "debug_router.log"

def log(message, level="INFO"):
    """Log a message to both the console and log file"""
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    formatted_msg = f"[{timestamp}] [{level}] {message}"
    
    print(formatted_msg)
    
    with open(LOG_FILE, "a") as f:
        f.write(formatted_msg + "\n")

def log_separator():
    log("=" * 80)

def log_system_info():
    """Log detailed system information"""
    log_separator()
    log("SYSTEM INFORMATION", "DIAG")
    log_separator()
    
    log(f"Python Version: {sys.version}")
    log(f"Platform: {platform.platform()}")
    log(f"System: {platform.system()} {platform.release()}")
    log(f"Machine: {platform.machine()}")
    log(f"Current Working Directory: {os.getcwd()}")
    log(f"Script Directory: {os.path.dirname(os.path.abspath(__file__))}")
    
    # List environment variables
    log("Environment Variables:", "DIAG")
    for key, value in os.environ.items():
        if key.lower() in ('path', 'pythonpath', 'home', 'user'):
            log(f"  {key}={value}", "DIAG")
    
    log_separator()

def log_python_path():
    """Log details about Python path and modules"""
    log("PYTHON PATH INFORMATION", "DIAG")
    log_separator()
    
    log(f"sys.executable: {sys.executable}")
    log("sys.path:")
    for path in sys.path:
        log(f"  {path}")
    
    log_separator()

def check_module_path(module_name):
    """Check if a module can be imported and log its path"""
    try:
        spec = importlib.util.find_spec(module_name)
        if spec is not None:
            log(f"Module '{module_name}' found at: {spec.origin}")
            return True
        else:
            log(f"Module '{module_name}' not found", "ERROR")
            return False
    except Exception as e:
        log(f"Error checking module '{module_name}': {str(e)}", "ERROR")
        return False

def log_dependencies():
    """Check and log status of dependencies"""
    log("DEPENDENCY CHECK", "DIAG")
    log_separator()
    
    # Check critical dependencies
    check_module_path("pyperclip")
    check_module_path("plyer")
    check_module_path("plyer.notification")
    
    # Try to import pyperclip and test clipboard functionality
    try:
        import pyperclip
        log("Testing clipboard access...")
        test_text = "GOD_MODE_TEST_STRING"
        original_clipboard = pyperclip.paste()
        pyperclip.copy(test_text)
        result = pyperclip.paste()
        
        if result == test_text:
            log("✓ Clipboard test successful")
        else:
            log(f"✗ Clipboard test failed. Expected '{test_text}', got '{result}'", "ERROR")
        
        # Restore original clipboard content
        pyperclip.copy(original_clipboard)
    except Exception as e:
        log(f"Clipboard test failed with error: {str(e)}", "ERROR")
    
    # Test plyer notification
    try:
        from plyer import notification
        log("Testing notification functionality...")
        notification.notify(
            title="God Mode Test",
            message="This is a test notification from God Mode debug script",
            app_name="God Mode Debug",
            timeout=1
        )
        log("✓ Notification test completed (check if you received it)")
    except Exception as e:
        log(f"Notification test failed with error: {str(e)}", "ERROR")
    
    log_separator()

def check_file_permissions():
    """Check permissions of critical files"""
    log("FILE PERMISSIONS CHECK", "DIAG")
    log_separator()
    
    script_dir = Path(__file__).parent
    files_to_check = [
        script_dir / "route",
        script_dir / "script_message_router.py",
        script_dir.parent / "logs"
    ]
    
    for file_path in files_to_check:
        if file_path.exists():
            try:
                perms = oct(file_path.stat().st_mode)[-3:]
                is_executable = os.access(file_path, os.X_OK)
                log(f"✓ {file_path}: permissions={perms}, executable={is_executable}")
            except Exception as e:
                log(f"✗ Error checking permissions for {file_path}: {str(e)}", "ERROR")
        else:
            log(f"✗ File not found: {file_path}", "ERROR")
    
    log_separator()

def check_route_script():
    """Check if the route script exists and is executable"""
    log("ROUTE SCRIPT CHECK", "DIAG")
    log_separator()
    
    script_dir = Path(__file__).parent
    route_script = script_dir / "route"
    
    if route_script.exists():
        log(f"✓ Route script found at: {route_script}")
        
        if os.access(route_script, os.X_OK):
            log("✓ Route script is executable")
            
            # Check the content of the route script to see what it's doing
            try:
                with open(route_script, "r") as f:
                    content = f.read()
                log(f"Route script content (first 200 chars): {content[:200]}")
            except Exception as e:
                log(f"Error reading route script: {str(e)}", "ERROR")
        else:
            log("✗ Route script is not executable", "ERROR")
            log("Attempting to make it executable...")
            try:
                route_script.chmod(0o755)
                log("✓ Made route script executable")
            except Exception as e:
                log(f"Error making route script executable: {str(e)}", "ERROR")
    else:
        log(f"✗ Route script not found at expected location: {route_script}", "ERROR")
        
        # Try to find it elsewhere
        try:
            result = subprocess.run(["find", script_dir.parent.parent, "-name", "route", "-type", "f"], 
                                   capture_output=True, text=True)
            if result.stdout:
                log(f"Found potential route scripts at:\n{result.stdout}")
            else:
                log("No route script found in the project directory", "ERROR")
        except Exception as e:
            log(f"Error searching for route script: {str(e)}", "ERROR")
    
    log_separator()

def run_with_error_handling():
    """Run the message router with comprehensive error handling"""
    log("STARTING MESSAGE ROUTER WITH ERROR HANDLING", "DIAG")
    log_separator()
    
    script_dir = Path(__file__).parent
    router_script = script_dir / "script_message_router.py"
    
    if not router_script.exists():
        log(f"✗ Message router script not found at: {router_script}", "ERROR")
        return
    
    log(f"Running message router script: {router_script}")
    
    try:
        # First, try to import the script as a module and run its main function
        log("Method 1: Importing as module and running main()")
        
        # Add the script's directory to sys.path if not already there
        if str(script_dir) not in sys.path:
            sys.path.insert(0, str(script_dir))
        
        try:
            # Import the message router module
            spec = importlib.util.spec_from_file_location(
                "script_message_router", router_script)
            router_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(router_module)
            
            # Run the main function with --watch flag
            log("Calling main() function with --watch flag")
            sys.argv = [str(router_script), "--watch"]
            router_module.main()
        except Exception as e:
            log(f"Error running message router as module: {str(e)}", "ERROR")
            log(traceback.format_exc(), "ERROR")
            
            # If that fails, try running it as a subprocess
            log("Method 2: Running as subprocess")
            try:
                result = subprocess.run(
                    [sys.executable, str(router_script), "--watch", "--debug"],
                    capture_output=True, text=True
                )
                log(f"Subprocess exit code: {result.returncode}")
                if result.stdout:
                    log(f"Subprocess stdout:\n{result.stdout}")
                if result.returncode != 0 and result.stderr:
                    log(f"Subprocess stderr:\n{result.stderr}", "ERROR")
            except Exception as sub_e:
                log(f"Error running as subprocess: {str(sub_e)}", "ERROR")
    except Exception as outer_e:
        log(f"Uncaught exception: {str(outer_e)}", "ERROR")
        log(traceback.format_exc(), "ERROR")
    
    log_separator()

def main():
    """Main function that runs diagnostics and tries to start the message router"""
    try:
        log("STARTING GOD MODE DEBUG UTILITY", "DIAG")
        log(f"Log file: {LOG_FILE}")
        
        log_system_info()
        log_python_path()
        log_dependencies()
        check_file_permissions()
        check_route_script()
        
        run_with_error_handling()
        
        log("GOD MODE DEBUG UTILITY COMPLETE", "DIAG")
    except Exception as e:
        log(f"Critical error in debug utility: {str(e)}", "ERROR")
        log(traceback.format_exc(), "ERROR")

if __name__ == "__main__":
    main() 