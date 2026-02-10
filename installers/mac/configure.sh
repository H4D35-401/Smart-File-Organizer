#!/bin/bash
TARGET_DIR="$HOME/Documents/SmartFileOrganizer"

if [ -f "$TARGET_DIR/gui.py" ]; then
    echo "Starting Configuration..."
    python3 "$TARGET_DIR/gui.py"
else
    echo "Error: Smart File Organizer not found in Documents."
    echo "Please run install.sh first."
fi
