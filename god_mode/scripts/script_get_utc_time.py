#!/usr/bin/env python3

"""
Script to get current UTC (Greenwich) time in a format suitable for changelog entries
Output format: YYYY-MM-DD HH:MM UTC
"""

import datetime

def get_utc_time():
    """Return current UTC time in the format YYYY-MM-DD HH:MM UTC"""
    now_utc = datetime.datetime.now(datetime.timezone.utc)
    formatted_time = now_utc.strftime("%Y-%m-%d %H:%M UTC")
    return formatted_time

if __name__ == "__main__":
    print(get_utc_time())

# Usage examples:
# 1. Direct output: python get_utc_time.py
# 2. Import in another script: 
#    from get_utc_time import get_utc_time 