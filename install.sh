#!/bin/bash

# --- Konfigurasi ---
REPO_URL="https://github.com/Sreetx/sxcc.git"
INSTALL_DIR="/opt/sxcc"
BIN_PATH="/usr/local/bin/sxcc"

echo "------------------------------------------"
echo "   SXCC Universal Installer for Linux     "
echo "------------------------------------------"

# 1. Minta akses sudo di awal
if [ "$EUID" -ne 0 ]; then
    echo "[*] This script requires root access for installation to /opt."
    echo "[*] Enter your sudo password: "
    exec sudo "$0" "$@"
fi

# 2. Cek OS
if [[ "$OSTYPE" != "linux-gnu"* ]]; then
    echo "Error: Your OS not Linux!"
    exit 1
fi

# 3. Cek & Install Git (Dependency awal)
if ! command -v git &> /dev/null; then
    echo "[*] Git not found, installing..."
    if command -v pacman &> /dev/null; then pacman -S --noconfirm git
    elif command -v apt-get &> /dev/null; then apt-get update && apt-get install -y git
    elif command -v dnf &> /dev/null; then dnf install -y git
    fi
fi

# 4. Proses Clone menggunakan folder sementara (/tmp)
TEMP_DIR=$(mktemp -d)
echo "[*] Downloading the project file to $TEMP_DIR..."

if git clone "$REPO_URL" "$TEMP_DIR"; then
    echo "[*] Installing to $INSTALL_DIR..."
    rm -rf "$INSTALL_DIR"
    mv "$TEMP_DIR" "$INSTALL_DIR"
else
    echo "Error: Clone repository fail!"
    rm -rf "$TEMP_DIR"
    exit 1
fi

# 5. Pasang Dependency Sistem (xcursorgen)
echo "[*] Checking system deps..."
if command -v pacman &> /dev/null; then
    pacman -S --needed --noconfirm xorg-xcursorgen python
elif command -v apt-get &> /dev/null; then
    apt-get update && apt-get install -y x11-apps python3
elif command -v dnf &> /dev/null; then
    dnf install -y xorg-x11-apps python3
fi

# 6. Setup Executable & Symlink
echo "[*] Configuration command access to 'sxcc'..."
chmod +x "$INSTALL_DIR/main.py"
ln -sf "$INSTALL_DIR/main.py" "$BIN_PATH"

echo "------------------------------------------"
echo "  BERHASIL! SXCC sudah terpasang.         "
echo "  Ketik 'sxcc' untuk mulai konversi.      "
echo "------------------------------------------"
