"""
MP4 to MP3 Converter for macOS
-------------------------------
Requirements: ffmpeg must be installed.
Install via Homebrew:  brew install ffmpeg
"""

import subprocess
import sys
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path


def check_ffmpeg():
    """Check if ffmpeg is installed."""
    result = subprocess.run(["which", "ffmpeg"], capture_output=True, text=True)
    return result.returncode == 0


def convert(input_path: str, output_path: str, bitrate: str, progress_label) -> bool:
    """Run ffmpeg conversion and return True on success."""
    cmd = [
        "ffmpeg",
        "-i", input_path,
        "-vn",                   # no video
        "-acodec", "libmp3lame",
        "-ab", bitrate,
        "-ar", "44100",          # sample rate
        "-y",                    # overwrite output
        output_path
    ]
    progress_label.config(text="Converting... please wait ⏳")
    progress_label.update()

    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0


def browse_file(entry_widget):
    path = filedialog.askopenfilename(
        title="Select MP4 file",
        filetypes=[("MP4 files", "*.mp4"), ("All files", "*.*")]
    )
    if path:
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, path)
        # Auto-fill output path
        output = str(Path(path).with_suffix(".mp3"))
        out_entry.delete(0, tk.END)
        out_entry.insert(0, output)


def browse_output(entry_widget):
    path = filedialog.asksaveasfilename(
        title="Save MP3 as",
        defaultextension=".mp3",
        filetypes=[("MP3 files", "*.mp3")]
    )
    if path:
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, path)


def run_conversion():
    input_path = in_entry.get().strip()
    output_path = out_entry.get().strip()
    bitrate = bitrate_var.get()

    if not input_path:
        messagebox.showerror("Error", "Please select an MP4 file.")
        return
    if not os.path.isfile(input_path):
        messagebox.showerror("Error", f"File not found:\n{input_path}")
        return
    if not output_path:
        messagebox.showerror("Error", "Please specify an output path.")
        return

    success = convert(input_path, output_path, bitrate, status_label)

    if success:
        size_mb = os.path.getsize(output_path) / (1024 * 1024)
        status_label.config(text=f"✅ Done!  Saved to: {output_path}  ({size_mb:.1f} MB)", fg="green")
        messagebox.showinfo("Success", f"Conversion complete!\n\nSaved to:\n{output_path}")
    else:
        status_label.config(text="❌ Conversion failed.", fg="red")
        messagebox.showerror("Error", "Conversion failed. Make sure ffmpeg is installed:\n\nbrew install ffmpeg")


# ── GUI setup ──────────────────────────────────────────────────
root = tk.Tk()
root.title("MP4 → MP3 Converter")
root.resizable(False, False)

pad = {"padx": 10, "pady": 6}

# Check ffmpeg on startup
if not check_ffmpeg():
    messagebox.showwarning(
        "ffmpeg not found",
        "ffmpeg is required but not installed.\n\nInstall it with:\n  brew install ffmpeg"
    )

# Input file row
tk.Label(root, text="Input MP4:", anchor="w", width=12).grid(row=0, column=0, **pad, sticky="w")
in_entry = tk.Entry(root, width=50)
in_entry.grid(row=0, column=1, **pad)
tk.Button(root, text="Browse…", command=lambda: browse_file(in_entry)).grid(row=0, column=2, **pad)

# Output file row
tk.Label(root, text="Output MP3:", anchor="w", width=12).grid(row=1, column=0, **pad, sticky="w")
out_entry = tk.Entry(root, width=50)
out_entry.grid(row=1, column=1, **pad)
tk.Button(root, text="Browse…", command=lambda: browse_output(out_entry)).grid(row=1, column=2, **pad)

# Bitrate selector
tk.Label(root, text="Bitrate:", anchor="w", width=12).grid(row=2, column=0, **pad, sticky="w")
bitrate_var = tk.StringVar(value="192k")
bitrate_menu = ttk.Combobox(root, textvariable=bitrate_var,
                             values=["128k", "192k", "256k", "320k"],
                             state="readonly", width=10)
bitrate_menu.grid(row=2, column=1, **pad, sticky="w")
tk.Label(root, text="(320k = best quality)", fg="grey").grid(row=2, column=1, padx=120, sticky="w")

# Convert button
tk.Button(root, text="Convert to MP3", command=run_conversion,
          bg="#007AFF", fg="white", font=("Helvetica", 13, "bold"),
          padx=12, pady=6).grid(row=3, column=0, columnspan=3, pady=12)

# Status label
status_label = tk.Label(root, text="", fg="grey", wraplength=500)
status_label.grid(row=4, column=0, columnspan=3, **pad)

root.mainloop()
