#!/usr/bin/env python3
"""
TAG Feedback and Reinforcement Learning Script

This script analyzes and enforces the usage of TAGs in AI responses, creating a self-reinforcing
feedback loop that adjusts TAG enforcement based on compliance levels.

Key functions:
1. Track TAG usage compliance over time
2. Generate compliance reports and trends
3. Validate messages for proper TAG usage
4. Adjust reminder strength based on compliance history

The system is designed to automatically adapt enforcement levels based on past behavior,
creating a learning system that strengthens or relaxes requirements as needed.

Usage:
    python script_tag_feedback.py --validate "message.txt"  # Validate a message
    python script_tag_feedback.py --report                 # Generate a compliance report
"""

import os
import re
import sys
import json
import random
import argparse
import datetime
from pathlib import Path

# Get the directory of this script
SCRIPT_DIR = Path(os.path.dirname(os.path.abspath(__file__)))

# Define the project root relative to this script
PROJECT_ROOT = Path(SCRIPT_DIR).parent.parent

# Define the God Mode directory
GOD_MODE_DIR = Path(SCRIPT_DIR).parent

# Define memory directories
MEMORY_DIR = GOD_MODE_DIR / "memory"
MEMORY_TAG_METRICS_FILE = MEMORY_DIR / "memory_tag_metrics.md"

# Define cache directory
CACHE_DIR = GOD_MODE_DIR / ".cache"
TAG_CONFIG_FILE = CACHE_DIR / "tag_config.json"

# Define cursor configuration file
CURSOR_RULES_FILE = PROJECT_ROOT / ".cursorrules"

# Global debug flag
DEBUG_MODE = False

def debug_log(message):
    """Log debug messages when debug mode is enabled"""
    if DEBUG_MODE:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        print(f"[DEBUG] [{timestamp}] {message}")

def ensure_directory_exists(directory):
    """Create directory if it doesn't exist."""
    if not os.path.exists(directory):
        try:
            os.makedirs(directory)
            return True
        except Exception as e:
            print(f"Error creating directory {directory}: {e}", file=sys.stderr)
            return False
    return True

def ensure_metrics_file():
    """Ensure the metrics file exists with proper headers."""
    if not ensure_directory_exists(MEMORY_DIR):
        return False
        
    if not os.path.exists(MEMORY_TAG_METRICS_FILE):
        try:
            with open(MEMORY_TAG_METRICS_FILE, 'w') as f:
                f.write("# TAG Compliance Metrics\n\n")
                f.write("This file tracks the compliance of AI responses with the TAG system requirements.\n\n")
                f.write("| Date | Time | Valid | Reason | Required Tags Found | Optional Tags Found |\n")
                f.write("|------|------|-------|--------|---------------------|--------------------|\n")
            return True
        except Exception as e:
            print(f"Error creating metrics file: {e}", file=sys.stderr)
            return False
    return True

