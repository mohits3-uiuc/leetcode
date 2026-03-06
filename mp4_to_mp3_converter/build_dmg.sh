#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

APP_NAME="MP4 to MP3 Converter"
ENTRY_SCRIPT="mp4_to_mp3.py"
DIST_DIR="dist"
BUILD_DIR="build"
STAGING_DIR="$DIST_DIR/dmg_staging"
DMG_NAME="MP4-to-MP3-Converter-macOS.dmg"

if [[ -n "${PYTHON_BIN:-}" ]]; then
  PYTHON="$PYTHON_BIN"
elif [[ -n "${VIRTUAL_ENV:-}" && -x "${VIRTUAL_ENV}/bin/python" ]]; then
  PYTHON="${VIRTUAL_ENV}/bin/python"
elif [[ -x "${SCRIPT_DIR}/../.venv/bin/python" ]]; then
  PYTHON="${SCRIPT_DIR}/../.venv/bin/python"
else
  PYTHON="$(command -v python3)"
fi

export MACOSX_DEPLOYMENT_TARGET="${MACOSX_DEPLOYMENT_TARGET:-11.0}"

if [[ ! -f "$ENTRY_SCRIPT" ]]; then
  echo "Error: Could not find $ENTRY_SCRIPT in $SCRIPT_DIR"
  exit 1
fi

if ! command -v hdiutil >/dev/null 2>&1; then
  echo "Error: hdiutil not found. This script must run on macOS."
  exit 1
fi

if ! "$PYTHON" -m PyInstaller --version >/dev/null 2>&1; then
  echo "PyInstaller not found. Installing..."
  "$PYTHON" -m pip install --upgrade pip pyinstaller
fi

echo "Cleaning previous artifacts..."
rm -rf "$BUILD_DIR" "$DIST_DIR" "$APP_NAME.spec"

echo "Building macOS app bundle..."
"$PYTHON" -m PyInstaller \
  --noconfirm \
  --clean \
  --windowed \
  --name "$APP_NAME" \
  "$ENTRY_SCRIPT"

APP_PATH="$DIST_DIR/$APP_NAME.app"
if [[ ! -d "$APP_PATH" ]]; then
  echo "Error: App bundle was not generated at $APP_PATH"
  exit 1
fi

echo "Preparing DMG layout..."
mkdir -p "$STAGING_DIR"
cp -R "$APP_PATH" "$STAGING_DIR/"
ln -s /Applications "$STAGING_DIR/Applications"

echo "Creating DMG..."
hdiutil create \
  -volname "$APP_NAME Installer" \
  -srcfolder "$STAGING_DIR" \
  -ov \
  -format UDZO \
  "$DIST_DIR/$DMG_NAME"

rm -rf "$STAGING_DIR"

echo "Done. DMG created at: $DIST_DIR/$DMG_NAME"