#!/usr/bin/env python3

"""
God Mode MCP Server

This script implements a Model Context Protocol (MCP) server for God Mode,
allowing Cursor's AI to directly access God Mode capabilities.

For more information on MCP, see: https://docs.cursor.com/context/model-context-protocol
"""

import os
import sys
import json
import argparse
import subprocess
import tempfile
from pathlib import Path

# Get the directory of this script
SCRIPT_DIR = Path(os.path.dirname(os.path.abspath(__file__)))

# Define the God Mode directory (parent of scripts)
GOD_MODE_DIR = SCRIPT_DIR.parent

def run_script(script_name, *args):
    """Run a script from the scripts directory."""
    script_path = SCRIPT_DIR / script_name
    
    if not script_path.exists():
        return f"Error: Script {script_name} not found"
    
    try:
        # Make sure the script is executable
        if script_path.suffix == '.sh':
            os.chmod(script_path, 0o755)
        
        # Run the script with appropriate interpreter
        if script_path.suffix == '.py':
            result = subprocess.run(
                [sys.executable, script_path, *args],
                capture_output=True,
                text=True,
                check=True
            )
        else:
            result = subprocess.run(
                [script_path, *args],
                capture_output=True,
                text=True,
                check=True
            )
        
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr}"
    except Exception as e:
        return f"Error: {str(e)}"

def enhance_prompt(prompt):
    """Enhance a prompt using the God Mode enhancement script."""
    try:
        # Create temporary files for input/output
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as prompt_file:
            prompt_file.write(prompt)
            prompt_file_path = prompt_file.name
        
        output_file_path = prompt_file_path + "_enhanced"
        
        # Run the enhance prompt script
        run_script("script_prepare_response.sh")
        
        # Run the script with the --prompt argument
        enhance_result = subprocess.run(
            [sys.executable, SCRIPT_DIR / "script_enhance_prompt.py", "--prompt", prompt],
            capture_output=True,
            text=True
        ).stdout
        
        # Extract the enhanced prompt from the output
        enhanced_prompt = ""
        capture_next = False
        for line in enhance_result.splitlines():
            if line == "Enhanced prompt:":
                capture_next = True
                continue
            elif line == "The enhanced prompt has been copied to your clipboard!":
                break
            
            if capture_next:
                if enhanced_prompt:
                    enhanced_prompt += "\n"
                enhanced_prompt += line
        
        # If we couldn't extract the enhanced prompt, use the original
        if not enhanced_prompt:
            enhanced_prompt = prompt + "\n\n[Enhancement failed, using original prompt]"
        
        # Clean up
        os.unlink(prompt_file_path)
        if os.path.exists(output_file_path):
            os.unlink(output_file_path)
        
        return enhanced_prompt
    except Exception as e:
        return f"Error enhancing prompt: {str(e)}\n\n{prompt}"

def process_response(response, prompt=""):
    """Process an AI response using God Mode response processing."""
    try:
        # Create a temporary file for the response
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as response_file:
            response_file.write(response)
            response_file_path = response_file.name
        
        # Run the auto commit script (processes the response)
        process_result = ""
        with open(response_file_path, "r") as f:
            # Call the script_auto_commit.sh script with the response as input
            try:
                process_result = subprocess.run(
                    [SCRIPT_DIR / "script_auto_commit.sh"],
                    stdin=f,
                    capture_output=True,
                    text=True,
                    cwd=GOD_MODE_DIR
                ).stdout
            except Exception as e:
                process_result = f"Error: {str(e)}"
        
        # Clean up
        os.unlink(response_file_path)
        
        # Parse the results to extract logs, memory updates, etc.
        logs = []
        memory_updates = []
        committed_files = []
        
        for line in process_result.splitlines():
            if "Log saved to:" in line:
                logs.append(line.replace("Log saved to:", "").strip())
            elif "Memory updated:" in line:
                memory_updates.append(line.replace("Memory updated:", "").strip())
            elif "Committing file:" in line:
                committed_files.append(line.replace("Committing file:", "").strip())
        
        return {
            "process_result": process_result,
            "logs": logs,
            "memory_updates": memory_updates,
            "committed_files": committed_files
        }
    except Exception as e:
        return {"error": f"Error processing response: {str(e)}"}

