#!/usr/bin/env python3
"""
Session Continuity Script

This script helps maintain continuity between chat sessions by generating a
summary of recent conversations, important context, and the current state of the project.

Usage:
    python script_session_continuity.py [--days DAYS] [--output OUTPUT_FILE]
"""

import os
import sys
import argparse
import re
import datetime
from pathlib import Path
import json

# Get the directory of this script
SCRIPT_DIR = Path(os.path.dirname(os.path.abspath(__file__)))

# Define paths
PROJECT_ROOT = SCRIPT_DIR.parent.parent
GOD_MODE_DIR = SCRIPT_DIR.parent
MEMORY_DIR = GOD_MODE_DIR / "memory"
DISCUSSION_DIR = GOD_MODE_DIR / "discussion"
ROADMAP_DIR = GOD_MODE_DIR / "roadmap"
CONTINUITY_DIR = GOD_MODE_DIR / "memory" / "continuity"
CACHE_DIR = GOD_MODE_DIR / ".cache"

# Import enhance_prompt if available
try:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, script_dir)
    from script_enhance_prompt import enhance_prompt
    ENHANCE_AVAILABLE = True
except ImportError as e:
    ENHANCE_AVAILABLE = False
    print(f"Warning: Enhance prompt module not available: {str(e)}")
    
    def enhance_prompt(prompt):
        return f"[Enhanced Context would be added here]\n\n{prompt}"

def ensure_directory_exists(directory):
    """Ensure a directory exists, creating it if necessary."""
    os.makedirs(directory, exist_ok=True)

def get_timestamp():
    """Get current timestamp in YYYY-MM-DD HH:MM UTC format."""
    now_utc = datetime.datetime.now(datetime.timezone.utc)
    return now_utc.strftime("%Y-%m-%d %H:%M UTC")

def get_filename_timestamp():
    """Get a filename-friendly timestamp (YYYYMMDD_HHMMSS)."""
    now_utc = datetime.datetime.now(datetime.timezone.utc)
    return now_utc.strftime("%Y%m%d_%H%M%S")

def is_recent_file(file_path, days=7):
    """Check if a file was modified within the last N days."""
    if not file_path.exists():
        return False
    
    # Get the modification time
    mtime = datetime.datetime.fromtimestamp(file_path.stat().st_mtime)
    
    # Get the current time
    now = datetime.datetime.now()
    
    # Calculate the age in days
    age = (now - mtime).days
    
    return age <= days

def find_recent_discussions(days=7):
    """Find discussion files that were modified in the last N days."""
    recent_files = []
    
    # Check files in the discussion directory
    for file in DISCUSSION_DIR.glob("discussion_*.txt"):
        if is_recent_file(file, days):
            recent_files.append(file)
    
    # Check files in the discussion subdirectories
    for subdir in DISCUSSION_DIR.glob("discussion_*/"):
        for file in subdir.glob("*.txt"):
            if is_recent_file(file, days):
                recent_files.append(file)
    
    return recent_files

def find_recent_roadmaps(days=7):
    """Find roadmap files that were modified in the last N days."""
    recent_files = []
    
    for file in ROADMAP_DIR.glob("roadmap_*.md"):
        if is_recent_file(file, days):
            recent_files.append(file)
    
    return recent_files

