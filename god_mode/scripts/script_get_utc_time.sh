#!/bin/bash

# Script to get current UTC (Greenwich) time in a format suitable for changelog entries
# Output format: YYYY-MM-DD HH:MM UTC

current_utc_time=$(date -u +"%Y-%m-%d %H:%M UTC")
echo "$current_utc_time"

# Usage examples:
# 1. Direct output: ./get_utc_time.sh
# 2. Store in variable: UTC_TIME=$(./get_utc_time.sh) 