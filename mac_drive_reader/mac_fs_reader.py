"""
Mac Filesystem Reader – Unified Multi-Format Reader
----------------------------------------------------
Supports all macOS drive formats:
  • APFS  (Apple File System)         — macOS 10.13 High Sierra and later
  • HFS+  (Mac OS Extended)           — Mac OS 8.1 – macOS 12
  • HFS   (Mac OS Standard)           — classic, pre-HFS+, very old drives
  • exFAT / FAT32                     — cross-platform; used on SD cards, USB

Detection order:
  1. Auto-detect filesystem type via pytsk3
  2. If APFS container detected → use APFSReader (pure-Python fallback)
  3. If HFS/HFS+ → use TskReader (pytsk3)
  4. If FAT/exFAT → use TskReader (pytsk3)

Dependencies:
  pip install pytsk3 apfs construct
"""

import os
import datetime
import struct

# ── pytsk3 (The Sleuth Kit) ──────────────────────────────────────
try:
    import pytsk3
    TSK_AVAILABLE = True
except ImportError:
    TSK_AVAILABLE = False

# ── apfs Python library (pure-Python APFS parser) ───────────────
try:
    import apfs as apfslib
    APFS_LIB_AVAILABLE = True
except ImportError:
    APFS_LIB_AVAILABLE = False


# ═══════════════════════════════════════════════════════════════
#  Filesystem type constants
# ═══════════════════════════════════════════════════════════════
FS_UNKNOWN = "unknown"
FS_APFS    = "APFS"
FS_HFSPLUS = "HFS+"
FS_HFS     = "HFS"
FS_EXFAT   = "exFAT"
FS_FAT32   = "FAT32"
FS_FAT16   = "FAT16"


# ═══════════════════════════════════════════════════════════════
#  Image wrapper for pytsk3
# ═══════════════════════════════════════════════════════════════
class _ImgInfo(pytsk3.Img_Info) if TSK_AVAILABLE else object:
    def __init__(self, path):
        if TSK_AVAILABLE:
            super().__init__(url=path)


# ═══════════════════════════════════════════════════════════════
#  Probe: detect filesystem type from raw bytes
# ═══════════════════════════════════════════════════════════════
APFS_MAGIC    = b"NXSB"   # at offset 32 in APFS superblock
HFS_MAGIC     = b"\xD2\xD7"  # MDB signature offset 0 in HFS
HFSPLUS_MAGIC = b"\x00\x04"  # HFS+ wrapper in HFS volume
HFSPLUS_SIG   = b"H+"      # HFS+ volume header sig (sector 2, offset 0)
HFSX_SIG      = b"HX"      # HFSX (case-sensitive HFS+)
EXFAT_SIG     = b"EXFAT   "  # at offset 3

def probe_fs_type(path: str) -> str:
    """
    Read the first few sectors of a disk/image and guess the filesystem type.
    Returns one of the FS_* constants.
    """
    try:
        with open(path, "rb") as f:
            # Read first 4 KB
            header = f.read(4096)

            # APFS: NX superblock appears at block 0, magic "NXSB" at offset 32
            if len(header) > 36 and header[32:36] == APFS_MAGIC:
                return FS_APFS

            # exFAT: "EXFAT   " at bytes 3-10
            if len(header) > 11 and header[3:11] == EXFAT_SIG:
                return FS_EXFAT

            # HFS+/HFSX: volume header at sector 2 (offset 1024), magic first 2 bytes
            if len(header) > 1026:
                sig = header[1024:1026]
                if sig == b"H+":
                    return FS_HFSPLUS
                if sig == b"HX":
                    return FS_HFSPLUS   # HFSX is case-sensitive HFS+

            # Old HFS: MDB at offset 1024, signature 0x4244 ("BD")
            if len(header) > 1026 and header[1024:1026] == b"BD":
                return FS_HFS

            # FAT32: OEM name bytes 3-11, or check boot signature
            if len(header) > 512:
                # FAT32 has "FAT32   " at offset 82 in boot sector
                if header[82:90] == b"FAT32   ":
                    return FS_FAT32
                if header[54:62] == b"FAT16   ":
                    return FS_FAT16
                if header[54:62] == b"FAT     ":
                    return FS_FAT16
    except Exception:
        pass

    # Fallback: try to detect via GPT/MBR partition type GUIDs
    try:
        with open(path, "rb") as f:
            f.seek(512)          # LBA 1 – GPT header
            gpt_sig = f.read(8)
            if gpt_sig == b"EFI PART":
                # Read partition entries (LBA 2 onwards)
                f.seek(1024)
                entry = f.read(128)
                # APFS container GUID: 7C3457EF-0000-11AA-AA11-00306543ECAC
                apfs_guid = bytes.fromhex("EF57347C00001A11AA1100306543ECAC")
                if len(entry) >= 16 and entry[:16] == apfs_guid:
                    return FS_APFS
    except Exception:
        pass

    return FS_UNKNOWN


