#!/usr/bin/env python3

"""
Message Router Script for God Mode

This script automatically routes structured AI outputs to the appropriate documentation 
and log files based on special markers like [LOG_SUMMARY], [LOG_DETAIL], [MEMORY_UPDATE], etc.

It now also tracks TAG compliance for reinforcement learning to ensure consistent TAG usage.

Usage:
    python script_message_router.py --input "message.txt"
    python script_message_router.py --clipboard  # Read from clipboard
    python script_message_router.py --watch      # Watch clipboard for changes
"""

import os
import re
import sys
import argparse
import time
from pathlib import Path
import datetime
import subprocess
import traceback

# Global debug flag
DEBUG_MODE = False

def debug_log(message):
    """Log debug messages when debug mode is enabled"""
    if DEBUG_MODE:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        print(f"[DEBUG] [{timestamp}] {message}")

# Import the tracking module
try:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, script_dir)
    from script_track_routing import add_routing_event
    TRACKING_AVAILABLE = True
    debug_log("✅ Tracking module loaded successfully")
except ImportError as e:
    TRACKING_AVAILABLE = False
    debug_log(f"⚠️ Tracking module not available: {str(e)}")
    def add_routing_event(tag, file_path, content, line_number=None):
        # Stub function when tracking module is not available
        debug_log(f"Would track: {tag} -> {file_path}")
        pass

# Import tag feedback module (if available)
try:
    from script_tag_feedback import validate_message, log_tag_validation
    TAG_FEEDBACK_AVAILABLE = True
    debug_log("✅ Tag feedback module loaded successfully")
except ImportError as e:
    TAG_FEEDBACK_AVAILABLE = False
    debug_log(f"⚠️ Tag feedback module not available: {str(e)}")
    # Simple stub implementations if the module is not available
    def validate_message(message):
        # Basic validation - just checks if any tags exist
        required_tags = ["LOG_SUMMARY", "LOG_DETAIL", "MEMORY_UPDATE"]
        is_valid = any(f"[{tag}]" in message for tag in required_tags)
        return is_valid, "Simple validation (without full tag feedback module)"
    
    def log_tag_validation(is_valid, reason):
        # Stub that does nothing
        debug_log(f"Would log validation: {is_valid}, reason: {reason}")
        pass

# Check for required dependencies
def check_dependencies():
    missing_deps = []
    debug_log("Checking dependencies...")
    try:
        import pyperclip
        debug_log("✓ pyperclip module found")
    except ImportError as e:
        debug_log(f"✗ Failed to import pyperclip: {str(e)}")
        missing_deps.append("pyperclip")
    
    try:
        import plyer
        debug_log("✓ plyer module found")
        try:
            from plyer import notification
            debug_log("✓ plyer.notification module working")
        except (ImportError, AttributeError) as e:
            debug_log(f"Warning: plyer found but notification module has issues: {str(e)}")
            debug_log("Desktop notifications might not work, but the router will continue.")
            # Don't add to missing_deps as we can still function without notifications
    except ImportError as e:
        debug_log(f"✗ Failed to import plyer: {str(e)}")
        missing_deps.append("plyer")
    
    if missing_deps:
        print(f"ERROR: Missing required dependencies: {', '.join(missing_deps)}")
        print("Please install them using:")
        print(f"pip install {' '.join(missing_deps)}")
        
        print("\nThe Message Router cannot function without these dependencies.")
        sys.exit(1)
    else:
        print("All required dependencies found.")
        return True

# Check dependencies before proceeding
check_dependencies()

# Now import the dependencies after checking
import pyperclip

# Add notification support if available
try:
    from plyer import notification
    NOTIFICATION_AVAILABLE = True
    print("Successfully imported plyer.notification")
except (ImportError, AttributeError) as e:
    print(f"Warning: Could not import plyer.notification: {str(e)}")
    print("Desktop notifications will be disabled")
    NOTIFICATION_AVAILABLE = False

# Import the timestamp module
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(script_dir, 'utils'))
from script_timestamp import get_log_timestamp

