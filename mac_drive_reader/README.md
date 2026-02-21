# Mac Drive Reader for Windows

A Windows GUI application to **read HFS+ (Mac OS Extended) drives** on Windows — similar to MacDrive.

Connect a Mac-formatted external drive to your Windows PC and browse, view, and copy files from it.

---

## Features

- 📂 Browse the full folder/file tree of any HFS+ drive
- 📋 Copy individual files or entire folders to Windows
- 🔍 View file metadata (size, dates, permissions)
- 💽 Works with physical drives AND disk image files (`.dmg`, `.img`, `.dd`)
- 🖥️ Clean dark-themed GUI
- ⚡ Background loading — UI stays responsive

## Limitations

- **Read-only** — writing back to HFS+ drives is not supported
- **HFS+ only** — APFS drives (formatted on macOS 10.13+) are not supported in this version
- Requires running as **Administrator** to access physical drives

---

## Requirements

### On Windows (to run from source or to build)

| Requirement | How to get it |
|---|---|
| Python 3.10+ | https://www.python.org/downloads/ |
| pytsk3 | `pip install pytsk3` |
| PyInstaller (to build .exe) | `pip install pyinstaller` |
| Inno Setup 6 (to build installer) | https://jrsoftware.org/isdl.php |

---

## Quick Start (Run from Source on Windows)

```bat
git clone https://github.com/mohits3-uiuc/leetcode.git
cd leetcode\mac_drive_reader

pip install -r requirements.txt
python main.py
```

> **Run as Administrator** if you want to open physical drives (right-click → Run as Administrator).

---

## Build a Standalone Windows Installer

Run `build.bat` on a Windows machine:

```bat
build.bat
```

This will:
1. Install all Python dependencies
2. Build `dist\MacDriveReader.exe` (standalone, no Python needed)
3. Build `dist\MacDriveReader_Setup.exe` (Windows installer, if Inno Setup is installed)

---

## How to Use the App

### Step 1 — Connect your Mac drive
Plug in the Mac-formatted USB drive or external hard drive to your Windows PC.

### Step 2 — Open the drive
- **Disk Image**: Click **"Open Disk Image"** → select your `.dmg` or `.img` file
- **Physical Drive**: Click **"Open Physical Drive"** → select your drive from the list

> If the drive doesn't appear, run the app as Administrator.

### Step 3 — Browse files
- Click the **▶ arrows** to expand folders in the tree on the left
- **Double-click** a file or folder to see its properties on the right

### Step 4 — Copy files to Windows
- **Right-click** any item → **"Copy to Windows…"** → choose a destination folder
- Or select items and click **"Copy Selected to Windows…"** on the right panel
- To copy everything: click **"Copy All to Windows…"**

---

## Project Structure

```
mac_drive_reader/
├── main.py           ← GUI application (tkinter)
├── hfs_reader.py     ← HFS+ filesystem reader (pytsk3)
├── requirements.txt  ← Python dependencies
├── build.bat         ← Build script (Windows) → produces .exe + installer
├── installer.iss     ← Inno Setup script → produces Setup.exe
├── assets/           ← App icon goes here (icon.ico)
└── README.md         ← This file
```

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `ModuleNotFoundError: pytsk3` | Run `pip install pytsk3` |
| "Could not find HFS+ partition" | The drive may be APFS (not supported). Check if it was formatted as Mac OS Extended |
| Drive not listed | Run as Administrator |
| Files copy with garbled names | Use UTF-8 filenames. Non-ASCII characters may need manual renaming on Windows |
| App crashes on open | Make sure drive is fully connected and not being scanned by antivirus |

---

## Technical Details

- Uses **pytsk3** (Python bindings for [The Sleuth Kit](https://www.sleuthkit.org/)) for HFS+ parsing
- Supports both GPT and MBR partition tables to auto-detect the HFS+ partition
- File reading via `TSK_FS_TYPE_HFS` — same engine used by forensic tools
- GUI built with Python's built-in **tkinter** (no extra GUI frameworks needed)