# ═══════════════════════════════════════════════════════════════
#  TSK-based reader (HFS+, HFS, FAT, exFAT)
# ═══════════════════════════════════════════════════════════════
class TskReader:
    """
    Reader using The Sleuth Kit (pytsk3).
    Supports HFS+, HFS (classic), FAT32, exFAT, and auto-detection.
    """

    # Map our FS_* constants to TSK type constants
    _TSK_TYPEMAP = {}

    def __init__(self, path: str, fs_type_hint: str = FS_UNKNOWN):
        if not TSK_AVAILABLE:
            raise RuntimeError("pytsk3 is not installed. Run: pip install pytsk3")

        self.path         = path
        self.fs_type_hint = fs_type_hint
        self._img = _ImgInfo(path)
        self._fs  = None
        self._open()

    def _open(self):
        # Build TSK type map lazily (constants may not exist in all versions)
        tsk_types_to_try = []
        if self.fs_type_hint == FS_HFSPLUS:
            tsk_types_to_try = [
                getattr(pytsk3, "TSK_FS_TYPE_HFS",  None),
                getattr(pytsk3, "TSK_FS_TYPE_HFS_DETECT", None),
            ]
        elif self.fs_type_hint == FS_HFS:
            tsk_types_to_try = [
                getattr(pytsk3, "TSK_FS_TYPE_HFS",  None),
            ]
        elif self.fs_type_hint in (FS_EXFAT, FS_FAT32, FS_FAT16):
            tsk_types_to_try = [
                getattr(pytsk3, "TSK_FS_TYPE_FAT_DETECT", None),
                getattr(pytsk3, "TSK_FS_TYPE_EXFAT",      None),
            ]

        # Always add auto-detect as last resort
        tsk_types_to_try.append(getattr(pytsk3, "TSK_FS_TYPE_DETECT", None))
        tsk_types_to_try.append(None)   # no hint at all

        errors = []

        # --- Try direct FS open (no partition table) ---
        for tsk_type in tsk_types_to_try:
            try:
                kwargs = {}
                if tsk_type is not None:
                    kwargs["fstype"] = tsk_type
                self._fs = pytsk3.FS_Info(self._img, **kwargs)
                return
            except Exception as e:
                errors.append(str(e))

        # --- Try each partition in the partition table ---
        try:
            vs = pytsk3.VS_Info(self._img)
            for part in vs:
                if not hasattr(part, "start"):
                    continue
                offset = part.start * 512
                for tsk_type in tsk_types_to_try:
                    try:
                        kwargs = {"offset": offset}
                        if tsk_type is not None:
                            kwargs["fstype"] = tsk_type
                        self._fs = pytsk3.FS_Info(self._img, **kwargs)
                        return
                    except Exception as e:
                        errors.append(str(e))
        except Exception:
            pass

        raise RuntimeError(
            "Could not open the filesystem.\n"
            f"Detected type: {self.fs_type_hint}\n"
            "Last errors:\n" + "\n".join(errors[-3:])
        )

    def list_directory(self, path: str = "/") -> list:
        try:
            directory = self._fs.open_dir(path=path)
        except Exception as e:
            raise RuntimeError(f"Cannot open '{path}': {e}")

        entries = []
        for entry in directory:
            try:
                name = entry.info.name.name.decode("utf-8", errors="replace")
            except Exception:
                continue
            if not name or name in (".", ".."):
                continue

            is_dir = False
            size = 0
            modified = ""
            try:
                if entry.info.meta:
                    is_dir = (entry.info.meta.type ==
                              pytsk3.TSK_FS_META_TYPE_DIR)
                    size = entry.info.meta.size or 0
                    mtime = getattr(entry.info.meta, "mtime", None)
                    if mtime:
                        modified = datetime.datetime.fromtimestamp(mtime).strftime(
                            "%Y-%m-%d %H:%M")
            except Exception:
                pass

            entries.append({"name": name, "is_dir": is_dir,
                             "size": size, "modified": modified})
        return entries

    def read_file(self, path: str):
        try:
            f = self._fs.open(path=path)
        except Exception as e:
            raise RuntimeError(f"Cannot open '{path}': {e}")

        if f.info.meta and f.info.meta.type == pytsk3.TSK_FS_META_TYPE_DIR:
            return None

        size = (f.info.meta.size if f.info.meta else 0) or 0
        if size == 0:
            return b""
        return f.read_random(0, size)

    def get_info(self, path: str) -> dict:
        try:
            f = self._fs.open(path=path)
        except Exception as e:
            return {"Error": str(e)}

        info = {"Path": path, "Name": path.split("/")[-1]}
        try:
            meta = f.info.meta
            if meta:
                is_dir = meta.type == pytsk3.TSK_FS_META_TYPE_DIR
                info["Type"]     = "Directory" if is_dir else "File"
                info["Size"]     = _human_size(meta.size or 0)
                info["Inode"]    = meta.addr
                info["Mode"]     = oct(meta.mode)
                for attr, label in (("crtime", "Created"), ("mtime", "Modified"),
                                    ("atime", "Accessed")):
                    ts = getattr(meta, attr, None)
                    if ts:
                        info[label] = datetime.datetime.fromtimestamp(ts).strftime(
                            "%Y-%m-%d %H:%M:%S")
        except Exception as e:
            info["Warning"] = str(e)
        return info

    def drive_info(self) -> dict:
        fs_label = {
            FS_HFSPLUS: "HFS+ (Mac OS Extended)",
            FS_HFS:     "HFS (Mac OS Standard – Classic)",
            FS_EXFAT:   "exFAT",
            FS_FAT32:   "FAT32",
            FS_FAT16:   "FAT16",
        }.get(self.fs_type_hint, "Auto-detected")

        info = {"Source": self.path, "FS Type": fs_label}
        try:
            fs = self._fs
            info["Block Size"]  = f"{fs.info.block_size} bytes"
            info["Block Count"] = f"{fs.info.block_count:,}"
            total = fs.info.block_size * fs.info.block_count
            info["Total Size"]  = _human_size(total)
        except Exception as e:
            info["Warning"] = str(e)
        return info