def get_memory_content(file_name):
    """Get the content of a memory file."""
    try:
        memory_dir = GOD_MODE_DIR / "memory"
        
        # Check common locations/extensions
        possible_paths = [
            memory_dir / file_name,
            memory_dir / f"{file_name}.md",
            memory_dir / f"memory_{file_name}.md",
            memory_dir / f"{file_name}_summarized.md",
            memory_dir / f"{file_name}_detailed.md"
        ]
        
        for path in possible_paths:
            if path.exists():
                with open(path, "r") as f:
                    return f.read()
        
        return f"Memory file not found: {file_name}"
    except Exception as e:
        return f"Error accessing memory file: {str(e)}"

def handle_mcp_request(request):
    """Handle an MCP request and return a response."""
    try:
        # Parse the request
        request_type = request.get("type")
        
        if request_type == "list_tools":
            # Return the list of available tools
            return {
                "tools": [
                    {
                        "name": "god_mode.route",
                        "description": "Route content with tags to memory files",
                        "parameters": {
                            "content": {
                                "type": "string",
                                "description": "Content with [TAG] markers to route"
                            }
                        }
                    },
                    {
                        "name": "god_mode.memory",
                        "description": "Access God Mode memory files",
                        "parameters": {
                            "file": {
                                "type": "string",
                                "description": "Memory file to access (e.g., 'logs', 'architecture')"
                            }
                        }
                    },
                    {
                        "name": "god_mode.enhance",
                        "description": "Enhance a prompt with context",
                        "parameters": {
                            "prompt": {
                                "type": "string",
                                "description": "Prompt to enhance with context"
                            }
                        }
                    },
                    {
                        "name": "god_mode.process",
                        "description": "Process an AI response",
                        "parameters": {
                            "response": {
                                "type": "string",
                                "description": "AI response to process"
                            },
                            "prompt": {
                                "type": "string",
                                "description": "Original prompt (optional)"
                            }
                        }
                    }
                ]
            }
        elif request_type == "execute":
            # Handle tool execution
            tool_name = request.get("name")
            parameters = request.get("parameters", {})
            
            if tool_name == "god_mode.route":
                # Route content with tags
                content = parameters.get("content", "")
                # Call the message router script
                result = subprocess.run(
                    [sys.executable, SCRIPT_DIR / "script_message_router.py"],
                    input=content.encode(),
                    capture_output=True,
                    text=True
                ).stdout
                
                return {
                    "result": result or f"Routed content with {content.count('[')} tags"
                }
            elif tool_name == "god_mode.memory":
                # Access memory files
                file = parameters.get("file", "")
                content = get_memory_content(file)
                
                return {
                    "result": content
                }
            elif tool_name == "god_mode.enhance":
                # Enhance a prompt
                prompt = parameters.get("prompt", "")
                enhanced = enhance_prompt(prompt)
                
                return {
                    "result": enhanced
                }
            elif tool_name == "god_mode.process":
                # Process an AI response
                response = parameters.get("response", "")
                prompt = parameters.get("prompt", "")
                result = process_response(response, prompt)
                
                return {
                    "result": result
                }
            else:
                return {
                    "error": f"Unknown tool: {tool_name}"
                }
        else:
            return {
                "error": f"Unknown request type: {request_type}"
            }
    except Exception as e:
        return {
            "error": f"Error handling request: {str(e)}"
        }

def main():
    """Main function to run the MCP server."""
    parser = argparse.ArgumentParser(description="God Mode MCP Server")
    parser.add_argument("--debug", action="store_true", help="Enable debug output")
    args = parser.parse_args()
    
    debug = args.debug
    
    if debug:
        print("God Mode MCP Server started in debug mode", file=sys.stderr)
        print(f"Script directory: {SCRIPT_DIR}", file=sys.stderr)
        print(f"God Mode directory: {GOD_MODE_DIR}", file=sys.stderr)
    else:
        print("God Mode MCP Server started", file=sys.stderr)
    
    # Simple stdio-based MCP server
    try:
        while True:
            # Read a line from stdin
            line = sys.stdin.readline()
            if not line:
                break
            
            # Parse the request
            try:
                if debug:
                    print(f"Received: {line}", file=sys.stderr)
                
                request = json.loads(line)
                response = handle_mcp_request(request)
                
                if debug:
                    print(f"Sending: {json.dumps(response)}", file=sys.stderr)
                
                # Send the response
                print(json.dumps(response), flush=True)
            except json.JSONDecodeError:
                error_response = {"error": "Invalid JSON"}
                if debug:
                    print(f"Error: Invalid JSON\nLine: {line}", file=sys.stderr)
                    print(f"Sending: {json.dumps(error_response)}", file=sys.stderr)
                print(json.dumps(error_response), flush=True)
    except KeyboardInterrupt:
        print("MCP server stopped", file=sys.stderr)
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 