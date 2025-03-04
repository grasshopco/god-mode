#!/bin/bash

# god - A short command to access God Mode functions
# This script is a convenience wrapper around god_mode_remote.sh

# Get the directory of this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Check if the command is specified
if [ "$1" == "continue" ] || [ "$1" == "c" ]; then
    # Run the continue conversation script directly
    python3 "$SCRIPT_DIR/god_mode/scripts/script_continue_conversation.py" "${@:2}"
    exit $?
elif [ "$1" == "route" ] || [ "$1" == "r" ]; then
    # Route clipboard content
    "$SCRIPT_DIR/god_mode/scripts/route" --clipboard
    exit $?
elif [ "$1" == "enhance" ] || [ "$1" == "e" ]; then
    # Enhance prompt
    if [ -n "$2" ]; then
        python3 "$SCRIPT_DIR/god_mode/scripts/script_enhance_prompt.py" --prompt "$2" --copy
    else
        python3 "$SCRIPT_DIR/god_mode/scripts/script_enhance_prompt.py" --clipboard --copy
    fi
    exit $?
elif [ "$1" == "tag" ] || [ "$1" == "t" ]; then
    # TAG compliance
    if [ "$2" == "report" ]; then
        python3 "$SCRIPT_DIR/god_mode/scripts/script_tag_feedback.py" --report
    elif [ "$2" == "validate" ] && [ -n "$3" ]; then
        python3 "$SCRIPT_DIR/god_mode/scripts/script_tag_feedback.py" --validate "$3"
    else
        echo "Usage: god tag [report|validate <file>]"
    fi
    exit $?
elif [ "$1" == "help" ] || [ "$1" == "h" ] || [ "$1" == "--help" ]; then
    echo "God Mode Quick Command"
    echo "Usage: god [command] [options]"
    echo
    echo "Available commands:"
    echo "  continue, c [--custom \"question\"]  - Continue conversation with AI"
    echo "  route, r                          - Route clipboard content to memory files"
    echo "  enhance, e [\"prompt\"]             - Enhance a prompt with context"
    echo "  tag, t [report|validate <file>]   - Work with TAG compliance"
    echo "  help, h                           - Show this help"
    echo
    echo "If no command is specified, the God Mode menu will open."
    exit 0
fi

# If no specific command, open the main God Mode menu
"$SCRIPT_DIR/god_mode_remote.sh" "$@" 