# ═══════════════════════════════════════════════════════════════
#  APFS reader (uses the 'apfs' Python library)
# ═══════════════════════════════════════════════════════════════
class APFSReader:
    """
    Read APFS volumes using the pure-Python 'apfs' library.
    Falls back to pytsk3 APFS support if the library isn't available.
    """

    def __init__(self, path: str):
        self.path = path
        self._container = None
        self._volume    = None
        self._open()

    def _open(self):
        if APFS_LIB_AVAILABLE:
            try:
                with open(self.path, "rb") as fp:
                    self._container = apfslib.APFSContainer(fp)
                    if self._container.volumes:
                        self._volume = self._container.volumes[0]
                        return
            except Exception as e:
                pass   # fall through to TSK

        # Fallback: try pytsk3 with APFS type
        if TSK_AVAILABLE:
            apfs_type = getattr(pytsk3, "TSK_FS_TYPE_APFS", None)
            if apfs_type:
                try:
                    img = _ImgInfo(self.path)
                    # Try partition table first
                    try:
                        vs = pytsk3.VS_Info(img)
                        for part in vs:
                            if not hasattr(part, "start"):
                                continue
                            try:
                                self._tsk_fs = pytsk3.FS_Info(
                                    img, offset=part.start * 512,
                                    fstype=apfs_type)
                                self._use_tsk = True
                                return
                            except Exception:
                                pass
                    except Exception:
                        pass
                    # Try direct
                    self._tsk_fs = pytsk3.FS_Info(img, fstype=apfs_type)
                    self._use_tsk = True
                    return
                except Exception:
                    pass

        raise RuntimeError(
            "APFS support requires the 'apfs' Python package.\n"
            "Install it with:  pip install apfs\n\n"
            "Alternatively, newer versions of pytsk3 may support APFS.\n"
            "Ensure pytsk3 is up to date:  pip install --upgrade pytsk3"
        )

    # If using TSK fallback, delegate to TskReader methods
    def _tsk(self):
        if hasattr(self, "_use_tsk") and self._use_tsk:
            return True
        return False

    def list_directory(self, path: str = "/") -> list:
        if self._tsk():
            return _tsk_list_dir(self._tsk_fs, path)

        if self._volume is None:
            return []
        try:
            node = self._volume.get_by_path(path)
            entries = []
            for child in node.children:
                entries.append({
                    "name":     child.name,
                    "is_dir":   child.is_directory,
                    "size":     getattr(child, "size", 0) or 0,
                    "modified": _fmt_ts(getattr(child, "modified", None)),
                })
            return entries
        except Exception as e:
            raise RuntimeError(f"Cannot list '{path}': {e}")

    def read_file(self, path: str):
        if self._tsk():
            return _tsk_read_file(self._tsk_fs, path)

        if self._volume is None:
            raise RuntimeError("No APFS volume loaded.")
        try:
            node = self._volume.get_by_path(path)
            if node.is_directory:
                return None
            return node.read()
        except Exception as e:
            raise RuntimeError(f"Cannot read '{path}': {e}")

    def get_info(self, path: str) -> dict:
        if self._tsk():
            return _tsk_get_info(self._tsk_fs, path)

        info = {"Path": path, "Name": path.split("/")[-1]}
        try:
            node = self._volume.get_by_path(path)
            info["Type"]     = "Directory" if node.is_directory else "File"
            info["Size"]     = _human_size(getattr(node, "size", 0) or 0)
            info["Created"]  = _fmt_ts(getattr(node, "created", None))
            info["Modified"] = _fmt_ts(getattr(node, "modified", None))
        except Exception as e:
            info["Error"] = str(e)
        return info

    def drive_info(self) -> dict:
        info = {"Source": self.path, "FS Type": "APFS (Apple File System)"}
        if self._volume:
            try:
                info["Volume Name"] = getattr(self._volume, "name", "—")
                info["Volume Count"] = str(len(self._container.volumes))
                cap = getattr(self._container, "capacity", None)
                if cap:
                    info["Capacity"] = _human_size(cap)
            except Exception:
                pass
        return info