def load_tag_requirements():
    """Load TAG requirements from .cursorrules file."""
    if not os.path.exists(CURSOR_RULES_FILE):
        # Default tags if file not found
        return {
            "required": ["LOG_SUMMARY", "LOG_DETAIL", "MEMORY_UPDATE"],
            "optional": ["FEATURE_LOG", "DOC_UPDATE", "MEMORY_ARCHITECTURE", "MEMORY_CONVENTIONS"],
            "multi_tag_support": True
        }
    
    try:
        # Read .cursorrules and extract TAG requirements
        with open(CURSOR_RULES_FILE, 'r') as f:
            content = f.read()
        
        # Find TAG sections in the rules
        tag_section = re.search(r'TAG.*?support.*?](.*?)(?:\n\n|\n#|\Z)', content, re.DOTALL)
        if not tag_section:
            # Default if no specific TAG section found
            return {
                "required": ["LOG_SUMMARY", "LOG_DETAIL", "MEMORY_UPDATE"],
                "optional": ["FEATURE_LOG", "DOC_UPDATE", "MEMORY_ARCHITECTURE", "MEMORY_CONVENTIONS"],
                "multi_tag_support": True
            }
        
        # Extract tag requirements
        required_tags = re.findall(r'\[\s*([A-Z_]+)\s*\]\s*-\s*Required', tag_section.group(1), re.DOTALL)
        optional_tags = re.findall(r'\[\s*([A-Z_]+(?::[A-Za-z]*)?)\s*\]\s*-\s*(?:Optional|Recommended)', tag_section.group(1), re.DOTALL)
        
        # Check for multi-tag support
        multi_tag_support = '[MULTI_TAG' in content.upper()
        
        return {
            "required": required_tags if required_tags else ["LOG_SUMMARY", "LOG_DETAIL", "MEMORY_UPDATE"],
            "optional": optional_tags if optional_tags else ["FEATURE_LOG", "DOC_UPDATE"],
            "multi_tag_support": multi_tag_support
        }
    except Exception as e:
        debug_log(f"Error parsing TAG requirements: {e}")
        # Default tags if parsing fails
        return {
            "required": ["LOG_SUMMARY", "LOG_DETAIL", "MEMORY_UPDATE"],
            "optional": ["FEATURE_LOG", "DOC_UPDATE", "MEMORY_ARCHITECTURE", "MEMORY_CONVENTIONS"],
            "multi_tag_support": True
        }

def validate_message(message):
    """
    Validate a message for proper TAG usage
    
    Args:
        message (str): The message to validate
        
    Returns:
        tuple: (is_valid, reason)
    """
    if not message:
        return False, "Empty message"
    
    # Load tag requirements
    tag_requirements = load_tag_requirements()
    required_tags = tag_requirements["required"]
    
    # Check for required tags
    required_found = []
    for tag in required_tags:
        if f"[{tag}]" in message.upper():
            required_found.append(tag)
    
    # Check for optional tags
    optional_found = []
    for tag in tag_requirements["optional"]:
        if ":" in tag:
            # Handle tags with parameters (e.g., FEATURE_LOG:Name)
            base_tag = tag.split(":")[0]
            pattern = fr'\[\s*{base_tag}\s*:\s*([^]]+)\]'
            if re.search(pattern, message, re.IGNORECASE):
                optional_found.append(f"{base_tag}:PARAM")
        else:
            if f"[{tag}]" in message.upper():
                optional_found.append(tag)
    
    # Check for multi-tag usage if supported
    multi_tag_found = False
    if tag_requirements["multi_tag_support"]:
        multi_tag_pattern = r'\[\s*MULTI_TAG\s*:\s*([^]]+)\]'
        if re.search(multi_tag_pattern, message, re.IGNORECASE):
            multi_tag_found = True
            optional_found.append("MULTI_TAG")
    
    # Determine validity and reason
    is_valid = len(required_found) >= 2  # Require at least 2 of the required tags
    
    if is_valid:
        if len(required_found) == len(required_tags):
            reason = "All required tags found"
        else:
            reason = f"Some required tags found ({', '.join(required_found)})"
    else:
        if not required_found:
            reason = "No required tags found"
        else:
            reason = f"Insufficient required tags found (only {', '.join(required_found)})"
    
    # Return detailed validation result
    return is_valid, reason, {
        "required_found": required_found,
        "optional_found": optional_found,
        "multi_tag_found": multi_tag_found,
        "required_count": len(required_found),
        "optional_count": len(optional_found)
    }

