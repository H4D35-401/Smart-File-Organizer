# Smart File Organizer

A cross-platform tool to automatically organize your files into folders based on keywords and file types.

## Features
- **Smart Sorting**: Moves files to `College`, `JPN`, `Arch`, etc. based on filenames.
- **Script Organization**: Auto-moves `.py`, `.sh`, `.js` to `Scripts/`.
- **Background Service**: Runs silently in the background.
- **Cross-Platform**: Works on Linux, Windows, and macOS.

## Installation

### 🐧 Linux
```bash
# 1. Clone the repo
git clone https://github.com/yourusername/Smart-File-Organizer.git
cd Smart-File-Organizer/installers/linux

# 2. Run the installer
bash install.sh
```

### 🪟 Windows
1.  Navigate to `installers\windows`.
2.  Double-click **`install.bat`**.
3.  This will install dependencies and add the script to your **Startup** folder.

### 🍎 macOS
1.  Open Terminal.
2.  Navigate to the project folder:
    ```bash
    cd path/to/Smart-File-Organizer/installers/mac
    ```
3.  Run the installer:
    ```bash
    chmod +x install.sh
    ./install.sh
    ```

## Usage
Just save files to your **Documents/Inbox** folder!

| Context | Keyword Examples | Destination |
| :--- | :--- | :--- |
| **College (Sem 2)** | `dbms`, `oop`, `network`, `csa`, `english` | `College/Semester 2/...` |
| **Japanese** | `jpn`, `kanji`, `n5` | `JPN` |
| **Linux** | `arch`, `config` | `Arch` |
| **Scripts** | `.py`, `.sh`, `.js` | `Scripts` |
| **Misc** | *Anything else* | `Others` |

## Configuration (GUI)
You can customize folders and keywords using the **Settings App**.

- **Windows**: Double-click `installers/windows/configure.bat`.
- **macOS**: Run `installers/mac/configure.sh`.
- **Linux**: Run `python3 src/gui.py`.

Use the app to:
1.  Change your **Inbox** folder.
2.  Add new **Categories** (e.g., "Work").
3.  Add/Remove **Keywords**.