# ═══════════════════════════════════════════════════════════════
#  Factory — open any Mac drive/image automatically
# ═══════════════════════════════════════════════════════════════
class MacFSReader:
    """
    Unified entry point. Auto-detects the filesystem type and returns
    the appropriate reader. Use this instead of HFSReader directly.

    Usage:
        reader = MacFSReader.open(r"\\.\PHYSICALDRIVE1")
        reader = MacFSReader.open("backup.dmg")
    """

    @staticmethod
    def open(path: str):
        """Detect filesystem type and return the correct reader instance."""
        fs_type = probe_fs_type(path)

        if fs_type == FS_APFS:
            try:
                return APFSReader(path)
            except Exception as e:
                raise RuntimeError(
                    f"Detected APFS filesystem but failed to open it.\n{e}"
                )

        elif fs_type in (FS_HFSPLUS, FS_HFS):
            return TskReader(path, fs_type_hint=fs_type)

        elif fs_type in (FS_EXFAT, FS_FAT32, FS_FAT16):
            return TskReader(path, fs_type_hint=fs_type)

        else:
            # Unknown — try TSK auto-detect as last resort
            return TskReader(path, fs_type_hint=FS_UNKNOWN)

    @staticmethod
    def detect_type(path: str) -> str:
        """Return a human-readable description of the detected filesystem."""
        label = {
            FS_APFS:  "APFS (Apple File System)",
            FS_HFSPLUS: "HFS+ (Mac OS Extended)",
            FS_HFS:     "HFS (Mac OS Standard)",
            FS_EXFAT:   "exFAT",
            FS_FAT32:   "FAT32",
            FS_FAT16:   "FAT16",
            FS_UNKNOWN: "Unknown",
        }
        return label.get(probe_fs_type(path), "Unknown")


