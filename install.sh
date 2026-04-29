#!/bin/bash

# --- Konfigurasi Sreetx YouTube Downloader ---
NAMA_COMMAND="sxcc"
INSTALL_PATH="/opt/$NAMA_COMMAND"
REPO_URL="https://github.com/Sreetx/sxcc.git" # Pastikan URL ini bener
SCRIPT_UTAMA="main.py"

# --- Kode Warna (Rich Ala Terminal) ---
HIJAU='\033[0;32m'
BIRU='\033[0;34m'
BORANGE='\033[38;5;208m'
MERAH='\033[0;31m'
NORMAL='\033[0m'

echo -e "${BIRU}========================================${NORMAL}"
echo -e "${HIJAU} SXCC - Sreetx Cross Cursors Converter!    ${NORMAL}"
echo -e "${BIRU}========================================${NORMAL}"

# 1. DETEKSI OS (Pintu Keluar buat Windows/Android)
if [[ "$OSTYPE" != "linux-gnu"* ]]; then
    echo -e "${BORANGE} [!] OS Bukan Linux (Windows/Android detected) ${NORMAL}"
    echo -e " [#] Hanya akan melakukan cloning repository..."
    
    if [ -d "$NAMA_COMMAND" ]; then
        echo " Folder sudah ada, melakukan update..."
        cd "$NAMA_COMMAND" && git pull
    else
        git clone "$REPO_URL" "$NAMA_COMMAND"
    fi
    
    echo -e "${HIJAU} [#] Selesai! ${NORMAL}"
    echo -e " [>] Silakan ketik: ${BIRU}cd $NAMA_COMMAND && python $SCRIPT_UTAMA${NORMAL}"
    exit 0
fi

# 2. LOGIKA MULTI-DISTRO (Linux Only)
install_dependencies() {
    if command -v pacman &> /dev/null; then
        echo -e "[#] Arch Linux detected. Installing via pacman..."
        sudo pacman -S --noconfirm python python-pip git
    elif command -v apt &> /dev/null; then
        echo -e "[#] Debian/Ubuntu detected. Installing via apt..."
        sudo apt update
        sudo apt install -y python3 python3-pip git
    elif command -v dnf &> /dev/null; then
        echo -e "[#] Fedora detected. Installing via dnf..."
        sudo dnf install -y python3 python3-pip git
    fi
}

# Jalankan instalasi dependensi sistem
echo -e "${BIRU} [#] Checking system dependencies... ${NORMAL}"
install_dependencies

# 3. CLONE/UPDATE REPO KE /OPT
echo -e "${BIRU} [#] Setting up system-wide installation... ${NORMAL}"
if [ -d "/tmp/sxcc-build" ]; then
    sudo rm -rf /tmp/sxcc-build
fi

git clone "$REPO_URL" /tmp/sxcc-build
sudo mkdir -p "$INSTALL_PATH"
sudo cp -r /tmp/sxcc-build/* "$INSTALL_PATH/"

# 4. BIKIN COMMAND DI /BIN (WRAPPER)
echo -e "${BIRU} [#] Creating global command 'sxcc'... ${NORMAL}"
cat <<EOF | sudo tee /usr/bin/$NAMA_COMMAND > /dev/null
python3 $INSTALL_PATH/$SCRIPT_UTAMA "\$@"
#!/bin/bash
# Menjalankan tools dari folder /opt agar aset tetap terbaca
EOF

sudo chmod +x /usr/bin/$NAMA_COMMAND

# 5. JALANKAN INSTALLER PYTHON (Inside the App)
echo -e "${BIRU} [#] Installing Python libraries... ${NORMAL}"
# Memanggil script python kamu yang punya logika --break-system-packages

# 6. FINISHING
echo -e "${HIJAU} ======================================= ${NORMAL}"
echo -e "${HIJAU}    INSTALLASI BERHASIL! (Success)       ${NORMAL}"
echo -e "${HIJAU} ======================================= ${NORMAL}"
echo -e " [>] Sekarang kamu bisa ketik: ${BIRU}sxcc${NORMAL} di terminal."
echo -e " [>] Enjoy downloading with SXCC! "

# Hapus sisa build
sudo rm -rf /tmp/sytd-build
