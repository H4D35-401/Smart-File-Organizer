import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
import subprocess
import sys

# Constants
CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")

class ConfigGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Organizer Settings")
        self.root.geometry("600x500")
        
        self.config = self.load_config()
        
        self.create_widgets()

    def load_config(self):
        try:
            with open(CONFIG_FILE, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {"inbox_path": "", "root_path": "", "folders": {}, "extensions": {}, "fallback": "Others"}

    def save_config(self):
        try:
            with open(CONFIG_FILE, "w") as f:
                json.dump(self.config, f, indent=4)
            messagebox.showinfo("Success", "Configuration saved!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save config: {e}")

    def create_widgets(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # --- General Tab ---
        self.tab_general = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_general, text="General")
        self.create_general_tab()

        # --- Folders Tab ---
        self.tab_folders = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_folders, text="Folder Rules")
        self.create_folders_tab()
        
        # --- Bottom Buttons ---
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Button(btn_frame, text="Save Config", command=self.save_config).pack(side="right", padx=5)
        ttk.Button(btn_frame, text="Restart Service", command=self.restart_service).pack(side="right", padx=5)

    def create_general_tab(self):
        frame = ttk.Frame(self.tab_general, padding=10)
        frame.pack(fill="both", expand=True)
        
        # Inbox Path
        ttk.Label(frame, text="Inbox Path (Source):").grid(row=0, column=0, sticky="w", pady=5)
        self.inbox_var = tk.StringVar(value=self.config.get("inbox_path", ""))
        ttk.Entry(frame, textvariable=self.inbox_var, width=50).grid(row=1, column=0, padx=5)
        ttk.Button(frame, text="Browse", command=lambda: self.browse_folder(self.inbox_var)).grid(row=1, column=1)
        
        # Root Path
        ttk.Label(frame, text="Root Path (Destination):").grid(row=2, column=0, sticky="w", pady=5)
        self.root_path_var = tk.StringVar(value=self.config.get("root_path", ""))
        ttk.Entry(frame, textvariable=self.root_path_var, width=50).grid(row=3, column=0, padx=5)
        ttk.Button(frame, text="Browse", command=lambda: self.browse_folder(self.root_path_var)).grid(row=3, column=1)

        # Update config on change
        self.inbox_var.trace("w", lambda *args: self.config.update({"inbox_path": self.inbox_var.get()}))
        self.root_path_var.trace("w", lambda *args: self.config.update({"root_path": self.root_path_var.get()}))

    def create_folders_tab(self):
        paned = ttk.PanedWindow(self.tab_folders, orient="horizontal")
        paned.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Left: Folders List
        left_frame = ttk.LabelFrame(paned, text="Folders")
        paned.add(left_frame, weight=1)
        
        self.folder_list = tk.Listbox(left_frame)
        self.folder_list.pack(fill="both", expand=True, padx=5, pady=5)
        self.folder_list.bind("<<ListboxSelect>>", self.on_folder_select)
        
        btn_frame_l = ttk.Frame(left_frame)
        btn_frame_l.pack(fill="x", padx=5, pady=5)
        ttk.Button(btn_frame_l, text="+", width=3, command=self.add_folder).pack(side="left")
        ttk.Button(btn_frame_l, text="-", width=3, command=self.remove_folder).pack(side="left")

        # Right: Keywords List
        right_frame = ttk.LabelFrame(paned, text="Keywords")
        paned.add(right_frame, weight=2)
        
        self.keyword_list = tk.Listbox(right_frame)
        self.keyword_list.pack(fill="both", expand=True, padx=5, pady=5)
        
        btn_frame_r = ttk.Frame(right_frame)
        btn_frame_r.pack(fill="x", padx=5, pady=5)
        ttk.Button(btn_frame_r, text="+", width=3, command=self.add_keyword).pack(side="left")
        ttk.Button(btn_frame_r, text="-", width=3, command=self.remove_keyword).pack(side="left")

        # Populate Folders
        for folder in self.config.get("folders", {}):
            self.folder_list.insert(tk.END, folder)

    def browse_folder(self, var):
        path = filedialog.askdirectory()
        if path:
            var.set(path)

    def on_folder_select(self, event):
        selection = self.folder_list.curselection()
        if selection:
            self.keyword_list.delete(0, tk.END)
            folder = self.folder_list.get(selection[0])
            keywords = self.config["folders"].get(folder, [])
            for k in keywords:
                self.keyword_list.insert(tk.END, k)

    def add_folder(self):
        name = HelperDialog(self.root, "Add Folder", "Folder Name (e.g., College/Math):").result
        if name:
            if name not in self.config["folders"]:
                self.config["folders"][name] = []
                self.folder_list.insert(tk.END, name)

    def remove_folder(self):
        selection = self.folder_list.curselection()
        if selection:
            folder = self.folder_list.get(selection[0])
            if messagebox.askyesno("Confirm", f"Delete folder rule '{folder}'?"):
                del self.config["folders"][folder]
                self.folder_list.delete(selection[0])
                self.keyword_list.delete(0, tk.END)

    def add_keyword(self):
        selection = self.folder_list.curselection()
        if not selection: return
        folder = self.folder_list.get(selection[0])
        
        keyword = HelperDialog(self.root, "Add Keyword", "Keyword (e.g., invoice):").result
        if keyword:
            self.config["folders"][folder].append(keyword)
            self.keyword_list.insert(tk.END, keyword)

    def remove_keyword(self):
        sel_folder = self.folder_list.curselection()
        sel_key = self.keyword_list.curselection()
        if sel_folder and sel_key:
            folder = self.folder_list.get(sel_folder[0])
            keyword = self.keyword_list.get(sel_key[0])
            
            self.config["folders"][folder].remove(keyword)
            self.keyword_list.delete(sel_key[0])

    def restart_service(self):
        # Platform specific restart
        if sys.platform == "linux":
            cmd = ["systemctl", "--user", "restart", "file-organizer.service"]
        elif sys.platform == "darwin": # macOS
            cmd = ["launchctl", "stop", "com.user.fileorganizer"] 
            # Needs immediate start, but launchctl stop doesn't block properly sometimes.
            # Simplified for now.
            messagebox.showinfo("Info", "On macOS, the change might take effect automatically or you can run install.sh again.")
            return
        elif sys.platform == "win32":
            messagebox.showinfo("Info", "On Windows, restart the background script manually via Task Manager or reboot.")
            return
        
        try:
            subprocess.run(cmd, check=True)
            messagebox.showinfo("Success", "Service restarted!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to restart service: {e}")

class HelperDialog(tk.Toplevel):
    def __init__(self, parent, title, prompt):
        super().__init__(parent)
        self.transient(parent)
        self.title(title)
        self.result = None

        tk.Label(self, text=prompt).pack(padx=10, pady=5)
        self.e = tk.Entry(self)
        self.e.pack(padx=10, pady=5)
        self.e.bind("<Return>", self.ok)
        
        btn = tk.Button(self, text="OK", command=self.ok)
        btn.pack(pady=5)
        
        self.wait_visibility()
        self.grab_set()
        self.wait_window(self)

    def ok(self, event=None):
        self.result = self.e.get()
        self.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ConfigGUI(root)
    root.mainloop()
