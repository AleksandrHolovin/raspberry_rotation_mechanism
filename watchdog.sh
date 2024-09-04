#!/bin/bash

# Path to your Python script
SCRIPT_PATH="/home/veselka/Documents/raspberry_rotation_mechanism/app.py"

# Check if the script is running
if ! pgrep -f "$(basename "$SCRIPT_PATH")" > /dev/null; then
    # If not running, start the script
    /usr/bin/python3 "$SCRIPT_PATH" &
fi