# Define the project root relative to this script
PROJECT_ROOT = Path(script_dir).parent.parent

# Define the memory directory
MEMORY_DIR = Path(script_dir).parent / "memory"

# Define the documentation directory
DOCUMENTATION_DIR = Path(script_dir).parent / "documentation"

# Define the discussion directory
DISCUSSION_DIR = Path(script_dir).parent / "discussion"

# Define the log files
LOG_SUMMARY_FILE = MEMORY_DIR / "memory_logs_all.md"
LOG_DETAIL_FILE = MEMORY_DIR / "memory_logs_detailed.md"

# Define memory files
MEMORY_UPDATE_FILE = MEMORY_DIR / "MEMORY_CURSOR.md"
MEMORY_LEARNINGS_FILE = MEMORY_DIR / "memory_learnings.md"
MEMORY_UPDATES_FILE = MEMORY_DIR / "memory_updates.md"
MEMORY_REQUIREMENTS_FILE = MEMORY_DIR / "memory_requirements.md"
MEMORY_ROADMAP_FILE = MEMORY_DIR / "memory_roadmap.md"
MEMORY_ARCHITECTURE_FILE = MEMORY_DIR / "memory_architecture.md"
MEMORY_CONVENTIONS_FILE = MEMORY_DIR / "memory_conventions.md"
MEMORY_DEPENDENCIES_FILE = MEMORY_DIR / "memory_dependencies.md"
MEMORY_GLOSSARY_FILE = MEMORY_DIR / "memory_glossary.md"
MEMORY_TESTING_FILE = MEMORY_DIR / "memory_testing.md"
MEMORY_SECURITY_FILE = MEMORY_DIR / "memory_security.md"
MEMORY_PERFORMANCE_FILE = MEMORY_DIR / "memory_performance.md"
MEMORY_ACCESSIBILITY_FILE = MEMORY_DIR / "memory_accessibility.md"

# Define marker patterns and their corresponding files
MARKERS = {
    r"\[LOG_SUMMARY\](.*?)(?=\[|\Z)": LOG_SUMMARY_FILE,
    r"\[LOG_DETAIL\](.*?)(?=\[|\Z)": LOG_DETAIL_FILE,
    r"\[MEMORY_UPDATE\](.*?)(?=\[|\Z)": MEMORY_UPDATE_FILE,
    r"\[MEMORY_LEARNINGS\](.*?)(?=\[|\Z)": MEMORY_LEARNINGS_FILE,
    r"\[MEMORY_UPDATES\](.*?)(?=\[|\Z)": MEMORY_UPDATES_FILE,
    r"\[MEMORY_REQUIREMENTS\](.*?)(?=\[|\Z)": MEMORY_REQUIREMENTS_FILE,
    r"\[MEMORY_ROADMAP\](.*?)(?=\[|\Z)": MEMORY_ROADMAP_FILE,
    r"\[MEMORY_ARCHITECTURE\](.*?)(?=\[|\Z)": MEMORY_ARCHITECTURE_FILE,
    r"\[MEMORY_CONVENTIONS\](.*?)(?=\[|\Z)": MEMORY_CONVENTIONS_FILE,
    r"\[MEMORY_DEPENDENCIES\](.*?)(?=\[|\Z)": MEMORY_DEPENDENCIES_FILE,
    r"\[MEMORY_GLOSSARY\](.*?)(?=\[|\Z)": MEMORY_GLOSSARY_FILE,
    r"\[MEMORY_TESTING\](.*?)(?=\[|\Z)": MEMORY_TESTING_FILE,
    r"\[MEMORY_SECURITY\](.*?)(?=\[|\Z)": MEMORY_SECURITY_FILE,
    r"\[MEMORY_PERFORMANCE\](.*?)(?=\[|\Z)": MEMORY_PERFORMANCE_FILE,
    r"\[MEMORY_ACCESSIBILITY\](.*?)(?=\[|\Z)": MEMORY_ACCESSIBILITY_FILE,
    r"\[FEATURE_LOG\s*:\s*([^]]+)\](.*?)(?=\[|\Z)": '',  # Special case for feature logs
    r"\[DOC_UPDATE\s*:\s*([^]]+)\](.*?)(?=\[|\Z)": '',   # Special case for documentation updates
}

