"""
Mac Drive Reader for Windows
-----------------------------
Reads all macOS drive formats:
  • APFS  (Apple File System)         macOS 10.13 High Sierra and later
  • HFS+  (Mac OS Extended)           macOS 8.1 – 12
  • HFS   (Mac OS Standard / Classic) very old drives
  • exFAT / FAT32 / FAT16             cross-platform USB / SD cards

Dependencies: pytsk3, apfs, tkinter (built-in)
"""

import os
import sys
import threading
import shutil
import string
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path

try:
    import pytsk3
    TSK_AVAILABLE = True
except ImportError:
    TSK_AVAILABLE = False

# ── Try to import the unified Mac FS reader ────────────────────
try:
    from mac_fs_reader import MacFSReader
    FS_AVAILABLE = True
except ImportError:
    FS_AVAILABLE = False


# ═══════════════════════════════════════════════════════════════
#  Helpers
# ═══════════════════════════════════════════════════════════════

def get_windows_drives():
    """Return list of available Windows drive letters."""
    drives = []
    bitmask = 0
    try:
        import ctypes
        bitmask = ctypes.windll.kernel32.GetLogicalDrives()
    except Exception:
        pass
    for letter in string.ascii_uppercase:
        if bitmask & 1:
            drives.append(f"{letter}:\\")
        bitmask >>= 1
    return drives


def get_physical_disks():
    """Return list of physical disk paths accessible on Windows."""
    disks = []
    try:
        import subprocess
        result = subprocess.run(
            ["wmic", "diskdrive", "get", "DeviceID,Caption,Size"],
            capture_output=True, text=True, timeout=5
        )
        lines = [l.strip() for l in result.stdout.strip().splitlines() if l.strip()]
        for line in lines[1:]:          # skip header
            parts = line.split()
            if parts:
                device_id = parts[0]    # e.g. \\.\PHYSICALDRIVE1
                label = " ".join(parts[1:-1]) if len(parts) > 2 else device_id
                disks.append((device_id, label))
    except Exception:
        pass
    return disks


def human_size(n):
    """Convert bytes to human-readable string."""
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if n < 1024:
            return f"{n:.1f} {unit}"
        n /= 1024
    return f"{n:.1f} PB"


# ═══════════════════════════════════════════════════════════════
#  Main Application Window
# ═══════════════════════════════════════════════════════════════

class MacDriveReaderApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Mac Drive Reader")
        self.geometry("1000x650")
        self.minsize(800, 500)
        self.configure(bg="#1e1e2e")

        self.reader = None          # MacFSReader instance
        self.current_path = "/"    # current browsed path
        self._node_map = {}         # treeview node → virtual path

        self._build_ui()
        self._check_dependencies()

    # ── Dependency check ────────────────────────────────────────
    def _check_dependencies(self):
        if not TSK_AVAILABLE:
            self.set_status(
                "⚠  pytsk3 not installed — run:  pip install pytsk3",
                color="#f38ba8"
            )

    # ── UI Construction ─────────────────────────────────────────
    def _build_ui(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("Treeview",
                        background="#313244", foreground="#cdd6f4",
                        fieldbackground="#313244", rowheight=24)
        style.configure("Treeview.Heading",
                        background="#45475a", foreground="#cdd6f4",
                        font=("Segoe UI", 9, "bold"))
        style.map("Treeview", background=[("selected", "#89b4fa")])
        style.configure("TButton", padding=6)
        style.configure("TLabel", background="#1e1e2e", foreground="#cdd6f4")
        style.configure("TFrame", background="#1e1e2e")

        # ── Top bar ──
        top = ttk.Frame(self, padding=(10, 8))
        top.pack(fill="x")

        ttk.Label(top, text="🍎 Mac Drive Reader",
                  font=("Segoe UI", 14, "bold")).pack(side="left")

        ttk.Button(top, text="Open Disk Image (.dmg / .img)",
                   command=self._open_image).pack(side="left", padx=(20, 4))
        ttk.Button(top, text="Open Physical Drive",
                   command=self._open_physical).pack(side="left", padx=4)

        # ── Path bar ──
        path_frame = ttk.Frame(self)
        path_frame.pack(fill="x", padx=10, pady=(0, 4))
        ttk.Label(path_frame, text="Path:").pack(side="left")
        self.path_var = tk.StringVar(value="—")
        ttk.Label(path_frame, textvariable=self.path_var,
                  foreground="#89dceb").pack(side="left", padx=6)

        # ── Main pane (tree left, detail right) ──
        pane = tk.PanedWindow(self, orient="horizontal",
                              bg="#1e1e2e", sashwidth=5)
        pane.pack(fill="both", expand=True, padx=10, pady=4)

        # Left — filesystem tree
        left = ttk.Frame(pane)
        pane.add(left, minsize=280)

        ttk.Label(left, text="File Browser",
                  font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(0, 2))

        tree_frame = ttk.Frame(left)
        tree_frame.pack(fill="both", expand=True)

        self.tree = ttk.Treeview(tree_frame, columns=("size", "type"),
                                  selectmode="extended")
        self.tree.heading("#0",     text="Name")
        self.tree.heading("size",   text="Size")
        self.tree.heading("type",   text="Type")
        self.tree.column("#0",      width=220, minwidth=120)
        self.tree.column("size",    width=80,  anchor="e")
        self.tree.column("type",    width=70,  anchor="center")

        vsb = ttk.Scrollbar(tree_frame, orient="vertical",
                             command=self.tree.yview)
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal",
                             command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set,
                             xscrollcommand=hsb.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        tree_frame.rowconfigure(0, weight=1)
        tree_frame.columnconfigure(0, weight=1)

        self.tree.bind("<<TreeviewOpen>>", self._on_expand)
        self.tree.bind("<Double-1>",       self._on_double_click)
        self.tree.bind("<Button-3>",       self._on_right_click)

        # Right — info + actions
        right = ttk.Frame(pane, padding=10)
        pane.add(right, minsize=200)

        ttk.Label(right, text="Selected Item",
                  font=("Segoe UI", 10, "bold")).pack(anchor="w")

        self.info_box = tk.Text(right, height=10, bg="#313244",
                                 fg="#cdd6f4", relief="flat",
                                 font=("Consolas", 9), state="disabled")
        self.info_box.pack(fill="x", pady=(4, 10))

        ttk.Button(right, text="📋  Copy Selected to Windows…",
                   command=self._copy_selected).pack(fill="x", pady=2)
        ttk.Button(right, text="💾  Copy All to Windows…",
                   command=self._copy_all).pack(fill="x", pady=2)

        ttk.Separator(right, orient="horizontal").pack(fill="x", pady=10)

        ttk.Label(right, text="Drive Info",
                  font=("Segoe UI", 10, "bold")).pack(anchor="w")
        self.drive_info = tk.Text(right, height=6, bg="#313244",
                                   fg="#a6e3a1", relief="flat",
                                   font=("Consolas", 9), state="disabled")
        self.drive_info.pack(fill="x", pady=(4, 0))

        # ── Status bar ──
        self.status_var = tk.StringVar(value="Ready — open a disk image or physical drive")
        status = tk.Label(self, textvariable=self.status_var,
                          bg="#313244", fg="#a6adc8",
                          anchor="w", padx=8, pady=4)
        status.pack(fill="x", side="bottom")
        self._status_label = status

    # ── Open sources ────────────────────────────────────────────
    def _open_image(self):
        path = filedialog.askopenfilename(
            title="Select macOS Disk Image",
            filetypes=[
                ("Disk images", "*.dmg *.img *.iso *.dd *.raw *.bin"),
                ("DMG files", "*.dmg"),
                ("Raw images", "*.img *.raw *.bin *.dd"),
                ("ISO images", "*.iso"),
                ("All files", "*.*")
            ]
        )
        if path:
            self._load_drive(path)

    def _open_physical(self):
        disks = get_physical_disks()
        if not disks:
            messagebox.showinfo("No Disks", "No physical disks found.\n"
                                "Try running the app as Administrator.")
            return
        self._pick_disk_dialog(disks)

    def _pick_disk_dialog(self, disks):
        win = tk.Toplevel(self)
        win.title("Select Physical Disk")
        win.geometry("500x300")
        win.configure(bg="#1e1e2e")
        win.grab_set()

        ttk.Label(win, text="Select a disk to open (read-only):",
                  font=("Segoe UI", 10)).pack(pady=(12, 4), padx=10, anchor="w")

        lb = tk.Listbox(win, bg="#313244", fg="#cdd6f4",
                        font=("Consolas", 9), height=10)
        lb.pack(fill="both", expand=True, padx=10, pady=4)

        for device_id, label in disks:
            lb.insert("end", f"{device_id}  —  {label}")

        lb.select_set(0)

        def confirm():
            sel = lb.curselection()
            if sel:
                device_id = disks[sel[0]][0]
                win.destroy()
                self._load_drive(device_id)

        ttk.Button(win, text="Open (read-only)", command=confirm).pack(pady=8)

    def _load_drive(self, path):
        if not FS_AVAILABLE or not TSK_AVAILABLE:
            messagebox.showerror(
                "Missing Dependency",
                "pytsk3 is required.\n\nInstall it with:\n  pip install pytsk3"
            )
            return

        self.set_status(f"Opening: {path} …", color="#f9e2af")
        self.tree.delete(*self.tree.get_children())
        self._node_map.clear()

        def task():
            try:
                reader = MacFSReader.open(path)
                self.reader = reader
                self.after(0, lambda: self._populate_tree(reader))
                self.after(0, lambda: self._show_drive_info(reader))
                self.after(0, lambda: self.set_status(
                    f"✅  Opened: {path}", color="#a6e3a1"))
            except Exception as e:
                self.after(0, lambda: self.set_status(
                    f"❌  Error: {e}", color="#f38ba8"))
                self.after(0, lambda: messagebox.showerror("Open Failed", str(e)))

        threading.Thread(target=task, daemon=True).start()

    # ── Tree population ─────────────────────────────────────────
    def _populate_tree(self, reader):
        self.tree.delete(*self.tree.get_children())
        self._node_map.clear()
        self.path_var.set("/")
        self._load_directory(reader, "", "/")

    def _load_directory(self, reader, parent_node, path):
        try:
            entries = reader.list_directory(path)
        except Exception as e:
            self.set_status(f"⚠  Cannot read {path}: {e}", color="#fab387")
            return

        for entry in sorted(entries, key=lambda e: (not e["is_dir"], e["name"].lower())):
            name = entry["name"]
            if name in (".", ".."):
                continue

            size_str = human_size(entry["size"]) if not entry["is_dir"] else ""
            kind     = "📁 Folder" if entry["is_dir"] else "📄 File"
            icon     = "📁" if entry["is_dir"] else "📄"
            full_path = (path.rstrip("/") + "/" + name)

            node = self.tree.insert(
                parent_node, "end",
                text=f"{icon}  {name}",
                values=(size_str, kind)
            )
            self._node_map[node] = full_path

            if entry["is_dir"]:
                # Lazy-load placeholder
                self.tree.insert(node, "end", text="⏳ Loading…", values=("", ""))

    def _on_expand(self, event):
        node = self.tree.focus()
        children = self.tree.get_children(node)
        if len(children) == 1:
            child_text = self.tree.item(children[0], "text")
            if "Loading" in child_text:
                self.tree.delete(children[0])
                path = self._node_map.get(node, "/")
                self._load_directory(self.reader, node, path)

    def _on_double_click(self, event):
        node = self.tree.focus()
        path = self._node_map.get(node)
        if path:
            self.path_var.set(path)
            self._show_item_info(path)

    # ── Right-click context menu ─────────────────────────────────
    def _on_right_click(self, event):
        node = self.tree.identify_row(event.y)
        if not node:
            return
        self.tree.selection_set(node)
        menu = tk.Menu(self, tearoff=0, bg="#313244", fg="#cdd6f4",
                       activebackground="#89b4fa", activeforeground="#1e1e2e")
        menu.add_command(label="📋  Copy to Windows…",
                         command=self._copy_selected)
        menu.add_command(label="ℹ  Properties",
                         command=lambda: self._show_item_info(
                             self._node_map.get(node, "")))
        menu.tk_popup(event.x_root, event.y_root)

    # ── Info panels ──────────────────────────────────────────────
    def _show_item_info(self, path):
        if not self.reader or not path:
            return
        try:
            info = self.reader.get_info(path)
            text = "\n".join(f"{k}: {v}" for k, v in info.items())
        except Exception as e:
            text = f"Error: {e}"

        self.info_box.config(state="normal")
        self.info_box.delete("1.0", "end")
        self.info_box.insert("end", text)
        self.info_box.config(state="disabled")

    def _show_drive_info(self, reader):
        try:
            info = reader.drive_info()
            text = "\n".join(f"{k}: {v}" for k, v in info.items())
        except Exception as e:
            text = f"Error: {e}"

        self.drive_info.config(state="normal")
        self.drive_info.delete("1.0", "end")
        self.drive_info.insert("end", text)
        self.drive_info.config(state="disabled")

    # ── Copy operations ──────────────────────────────────────────
    def _copy_selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Nothing selected", "Select one or more files first.")
            return
        dest = filedialog.askdirectory(title="Copy to Windows folder…")
        if dest:
            paths = [self._node_map[n] for n in selected if n in self._node_map]
            self._do_copy(paths, dest)

    def _copy_all(self):
        if not self.reader:
            messagebox.showinfo("No drive open", "Open a drive first.")
            return
        dest = filedialog.askdirectory(title="Copy ALL files to Windows folder…")
        if dest:
            self._do_copy(["/"], dest)

    def _do_copy(self, src_paths, dest_dir):
        self.set_status("Copying… please wait ⏳", color="#f9e2af")

        def task():
            copied = 0
            errors = 0
            for src in src_paths:
                try:
                    name = Path(src).name or "mac_drive_root"
                    dest_path = os.path.join(dest_dir, name)
                    data = self.reader.read_file(src)
                    if data is not None:
                        with open(dest_path, "wb") as f:
                            f.write(data)
                        copied += 1
                    else:
                        # It's a directory — recursively copy
                        self._copy_dir_recursive(src, dest_dir)
                        copied += 1
                except Exception as e:
                    errors += 1

            msg = f"✅  Copied {copied} item(s) to {dest_dir}"
            if errors:
                msg += f"  |  ⚠ {errors} error(s)"
            self.after(0, lambda: self.set_status(msg, color="#a6e3a1"))
            self.after(0, lambda: messagebox.showinfo("Done", msg))

        threading.Thread(target=task, daemon=True).start()

    def _copy_dir_recursive(self, src_path, dest_parent):
        dest_dir = os.path.join(dest_parent, Path(src_path).name)
        os.makedirs(dest_dir, exist_ok=True)
        for entry in self.reader.list_directory(src_path):
            if entry["name"] in (".", ".."):
                continue
            child = src_path.rstrip("/") + "/" + entry["name"]
            if entry["is_dir"]:
                self._copy_dir_recursive(child, dest_dir)
            else:
                data = self.reader.read_file(child)
                if data is not None:
                    with open(os.path.join(dest_dir, entry["name"]), "wb") as f:
                        f.write(data)

    # ── Status bar helper ────────────────────────────────────────
    def set_status(self, msg, color="#a6adc8"):
        self.status_var.set(msg)
        self._status_label.config(fg=color)
        self.update_idletasks()


# ═══════════════════════════════════════════════════════════════
#  Entry point
# ═══════════════════════════════════════════════════════════════
if __name__ == "__main__":
    app = MacDriveReaderApp()
    app.mainloop()
