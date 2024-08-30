#!/bin/bash

# Path to your Python script
SCRIPT_PATH="/home/oleksandr/Projects/rotation_machanism/app.py"

# Check if the script is running
if ! pgrep -f "$(basename "$SCRIPT_PATH")" > /dev/null; then
    # If not running, start the script
    /usr/bin/python3 "$SCRIPT_PATH" &
fi