# New multi-tag pattern
MULTI_TAG_PATTERN = r"\[MULTI_TAG\s*:\s*([^]]+)\](.*?)(?=\[|\Z)"

def send_notification(title, message):
    """Send a desktop notification if available."""
    debug_log(f"Attempting to send notification: {title} - {message}")
    if NOTIFICATION_AVAILABLE:
        try:
            notification.notify(
                title=title,
                message=message,
                app_name="God Mode",
                timeout=5  # seconds
            )
            debug_log(f"✓ Notification sent: {title} - {message}")
            print(f"✓ Notification sent: {title} - {message}")
            return True
        except Exception as e:
            debug_log(f"✗ Error sending notification: {str(e)}")
            print(f"Warning: Could not send notification: {str(e)}")
            print(f"Notification content: {title} - {message}")
            return False
    else:
        debug_log(f"Notifications not available. Would have shown: {title} - {message}")
        print(f"Info: Notification would have shown: {title} - {message}")
        return False

def get_timestamp():
    """Get current timestamp in YYYY-MM-DD HH:MM UTC format."""
    try:
        # Try to use the helper script if available
        timestamp_script = Path(script_dir) / "utils" / "script_timestamp.py"
        if timestamp_script.exists():
            result = subprocess.run(
                [sys.executable, str(timestamp_script)],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
    except Exception as e:
        print(f"Error using timestamp script: {e}")
    
    # Fallback to built-in datetime
    now_utc = datetime.datetime.now(datetime.timezone.utc)
    return now_utc.strftime("%Y-%m-%d %H:%M UTC")

def ensure_directory_exists(directory):
    """
    Ensure a directory exists, creating it if necessary.
    
    Args:
        directory (Path): Path to the directory
        
    Returns:
        bool: True if the directory exists or was created, False otherwise
    """
    try:
        os.makedirs(directory, exist_ok=True)
        return True
    except Exception as e:
        print(f"Error creating directory {directory}: {e}")
        return False

def ensure_file_exists(filepath):
    """
    Ensure a file exists, creating it with appropriate headers if necessary.
    
    Args:
        filepath (Path): Path to the file
        
    Returns:
        bool: True if the file exists or was created, False otherwise
    """
    # First ensure the parent directory exists
    if not ensure_directory_exists(filepath.parent):
        return False
        
    # Check if the file already exists
    if filepath.exists():
        return True
        
    # Create the file with appropriate headers based on file name
    try:
        with open(filepath, 'w') as f:
            filepath_str = str(filepath)
            if filepath_str.endswith('memory_logs_all.md'):
                f.write("# God Mode Summary Logs\n\nThis file contains summary logs of all God Mode activities.\n\n")
            elif filepath_str.endswith('memory_logs_detailed.md'):
                f.write("# God Mode Detailed Logs\n\nThis file contains detailed logs of all God Mode activities.\n\n")
            elif filepath_str.endswith('MEMORY_CURSOR.md'):
                f.write("# Memory: Project Context\n\nThis file contains important project context information that should persist across sessions.\n\n")
            elif filepath_str.endswith('memory_learnings.md'):
                f.write("# Memory: Learnings\n\nThis file contains lessons learned and insights gained during development.\n\n")
            elif filepath_str.endswith('memory_updates.md'):
                f.write("# Memory: Updates\n\nThis file contains important updates to the project.\n\n")
            elif filepath_str.endswith('memory_requirements.md'):
                f.write("# Memory: Requirements\n\nThis file contains project requirements and specifications.\n\n")
            elif filepath_str.endswith('memory_roadmap.md'):
                f.write("# Memory: Roadmap\n\nThis file contains the project roadmap and future plans.\n\n") 
            elif filepath_str.endswith('memory_architecture.md'):
                f.write("# Memory: Architecture\n\nThis file contains architectural decisions and design patterns.\n\n")
            elif filepath_str.endswith('memory_conventions.md'):
                f.write("# Memory: Conventions\n\nThis file contains coding conventions and style guidelines.\n\n")
            elif filepath_str.endswith('memory_dependencies.md'):
                f.write("# Memory: Dependencies\n\nThis file contains information about project dependencies.\n\n")
            elif filepath_str.endswith('memory_glossary.md'):
                f.write("# Memory: Glossary\n\nThis file contains definitions of key terms used in the project.\n\n")
            elif filepath_str.endswith('memory_testing.md'):
                f.write("# Memory: Testing\n\nThis file contains information about testing strategies and test cases.\n\n")
            elif filepath_str.endswith('memory_security.md'):
                f.write("# Memory: Security\n\nThis file contains security considerations and practices.\n\n")
            elif filepath_str.endswith('memory_performance.md'):
                f.write("# Memory: Performance\n\nThis file contains performance considerations and optimizations.\n\n")
            elif filepath_str.endswith('memory_accessibility.md'):
                f.write("# Memory: Accessibility\n\nThis file contains accessibility features and considerations.\n\n")
            else:
                f.write(f"# {filepath.stem}\n\nCreated: {datetime.datetime.now()}\n\n")
                
        debug_log(f"Created new file: {filepath}")
        return True
    except Exception as e:
        print(f"Error creating file {filepath}: {e}")
        return False

def append_to_file(file_path, content):
    """
    Append content to a file with timestamp
    
    Args:
        file_path (Path): Path to the file
        content (str): Content to append
        
    Returns:
        bool: True if successful, False otherwise
    """
    # First, ensure the file exists
    if not ensure_file_exists(file_path):
        return False
    
    # Track the current line count to determine where content will be added
    line_number = None
    try:
        with open(file_path, 'r') as f:
            line_number = sum(1 for _ in f) + 1  # +1 because we'll add content at the next line
    except:
        line_number = 1  # If file exists but can't be read, assume line 1
    
    try:
        # Add a timestamp to markdown files
        _, ext = os.path.splitext(file_path)
        if ext.lower() in ['.md', '.markdown', '.txt']:
            # Get current UTC time
            timestamp = datetime.datetime.utcnow()
            iso_format = timestamp.isoformat()
            filename_format = timestamp.strftime("%Y%m%d_%H%M%S")
            log_format = timestamp.strftime("%Y-%m-%d %H:%M:%S UTC")
            
            # Format header for timestamp
            header = f"\n\n## Current UTC timestamp: {timestamp.strftime('%Y-%m-%d %H:%M')} UTC\n"
            header += f"ISO format: {iso_format}\n"
            header += f"Filename format: {filename_format}\n"
            header += f"Log format: {log_format}\n\n"
            
            # Append to file
            with open(file_path, 'a') as f:
                f.write(header + content + "\n")
        else:
            # For non-markdown files, just append the content
            with open(file_path, 'a') as f:
                f.write("\n" + content + "\n")
        
        # Add to routing history
        if TRACKING_AVAILABLE:
            # Determine the tag based on the file path
            tag = "Unknown"
            file_path_str = str(file_path).lower()
            
            # Try to determine tag from filename patterns
            if "memory_logs_all.md" in file_path_str or "log_summary" in file_path_str:
                tag = "LOG_SUMMARY"
            elif "memory_logs_detailed.md" in file_path_str or "log_detail" in file_path_str:
                tag = "LOG_DETAIL"
            elif "memory_cursor.md" in file_path_str or "memory_update" in file_path_str:
                tag = "MEMORY_UPDATE"
            elif "feature_log" in file_path_str:
                # Extract feature name from path for feature logs
                match = re.search(r'feature_log[_-]([^/.]+)', file_path_str)
                if match:
                    feature_name = match.group(1)
                    tag = f"FEATURE_LOG:{feature_name}"
                else:
                    tag = "FEATURE_LOG:unknown"
            elif "documentation" in file_path_str:
                # Extract doc type for documentation files
                match = re.search(r'documentation[_-]([^/.]+)', file_path_str)
                if match:
                    doc_type = match.group(1)
                    tag = f"DOC_UPDATE:{doc_type}"
                else:
                    tag = "DOC_UPDATE:unknown"
            
            # Now track the event
            try:
                debug_log(f"Tracking routing event: {tag} -> {file_path}")
                add_routing_event(tag, file_path, content, line_number)
            except Exception as e:
                debug_log(f"Error tracking routing event: {e}")
        
        debug_log(f"✅ Content appended to {file_path.name}")
        return True
    except Exception as e:
        print(f"Error appending to {file_path}: {e}")
        return False

def process_feature_log(feature_name, content):
    """Process a feature log entry"""
    # Sanitize the feature name for file naming
    sanitized_name = feature_name.lower().replace(' ', '_')
    file_name = f"memory_log_feature_{sanitized_name}.md"
    
    # Use the memory directory for feature logs to match expectations
    feature_logs_dir = MEMORY_DIR
    ensure_directory_exists(feature_logs_dir)
    
    # Full path to the feature log file
    file_path = feature_logs_dir / file_name
    
    # Create the file if it doesn't exist
    if not file_path.exists():
        with open(file_path, 'w') as f:
            f.write(f"# Feature Log: {feature_name}\n\n")
            f.write("This file tracks development and changes related to this feature.\n\n")
        debug_log(f"Created new feature log file: {file_path}")
    
    # Append content to the file
    success = append_to_file(file_path, content)
    
    return success

def process_doc_update(doc_type, content):
    """Process a documentation update entry"""
    # Determine which documentation file to update
    if doc_type.lower() in ['project', 'system']:
        file_name = "documentation_project_main.md"
    elif doc_type.lower() in ['feature', 'features']:
        file_name = "documentation_feature_main.md"
    elif doc_type.lower() in ['design', 'architecture']:
        file_name = "documentation_design_main.md"
    elif doc_type.lower() in ['data', 'model', 'schema']:
        file_name = "documentation_data_model_main.md"
    else:
        file_name = f"documentation_{doc_type.lower()}_main.md"
    
    # Use the documentation directory
    doc_dir = DOCUMENTATION_DIR / doc_type.lower()
    ensure_file_exists(doc_dir / file_name)
    
    # Append to the documentation file
    append_to_file(doc_dir / file_name, content)

def process_single_tag(tag, content):
    """Process a single tag from a multi-tag block"""
    try:
        debug_log(f"Processing single tag: {tag}")
        
        # Handle feature logs
        feature_log_match = re.match(r"FEATURE_LOG\s*:\s*([^,]+)", tag)
        if feature_log_match:
            feature_name = feature_log_match.group(1).strip()
            process_feature_log(feature_name, content)
            return

        # Handle doc updates
        doc_update_match = re.match(r"DOC_UPDATE\s*:\s*([^,]+)", tag)
        if doc_update_match:
            doc_type = doc_update_match.group(1).strip()
            process_doc_update(doc_type, content)
            return

        # Handle standard tags
        for pattern, file_path in MARKERS.items():
            # Convert regex pattern to a simple tag name for comparison
            # This is a heuristic approach - it may need refinement
            simple_pattern = pattern.replace(r"\[", "").replace(r"\]", "").split("\\")[0]
            if tag == simple_pattern or tag == simple_pattern.replace("_", " "):
                if file_path:
                    debug_log(f"Matched tag {tag} to file {file_path}")
                    append_to_file(file_path, content)
                    send_notification("Content Routed", f"Content added to {os.path.basename(file_path)}")
                    return
        
        debug_log(f"No matching file found for tag: {tag}")
    except Exception as e:
        print(f"Error processing tag '{tag}': {str(e)}")
        debug_log(f"Exception in process_single_tag: {str(e)}")
        debug_log(traceback.format_exc())

def route_message(message):
    """Process a message and extract/route content based on markers."""
    updated_files = []
    
    # Validate message structure before routing
    if TAG_FEEDBACK_AVAILABLE:
        is_valid, reason = validate_message(message)
        log_tag_validation(is_valid, reason)
        if not is_valid:
            debug_log(f"⚠️ Message validation failed: {reason}")
            # We still process the message even if validation fails
            # This ensures content isn't lost, but the feedback loop will improve future messages
    
    # Process multi-tag content first
    debug_log("Processing multi-tag content")
    multi_tag_matches = re.finditer(MULTI_TAG_PATTERN, message, re.DOTALL)
    for match in multi_tag_matches:
        tags_str = match.group(1).strip()
        content = match.group(2).strip()
        
        if not content:
            debug_log(f"Multi-tag content for '{tags_str}' is empty, skipping")
            continue
            
        debug_log(f"Found multi-tag: {tags_str}")
        # Parse the tags (comma-separated list)
        tags = [tag.strip() for tag in tags_str.split(',')]
        
        for tag in tags:
            debug_log(f"Processing tag '{tag}' from multi-tag")
            # Handle standard memory tags
            if tag.upper() in [
                "LOG_SUMMARY", "LOG_DETAIL", "MEMORY_UPDATE",
                "MEMORY_LEARNINGS", "MEMORY_UPDATES", "MEMORY_REQUIREMENTS",
                "MEMORY_ROADMAP", "MEMORY_ARCHITECTURE", "MEMORY_CONVENTIONS",
                "MEMORY_DEPENDENCIES", "MEMORY_GLOSSARY", "MEMORY_TESTING",
                "MEMORY_SECURITY", "MEMORY_PERFORMANCE", "MEMORY_ACCESSIBILITY"
            ]:
                # Find the corresponding file for this tag
                for pattern, file_path in MARKERS.items():
                    if tag.upper() in pattern:
                        if append_to_file(file_path, content):
                            updated_files.append(file_path.name)
                        break
            
            # Handle feature logs (format: FEATURE_LOG:Name)
            elif tag.upper().startswith("FEATURE_LOG:"):
                parts = tag.split(":", 1)
                if len(parts) == 2:
                    feature_name = parts[1].strip()
                    process_feature_log(feature_name, content)
                    updated_files.append(f"feature_log_{feature_name.lower().replace(' ', '_')}.md")
            
            # Handle documentation updates (format: DOC_UPDATE:Type)
            elif tag.upper().startswith("DOC_UPDATE:"):
                parts = tag.split(":", 1)
                if len(parts) == 2:
                    doc_type = parts[1].strip()
                    process_doc_update(doc_type, content)
                    updated_files.append(f"documentation_{doc_type.lower()}_main.md")
    
    # Process standard markers
    debug_log("Processing standard markers")
    for pattern, file_path in MARKERS.items():
        debug_log(f"Checking pattern {pattern}")
        matches = re.finditer(pattern, message, re.DOTALL)
        for match in matches:
            content = match.group(1).strip()
            debug_log(f"Found pattern match for {pattern}, saving to {file_path}")
            if content and append_to_file(file_path, content):
                updated_files.append(file_path.name)
    
    # Special case for feature logs
    debug_log("Processing feature logs")
    feature_pattern = r"\[FEATURE_LOG\s*:\s*([^]]+)\](.*?)(?=\[|\Z)"
    for match in re.finditer(feature_pattern, message, re.DOTALL):
        feature_name = match.group(1).strip()
        content = match.group(2).strip()
        if feature_name and content:
            process_feature_log(feature_name, content)
            updated_files.append(f"feature_log_{feature_name.lower().replace(' ', '_')}.md")
    
    # Special case for documentation updates
    debug_log("Processing documentation updates")
    doc_pattern = r"\[DOC_UPDATE\s*:\s*([^]]+)\](.*?)(?=\[|\Z)"
    for match in re.finditer(doc_pattern, message, re.DOTALL):
        doc_type = match.group(1).strip()
        content = match.group(2).strip()
        if doc_type and content:
            process_doc_update(doc_type, content)
            updated_files.append(f"documentation_{doc_type.lower()}_main.md")
    
    # Show notification with summary of updated files
    if updated_files:
        title = "God Mode: Content Routed"
        if len(updated_files) == 1:
            message = f"Updated file: {updated_files[0]}"
        else:
            message = f"Updated {len(updated_files)} files"
            if len(updated_files) <= 5:  # Show all files if 5 or fewer
                message += ":\n" + "\n".join(f"- {f}" for f in updated_files)
            else:  # Show just the first 3 if more than 5
                message += f" including:\n" + "\n".join(f"- {f}" for f in updated_files[:3]) + "\n- ..."
        send_notification(title, message)
    else:
        debug_log("No content found to route")
    
    return len(updated_files)

def read_from_file(filepath):
    """Read content from a file"""
    try:
        with open(filepath, 'r') as f:
            return f.read()
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return None

def read_from_clipboard():
    """Read content from the clipboard"""
    try:
        return pyperclip.paste()
    except Exception as e:
        print(f"❌ Error reading clipboard: {e}")
        return None

def watch_clipboard(interval=2.0):
    """Watch clipboard for changes and process routing when markers are detected."""
    try:
        debug_log("Attempting to import pyperclip for clipboard watching")
        import pyperclip
        
        # Initial clipboard read with error handling
        try:
            previous_content = pyperclip.paste()
            print("✅ Successfully connected to clipboard")
        except Exception as e:
            print(f"❌ Error accessing clipboard: {e}")
            print("💡 Troubleshooting tips:")
            print("  - Make sure pyperclip is installed: pip install pyperclip")
            print("  - On Linux, you may need xclip or xsel: sudo apt-get install xclip")
            print("  - On macOS, ensure terminal has accessibility permissions")
            debug_log(f"Error initializing clipboard access: {str(e)}")
            return
        
        print(f"⏱️  Checking clipboard every {interval} seconds...")
        
        last_update_time = time.time()
        
        while True:
            try:
                current_content = pyperclip.paste()
                
                # Only process if the content has changed and contains a marker pattern
                if current_content != previous_content:
                    debug_log("Clipboard content changed")
                    
                    # Check if the content contains any of our markers
                    contains_marker = False
                    
                    # Check for any marker pattern
                    for pattern in MARKERS.keys():
                        if re.search(pattern, current_content, re.DOTALL):
                            contains_marker = True
                            break
                    
                    # Check for multi-tag pattern
                    if not contains_marker and re.search(MULTI_TAG_PATTERN, current_content, re.DOTALL):
                        contains_marker = True
                    
                    # Check for feature log pattern
                    if not contains_marker and re.search(r"\[FEATURE_LOG\s*:\s*([^]]+)\]", current_content, re.DOTALL):
                        contains_marker = True
                    
                    # Check for doc update pattern
                    if not contains_marker and re.search(r"\[DOC_UPDATE\s*:\s*([^]]+)\]", current_content, re.DOTALL):
                        contains_marker = True
                    
                    # Validate message (even if no markers found, this helps catch missing tags)
                    if TAG_FEEDBACK_AVAILABLE:
                        is_valid, reason = validate_message(current_content)
                        log_tag_validation(is_valid, reason)
                        
                        if not is_valid and not contains_marker:
                            # Print validation warning only if no markers were found
                            # (to avoid duplicate messages when routing happens)
                            print("\n⚠️ Clipboard content missing required TAGs")
                            print(f"Reason: {reason}")
                            # We still update previous_content to avoid repeated warnings
                    
                    if contains_marker:
                        print("\n📋 New clipboard content detected with markers")
                        updated_files = route_message(current_content)
                        if updated_files > 0:
                            print(f"✅ Successfully routed content to {updated_files} file(s)")
                        else:
                            print("ℹ️ No content was routed")
                    else:
                        debug_log("Clipboard changed but no markers found")
                    
                    previous_content = current_content
                
                # Log a heartbeat every 60 seconds
                current_time = time.time()
                if current_time - last_update_time > 60:
                    debug_log("Clipboard watcher heartbeat - still running")
                    last_update_time = current_time
                
                time.sleep(interval)
            except KeyboardInterrupt:
                print("\n🛑 Clipboard watching stopped by user")
                break
            except Exception as e:
                print(f"❌ Error watching clipboard: {e}")
                print(f"⚠️ Will try again in {interval} seconds...")
                debug_log(f"Exception in clipboard watcher: {str(e)}")
                debug_log(traceback.format_exc())
                # Continue watching despite errors
                time.sleep(interval)
    except Exception as e:
        print(f"Critical error in watch_clipboard: {str(e)}")
        debug_log(f"Critical exception in watch_clipboard: {str(e)}")
        debug_log(traceback.format_exc())
        raise

def main():
    """Main entry point for the message router script."""
    global DEBUG_MODE
    
    # Set up command line argument parsing
    parser = argparse.ArgumentParser(description='Route messages with special markers to appropriate files.')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--input', type=str, help='Input file to read from')
    group.add_argument('--clipboard', action='store_true', help='Read from clipboard')
    group.add_argument('--watch', action='store_true', help='Watch clipboard for changes')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode for verbose logging')
    parser.add_argument('--interval', type=float, default=2.0, help='Polling interval in seconds for --watch mode')
    
    try:
        args = parser.parse_args()
        
        # Set debug mode if requested
        DEBUG_MODE = args.debug
        
        if DEBUG_MODE:
            print("Debug mode enabled - verbose logging active")
            debug_log("Debug mode initialized")
            debug_log(f"Arguments: {args}")
        
        # Create log directory if it doesn't exist
        log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'logs')
        os.makedirs(log_dir, exist_ok=True)
        debug_log(f"Log directory: {log_dir}")
        
        message = None
        
        if args.input:
            debug_log(f"Reading from input file: {args.input}")
            try:
                message = read_from_file(args.input)
                if message:
                    updated_files = route_message(message)
                    if updated_files > 0:
                        print(f"✅ Successfully routed content to {updated_files} file(s)")
                    else:
                        print("ℹ️ No markers found to route")
                else:
                    print("❌ Input file is empty")
            except Exception as e:
                print(f"Error reading from file: {str(e)}")
                debug_log(f"Exception reading from file: {str(e)}")
                debug_log(traceback.format_exc())
                return 1
                
        elif args.clipboard:
            debug_log("Reading from clipboard")
            try:
                message = read_from_clipboard()
                if message:
                    updated_files = route_message(message)
                    if updated_files > 0:
                        print(f"✅ Successfully routed content to {updated_files} file(s)")
                    else:
                        print("ℹ️ No markers found to route")
                else:
                    print("❌ Clipboard is empty")
            except Exception as e:
                print(f"Error reading from clipboard: {str(e)}")
                debug_log(f"Exception reading from clipboard: {str(e)}")
                debug_log(traceback.format_exc())
                return 1
                
        elif args.watch:
            debug_log(f"Watching clipboard with interval: {args.interval}s")
            try:
                watch_clipboard(interval=args.interval)
            except Exception as e:
                print(f"Error watching clipboard: {str(e)}")
                debug_log(f"Exception watching clipboard: {str(e)}")
                debug_log(traceback.format_exc())
                return 1
        
        return 0
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        if DEBUG_MODE:
            debug_log(f"Unexpected exception in main: {str(e)}")
            debug_log(traceback.format_exc())
        return 1

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except Exception as e:
        print(f"Critical error: {str(e)}")
        if 'DEBUG_MODE' in globals() and DEBUG_MODE:
            debug_log(f"Critical exception: {str(e)}")
            debug_log(traceback.format_exc())
        sys.exit(1) 