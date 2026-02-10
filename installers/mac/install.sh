#!/bin/bash
set -e

echo "--- Installing Smart File Organizer (macOS) ---"

# 1. Install Watchdog
echo "[*] Installing dependencies..."
pip3 install watchdog

# 2. Setup Directories
SRC_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../src" && pwd)"
TARGET_DIR="$HOME/Documents/SmartFileOrganizer"

echo "[*] Copying files to $TARGET_DIR..."
mkdir -p "$TARGET_DIR"
cp -R "$SRC_DIR/"* "$TARGET_DIR/"

# 3. Create Launch Agent
PLIST_path="$HOME/Library/LaunchAgents/com.user.fileorganizer.plist"
echo "[*] Creating Launch Agent at $PLIST_path..."

cat <<EOF > "$PLIST_path"
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.user.fileorganizer</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>$TARGET_DIR/organizer.py</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardErrorPath</key>
    <string>$TARGET_DIR/organizer.err</string>
    <key>StandardOutPath</key>
    <string>$TARGET_DIR/organizer.out</string>
</dict>
</plist>
EOF

# 4. Load Agent
echo "[*] Loading Launch Agent..."
launchctl unload "$PLIST_path" 2>/dev/null || true
launchctl load "$PLIST_path"

echo "--- Done! Service started. ---"
