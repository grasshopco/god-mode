#!/usr/bin/env python3

"""
Timestamp utility module for God Mode scripts
Provides consistent timestamp formatting across all logging and documentation scripts
"""

import datetime

def get_utc_timestamp(format_str="%Y-%m-%d %H:%M UTC"):
    """
    Get the current UTC timestamp in the specified format
    
    Args:
        format_str (str): The datetime format string
        
    Returns:
        str: The formatted timestamp
    """
    now_utc = datetime.datetime.now(datetime.timezone.utc)
    return now_utc.strftime(format_str)

def get_iso_timestamp():
    """
    Get the current UTC timestamp in ISO 8601 format
    
    Returns:
        str: The ISO 8601 formatted timestamp
    """
    now_utc = datetime.datetime.now(datetime.timezone.utc)
    return now_utc.isoformat()

def get_filename_timestamp():
    """
    Get a timestamp formatted for use in filenames
    
    Returns:
        str: A filename-safe timestamp
    """
    now_utc = datetime.datetime.now(datetime.timezone.utc)
    return now_utc.strftime("%Y%m%d_%H%M%S")

def get_log_timestamp():
    """
    Get a timestamp specifically formatted for log entries
    
    Returns:
        str: A timestamp formatted for logs
    """
    return get_utc_timestamp("%Y-%m-%d %H:%M:%S UTC")

if __name__ == "__main__":
    # If run directly, print the current timestamp
    print(f"Current UTC timestamp: {get_utc_timestamp()}")
    print(f"ISO format: {get_iso_timestamp()}")
    print(f"Filename format: {get_filename_timestamp()}")
    print(f"Log format: {get_log_timestamp()}") 