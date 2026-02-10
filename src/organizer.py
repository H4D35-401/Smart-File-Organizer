import os
import sys
import time
import shutil
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Configuration
CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")

def load_config():
    try:
        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)
        # Expand user paths
        config["inbox_path"] = os.path.expanduser(config["inbox_path"])
        config["root_path"] = os.path.expanduser(config["root_path"])
        return config
    except FileNotFoundError:
        print("[ERROR] config.json not found. Generating default.")
        # Default config (fallback)
        default_config = {
            "inbox_path": "~/Documents/Inbox",
            "root_path": "~/Documents/Organized",
            "folders": {
                "Others": [] # Ensure fallback exists
            },
            "extensions": {},
            "fallback": "Others"
        }
        with open(CONFIG_FILE, "w") as f:
            json.dump(default_config, f, indent=4)
        return load_config()

class OrganizerHandler(FileSystemEventHandler):
    def __init__(self, config):
        self.config = config
        self.ensure_directories()

    def ensure_directories(self):
        # Create inbox
        os.makedirs(self.config["inbox_path"], exist_ok=True)
        # Create root
        os.makedirs(self.config["root_path"], exist_ok=True)
        # Create subfolders
        for folder in self.config["folders"]:
            path = os.path.join(self.config["root_path"], folder)
            os.makedirs(path, exist_ok=True)
        # Create extension folders
        for folder in self.config["extensions"]:
            path = os.path.join(self.config["root_path"], folder)
            os.makedirs(path, exist_ok=True)
        # Create fallback
        os.makedirs(os.path.join(self.config["root_path"], self.config["fallback"]), exist_ok=True)

    def on_created(self, event):
        if not event.is_directory:
            self.process_file(event.src_path)

    def on_moved(self, event):
        if not event.is_directory:
            if event.dest_path.startswith(self.config["inbox_path"]):
                self.process_file(event.dest_path)

    def process_file(self, file_path):
        filename = os.path.basename(file_path)
        if filename.startswith("."): return

        time.sleep(1) # Wait for write
        
        name, ext = os.path.splitext(filename)
        name_lower = name.lower()
        ext_lower = ext.lower()

        dest_subfolder = None

        # 1. Check Keywords
        for folder, keywords in self.config["folders"].items():
            for k in keywords:
                if k.lower() in name_lower:
                    dest_subfolder = folder
                    break
            if dest_subfolder: break

        # 2. Check Extensions
        if not dest_subfolder:
            for folder, extensions in self.config["extensions"].items():
                if ext_lower in extensions:
                    dest_subfolder = folder
                    break

        # 3. Fallback
        if not dest_subfolder:
            dest_subfolder = self.config["fallback"]

        # Move
        dest_path = os.path.join(self.config["root_path"], dest_subfolder)
        self.move_file(file_path, dest_path)

    def move_file(self, src, dest_folder):
        filename = os.path.basename(src)
        dest_path = os.path.join(dest_folder, filename)
        
        os.makedirs(dest_folder, exist_ok=True)

        if os.path.exists(dest_path):
            base, extension = os.path.splitext(filename)
            counter = 1
            while os.path.exists(dest_path):
                dest_path = os.path.join(dest_folder, f"{base}_{counter}{extension}")
                counter += 1
        
        try:
            shutil.move(src, dest_path)
            print(f"[MOVE] {filename} -> {dest_folder}")
        except Exception as e:
            print(f"[ERROR] Moving {filename}: {e}")

if __name__ == "__main__":
    config = load_config()
    print(f"--- Smart File Organizer ---")
    print(f"Monitoring: {config['inbox_path']}")
    
    observer = Observer()
    event_handler = OrganizerHandler(config)
    observer.schedule(event_handler, config['inbox_path'], recursive=False)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
