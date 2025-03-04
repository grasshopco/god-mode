# Message Router Script

## Overview

The Message Router Script is a core component of the enhanced God Mode system. It automatically routes structured AI outputs to the appropriate documentation and log files based on special markers in the text.

## Features

- Automatically detects special markers in text and routes content to the appropriate files
- Adds timestamps to each entry for consistent logging
- Handles multiple log types (summary logs, detailed logs, feature logs, etc.)
- Can read input from files, direct text, or clipboard
- Can watch the clipboard in real-time for continuous processing

## Special Markers

The script recognizes the following markers:

| Marker | Target File | Description |
|--------|-------------|-------------|
| `[LOG_SUMMARY]content` | memory_logs_all.md | Adds a brief summary entry to the all logs file |
| `[LOG_DETAIL]content` | memory_logs_detailed.md | Adds a detailed explanation to the detailed logs file |
| `[MEMORY_UPDATE]content` | memory_cursor.md | Updates the CURSOR MEMORY file with new context |
| `[FEATURE_LOG: featureName]content` | memory_log_feature_*.md | Updates the log for a specific feature |
| `[DOC_UPDATE: docType]content` | documentation_*.md | Updates a specific documentation file |
| `[LEARNING]content` | memory_learnings.md | Adds insights and learnings |
| `[PROMPT_LEARNING]content` | memory_prompt_learnings.md | Adds insights for improving prompts |
| `[DISCUSSION]content` | discussion_grasshop.md | Adds entries to the discussion file |

## Requirements

- Python 3.6+
- `pyperclip` library (for clipboard functionality)

## Installation

1. Ensure you have Python 3.6+ installed
2. Install the required packages:
   ```
   pip install pyperclip
   ```

## Usage

### Process a file:
```bash
python script_message_router.py --input path/to/message.txt
```

### Process text directly:
```bash
python script_message_router.py --message "[LOG_SUMMARY]This is a summary entry."
```

### Process clipboard content:
```bash
python script_message_router.py --clipboard
```

### Watch clipboard for changes:
```bash
python script_message_router.py --watch
```

## Example AI Output with Markers

```
I've updated the authentication system to use JWT tokens.

[LOG_SUMMARY]Updated authentication system to use JWT tokens in auth.js

[LOG_DETAIL]
## Authentication System Update

Made the following changes to the authentication system:
1. Replaced cookie-based auth with JWT tokens
2. Added token refresh mechanism
3. Improved error handling for auth failures

These changes improve security and allow for better cross-domain authentication.

[MEMORY_UPDATE]
The authentication system now uses JWT tokens instead of cookies. This is important context for any future auth-related tasks.

[FEATURE_LOG: Authentication]
Updated the authentication system to use JWT tokens. This includes token refresh and improved error handling.

[DOC_UPDATE: features]
## Authentication

The system uses JWT (JSON Web Tokens) for authentication with the following flow:
1. User logs in with credentials
2. Server validates and returns a JWT token
3. Client stores token and includes it in subsequent requests
4. Token is automatically refreshed when needed

[LEARNING]
Using JWT for authentication simplified the cross-domain authentication process but required additional security considerations for token storage.
```

## How It Works

1. The script parses the input text looking for special markers
2. For each marker found, it extracts the content and determines the target file
3. It adds appropriate timestamps and formatting based on the target file type
4. It appends the content to the target file, creating the file if it doesn't exist

## Tips for AI Use

1. When generating responses, include appropriate markers for content that should be logged or documented
2. Use multiple markers in a single response to update different documentation files
3. For feature logs, be sure to include the feature name in the marker
4. For documentation updates, specify the documentation type (data_model, features, design, etc.)

## Integration with God Mode Workflow

This script is ideally run after each AI interaction to automatically process and route the AI's output to the appropriate files. It can be:

1. Run manually after reviewing the AI's response
2. Set up to watch the clipboard in a separate terminal window
3. Integrated into other automated workflows 