def extract_recent_log_entries(days=7):
    """Extract recent log entries from the memory logs."""
    # Get the logs file
    logs_file = MEMORY_DIR / "memory_logs_all.md"
    if not logs_file.exists():
        return []
    
    # Read the logs file
    with open(logs_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract log entries with timestamps
    timestamp_pattern = r'- \[(\d{4}-\d{2}-\d{2} \d{2}:\d{2} UTC)\] (.*)'
    matches = re.finditer(timestamp_pattern, content, re.MULTILINE)
    
    recent_entries = []
    for match in matches:
        timestamp_str = match.group(1)
        entry = match.group(2)
        
        # Parse the timestamp
        timestamp = datetime.datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M UTC")
        
        # Calculate the age in days
        age = (datetime.datetime.now() - timestamp).days
        
        if age <= days:
            recent_entries.append((timestamp_str, entry))
    
    return recent_entries

def get_current_issues():
    """Extract current issues from the issue tracker or memory."""
    issues = []
    
    # Check the issues directory
    issues_dir = GOD_MODE_DIR / "issues"
    if issues_dir.exists():
        for file in issues_dir.glob("issue_*.md"):
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract the issue title
            title_match = re.search(r'# Issue: (.+)', content)
            if title_match:
                title = title_match.group(1)
                
                # Extract the status
                status_match = re.search(r'Status: (.+)', content)
                status = status_match.group(1) if status_match else "Unknown"
                
                if status.lower() not in ["closed", "resolved", "completed", "fixed"]:
                    issues.append((title, status))
    
    return issues

def extract_conversation_summary(file_path):
    """Extract a summary of a conversation from a discussion file."""
    if not file_path.exists():
        return None
    
    # Read the file
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract the user messages (messages starting with "**User:**")
    user_messages = []
    user_pattern = r'(?:^|\n)(?:\*\*)?User(?:\*\*)?: (.+?)(?=(?:\n(?:\*\*)?(?:AI|Assistant|Claude)(?:\*\*)?:|\Z))'
    for match in re.finditer(user_pattern, content, re.DOTALL):
        message = match.group(1).strip()
        # Truncate long messages
        if len(message) > 200:
            message = message[:197] + "..."
        user_messages.append(message)
    
    # Extract AI responses (messages starting with "**AI:**" or "**Claude:**" or "**Assistant:**")
    ai_responses = []
    ai_pattern = r'(?:^|\n)(?:\*\*)?(?:AI|Assistant|Claude)(?:\*\*)?: (.+?)(?=(?:\n(?:\*\*)?User(?:\*\*)?:|\Z))'
    for match in re.finditer(ai_pattern, content, re.DOTALL):
        response = match.group(1).strip()
        # Truncate long responses
        if len(response) > 200:
            response = response[:197] + "..."
        ai_responses.append(response)
    
    # Create a summary of the conversation
    summary = {
        "file": file_path.name,
        "user_messages": user_messages[-3:],  # Most recent 3 user messages
        "ai_responses": ai_responses[-3:],    # Most recent 3 AI responses
    }
    
    return summary

def extract_roadmap_summary(file_path):
    """Extract a summary of a roadmap file."""
    if not file_path.exists():
        return None
    
    # Read the file
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract the title
    title_match = re.search(r'# God Mode System: (.+)', content)
    title = title_match.group(1) if title_match else file_path.stem
    
    # Extract current issues
    issues_section = re.search(r'## Current Bottlenecks and Issues\s+(.+?)(?=^##)', content, re.MULTILINE | re.DOTALL)
    issues = []
    if issues_section:
        issues_text = issues_section.group(1)
        issue_pattern = r'### Issue \d+: (.+?)[\n-]'
        for match in re.finditer(issue_pattern, issues_text):
            issues.append(match.group(1).strip())
    
    # Extract upcoming tasks
    tasks_section = re.search(r'## Upcoming Implementation Plan\s+(.+?)(?=^##)', content, re.MULTILINE | re.DOTALL)
    tasks = []
    if tasks_section:
        tasks_text = tasks_section.group(1)
        task_pattern = r'- \[ \] \*\*(Task [^:]+):\*\* (.+?)\n'
        for match in re.finditer(task_pattern, tasks_text):
            task_id = match.group(1)
            task_desc = match.group(2)
            tasks.append(f"{task_id}: {task_desc}")
    
    # Create a summary
    summary = {
        "file": file_path.name,
        "title": title,
        "issues": issues[:5],  # Top 5 issues
        "tasks": tasks[:5],    # Top 5 tasks
    }
    
    return summary

def generate_continuity_summary(days=7):
    """Generate a summary of recent activity for continuity between sessions."""
    print(f"Generating continuity summary for the last {days} days...")
    
    # Ensure the continuity directory exists
    ensure_directory_exists(CONTINUITY_DIR)
    
    # Find recent discussions
    recent_discussions = find_recent_discussions(days)
    print(f"Found {len(recent_discussions)} recent discussions")
    
    # Find recent roadmaps
    recent_roadmaps = find_recent_roadmaps(days)
    print(f"Found {len(recent_roadmaps)} recent roadmaps")
    
    # Extract recent log entries
    recent_logs = extract_recent_log_entries(days)
    print(f"Found {len(recent_logs)} recent log entries")
    
    # Get current issues
    current_issues = get_current_issues()
    print(f"Found {len(current_issues)} current issues")
    
    # Generate conversation summaries
    conversation_summaries = []
    for file in recent_discussions:
        summary = extract_conversation_summary(file)
        if summary:
            conversation_summaries.append(summary)
    
    # Generate roadmap summaries
    roadmap_summaries = []
    for file in recent_roadmaps:
        summary = extract_roadmap_summary(file)
        if summary:
            roadmap_summaries.append(summary)
    
    # Put it all together
    continuity_data = {
        "generated_at": get_timestamp(),
        "time_span_days": days,
        "recent_logs": recent_logs,
        "current_issues": current_issues,
        "conversation_summaries": conversation_summaries,
        "roadmap_summaries": roadmap_summaries,
    }
    
    # Generate the markdown summary
    summary_md = format_continuity_summary(continuity_data)
    
    # Save the summary to a file
    timestamp = get_filename_timestamp()
    summary_file = CONTINUITY_DIR / f"continuity_summary_{timestamp}.md"
    
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write(summary_md)
    
    # Also save the latest version to a fixed location
    latest_file = CONTINUITY_DIR / "latest_continuity_summary.md"
    
    with open(latest_file, 'w', encoding='utf-8') as f:
        f.write(summary_md)
    
    print(f"Continuity summary saved to {summary_file}")
    print(f"Latest summary also saved to {latest_file}")
    
    return summary_file

def format_continuity_summary(data):
    """Format the continuity data as a markdown document."""
    md = [
        "# God Mode Continuity Summary",
        "",
        f"**Generated At**: {data['generated_at']}",
        f"**Time Span**: Last {data['time_span_days']} days",
        "",
        "This document provides a summary of recent activity and context to maintain continuity between chat sessions.",
        "",
        "## Recent Activity Summary",
        "",
    ]
    
    # Add recent logs
    if data['recent_logs']:
        md.append("### Recent Changes")
        md.append("")
        for timestamp, entry in data['recent_logs']:
            md.append(f"- **[{timestamp}]** {entry}")
        md.append("")
    
    # Add current issues
    if data['current_issues']:
        md.append("### Current Issues")
        md.append("")
        for title, status in data['current_issues']:
            md.append(f"- **{title}** (Status: {status})")
        md.append("")
    
    # Add roadmap summaries
    if data['roadmap_summaries']:
        md.append("## Recent Roadmap Updates")
        md.append("")
        
        for summary in data['roadmap_summaries']:
            md.append(f"### {summary['title']}")
            md.append(f"*From {summary['file']}*")
            md.append("")
            
            if summary['issues']:
                md.append("**Current Issues:**")
                for issue in summary['issues']:
                    md.append(f"- {issue}")
                md.append("")
            
            if summary['tasks']:
                md.append("**Upcoming Tasks:**")
                for task in summary['tasks']:
                    md.append(f"- {task}")
                md.append("")
    
    # Add conversation summaries
    if data['conversation_summaries']:
        md.append("## Recent Conversations")
        md.append("")
        
        for summary in data['conversation_summaries']:
            md.append(f"### Conversation: {summary['file']}")
            md.append("")
            
            if summary['user_messages']:
                md.append("**Recent User Messages:**")
                for msg in summary['user_messages']:
                    md.append(f"- \"{msg}\"")
                md.append("")
            
            if summary['ai_responses']:
                md.append("**Recent AI Responses:**")
                for resp in summary['ai_responses']:
                    md.append(f"- \"{resp}\"")
                md.append("")
    
    md.append("## Resuming Instructions")
    md.append("")
    md.append("When resuming work with the God Mode system:")
    md.append("")
    md.append("1. Review this summary to understand recent activity and context")
    md.append("2. Check the latest roadmap for current priorities")
    md.append("3. Address any outstanding issues")
    md.append("4. Continue with the next steps in the implementation plan")
    md.append("")
    md.append("To enhance this prompt with all available context, run:")
    md.append("```bash")
    md.append("python god_mode/scripts/script_enhance_prompt.py \"Your prompt here\"")
    md.append("```")
    md.append("")
    md.append("---")
    md.append("")
    md.append("*This document was automatically generated by the God Mode system to maintain continuity between sessions.*")
    
    return "\n".join(md)

def generate_session_restart_prompt(days=7, output_file=None):
    """Generate a prompt to restart a session with continuity."""
    # Generate the continuity summary
    summary_file = generate_continuity_summary(days)
    
    # Read the summary
    with open(summary_file, 'r', encoding='utf-8') as f:
        summary_content = f.read()
    
    # Create the restart prompt
    restart_prompt = f"""
I'm starting a new chat session and want to resume where we left off.

Please review the following summary of recent activity and context:

{summary_content}

Based on this information, let's continue our work. What's the current status and what should we focus on next?
"""
    
    # Enhance the prompt if available
    if ENHANCE_AVAILABLE:
        print("Enhancing the restart prompt with additional context...")
        enhanced_prompt = enhance_prompt(restart_prompt)
    else:
        enhanced_prompt = restart_prompt
    
    # Save the prompt to a file if requested
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(enhanced_prompt)
        print(f"Restart prompt saved to {output_file}")
    
    return enhanced_prompt

def main():
    parser = argparse.ArgumentParser(description="Generate a continuity summary for session transitions")
    parser.add_argument("--days", type=int, default=7, help="Number of days to include in the summary")
    parser.add_argument("--output", help="Output file for the restart prompt")
    parser.add_argument("--summary-only", action="store_true", help="Generate only the summary, not the restart prompt")
    
    args = parser.parse_args()
    
    if args.summary_only:
        summary_file = generate_continuity_summary(args.days)
        print(f"Summary generated and saved to {summary_file}")
    else:
        restart_prompt = generate_session_restart_prompt(args.days, args.output)
        if not args.output:
            print("\n--- RESTART PROMPT ---\n")
            print(restart_prompt)

if __name__ == "__main__":
    main() 