def log_tag_validation(is_valid, reason, details=None):
    """
    Log TAG validation results to the metrics file
    
    Args:
        is_valid (bool): Whether the message was valid
        reason (str): The reason for validation result
        details (dict, optional): Additional validation details
    """
    # Ensure the metrics file exists
    if not ensure_metrics_file():
        debug_log("Failed to ensure metrics file exists")
        return False
    
    # Format current timestamp
    now = datetime.datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S")
    
    # Format required and optional tags if details provided
    req_tags = "N/A"
    opt_tags = "N/A"
    if details:
        req_tags = ", ".join(details["required_found"]) if details["required_found"] else "None"
        opt_tags = ", ".join(details["optional_found"]) if details["optional_found"] else "None"
    
    # Format validation mark
    valid_mark = "✅" if is_valid else "❌"
    
    # Create log entry
    log_entry = f"| {date_str} | {time_str} | {valid_mark} | {reason} | {req_tags} | {opt_tags} |\n"
    
    # Append to metrics file
    try:
        with open(MEMORY_TAG_METRICS_FILE, 'a') as f:
            f.write(log_entry)
        return True
    except Exception as e:
        debug_log(f"Error logging tag validation: {e}")
        return False

def analyze_compliance():
    """
    Analyze TAG compliance metrics to determine compliance rate and trend
    
    Returns:
        tuple: (compliance_rate, trend)
    """
    if not os.path.exists(MEMORY_TAG_METRICS_FILE):
        return 0.5, "flat"  # Default values if file doesn't exist
    
    try:
        with open(MEMORY_TAG_METRICS_FILE, 'r') as f:
            lines = f.readlines()
        
        # Extract table rows (skip header rows)
        data_rows = [line for line in lines if line.startswith('|') and ' | ' in line]
        data_rows = data_rows[2:]  # Skip the first two header rows
        
        if not data_rows:
            return 0.5, "flat"  # No data yet
        
        # Count compliant entries
        recent_entries = data_rows[-20:]  # Look at the 20 most recent entries
        compliant_count = sum(1 for entry in recent_entries if "✅" in entry)
        compliance_rate = compliant_count / len(recent_entries)
        
        # Determine trend by comparing recent to older entries
        if len(data_rows) <= 20:
            trend = "flat"  # Not enough data for trend
        else:
            older_entries = data_rows[-40:-20]  # Previous 20 entries
            older_compliant = sum(1 for entry in older_entries if "✅" in entry)
            older_rate = older_compliant / len(older_entries)
            
            if compliance_rate > older_rate + 0.1:
                trend = "improving"
            elif compliance_rate < older_rate - 0.1:
                trend = "declining"
            else:
                trend = "flat"
        
        return compliance_rate, trend
    
    except Exception as e:
        debug_log(f"Error analyzing compliance: {e}")
        return 0.5, "flat"  # Default on error

def update_tag_config(compliance_rate, trend):
    """
    Update TAG configuration based on compliance analysis
    
    Args:
        compliance_rate (float): The current compliance rate
        trend (str): The trend direction ("improving", "declining", "flat")
        
    Returns:
        dict: Updated configuration
    """
    # Ensure cache directory exists
    ensure_directory_exists(CACHE_DIR)
    
    # Load current config if it exists
    config = {
        "reminder_level": "normal",
        "check_frequency": 0.7,
        "last_updated": "",
        "compliance_rate": 0.5,
        "trend": "flat"
    }
    
    if os.path.exists(TAG_CONFIG_FILE):
        try:
            with open(TAG_CONFIG_FILE, 'r') as f:
                loaded_config = json.load(f)
                config.update(loaded_config)
        except Exception as e:
            debug_log(f"Error loading TAG config: {e}")
    
    # Update configuration based on compliance and trend
    if compliance_rate < 0.3:
        config["reminder_level"] = "severe"
        config["check_frequency"] = 1.0  # Always show reminders
    elif compliance_rate < 0.7:
        config["reminder_level"] = "normal"
        config["check_frequency"] = 0.7  # Show reminders 70% of the time
    else:
        config["reminder_level"] = "mild"
        config["check_frequency"] = 0.3  # Show reminders 30% of the time
    
    # Adjust based on trend
    if trend == "improving" and config["check_frequency"] > 0.2:
        config["check_frequency"] -= 0.1  # Reduce frequency if improving
    elif trend == "declining" and config["check_frequency"] < 0.9:
        config["check_frequency"] += 0.1  # Increase frequency if declining
    
    # Update metadata
    config["last_updated"] = datetime.datetime.now().isoformat()
    config["compliance_rate"] = compliance_rate
    config["trend"] = trend
    
    # Save updated config
    try:
        with open(TAG_CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=2)
    except Exception as e:
        debug_log(f"Error saving TAG config: {e}")
    
    return config

