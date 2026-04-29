#!/bin/bash

SRC_FILE="main.py"
BIN_NAME="sxcc"

echo "--- SXCC Universal Installer ---"

# 1. Cek OS (Linux Only)
if [[ "$OSTYPE" != "linux-gnu"* ]]; then
    echo "Error: The OS is not Linux. This script requires a Linux environment."
    exit 1
fi

# 2. Fungsi deteksi dan install package
install_pkg() {
    local PKG_NAME=$1
    echo "Searching $PKG_NAME..."

    if ! command -v $PKG_NAME &> /dev/null; then
        echo "$PKG_NAME Not yet. Trying to install..."
        
        if command -v pacman &> /dev/null; then
            # Arch Linux / CachyOS / Manjaro
            sudo pacman -S --noconfirm $PKG_NAME
        elif command -v apt-get &> /dev/null; then
            # Debian / Ubuntu / Mint
            sudo apt-get update && sudo apt-get install -y $PKG_NAME
        elif command -v dnf &> /dev/null; then
            # Fedora / RHEL
            sudo dnf install -y $PKG_NAME
        elif command -v zypper &> /dev/null; then
            # openSUSE
            sudo zypper install -y $PKG_NAME
        else
            echo "Failed: Package manager not supported. Please install $PKG_NAME manually!"
            exit 1
        fi
    else
        echo "$PKG_NAME Installed."
    fi
}

# 3. Eksekusi Install Dependency
# Python3 biasanya nama paketnya 'python' atau 'python3'
install_pkg "python3"

# xcursorgen biasanya ada di paket xorg-xcursorgen atau x11-apps tergantung distro
echo "Installing xcursorgen..."
if command -v pacman &> /dev/null; then
    sudo pacman -S --noconfirm xorg-xcursorgen
elif command -v apt-get &> /dev/null; then
    sudo apt-get install -y x11-apps
elif command -v dnf &> /dev/null; then
    sudo dnf install -y xorg-x11-apps
fi

# 4. Finalisasi script sxcc
if [ -f "$SRC_FILE" ]; then
    chmod +x "$SRC_FILE"
    sudo cp "$SRC_FILE" "/usr/local/bin/$BIN_NAME"
    echo "------------------------------------------------"
    echo "BERHASIL! sxcc siap digunakan."
    echo "------------------------------------------------"
else
    echo "Error: File $SRC_FILE tidak ditemukan!"
    exit 1
fi
