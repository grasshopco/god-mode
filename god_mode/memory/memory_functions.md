# Project Functions
*Generated: Current UTC timestamp: 2025-03-04 21:34 UTC
ISO format: 2025-03-04T21:34:05.179254+00:00
Filename format: 20250304_213405
Log format: 2025-03-04 21:34:05 UTC*
This document maps all functions and methods in the project.

## Table of Contents
- [god_mode/scripts/examples/demo_router_usage.py](#god_mode_scripts_examples_demo_router_usage_py)
- [god_mode/scripts/script_analyze_patterns.py](#god_mode_scripts_script_analyze_patterns_py)
- [god_mode/scripts/script_auto_commit.py](#god_mode_scripts_script_auto_commit_py)
- [god_mode/scripts/script_check_feature_logs.py](#god_mode_scripts_script_check_feature_logs_py)
- [god_mode/scripts/script_continue_conversation.py](#god_mode_scripts_script_continue_conversation_py)
- [god_mode/scripts/script_create_supabase_integration.py](#god_mode_scripts_script_create_supabase_integration_py)
- [god_mode/scripts/script_cursor_watch.py](#god_mode_scripts_script_cursor_watch_py)
- [god_mode/scripts/script_debug_router.py](#god_mode_scripts_script_debug_router_py)
- [god_mode/scripts/script_enhance_message_content.py](#god_mode_scripts_script_enhance_message_content_py)
- [god_mode/scripts/script_enhance_prompt.py](#god_mode_scripts_script_enhance_prompt_py)
- [god_mode/scripts/script_generate_roadmap.py](#god_mode_scripts_script_generate_roadmap_py)
- [god_mode/scripts/script_get_utc_time.py](#god_mode_scripts_script_get_utc_time_py)
- [god_mode/scripts/script_initialize_tracking.py](#god_mode_scripts_script_initialize_tracking_py)
- [god_mode/scripts/script_mcp_server.py](#god_mode_scripts_script_mcp_server_py)
- [god_mode/scripts/script_message_router.py](#god_mode_scripts_script_message_router_py)
- [god_mode/scripts/script_notification_settings.py](#god_mode_scripts_script_notification_settings_py)
- [god_mode/scripts/script_session_continuity.py](#god_mode_scripts_script_session_continuity_py)
- [god_mode/scripts/script_tag_feedback.py](#god_mode_scripts_script_tag_feedback_py)
- [god_mode/scripts/script_test_god_mode.py](#god_mode_scripts_script_test_god_mode_py)
- [god_mode/scripts/script_test_sqlite.py](#god_mode_scripts_script_test_sqlite_py)
- [god_mode/scripts/script_track_routing.py](#god_mode_scripts_script_track_routing_py)
- [god_mode/scripts/script_update_cursor_rules.py](#god_mode_scripts_script_update_cursor_rules_py)
- [god_mode/scripts/script_update_functions_and_types.py](#god_mode_scripts_script_update_functions_and_types_py)
- [god_mode/scripts/script_update_project_structure.py](#god_mode_scripts_script_update_project_structure_py)
- [god_mode/scripts/script_verify_system.py](#god_mode_scripts_script_verify_system_py)
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


## god_mode/scripts/script_auto_commit.py <a id='god_mode_scripts_script_auto_commit_py'></a>

### **log_info(message)**

- **Type**: function
- **Line**: 25

*No documentation available.*

### **log_error(message)**

- **Type**: function
- **Line**: 26

*No documentation available.*

### **log_debug(message)**

- **Type**: function
- **Line**: 27

*No documentation available.*

### **log_warning(message)**

- **Type**: function
- **Line**: 28

*No documentation available.*

### **git_is_available()**

- **Type**: function
- **Line**: 30

Check if Git is available.

Returns:
    bool: True if Git is available, False otherwise

### **is_git_repository(path)**

- **Type**: function
- **Line**: 43

Check if the specified path is a Git repository.

Args:
    path (str): Path to check
    
Returns:
    bool: True if it's a Git repository, False otherwise

### **get_uncommitted_changes(repo_path)**

- **Type**: function
- **Line**: 59

Get a list of uncommitted changes in the repository.

Args:
    repo_path (str): Path to the repository
    
Returns:
    list: List of files with uncommitted changes

### **auto_commit(repo_path, commit_message)**

- **Type**: function
- **Line**: 89

Automatically commit changes to the repository.

Args:
    repo_path (str): Path to the repository
    commit_message (str, optional): Commit message. Defaults to a generated message.
    
Returns:
    bool: True if the commit was successful, False otherwise

### **register_end_of_conversation_hook(repo_path)**

- **Type**: function
- **Line**: 164

Register a hook that will be called at the end of a conversation to auto-commit changes.

Args:
    repo_path (str): Path to the repository

### **main()**

- **Type**: function
- **Line**: 177

Main function to run the auto-commit script.

Returns:
    int: 0 for success, 1 for failure


## god_mode/scripts/script_check_feature_logs.py <a id='god_mode_scripts_script_check_feature_logs_py'></a>

### **ensure_directory_exists(directory)**

- **Type**: function
- **Line**: 38

Ensure a directory exists, creating it if necessary.

### **get_timestamp()**

- **Type**: function
- **Line**: 42

Get current timestamp in YYYY-MM-DD HH:MM UTC format.

### **get_detailed_timestamp()**

- **Type**: function
- **Line**: 47

Get detailed timestamp in YYYY-MM-DD HH:MM:SS format.

### **extract_feature_name(filename)**

- **Type**: function
- **Line**: 52

Extract the feature name from a feature log filename.

### **get_template_structure()**

- **Type**: function
- **Line**: 59

Read the template file and extract its structure.

Returns:
    str: The template structure

### **extract_existing_content(log_content)**

- **Type**: function
- **Line**: 83

Extract existing content from a feature log while preserving structure.

Args:
    log_content (str): The content of the log file
    
Returns:
    dict: Extracted content sections

### **find_latest_roadmap_file()**

- **Type**: function
- **Line**: 112

Find the most recently created or updated roadmap file.

Returns:
    Path: Path to the most recent roadmap file, or None if none found

### **update_roadmap_task(task_name)**

- **Type**: function
- **Line**: 133

Update the roadmap file to mark a task as completed.

Args:
    task_name (str): The name of the task to mark as completed
    
Returns:
    bool: True if successful, False otherwise

### **check_feature_log(file_path, template, fix)**

- **Type**: function
- **Line**: 197

Check if a feature log file follows the template and fix it if needed.

Args:
    file_path (Path): Path to the feature log file
    template (str): The template structure
    fix (bool): Whether to fix the file if it doesn't match the template
    
Returns:
    tuple: (needs_fix, was_fixed, error_message)

### **process_all_feature_logs(fix, check_only, update_roadmap)**

- **Type**: function
- **Line**: 336

Process all feature log files to ensure they follow the template.

Args:
    fix (bool): Whether to fix files that don't match the template
    check_only (bool): Only check files, don't print detailed results
    update_roadmap (bool): Whether to update the roadmap with results
    
Returns:
    tuple: (total_files, files_needing_fix, files_fixed)

### **main()**

- **Type**: function
- **Line**: 398

Main entry point for the script.


## god_mode/scripts/script_continue_conversation.py <a id='god_mode_scripts_script_continue_conversation_py'></a>

### **enhance_prompt(prompt)**

- **Type**: function
- **Line**: 49

*No documentation available.*

### **debug_log(message)**

- **Type**: function
- **Line**: 52

Print debug message if verbose mode is enabled.

### **ensure_directory_exists(directory)**

- **Type**: function
- **Line**: 57

Ensure a directory exists, creating it if necessary.

### **load_cache()**

- **Type**: function
- **Line**: 61

Load the conversation cache file or create it if it doesn't exist.

### **save_cache(cache)**

- **Type**: function
- **Line**: 83

Save the conversation cache to file.

### **update_preset_questions(response_content)**

- **Type**: function
- **Line**: 93

Extract potential preset questions from an AI response.
Looks for lines that end with a question mark or start with bullet points.

### **find_most_recent_response()**

- **Type**: function
- **Line**: 124

Try to find the most recent AI response in the clipboard or a temporary file.

### **process_response_for_questions()**

- **Type**: function
- **Line**: 155

Process the most recent response to extract preset questions.

### **display_preset_menu()**

- **Type**: function
- **Line**: 172

Display the menu of preset questions.

### **save_question(question)**

- **Type**: function
- **Line**: 210

Save a question to the questions file.

### **get_questions()**

- **Type**: function
- **Line**: 228

Get a list of predefined questions from the questions file.

### **extract_questions_from_file(file_path)**

- **Type**: function
- **Line**: 242

Extract questions from a file containing an AI response.

### **scan_for_questions()**

- **Type**: function
- **Line**: 264

Scan recent AI responses for questions and save them.

### **continue_conversation(custom_question)**

- **Type**: function
- **Line**: 275

Continue the conversation with a preset or custom question.

### **main()**

- **Type**: function
- **Line**: 310

Main function for the conversation continuation script.


## god_mode/scripts/script_create_supabase_integration.py <a id='god_mode_scripts_script_create_supabase_integration_py'></a>

### **debug_log(message)**

- **Type**: function
- **Line**: 56

Log debug messages when debug mode is enabled

### **ensure_directory_exists(directory)**

- **Type**: function
- **Line**: 62

Ensure a directory exists, creating it if necessary.

### **get_latest_package_version(package_name)**

- **Type**: function
- **Line**: 66

Get the latest version of a PyPI package by querying PyPI API.

Args:
    package_name (str): The name of the package to check
    
Returns:
    str: The latest version or None if it couldn't be determined

### **is_package_installed(package_name)**

- **Type**: function
- **Line**: 88

Check if a Python package is installed.

### **install_package(package_name, version)**

- **Type**: function
- **Line**: 96

Install a Python package with optional version.

Args:
    package_name (str): The name of the package to install
    version (str, optional): Specific version to install
    
Returns:
    bool: True if installation succeeded, False otherwise

### **load_db_config()**

- **Type**: function
- **Line**: 121

Load database configuration from the config file.

Returns:
    dict: The database configuration

### **load_backends_config()**

- **Type**: function
- **Line**: 165

Load all configured backends from the backends file.

Returns:
    dict: The configured backends

### **save_backends_config(config)**

- **Type**: function
- **Line**: 194

Save backends configuration to the config file.

Args:
    config (dict): The backends configuration

### **save_db_config(config)**

- **Type**: function
- **Line**: 209

Save database configuration to the config file.

Args:
    config (dict): The database configuration

### **is_supabase_available()**

- **Type**: function
- **Line**: 224

Check if the Supabase Python client is available.

### **install_supabase()**

- **Type**: function
- **Line**: 228

Install the Supabase Python client.

### **create_supabase_client(backend_name)**

- **Type**: function
- **Line**: 239

Create a Supabase client using the configured URL and key.

Args:
    backend_name (str, optional): The name of the backend to use
    
Returns:
    Client: The Supabase client, or None if not configured

### **setup_db_integration()**

- **Type**: function
- **Line**: 287

Interactive setup for application database backend.

### **check_supabase_requirements()**

- **Type**: function
- **Line**: 344

Check if Supabase requirements are met and install if needed

### **setup_provider_selection()**

- **Type**: function
- **Line**: 373

Present provider options and return the selected provider

### **setup_new_backend(provider)**

- **Type**: function
- **Line**: 395

Set up a new backend with the specified provider

### **setup_sqlite_backend()**

- **Type**: function
- **Line**: 517

Set up a local SQLite database backend for development

### **sync_with_remote(backend_name)**

- **Type**: function
- **Line**: 664

Sync local memory files with the remote database.

Args:
    backend_name (str, optional): Name of the backend to sync with. If None, uses active backend.

### **backup_memory_files(backend_name)**

- **Type**: function
- **Line**: 803

Backup all memory files to the remote database.

Args:
    backend_name (str, optional): Name of the backend to backup to. If None, uses active backend.

### **restore_from_backup(backend_name)**

- **Type**: function
- **Line**: 849

Restore memory files from a backup.

Args:
    backend_name (str, optional): Name of the backend to restore from. If None, provides local and remote options.

### **restore_from_database(backend_name)**

- **Type**: function
- **Line**: 955

Restore memory files from a database.

Args:
    backend_name (str): Name of the backend to restore from

### **main()**

- **Type**: function
- **Line**: 1051

Main function to parse arguments and execute commands


## god_mode/scripts/script_cursor_watch.py <a id='god_mode_scripts_script_cursor_watch_py'></a>

### **ensure_directory_exists(directory)**

- **Type**: function
- **Line**: 57

Ensure a directory exists, creating it if necessary.

### **get_workspace_storage_paths()**

- **Type**: function
- **Line**: 61

Get potential workspace storage paths based on the OS.

### **log_message(message)**

- **Type**: function
- **Line**: 86

Log a message with timestamp.

### **log_error(message)**

- **Type**: function
- **Line**: 92

Log an error message with timestamp.

### **log_debug(message)**

- **Type**: function
- **Line**: 98

Log a debug message with timestamp (only if debug mode is enabled).

### **log_warning(message)**

- **Type**: function
- **Line**: 105

Log a warning message with timestamp.

### **log_info(message)**

- **Type**: function
- **Line**: 111

Log an info message with timestamp.

### **extract_tags_from_text(text)**

- **Type**: function
- **Line**: 117

Extract tags from text using regex.

Args:
    text (str): The text to extract tags from
    
Returns:
    list: List of tags found in the text

### **find_all_workspace_dbs()**

- **Type**: function
- **Line**: 132

Find all the state.vscdb files in Cursor's workspaceStorage.

Returns:
    list: List of Paths to all workspace database files

### **query_cursor_database(db_path)**

- **Type**: function
- **Line**: 162

Query a Cursor SQLite database for conversation messages.

Args:
    db_path (Path): Path to the database file
    
Returns:
    list: List of message dictionaries, or empty list if none found or on error

### **extract_conversations_from_chat_data(chat_data)**

- **Type**: function
- **Line**: 252

Extract conversations from the chat data.

Args:
    chat_data (dict): Chat data from querying the database
    
Returns:
    list: List of conversation objects with user and assistant messages

### **get_message_content(message)**

- **Type**: function
- **Line**: 292

Get content from a message object with error handling.

Args:
    message (dict): The message object
    
Returns:
    str: The content of the message

### **get_last_assistant_message(conversation)**

- **Type**: function
- **Line**: 307

Get the last assistant message from a conversation.

Args:
    conversation (dict): The conversation object
    
Returns:
    dict: The last assistant message

### **check_for_messages_without_tags(db_path, conversation, last_check_time)**

- **Type**: function
- **Line**: 331

Check for assistant messages that don't have tags.

Args:
    db_path (Path): Path to the database
    conversation (dict): The conversation object
    last_check_time (float): Timestamp of the last check
    
Returns:
    list: List of messages that need tags

### **get_ai_rules_from_file()**

- **Type**: function
- **Line**: 377

Get AI rules from the cursorrules file.

Returns:
    str: The AI rules

### **enhance_user_prompt(user_prompt)**

- **Type**: function
- **Line**: 402

Enhance the user prompt with relevant context from the project.
This function uses the enhance_prompt.py script to add context.

Args:
    user_prompt (str): The user's prompt
    
Returns:
    str: The enhanced prompt

### **should_add_tags_to_message(message)**

- **Type**: function
- **Line**: 418

Determines if a message should have tags based on its content.

Args:
    message (str): The message to check
    
Returns:
    bool: True if the message should have tags, False otherwise

### **check_message_has_tags(message_content, message_id)**

- **Type**: function
- **Line**: 459

Check if a message has the required tags, log if tags are missing.

Args:
    message_content (str): The content of the message to check
    message_id (str): The ID of the message for reference
    
Returns:
    bool: True if the message has tags or doesn't need them, False if tags are missing

### **watch_cursor_databases()**

- **Type**: function
- **Line**: 487

Main function to watch Cursor SQLite databases for changes and ensure proper tagging.

### **main()**

- **Type**: function
- **Line**: 598

Main function to run the script.


## god_mode/scripts/script_debug_router.py <a id='god_mode_scripts_script_debug_router_py'></a>

### **log_message(message)**

- **Type**: function
- **Line**: 29

Log a message with timestamp to both console and file

### **read_file_safely(filepath)**

- **Type**: function
- **Line**: 41

Read a file with detailed error handling

### **debug_pattern_matching(content)**

- **Type**: function
- **Line**: 55

Debug regex pattern matching on content

### **simulate_routing(content)**

- **Type**: function
- **Line**: 94

Simulate the routing process without actually writing to files

### **main()**

- **Type**: function
- **Line**: 116

Main entry point for the debug router script.


## god_mode/scripts/script_enhance_message_content.py <a id='god_mode_scripts_script_enhance_message_content_py'></a>

### **debug_log(message)**

- **Type**: function
- **Line**: 49

*No documentation available.*

### **route_message(message)**

- **Type**: function
- **Line**: 52

*No documentation available.*

### **ensure_directory_exists(directory)**

- **Type**: function
- **Line**: 56

Ensure a directory exists, creating it if necessary.

### **get_timestamp()**

- **Type**: function
- **Line**: 60

Get current timestamp in YYYY-MM-DD HH:MM UTC format.

### **is_empty_content(content)**

- **Type**: function
- **Line**: 65

Check if content is effectively empty (just a timestamp or metadata).

Args:
    content (str): The content to check
    
Returns:
    bool: True if the content is empty or just contains metadata

### **find_latest_roadmap_file()**

- **Type**: function
- **Line**: 98

Find the most recently created or updated roadmap file.

Returns:
    Path: Path to the most recent roadmap file, or None if none found

### **get_file_context(filepath)**

- **Type**: function
- **Line**: 119

Extract context about a file to help generate more relevant content.

Args:
    filepath (Path): Path to the file
    
Returns:
    dict: Context information about the file

### **find_task_in_roadmap(task_name, roadmap_file)**

- **Type**: function
- **Line**: 146

Find a task in the roadmap file by its name.

Args:
    task_name (str): The task name to search for
    roadmap_file (Path): Path to the roadmap file
    
Returns:
    tuple: (line_number, line, is_checked) or (None, None, None) if not found

### **update_roadmap_file(task_name, notes)**

- **Type**: function
- **Line**: 181

Update the roadmap file to mark a task as completed.

Args:
    task_name (str): The name of the task to mark as completed
    notes (str, optional): Additional notes about the completion
    
Returns:
    bool: True if successful, False otherwise

### **generate_contextual_content(tag_type, filepath, context)**

- **Type**: function
- **Line**: 238

Generate content that's contextually relevant based on file analysis.

Args:
    tag_type (str): The type of tag (LOG_SUMMARY, MEMORY_ARCHITECTURE, etc.)
    filepath (Path): The file path for context
    context (dict, optional): Additional context information
    
Returns:
    str: Generated contextually relevant content

### **generate_log_summary(file_purpose, filepath, context)**

- **Type**: function
- **Line**: 302

Generate a meaningful log summary based on context.

### **generate_log_detail(file_purpose, filepath, context)**

- **Type**: function
- **Line**: 316

Generate detailed log content based on context.

### **generate_memory_update(file_purpose, filepath, context)**

- **Type**: function
- **Line**: 344

Generate a memory update entry based on context.

### **generate_memory_architecture(file_purpose, filepath, context)**

- **Type**: function
- **Line**: 385

Generate architecture-specific content based on context.

### **generate_memory_requirements(file_purpose, filepath, context)**

- **Type**: function
- **Line**: 432

Generate requirements-specific content based on context.

### **generate_memory_roadmap(file_purpose, filepath, context)**

- **Type**: function
- **Line**: 472

Generate roadmap-specific content based on context.

### **generate_memory_conventions(file_purpose, filepath, context)**

- **Type**: function
- **Line**: 520

Generate conventions-specific content based on context.

### **generate_memory_dependencies(file_purpose, filepath, context)**

- **Type**: function
- **Line**: 574

Generate dependencies-specific content based on context.

### **generate_memory_glossary(file_purpose, filepath, context)**

- **Type**: function
- **Line**: 620

Generate glossary-specific content based on context.

### **generate_memory_testing(file_purpose, filepath, context)**

- **Type**: function
- **Line**: 669

Generate testing-specific content based on context.

### **generate_memory_security(file_purpose, filepath, context)**

- **Type**: function
- **Line**: 723

Generate security-specific content based on context.

### **generate_memory_performance(file_purpose, filepath, context)**

- **Type**: function
- **Line**: 773

Generate performance-specific content based on context.

### **generate_memory_accessibility(file_purpose, filepath, context)**

- **Type**: function
- **Line**: 827

Generate accessibility-specific content based on context.

### **generate_memory_learnings(file_purpose, filepath, context)**

- **Type**: function
- **Line**: 881

Generate learnings-specific content based on context.

### **generate_doc_update(file_purpose, filepath, context)**

- **Type**: function
- **Line**: 927

Generate documentation update content based on context.

### **generate_feature_log_content(feature_name, filepath, context)**

- **Type**: function
- **Line**: 969

Generate content specifically for feature logs.

### **generate_feature_log_update(feature_name)**

- **Type**: function
- **Line**: 983

Generate a complete feature log update.

### **generate_roadmap_content(filepath, context)**

- **Type**: function
- **Line**: 1053

Generate content specifically for roadmap files.

### **generate_relevant_content(tag_type, filepath, existing_content)**

- **Type**: function
- **Line**: 1066

Generate relevant content for a specific tag type and file.

Args:
    tag_type (str): The type of tag (LOG_SUMMARY, MEMORY_ARCHITECTURE, etc.)
    filepath (Path): The file path for context
    existing_content (str): Any existing content for context
    
Returns:
    str: Generated relevant content

### **enhance_message(message)**

- **Type**: function
- **Line**: 1085

Enhance a message with relevant content.

Args:
    message (str): The message to enhance
    
Returns:
    str: The enhanced message

### **audit_memory_files()**

- **Type**: function
- **Line**: 1178

Scan memory files for empty log entries and enhance them.

Returns:
    int: Number of files updated

### **main()**

- **Type**: function
- **Line**: 1278

Main entry point for the script.


## god_mode/scripts/script_enhance_prompt.py <a id='god_mode_scripts_script_enhance_prompt_py'></a>

### **log_message(message, level)**

- **Type**: function
- **Line**: 29

Log a message with timestamp and level.

### **log_debug(message)**

- **Type**: function
- **Line**: 35

Log a debug message.

### **log_error(message)**

- **Type**: function
- **Line**: 40

Log an error message.

### **log_info(message)**

- **Type**: function
- **Line**: 44

Log an info message.

### **log_warning(message)**

- **Type**: function
- **Line**: 48

Log a warning message.

### **get_project_structure()**

- **Type**: function
- **Line**: 52

Get a summary of the project structure.

Returns:
    str: A brief summary of the project structure

### **get_memory_highlights()**

- **Type**: function
- **Line**: 84

Get highlights from memory files.

Returns:
    str: A summary of key information from memory files

### **get_recent_logs()**

- **Type**: function
- **Line**: 132

Get recent logs for context.

Returns:
    str: Recent log entries

### **enhance_prompt(user_prompt)**

- **Type**: function
- **Line**: 167

Enhance a user prompt with relevant context.

Args:
    user_prompt (str): The original user prompt
    
Returns:
    str: The enhanced prompt with added context

### **main()**

- **Type**: function
- **Line**: 216

Main function to parse arguments and enhance prompts.


## god_mode/scripts/script_generate_roadmap.py <a id='god_mode_scripts_script_generate_roadmap_py'></a>

### **ensure_directory_exists(directory)**

- **Type**: function
- **Line**: 29

Ensure a directory exists, creating it if necessary.

### **get_timestamp()**

- **Type**: function
- **Line**: 33

Get current timestamp in YYYY-MM-DD HH:MM UTC format.

### **get_filename_timestamp()**

- **Type**: function
- **Line**: 38

Get a filename-friendly timestamp (YYYYMMDD_HHMMSS).

### **generate_roadmap_file(title)**

- **Type**: function
- **Line**: 43

Generate a new roadmap file from the template.

Args:
    title: Optional title for the roadmap file

Returns:
    Path: Path to the generated file

### **main()**

- **Type**: function
- **Line**: 86

*No documentation available.*


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


## god_mode/scripts/script_mcp_server.py <a id='god_mode_scripts_script_mcp_server_py'></a>

### **handle_mcp_request(request)**

- **Type**: function
- **Line**: 24

Handle an MCP request and return a response.

### **main()**

- **Type**: function
- **Line**: 105

Main function to run the MCP server.


## god_mode/scripts/script_message_router.py <a id='god_mode_scripts_script_message_router_py'></a>

### **debug_log(message)**

- **Type**: function
- **Line**: 31

Log debug messages when debug mode is enabled

### **add_routing_event(tag, file_path, content, line_number)**

- **Type**: function
- **Line**: 47

*No documentation available.*

### **validate_message(message)**

- **Type**: function
- **Line**: 61

Basic validation - just checks if any tags exist

Args:
    message (str): The message to validate
    
Returns:
    tuple: (is_valid, reason)

### **log_tag_validation(is_valid, reason)**

- **Type**: function
- **Line**: 100

*No documentation available.*

### **check_dependencies()**

- **Type**: function
- **Line**: 106

*No documentation available.*

### **send_notification(title, message)**

- **Type**: function
- **Line**: 220

Send a desktop notification with the given title and message.
Also plays a sound effect to alert the user.

Args:
    title (str): The notification title
    message (str): The notification message

### **play_sound()**

- **Type**: function
- **Line**: 292

Play a sound notification.

### **toggle_notification_settings(sound_enabled, notifications_enabled)**

- **Type**: function
- **Line**: 340

Toggle notification settings.

Args:
    sound_enabled (bool, optional): Whether to enable sound effects
    notifications_enabled (bool, optional): Whether to enable desktop notifications
    
Returns:
    dict: The current notification settings

### **get_notification_settings()**

- **Type**: function
- **Line**: 383

Get the current notification settings.

Returns:
    dict: The current notification settings

### **get_timestamp()**

- **Type**: function
- **Line**: 407

Get current timestamp in YYYY-MM-DD HH:MM UTC format.

### **ensure_directory_exists(directory)**

- **Type**: function
- **Line**: 427

Ensure a directory exists, creating it if necessary.

Args:
    directory (Path): Path to the directory
    
Returns:
    bool: True if the directory exists or was created, False otherwise

### **ensure_file_exists(filepath)**

- **Type**: function
- **Line**: 444

Ensure a file exists, creating it with appropriate headers if necessary.

Args:
    filepath (Path): Path to the file
    
Returns:
    bool: True if the file exists or was created, False otherwise

### **append_to_file(file_path, content)**

- **Type**: function
- **Line**: 505

Append content to a file with a timestamp

Args:
    file_path (Path or str): Path to the file to append to
    content (str): Content to append to the file
    
Returns:
    bool: True if successful, False otherwise

### **process_feature_log(feature_name, content)**

- **Type**: function
- **Line**: 562

Process a feature log entry

### **process_doc_update(doc_type, content)**

- **Type**: function
- **Line**: 598

Process a documentation update entry

### **process_single_tag(tag, content)**

- **Type**: function
- **Line**: 619

Process a single tag from a multi-tag block

### **route_message(message)**

- **Type**: function
- **Line**: 656

Process a message and extract/route content based on markers.

### **read_from_file(filepath)**

- **Type**: function
- **Line**: 780

Read content from a file

### **read_from_clipboard()**

- **Type**: function
- **Line**: 799

Read content from the clipboard

### **watch_clipboard(interval)**

- **Type**: function
- **Line**: 807

Watch clipboard for changes and process routing when markers are detected.

### **should_add_tags_to_message(message)**

- **Type**: function
- **Line**: 906

Determines if a message should have tags based on its content.

Args:
    message (str): The message to check
    
Returns:
    bool: True if the message should have tags, False otherwise

### **count_lines(file_path)**

- **Type**: function
- **Line**: 938

Count the number of lines in a file

Args:
    file_path (Path or str): Path to the file
    
Returns:
    int: Number of lines in the file

### **extract_tag_from_path(file_path)**

- **Type**: function
- **Line**: 955

Extract a tag name from a file path

Args:
    file_path (Path or str): Path to the file
    
Returns:
    str: Tag name derived from the file path

### **main()**

- **Type**: function
- **Line**: 989

Main entry point for the message router script.


## god_mode/scripts/script_notification_settings.py <a id='god_mode_scripts_script_notification_settings_py'></a>

### **ensure_directory_exists(directory)**

- **Type**: function
- **Line**: 47

Ensure a directory exists, creating it if necessary.

### **get_notification_settings()**

- **Type**: function
- **Line**: 51

Get the current notification settings.

Returns:
    dict: The current notification settings

### **toggle_notification_settings(sound_enabled, notifications_enabled)**

- **Type**: function
- **Line**: 73

Toggle notification settings.

Args:
    sound_enabled (bool, optional): Whether to enable sound effects
    notifications_enabled (bool, optional): Whether to enable desktop notifications
    
Returns:
    dict: The current notification settings

### **send_notification(title, message)**

- **Type**: function
- **Line**: 105

Simple fallback to print notifications if import fails.

### **list_settings()**

- **Type**: function
- **Line**: 118

List current notification settings.

### **test_notifications()**

- **Type**: function
- **Line**: 138

Test notifications with current settings.

### **main()**

- **Type**: function
- **Line**: 155

Main function to parse arguments and manage notification settings.


## god_mode/scripts/script_session_continuity.py <a id='god_mode_scripts_script_session_continuity_py'></a>

### **enhance_prompt(prompt)**

- **Type**: function
- **Line**: 42

*No documentation available.*

### **ensure_directory_exists(directory)**

- **Type**: function
- **Line**: 45

Ensure a directory exists, creating it if necessary.

### **get_timestamp()**

- **Type**: function
- **Line**: 49

Get current timestamp in YYYY-MM-DD HH:MM UTC format.

### **get_filename_timestamp()**

- **Type**: function
- **Line**: 54

Get a filename-friendly timestamp (YYYYMMDD_HHMMSS).

### **is_recent_file(file_path, days)**

- **Type**: function
- **Line**: 59

Check if a file was modified within the last N days.

### **find_recent_discussions(days)**

- **Type**: function
- **Line**: 75

Find discussion files that were modified in the last N days.

### **find_recent_roadmaps(days)**

- **Type**: function
- **Line**: 92

Find roadmap files that were modified in the last N days.

### **extract_recent_log_entries(days)**

- **Type**: function
- **Line**: 102

Extract recent log entries from the memory logs.

### **get_current_issues()**

- **Type**: function
- **Line**: 133

Extract current issues from the issue tracker or memory.

### **extract_conversation_summary(file_path)**

- **Type**: function
- **Line**: 158

Extract a summary of a conversation from a discussion file.

### **extract_roadmap_summary(file_path)**

- **Type**: function
- **Line**: 196

Extract a summary of a roadmap file.

### **generate_continuity_summary(days)**

- **Type**: function
- **Line**: 239

Generate a summary of recent activity for continuity between sessions.

### **format_continuity_summary(data)**

- **Type**: function
- **Line**: 307

Format the continuity data as a markdown document.

### **generate_session_restart_prompt(days, output_file)**

- **Type**: function
- **Line**: 400

Generate a prompt to restart a session with continuity.

### **main()**

- **Type**: function
- **Line**: 435

*No documentation available.*


## god_mode/scripts/script_tag_feedback.py <a id='god_mode_scripts_script_tag_feedback_py'></a>

### **debug_log(message)**

- **Type**: function
- **Line**: 54

Log debug messages when debug mode is enabled

### **ensure_directory_exists(directory)**

- **Type**: function
- **Line**: 60

Create directory if it doesn't exist.

### **ensure_metrics_file()**

- **Type**: function
- **Line**: 71

Ensure the metrics file exists with proper headers.

### **load_tag_requirements()**

- **Type**: function
- **Line**: 89

Load TAG requirements from .cursorrules file.

### **validate_message(message)**

- **Type**: function
- **Line**: 135

Validate a message for proper TAG usage

Args:
    message (str): The message to validate
    
Returns:
    tuple: (is_valid, reason)

### **log_tag_validation(is_valid, reason, details)**

- **Type**: function
- **Line**: 202

Log TAG validation results to the metrics file

Args:
    is_valid (bool): Whether the message was valid
    reason (str): The reason for validation result
    details (dict, optional): Additional validation details

### **analyze_compliance()**

- **Type**: function
- **Line**: 243

Analyze TAG compliance metrics to determine compliance rate and trend

Returns:
    tuple: (compliance_rate, trend)

### **update_tag_config(compliance_rate, trend)**

- **Type**: function
- **Line**: 290

Update TAG configuration based on compliance analysis

Args:
    compliance_rate (float): The current compliance rate
    trend (str): The trend direction ("improving", "declining", "flat")
    
Returns:
    dict: Updated configuration

### **generate_report()**

- **Type**: function
- **Line**: 352

Generate a report on TAG compliance and configuration

Returns:
    str: The report

### **main()**

- **Type**: function
- **Line**: 429

Main entry point for the script.


## god_mode/scripts/script_test_god_mode.py <a id='god_mode_scripts_script_test_god_mode_py'></a>

### **print_header(text)**

- **Type**: function
- **Line**: 47

Print a header with nice formatting

### **print_status(test_name, status, message)**

- **Type**: function
- **Line**: 53

Print the status of a test

### **run_script(script_name, args)**

- **Type**: function
- **Line**: 62

Run a script and return the exit code and output

### **check_file_updated(file_path, last_modified)**

- **Type**: function
- **Line**: 74

Check if a file exists and has been modified since last_modified

### **test_project_structure()**

- **Type**: function
- **Line**: 87

Test the project structure script

### **test_enhance_message_content()**

- **Type**: function
- **Line**: 116

Test the message content enhancer script

### **test_feature_logs()**

- **Type**: function
- **Line**: 135

Test the feature logs script

### **test_session_continuity()**

- **Type**: function
- **Line**: 154

Test the session continuity script

### **test_roadmap_generator()**

- **Type**: function
- **Line**: 172

Test the roadmap generator script

### **test_message_routing()**

- **Type**: function
- **Line**: 207

Test the message routing system by simulating clipboard content

### **run_all_tests()**

- **Type**: function
- **Line**: 260

Run all the tests


## god_mode/scripts/script_test_sqlite.py <a id='god_mode_scripts_script_test_sqlite_py'></a>

### **get_workspace_storage_paths()**

- **Type**: function
- **Line**: 13

Get potential workspace storage paths based on the OS.

### **find_all_workspace_dbs()**

- **Type**: function
- **Line**: 38

Find all the state.vscdb files in Cursor's workspaceStorage.

Returns:
    list: List of Paths to all workspace database files

### **query_database(db_path)**

- **Type**: function
- **Line**: 68

Query a SQLite database to extract chat data.

Args:
    db_path (Path): Path to the SQLite database
    
Returns:
    dict: Dictionary of chat data with keys for different types of chat data

### **extract_conversations_from_chat_data(chat_data)**

- **Type**: function
- **Line**: 123

Extract conversations from the chat data.

Args:
    chat_data (dict): Chat data from querying the database
    
Returns:
    list: List of conversation objects with user and assistant messages

### **main()**

- **Type**: function
- **Line**: 165

*No documentation available.*


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
- **Line**: 95

Check if a path should be ignored.

Args:
    path (Path): The path to check
    
Returns:
    bool: True if the path should be ignored, False otherwise

### **extract_file_description(file_path, default_description)**

- **Type**: function
- **Line**: 119

Extract a description from a file's docstring, header comment, or other sources.

Args:
    file_path (Path): The path to the file
    default_description (str): A default description to use if none can be extracted
    
Returns:
    str: The extracted description or default

### **scan_directory(directory, prefix, descriptions, indent_level, processed_paths)**

- **Type**: function
- **Line**: 194

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
- **Line**: 317

Generate the content for the project structure file.

Args:
    descriptions (dict): A dictionary mapping file/directory paths to descriptions
    
Returns:
    str: The content for the project structure file

### **update_project_structure()**

- **Type**: function
- **Line**: 360

Update the project structure file.


## god_mode/scripts/script_verify_system.py <a id='god_mode_scripts_script_verify_system_py'></a>

### **log(message, level)**

- **Type**: function
- **Line**: 26

*No documentation available.*

### **print_status(component, status, details)**

- **Type**: function
- **Line**: 36

Print the status of a component with color coding.

Args:
    component (str): Name of the component
    status (str): Status of the component (PASS, FAIL, WARNING)
    details (str): Additional details about the status

### **check_process_running(process_name)**

- **Type**: function
- **Line**: 54

Check if a process is running.

Args:
    process_name (str): Name of the process to check
    
Returns:
    tuple: (is_running, pid or None)

### **check_file_exists(file_path, component_name)**

- **Type**: function
- **Line**: 72

Check if a file exists and report status.

Args:
    file_path (str): Path to the file
    component_name (str): Name of the component for reporting
    
Returns:
    bool: True if the file exists, False otherwise

### **verify_cursor_watch()**

- **Type**: function
- **Line**: 90

Verify cursor_watch script status and functionality.

Returns:
    bool: True if cursor_watch is running correctly, False otherwise

### **verify_message_router()**

- **Type**: function
- **Line**: 121

Verify message_router script status and functionality.

Returns:
    bool: True if message_router is configured correctly, False otherwise

### **verify_cursor_rules()**

- **Type**: function
- **Line**: 151

Verify cursor rules are properly set up.

Returns:
    bool: True if cursor rules are set up correctly, False otherwise

### **verify_memory_files()**

- **Type**: function
- **Line**: 198

Verify memory files exist and are accessible.

Returns:
    bool: True if memory files are set up correctly, False otherwise

### **verify_auto_commit()**

- **Type**: function
- **Line**: 228

Verify the auto-commit functionality.

Returns:
    bool: True if auto-commit is set up correctly, False otherwise

### **run_verification()**

- **Type**: function
- **Line**: 276

Run all verification checks and print a summary.

Returns:
    int: 0 if all checks pass, 1 if any check fails


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