def generate_report():
    """
    Generate a report on TAG compliance and configuration
    
    Returns:
        str: The report
    """
    # Analyze compliance
    compliance_rate, trend = analyze_compliance()
    config = update_tag_config(compliance_rate, trend)
    
    # Gather data for report
    if os.path.exists(MEMORY_TAG_METRICS_FILE):
        try:
            with open(MEMORY_TAG_METRICS_FILE, 'r') as f:
                lines = f.readlines()
            
            # Extract table rows (skip header rows)
            data_rows = [line for line in lines if line.startswith('|') and ' | ' in line]
            data_rows = data_rows[2:]  # Skip the first two header rows
            
            total_entries = len(data_rows)
            compliant_entries = sum(1 for entry in data_rows if "✅" in entry)
            
            if total_entries > 0:
                overall_rate = compliant_entries / total_entries
            else:
                overall_rate = 0
                
            # Most common issues (reasons for failure)
            issues = []
            for row in data_rows:
                if "❌" in row:
                    cols = [col.strip() for col in row.split('|')]
                    if len(cols) >= 5:  # Ensure we have enough columns
                        issue = cols[4]  # The reason column
                        issues.append(issue)
            
            issue_counts = {}
            for issue in issues:
                issue_counts[issue] = issue_counts.get(issue, 0) + 1
            
            top_issues = sorted(issue_counts.items(), key=lambda x: x[1], reverse=True)[:3]
            
        except Exception as e:
            debug_log(f"Error reading metrics for report: {e}")
            total_entries = 0
            compliant_entries = 0
            overall_rate = 0
            top_issues = []
    else:
        total_entries = 0
        compliant_entries = 0
        overall_rate = 0
        top_issues = []
    
    # Format the report
    report = [
        "# TAG Compliance Report\n",
        f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n",
        "\n## Compliance Metrics\n",
        f"- Recent compliance rate: {compliance_rate:.1%}",
        f"- Trend: {trend}",
        f"- Overall compliance: {overall_rate:.1%} ({compliant_entries}/{total_entries} entries)\n",
        "\n## Configuration\n",
        f"- Reminder level: {config['reminder_level']}",
        f"- Check frequency: {config['check_frequency']:.1%}",
        f"- Last updated: {config['last_updated']}\n"
    ]
    
    if top_issues:
        report.append("\n## Common Issues\n")
        for issue, count in top_issues:
            report.append(f"- {issue}: {count} occurrences")
    
    return "\n".join(report)

def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(description="TAG Feedback and Validation Script")
    parser.add_argument("--validate", metavar="FILE", help="Validate TAGs in the specified file")
    parser.add_argument("--report", action="store_true", help="Generate a TAG compliance report")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    args = parser.parse_args()
    
    global DEBUG_MODE
    DEBUG_MODE = args.debug
    
    if args.debug:
        print("Debug mode enabled")
    
    if args.validate:
        try:
            with open(args.validate, 'r') as f:
                message = f.read()
            
            is_valid, reason, details = validate_message(message)
            log_tag_validation(is_valid, reason, details)
            
            print(f"Validation result: {'Valid' if is_valid else 'Invalid'}")
            print(f"Reason: {reason}")
            print(f"Required tags found: {', '.join(details['required_found']) if details['required_found'] else 'None'}")
            print(f"Optional tags found: {', '.join(details['optional_found']) if details['optional_found'] else 'None'}")
            
        except Exception as e:
            print(f"Error validating file: {e}")
            return 1
    
    elif args.report:
        report = generate_report()
        print(report)
    
    else:
        parser.print_help()
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 