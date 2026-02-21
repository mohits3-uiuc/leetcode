"""
HFS+ File System Reader
------------------------
Uses pytsk3 (Python bindings for The Sleuth Kit) to read
HFS+ (Mac OS Extended) volumes from disk images or physical drives.

Supports:
  - Listing directories
  - Reading file contents
  - Getting file/folder metadata
  - Detecting HFS+ partitions automatically
"""

import os
import datetime
import pytsk3


class ImgInfo(pytsk3.Img_Info):
    """Wraps a raw file path or physical device as a pytsk3 image."""
    def __init__(self, path):
        self._path = path
        super().__init__(url=path)


class HFSReader:
    """
    Read-only HFS+ filesystem reader.

    Usage:
        reader = HFSReader(r"\\.\PHYSICALDRIVE1")   # physical disk
        reader = HFSReader("backup.dmg")             # disk image
    """

    def __init__(self, path: str):
        self.path = path
        self._img  = None
        self._fs   = None
        self._vs   = None        # volume system (partition table)
        self._open()

    # ── Internal open logic ──────────────────────────────────────
    def _open(self):
        self._img = ImgInfo(self.path)

        # Try direct FS open first (raw HFS+ image / single partition)
        try:
            self._fs = pytsk3.FS_Info(self._img, fstype=pytsk3.TSK_FS_TYPE_HFS)
            return
        except Exception:
            pass

        # Try auto-detect (could be HFS+ without specifying type)
        try:
            self._fs = pytsk3.FS_Info(self._img)
            return
        except Exception:
            pass

        # Try partition table (GPT/MBR) and find HFS+ partition
        try:
            self._vs = pytsk3.VS_Info(self._img)
            for part in self._vs:
                if not hasattr(part, "addr"):
                    continue
                try:
                    offset = part.start * 512   # sector to bytes
                    fs = pytsk3.FS_Info(self._img, offset=offset,
                                        fstype=pytsk3.TSK_FS_TYPE_HFS)
                    self._fs = fs
                    return
                except Exception:
                    try:
                        fs = pytsk3.FS_Info(self._img, offset=offset)
                        self._fs = fs
                        return
                    except Exception:
                        continue
        except Exception:
            pass

        raise RuntimeError(
            "Could not find an HFS+ partition on this drive.\n"
            "Make sure the drive was formatted as 'Mac OS Extended (HFS+)'.\n"
            "APFS drives are not supported in this version."
        )

    # ── Directory listing ────────────────────────────────────────
    def list_directory(self, path: str = "/") -> list:
        """
        Return a list of dicts for each entry in the directory:
          { name, is_dir, size, inode, modified }
        """
        try:
            directory = self._fs.open_dir(path=path)
        except Exception as e:
            raise RuntimeError(f"Cannot open directory '{path}': {e}")

        entries = []
        for entry in directory:
            try:
                name = entry.info.name.name.decode("utf-8", errors="replace")
            except Exception:
                continue

            is_dir = (entry.info.meta is not None and
                      entry.info.meta.type == pytsk3.TSK_FS_META_TYPE_DIR)

            size = 0
            modified = ""
            try:
                if entry.info.meta:
                    size = entry.info.meta.size
                    mtime = entry.info.meta.mtime
                    if mtime:
                        modified = datetime.datetime.fromtimestamp(mtime).strftime(
                            "%Y-%m-%d %H:%M")
            except Exception:
                pass

            entries.append({
                "name":     name,
                "is_dir":   is_dir,
                "size":     size,
                "modified": modified,
            })

        return entries

    # ── Read a file ──────────────────────────────────────────────
    def read_file(self, path: str) -> bytes | None:
        """
        Read and return a file's contents as bytes.
        Returns None if the path is a directory.
        """
        try:
            f = self._fs.open(path=path)
        except Exception as e:
            raise RuntimeError(f"Cannot open file '{path}': {e}")

        if f.info.meta and f.info.meta.type == pytsk3.TSK_FS_META_TYPE_DIR:
            return None     # caller should handle directories separately

        size = f.info.meta.size if f.info.meta else 0
        if size == 0:
            return b""

        try:
            data = f.read_random(0, size)
            return data
        except Exception as e:
            raise RuntimeError(f"Error reading '{path}': {e}")

    # ── File metadata ────────────────────────────────────────────
    def get_info(self, path: str) -> dict:
        """Return a dict of metadata for the given path."""
        try:
            f = self._fs.open(path=path)
        except Exception as e:
            return {"Error": str(e)}

        info = {}
        try:
            info["Path"]     = path
            info["Name"]     = path.split("/")[-1]
            meta = f.info.meta
            if meta:
                is_dir = meta.type == pytsk3.TSK_FS_META_TYPE_DIR
                info["Type"]     = "Directory" if is_dir else "File"
                info["Size"]     = _human_size(meta.size)
                info["Inode"]    = meta.addr
                info["Mode"]     = oct(meta.mode)
                for attr_name, label in (("crtime", "Created"),
                                          ("mtime",  "Modified"),
                                          ("atime",  "Accessed")):
                    ts = getattr(meta, attr_name, None)
                    if ts:
                        info[label] = datetime.datetime.fromtimestamp(ts).strftime(
                            "%Y-%m-%d %H:%M:%S")
        except Exception as e:
            info["Error"] = str(e)

        return info

    # ── Drive-level info ─────────────────────────────────────────
    def drive_info(self) -> dict:
        """Return high-level information about the HFS+ volume."""
        info = {"Source": self.path}
        try:
            fs = self._fs
            info["FS Type"]        = "HFS+ (Mac OS Extended)"
            info["Block Size"]     = f"{fs.info.block_size} bytes"
            info["Block Count"]    = f"{fs.info.block_count:,}"
            total = fs.info.block_size * fs.info.block_count
            info["Total Size"]     = _human_size(total)
            info["Root Inode"]     = fs.info.root_inum
            info["First Inode"]    = fs.info.first_inum
            info["Last Inode"]     = fs.info.last_inum
        except Exception as e:
            info["Error"] = str(e)
        return info


# ── Helper ───────────────────────────────────────────────────────
def _human_size(n):
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if n < 1024:
            return f"{n:.1f} {unit}"
        n /= 1024
    return f"{n:.1f} PB"
