# -*- mode: python ; coding: utf-8 -*-
# ──────────────────────────────────────────────────────────────────────
#  Mac Drive Reader – PyInstaller spec (single-file, windowed)
#  Build with:  pyinstaller MacDriveReader.spec
# ──────────────────────────────────────────────────────────────────────
import sys
from PyInstaller.utils.hooks import collect_all, collect_submodules

# Collect all files from apfs and construct (they use dynamic imports)
apfs_datas,      apfs_bins,      apfs_hiddens      = collect_all('apfs')
construct_datas, construct_bins, construct_hiddens  = collect_all('construct')

a = Analysis(
    ['main.py'],
    pathex=['.'],
    binaries=apfs_bins + construct_bins,
    datas=[
        ('assets',         'assets'),
        ('mac_fs_reader.py', '.'),
        ('hfs_reader.py',    '.'),
    ] + apfs_datas + construct_datas,
    hiddenimports=[
        # pytsk3 – The Sleuth Kit bindings
        'pytsk3',
        # apfs pure-Python parser
        'apfs',
        # construct – binary parser used by apfs
        'construct',
        'construct.lib',
        'construct.core',
        # tkinter & ttk (sometimes missed on Windows)
        'tkinter',
        'tkinter.ttk',
        'tkinter.filedialog',
        'tkinter.messagebox',
        # standard library extras
        'threading',
        'pathlib',
        'shutil',
        'struct',
        'datetime',
    ] + apfs_hiddens + construct_hiddens
      + collect_submodules('apfs')
      + collect_submodules('construct'),
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['matplotlib', 'numpy', 'pandas', 'scipy', 'PIL',
              'IPython', 'jupyter', 'pyspark'],
    noarchive=False,
)

pyz = PYZ(a.pure)

# ── Single-file EXE ───────────────────────────────────────────────────
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='MacDriveReader',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,           # compress with UPX if available (smaller file)
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,      # windowed – no console window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets\\icon.ico',
    version='version_info.txt',  # optional – see build.bat
)
