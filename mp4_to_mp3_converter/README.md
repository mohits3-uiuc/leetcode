# MP4 to MP3 Converter

A simple macOS GUI app to convert MP4 video files to MP3 audio files.

---

## Requirements

- macOS
- Python 3 (comes pre-installed on macOS, or install via [Homebrew](https://brew.sh))
- `ffmpeg` — used to do the actual conversion
- `tkinter` — used for the GUI

---

## One-Time Setup

Open Terminal and run these commands once:

### 1. Install Homebrew (if not already installed)
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### 2. Install ffmpeg
```bash
brew install ffmpeg
```

### 3. Install tkinter support for Python
```bash
brew install python-tk
```

---

## How to Start the App

Open Terminal, navigate to this folder, and run:

```bash
cd /Users/mohit/Downloads/leetcode/mp4_to_mp3_converter
/opt/homebrew/bin/python3 mp4_to_mp3.py
```

Or run it directly from anywhere:

```bash
/opt/homebrew/bin/python3 /Users/mohit/Downloads/leetcode/mp4_to_mp3_converter/mp4_to_mp3.py
```

---

## How to Use the App

Once the window opens:

1. **Input MP4** — Click **Browse…** and select your `.mp4` file
2. **Output MP3** — The output path is auto-filled (same location, `.mp3` extension). Change it if needed by clicking **Browse…**
3. **Bitrate** — Choose audio quality from the dropdown:
   - `128k` — smaller file size, acceptable quality
   - `192k` — default, good balance ✅
   - `256k` — high quality
   - `320k` — best quality, largest file
4. Click **Convert to MP3**
5. A success message will appear when done, showing the output file path and size

---

## Project Structure

```
mp4_to_mp3_converter/
├── mp4_to_mp3.py   ← main application
└── README.md       ← this file
```

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `ModuleNotFoundError: No module named '_tkinter'` | Run `brew install python-tk` |
| `ffmpeg not found` warning on startup | Run `brew install ffmpeg` |
| Conversion fails | Make sure the input file is a valid `.mp4` and ffmpeg is installed |
