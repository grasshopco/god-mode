# Project Functions
*Generated: Current UTC timestamp: 2025-03-04 09:26 UTC
ISO format: 2025-03-04T09:26:41.071664+00:00
Filename format: 20250304_092641
Log format: 2025-03-04 09:26:41 UTC*
This document maps all functions and methods in the project.

## Table of Contents
- [god_mode/scripts/examples/demo_router_usage.py](#god_mode_scripts_examples_demo_router_usage_py)
- [god_mode/scripts/script_analyze_patterns.py](#god_mode_scripts_script_analyze_patterns_py)
- [god_mode/scripts/script_cursor_watch.py](#god_mode_scripts_script_cursor_watch_py)
- [god_mode/scripts/script_debug_router.py](#god_mode_scripts_script_debug_router_py)
- [god_mode/scripts/script_enhance_prompt.py](#god_mode_scripts_script_enhance_prompt_py)
- [god_mode/scripts/script_get_utc_time.py](#god_mode_scripts_script_get_utc_time_py)
- [god_mode/scripts/script_initialize_tracking.py](#god_mode_scripts_script_initialize_tracking_py)
- [god_mode/scripts/script_message_router.py](#god_mode_scripts_script_message_router_py)
- [god_mode/scripts/script_track_routing.py](#god_mode_scripts_script_track_routing_py)
- [god_mode/scripts/script_update_cursor_rules.py](#god_mode_scripts_script_update_cursor_rules_py)
- [god_mode/scripts/script_update_functions_and_types.py](#god_mode_scripts_script_update_functions_and_types_py)
- [god_mode/scripts/script_update_project_structure.py](#god_mode_scripts_script_update_project_structure_py)
- [god_mode/scripts/tests/test_message_router.py](#god_mode_scripts_tests_test_message_router_py)
- [god_mode/scripts/utils/script_timestamp.py](#god_mode_scripts_utils_script_timestamp_py)

## god_mode/scripts/examples/demo_router_usage.py <a id='god_mode_scripts_examples_demo_router_usage_py'></a>

### **demo_direct_function_call()**

- **Type**: function
- **Line**: 19

Demonstrate using the router by directly calling its functions.

### **demo_subprocess_call()**

- **Type**: function
- **Line**: 44

Demonstrate using the router by calling it as a subprocess.

### **demo_in_memory_generation()**

- **Type**: function
- **Line**: 83

Demonstrate generating content with markers in code.


## god_mode/scripts/script_analyze_patterns.py <a id='god_mode_scripts_script_analyze_patterns_py'></a>

### **ensure_directory_exists(directory)**

- **Type**: function
- **Line**: 45

Ensure a directory exists, creating it if necessary.

### **get_timestamp()**

- **Type**: function
- **Line**: 49

Get current timestamp in YYYY-MM-DD HH:MM UTC format.

### **get_recent_discussion_files(days)**

- **Type**: function
- **Line**: 69

Get recent discussion files from the last N days.

Args:
    days (int): Number of days to look back
    
Returns:
    list: List of discussion file paths

### **extract_user_queries(file_path)**

- **Type**: function
- **Line**: 99

Extract user queries from a discussion file.

Args:
    file_path (str): Path to the discussion file
    
Returns:
    list: List of user query strings

### **extract_ai_responses(file_path)**

- **Type**: function
- **Line**: 130

Extract AI responses from a discussion file.

Args:
    file_path (str): Path to the discussion file
    
Returns:
    list: List of AI response strings

### **analyze_query_keywords(queries)**

- **Type**: function
- **Line**: 161

Analyze keywords used in user queries.

Args:
    queries (list): List of user query strings
    
Returns:
    Counter: Frequency count of keywords

### **analyze_query_patterns(queries)**

- **Type**: function
- **Line**: 205

Analyze patterns in user queries.

Args:
    queries (list): List of user query strings
    
Returns:
    dict: Dictionary of identified patterns

### **analyze_response_effectiveness(queries, responses)**

- **Type**: function
- **Line**: 306

Analyze the effectiveness of AI responses based on user follow-ups.

Args:
    queries (list): List of user query strings
    responses (list): List of AI response strings
    
Returns:
    dict: Dictionary of effectiveness metrics

### **identify_improvement_opportunities(keywords, patterns, effectiveness)**

- **Type**: function
- **Line**: 388

Identify opportunities for improving the God Mode system.

Args:
    keywords (Counter): Frequency count of keywords
    patterns (dict): Dictionary of identified patterns
    effectiveness (dict): Dictionary of effectiveness metrics
    
Returns:
    list: List of improvement opportunities

### **generate_improvement_recommendations(keywords, patterns, effectiveness, opportunities)**

- **Type**: function
- **Line**: 436

Generate specific recommendations for improving the God Mode system.

Args:
    keywords (Counter): Frequency count of keywords
    patterns (dict): Dictionary of identified patterns
    effectiveness (dict): Dictionary of effectiveness metrics
    opportunities (list): List of improvement opportunities
    
Returns:
    str: Markdown formatted recommendations

### **generate_prompt_learnings(keywords, patterns, effectiveness, opportunities)**

- **Type**: function
- **Line**: 588

Generate learnings for improving prompts based on interaction analysis.

Args:
    keywords (Counter): Frequency count of keywords
    patterns (dict): Dictionary of identified patterns
    effectiveness (dict): Dictionary of effectiveness metrics
    opportunities (list): List of improvement opportunities
    
Returns:
    str: Markdown formatted prompt learnings

### **update_patterns_file(content)**

- **Type**: function
- **Line**: 679

Update the patterns file with new content.

Args:
    content (str): New content to write
    
Returns:
    bool: True if successful, False otherwise

### **update_prompt_learnings_file(content)**

- **Type**: function
- **Line**: 722

Update the prompt learnings file with new content.

Args:
    content (str): New content to append
    
Returns:
    bool: True if successful, False otherwise

### **main()**

- **Type**: function
- **Line**: 760

Main function to parse arguments and analyze patterns.


## god_mode/scripts/script_cursor_watch.py <a id='god_mode_scripts_script_cursor_watch_py'></a>

### **ensure_directory_exists(directory)**

- **Type**: function
- **Line**: 55

Ensure a directory exists, creating it if necessary.

### **log_message(message)**

- **Type**: function
- **Line**: 59

Log a message to the log file.

### **is_valid_conversation_file(file_path)**

- **Type**: function
- **Line**: 67

Check if a file is a valid Cursor conversation file.

Args:
    file_path (Path): Path to the file to check
    
Returns:
    bool: True if the file is a valid conversation file, False otherwise

### **find_cursor_conversation_file()**

- **Type**: function
- **Line**: 109

Find the Cursor conversation file.
This function tries different possible locations based on the OS.

Returns:
    Path: Path to the Cursor conversation file, or None if not found

### **enhance_user_prompt(prompt)**

- **Type**: function
- **Line**: 190

Enhance a user prompt using the script_enhance_prompt.py script.

Args:
    prompt (str): The user's original prompt
    
Returns:
    str: The enhanced prompt, or the original prompt if enhancement fails

### **watch_cursor_conversation()**

- **Type**: function
- **Line**: 229

Watch the Cursor conversation file for changes and enhance user prompts.

### **main()**

- **Type**: function
- **Line**: 339

Main function to run the script.


## god_mode/scripts/script_debug_router.py <a id='god_mode_scripts_script_debug_router_py'></a>

### **log(message, level)**

- **Type**: function
- **Line**: 27

Log a message to both the console and log file

### **log_separator()**

- **Type**: function
- **Line**: 37

*No documentation available.*

### **log_system_info()**

- **Type**: function
- **Line**: 40

Log detailed system information

### **log_python_path()**

- **Type**: function
- **Line**: 61

Log details about Python path and modules

### **check_module_path(module_name)**

- **Type**: function
- **Line**: 73

Check if a module can be imported and log its path

### **log_dependencies()**

- **Type**: function
- **Line**: 87

Check and log status of dependencies

### **check_file_permissions()**

- **Type**: function
- **Line**: 132

Check permissions of critical files

### **check_route_script()**

- **Type**: function
- **Line**: 157

Check if the route script exists and is executable

### **run_with_error_handling()**

- **Type**: function
- **Line**: 202

Run the message router with comprehensive error handling

### **main()**

- **Type**: function
- **Line**: 259

Main function that runs diagnostics and tries to start the message router


## god_mode/scripts/script_enhance_prompt.py <a id='god_mode_scripts_script_enhance_prompt_py'></a>

### **ensure_directory_exists(directory)**

- **Type**: function
- **Line**: 58

Ensure a directory exists, creating it if necessary.

### **load_file_content(file_path, max_lines, recent_only)**

- **Type**: function
- **Line**: 62

Load content from a file.

Args:
    file_path (Path): Path to the file
    max_lines (int): Maximum number of lines to read
    recent_only (bool): If True, read only the most recent entries
    
Returns:
    str: The file content or empty string if file doesn't exist

### **get_recent_discussion_content()**

- **Type**: function
- **Line**: 102

Get content from recent discussions.

### **get_project_structure()**

- **Type**: function
- **Line**: 115

Get a summary of the project structure.

### **get_recent_changes()**

- **Type**: function
- **Line**: 130

Get a summary of recent changes from the logs.

### **get_system_context()**

- **Type**: function
- **Line**: 135

Get information about the user's system.

### **should_include_file(file_name, user_query)**

- **Type**: function
- **Line**: 145

Determine if a file should be included in context based on the user query.
This uses simple keyword matching - more sophisticated methods could be used.

### **get_specialized_memory_content(user_query)**

- **Type**: function
- **Line**: 177

Get content from specialized memory files based on the user query.
Only includes relevant files to avoid context overload.

### **get_notepad_references(user_query)**

- **Type**: function
- **Line**: 200

Get references to relevant notepads based on the user query.

### **load_cache()**

- **Type**: function
- **Line**: 236

Load the context cache if it exists.

### **save_cache(cache)**

- **Type**: function
- **Line**: 248

Save the context cache.

### **enhance_prompt(prompt)**

- **Type**: function
- **Line**: 258

Enhance a user prompt with relevant context.

Args:
    prompt (str): The user's original prompt
    
Returns:
    str: The enhanced prompt with context

### **main()**

- **Type**: function
- **Line**: 341

Main function to parse arguments and enhance prompts.


## god_mode/scripts/script_get_utc_time.py <a id='god_mode_scripts_script_get_utc_time_py'></a>

### **get_utc_time()**

- **Type**: function
- **Line**: 10

Return current UTC time in the format YYYY-MM-DD HH:MM UTC


## god_mode/scripts/script_initialize_tracking.py <a id='god_mode_scripts_script_initialize_tracking_py'></a>

### **ensure_directory_exists(directory)**

- **Type**: function
- **Line**: 30

Ensure a directory exists, creating it if necessary.

### **initialize_tracking()**

- **Type**: function
- **Line**: 34

Initialize the tracking system.

### **main()**

- **Type**: function
- **Line**: 70

Main function.


## god_mode/scripts/script_message_router.py <a id='god_mode_scripts_script_message_router_py'></a>

### **debug_log(message)**

- **Type**: function
- **Line**: 28

Log debug messages when debug mode is enabled

### **add_routing_event(tag, file_path, content, line_number)**

- **Type**: function
- **Line**: 44

*No documentation available.*

### **check_dependencies()**

- **Type**: function
- **Line**: 50

*No documentation available.*

### **send_notification(title, message)**

- **Type**: function
- **Line**: 161

Send a desktop notification if available.

### **get_timestamp()**

- **Type**: function
- **Line**: 185

Get current timestamp in YYYY-MM-DD HH:MM UTC format.

### **ensure_directory_exists(directory)**

- **Type**: function
- **Line**: 205

Ensure a directory exists, creating it if necessary.

Args:
    directory (Path): Path to the directory
    
Returns:
    bool: True if the directory exists or was created, False otherwise

### **ensure_file_exists(filepath)**

- **Type**: function
- **Line**: 222

Ensure a file exists, creating it with appropriate headers if necessary.

Args:
    filepath (Path): Path to the file
    
Returns:
    bool: True if the file exists or was created, False otherwise

### **append_to_file(file_path, content)**

- **Type**: function
- **Line**: 283

Append content to a file with timestamp

Args:
    file_path (Path): Path to the file
    content (str): Content to append
    
Returns:
    bool: True if successful, False otherwise

### **process_feature_log(feature_name, content)**

- **Type**: function
- **Line**: 373

Process a feature log entry

### **process_doc_update(doc_type, content)**

- **Type**: function
- **Line**: 398

Process a documentation update entry

### **process_single_tag(tag, content)**

- **Type**: function
- **Line**: 419

Process a single tag from a multi-tag block

### **route_message(message)**

- **Type**: function
- **Line**: 456

Process a message and extract/route content based on markers.

### **read_from_file(filepath)**

- **Type**: function
- **Line**: 556

Read content from a file

### **read_from_clipboard()**

- **Type**: function
- **Line**: 565

Read content from the clipboard

### **watch_clipboard(interval)**

- **Type**: function
- **Line**: 573

Watch clipboard for changes and process any content with markers.

### **main()**

- **Type**: function
- **Line**: 661

Main entry point for the message router script.


## god_mode/scripts/script_track_routing.py <a id='god_mode_scripts_script_track_routing_py'></a>

### **ensure_directory_exists(directory)**

- **Type**: function
- **Line**: 50

Ensure a directory exists, creating it if necessary.

### **load_routing_history()**

- **Type**: function
- **Line**: 54

Load routing history from file.

### **save_routing_history(history)**

- **Type**: function
- **Line**: 66

Save routing history to file.

### **add_routing_event(tag, file_path, content, line_number)**

- **Type**: function
- **Line**: 76

Add a new routing event to the history.

### **get_file_line_count(file_path)**

- **Type**: function
- **Line**: 97

Get the number of lines in a file.

### **open_file(file_path, line_number)**

- **Type**: function
- **Line**: 105

Open a file in the default text editor, optionally at a specific line.

### **format_relative_time(timestamp_str)**

- **Type**: function
- **Line**: 188

Format a timestamp as a relative time (e.g., '2 minutes ago').

### **truncate_path(path, max_length)**

- **Type**: function
- **Line**: 220

Truncate a path to a reasonable length for display.

### **display_routing_history(limit)**

- **Type**: function
- **Line**: 238

Display recent routing history.

### **main()**

- **Type**: function
- **Line**: 274

Main function to parse arguments and display or open files.


## god_mode/scripts/script_update_cursor_rules.py <a id='god_mode_scripts_script_update_cursor_rules_py'></a>

### **ensure_directory_exists(directory)**

- **Type**: function
- **Line**: 128

Ensure a directory exists, creating it if necessary.

### **read_cursor_rules_legacy()**

- **Type**: function
- **Line**: 132

Read the existing .cursorrules file.

Returns:
    str: The content of the .cursorrules file, or empty string if it doesn't exist

### **write_cursor_rules_legacy(content)**

- **Type**: function
- **Line**: 149

Write content to the .cursorrules file.

Args:
    content (str): The content to write
    
Returns:
    bool: True if successful, False otherwise

### **has_marker_rules_legacy(content)**

- **Type**: function
- **Line**: 172

Check if the content already has marker rules.

Args:
    content (str): The content to check
    
Returns:
    bool: True if marker rules exist, False otherwise

### **update_cursor_rules_legacy(force)**

- **Type**: function
- **Line**: 195

Update the .cursorrules file with marker rules.

Args:
    force (bool): Whether to force update even if marker rules already exist
    
Returns:
    bool: True if successful, False otherwise

### **update_cursor_rules_json(force)**

- **Type**: function
- **Line**: 240

Update or create the cursorrules.json file.

Args:
    force (bool): Whether to force update even if rule file already exists
    
Returns:
    bool: True if successful, False otherwise

### **update_cursor_config_json()**

- **Type**: function
- **Line**: 289

Update the cursor.json config file to set enhanced mode.

Returns:
    bool: True if successful, False otherwise

### **main()**

- **Type**: function
- **Line**: 319

Main function to parse arguments and update cursor rules.


## god_mode/scripts/script_update_functions_and_types.py <a id='god_mode_scripts_script_update_functions_and_types_py'></a>

### **ensure_directory_exists(directory)**

- **Type**: function
- **Line**: 61

Ensure a directory exists, creating it if necessary.

### **get_timestamp()**

- **Type**: function
- **Line**: 65

Get current timestamp in YYYY-MM-DD HH:MM UTC format.

### **determine_language(file_path)**

- **Type**: function
- **Line**: 85

Determine the programming language of a file based on its extension.

### **PythonAnalyzer.analyze_file(file_path)**

- **Type**: method
- **Line**: 97

Analyze a Python file for functions, classes, and types.

Args:
    file_path (str): Path to the Python file
    
Returns:
    tuple: (functions, types) where each is a list of dictionaries

### **analyze_file(file_path)**

- **Type**: function
- **Line**: 97

Analyze a Python file for functions, classes, and types.

Args:
    file_path (str): Path to the Python file
    
Returns:
    tuple: (functions, types) where each is a list of dictionaries

### **JavaScriptAnalyzer.analyze_file(file_path)**

- **Type**: method
- **Line**: 174

Analyze a JavaScript/TypeScript file for functions, classes, and types.

Args:
    file_path (str): Path to the JS/TS file
    
Returns:
    tuple: (functions, types) where each is a list of dictionaries

### **analyze_file(file_path)**

- **Type**: function
- **Line**: 174

Analyze a JavaScript/TypeScript file for functions, classes, and types.

Args:
    file_path (str): Path to the JS/TS file
    
Returns:
    tuple: (functions, types) where each is a list of dictionaries

### **get_analyzer_for_language(language)**

- **Type**: function
- **Line**: 262

Get the appropriate analyzer for a language.

### **scan_directory(directory, exclude_dirs)**

- **Type**: function
- **Line**: 271

Scan a directory for code files and analyze them.

Args:
    directory (str or Path): The directory to scan
    exclude_dirs (list): List of directory patterns to exclude
    
Returns:
    tuple: (functions, types) where each is a list of dictionaries

### **generate_functions_markdown(functions)**

- **Type**: function
- **Line**: 305

Generate Markdown documentation for functions.

Args:
    functions (list): List of function dictionaries
    
Returns:
    str: Markdown content

### **generate_types_markdown(types)**

- **Type**: function
- **Line**: 369

Generate Markdown documentation for types.

Args:
    types (list): List of type dictionaries
    
Returns:
    str: Markdown content

### **write_markdown_file(content, file_path)**

- **Type**: function
- **Line**: 427

Write content to a Markdown file.

### **main()**

- **Type**: function
- **Line**: 436

Main function to parse arguments and execute the script.


## god_mode/scripts/script_update_project_structure.py <a id='god_mode_scripts_script_update_project_structure_py'></a>

### **parse_existing_structure()**

- **Type**: function
- **Line**: 67

Parse the existing project structure file to extract descriptions.

Returns:
    dict: A dictionary mapping file/directory paths to descriptions

### **should_ignore(path)**

- **Type**: function
- **Line**: 93

Check if a path should be ignored.

Args:
    path (Path): The path to check
    
Returns:
    bool: True if the path should be ignored, False otherwise

### **scan_directory(directory, prefix, descriptions, indent_level, processed_paths)**

- **Type**: function
- **Line**: 117

Recursively scan a directory and generate a markdown representation.

Args:
    directory (Path): The directory to scan
    prefix (str): The prefix to use for relative paths
    descriptions (dict): A dictionary mapping file/directory paths to descriptions
    indent_level (int): The current indentation level
    processed_paths (set): Set of already processed paths to avoid duplicates
    
Returns:
    list: A list of markdown lines representing the directory structure

### **generate_structure_content(descriptions)**

- **Type**: function
- **Line**: 220

Generate the content for the project structure file.

Args:
    descriptions (dict): A dictionary mapping file/directory paths to descriptions
    
Returns:
    str: The content for the project structure file

### **update_project_structure()**

- **Type**: function
- **Line**: 266

Update the project structure file.


## god_mode/scripts/tests/test_message_router.py <a id='god_mode_scripts_tests_test_message_router_py'></a>

### **TestMessageRouter.setUp(self)**

- **Type**: method
- **Line**: 28

Set up temporary directory and files for testing.

### **setUp(self)**

- **Type**: function
- **Line**: 28

Set up temporary directory and files for testing.

### **TestMessageRouter.tearDown(self)**

- **Type**: method
- **Line**: 38

Clean up temporary files and restore environment.

### **tearDown(self)**

- **Type**: function
- **Line**: 38

Clean up temporary files and restore environment.

### **TestMessageRouter.test_ensure_file_exists(self)**

- **Type**: method
- **Line**: 50

Test that ensure_file_exists creates files and directories as needed.

### **test_ensure_file_exists(self)**

- **Type**: function
- **Line**: 50

Test that ensure_file_exists creates files and directories as needed.

### **TestMessageRouter.test_append_to_file(self)**

- **Type**: method
- **Line**: 60

Test appending content to a file.

### **test_append_to_file(self)**

- **Type**: function
- **Line**: 60

Test appending content to a file.

### **TestMessageRouter.test_parse_marker(self)**

- **Type**: method
- **Line**: 85

Test parsing markers from text.

### **test_parse_marker(self)**

- **Type**: function
- **Line**: 85

Test parsing markers from text.

### **TestMessageRouter.test_route_message(self)**

- **Type**: method
- **Line**: 107

Test routing messages with various markers.

### **test_route_message(self)**

- **Type**: function
- **Line**: 107

Test routing messages with various markers.


## god_mode/scripts/utils/script_timestamp.py <a id='god_mode_scripts_utils_script_timestamp_py'></a>

### **get_utc_timestamp(format_str)**

- **Type**: function
- **Line**: 10

Get the current UTC timestamp in the specified format

Args:
    format_str (str): The datetime format string
    
Returns:
    str: The formatted timestamp

### **get_iso_timestamp()**

- **Type**: function
- **Line**: 23

Get the current UTC timestamp in ISO 8601 format

Returns:
    str: The ISO 8601 formatted timestamp

### **get_filename_timestamp()**

- **Type**: function
- **Line**: 33

Get a timestamp formatted for use in filenames

Returns:
    str: A filename-safe timestamp

### **get_log_timestamp()**

- **Type**: function
- **Line**: 43

Get a timestamp specifically formatted for log entries

Returns:
    str: A timestamp formatted for logs

