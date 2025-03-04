#!/usr/bin/env python3
"""
Demo script showing how to use the message router from within another Python script.
"""

import os
import sys
import subprocess
from pathlib import Path

# Add the parent directory to the Python path to import the message router
script_dir = Path(os.path.dirname(os.path.abspath(__file__)))
parent_dir = script_dir.parent
sys.path.append(str(parent_dir))

# Import the message router module
from script_message_router import route_message

def demo_direct_function_call():
    """Demonstrate using the router by directly calling its functions."""
    print("Demo 1: Direct function call")
    
    # Example message with markers
    message = """
    This is a demo of using the message router directly.
    
    [LOG_SUMMARY]Demonstrated direct function call to message router
    
    [LOG_DETAIL]
    # Direct Function Call Demo
    
    This example shows how to import and use the message router's functions directly
    in another Python script without spawning a subprocess.
    
    [MEMORY_UPDATE]
    The message router can be imported and used directly in other Python scripts.
    """
    
    # Call the route_message function directly
    print("Routing message...")
    route_message(message)
    print("Message routed successfully!\n")

def demo_subprocess_call():
    """Demonstrate using the router by calling it as a subprocess."""
    print("Demo 2: Subprocess call")
    
    # Example message with markers
    message = """
    This is a demo of using the message router as a subprocess.
    
    [LOG_SUMMARY]Demonstrated subprocess call to message router
    
    [FEATURE_LOG: Message Router]
    The message router can be called as a subprocess from other scripts.
    """
    
    # Create a temporary file with the message
    temp_file = script_dir / "temp_message.txt"
    with open(temp_file, "w") as f:
        f.write(message)
    
    # Call the router script as a subprocess
    print("Calling router script as subprocess...")
    router_script = parent_dir / "script_message_router.py"
    result = subprocess.run(
        ["python", str(router_script), "--input", str(temp_file)],
        capture_output=True,
        text=True
    )
    
    # Print the result
    print(f"Return code: {result.returncode}")
    if result.stdout:
        print(f"Output: {result.stdout}")
    if result.stderr:
        print(f"Error: {result.stderr}")
    
    # Clean up the temporary file
    os.remove(temp_file)
    print("Message routed successfully!\n")

def demo_in_memory_generation():
    """Demonstrate generating content with markers in code."""
    print("Demo 3: In-memory generation")
    
    # Generate a log summary
    summary = "Generated a log summary programmatically"
    message = f"[LOG_SUMMARY]{summary}"
    
    # Generate a feature log
    feature_name = "API Integration"
    feature_log = "Added support for OAuth2 authentication"
    message += f"\n\n[FEATURE_LOG: {feature_name}]\n{feature_log}"
    
    # Route the generated message
    print("Routing programmatically generated message...")
    route_message(message)
    print("Message routed successfully!\n")

if __name__ == "__main__":
    print("Message Router Demo")
    print("=================\n")
    
    # Run the demos
    demo_direct_function_call()
    demo_subprocess_call()
    demo_in_memory_generation()
    
    print("All demos completed successfully!")
    print("Check the log files to see the routed messages.") 