# ═══════════════════════════════════════════════════════════════
#  Backward-compatibility alias (so main.py import still works)
# ═══════════════════════════════════════════════════════════════
HFSReader = MacFSReader.open


# ═══════════════════════════════════════════════════════════════
#  Private TSK helpers (used by APFSReader TSK fallback path)
# ═══════════════════════════════════════════════════════════════
def _tsk_list_dir(fs, path):
    entries = []
    try:
        directory = fs.open_dir(path=path)
        for entry in directory:
            try:
                name = entry.info.name.name.decode("utf-8", errors="replace")
            except Exception:
                continue
            if not name or name in (".", ".."):
                continue
            is_dir = False
            size = 0
            modified = ""
            try:
                if entry.info.meta:
                    is_dir = entry.info.meta.type == pytsk3.TSK_FS_META_TYPE_DIR
                    size = entry.info.meta.size or 0
                    mtime = getattr(entry.info.meta, "mtime", None)
                    if mtime:
                        modified = datetime.datetime.fromtimestamp(mtime).strftime(
                            "%Y-%m-%d %H:%M")
            except Exception:
                pass
            entries.append({"name": name, "is_dir": is_dir,
                             "size": size, "modified": modified})
    except Exception as e:
        raise RuntimeError(str(e))
    return entries


def _tsk_read_file(fs, path):
    f = fs.open(path=path)
    if f.info.meta and f.info.meta.type == pytsk3.TSK_FS_META_TYPE_DIR:
        return None
    size = (f.info.meta.size if f.info.meta else 0) or 0
    return f.read_random(0, size) if size > 0 else b""


def _tsk_get_info(fs, path):
    info = {"Path": path, "Name": path.split("/")[-1]}
    try:
        f = fs.open(path=path)
        meta = f.info.meta
        if meta:
            is_dir = meta.type == pytsk3.TSK_FS_META_TYPE_DIR
            info["Type"] = "Directory" if is_dir else "File"
            info["Size"] = _human_size(meta.size or 0)
    except Exception as e:
        info["Error"] = str(e)
    return info


# ═══════════════════════════════════════════════════════════════
#  Utilities
# ═══════════════════════════════════════════════════════════════
def _human_size(n):
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if n < 1024:
            return f"{n:.1f} {unit}"
        n /= 1024
    return f"{n:.1f} PB"


def _fmt_ts(ts):
    if ts is None:
        return "—"
    try:
        if isinstance(ts, (int, float)):
            return datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(ts, datetime.datetime):
            return ts.strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        pass
    return str(ts)
