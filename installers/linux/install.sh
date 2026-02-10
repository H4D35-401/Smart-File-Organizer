#!/bin/bash
set -e

echo "--- Installing Smart File Organizer ---"

# 1. Create Directories (Real User Paths)
echo "[*] Creating folder structure in ~/Documents..."
mkdir -p ~/Documents/Inbox
mkdir -p ~/Documents/Organized/{JPN,Personal,Arch,Scripts,Others}
mkdir -p "$HOME/Documents/Organized/College/Semester 2/"{DBMS,OOP,Networks,CSA,English}

# 2. Setup Python Environment (Venv)
echo "[*] Setting up Python virtual environment..."
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$PROJECT_DIR/.venv"

if [ ! -d "$VENV_DIR" ]; then
    python3 -m venv "$VENV_DIR"
fi

# Activate venv for installation
source "$VENV_DIR/bin/activate"

echo "[*] Installing dependencies..."
pip install watchdog

# 3. Setup Service
echo "[*] Setting up systemd service..."
mkdir -p ~/.config/systemd/user

# Create service file dynamically to use absolute path to venv python
cat <<EOF > ~/.config/systemd/user/file-organizer.service
[Unit]
Description=File Organization Automation
After=network.target

[Service]
ExecStart=$VENV_DIR/bin/python $PROJECT_DIR/organizer.py
Restart=always
WorkingDirectory=$PROJECT_DIR

[Install]
WantedBy=default.target
EOF

echo "[*] Reloading systemd..."
systemctl --user daemon-reload
systemctl --user enable --now file-organizer.service
systemctl --user restart file-organizer.service

echo "--- Done! ---"
echo "Service status:"
systemctl --user status file-organizer.service --no-pager
