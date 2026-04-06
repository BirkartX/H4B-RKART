#!/bin/bash
# ================================================
# BIRKARTX v2.4 - Ultra Pentest Suite
# Asan işə salma skripti (Linux / Kali / Termux)
# ================================================

echo -e "\033[92m"
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║               BIRKARTX v2.4 - ULTRA EDITION                  ║"
echo "║               Powered SQLi Data Dumper                       ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "\033[0m"

echo "[+] Sistem yoxlanılır..."

# Python3 quraşdırılıb mı?
if ! command -v python3 &> /dev/null; then
    echo "[!] python3 tapılmadı. python ilə cəhd edilir..."
    PYTHON_CMD="python"
else
    PYTHON_CMD="python3"
fi

# Lazımi Python paketləri
echo "[+] Lazımi paketlər quraşdırılır..."
$PYTHON_CMD -m pip install --quiet --upgrade pip
$PYTHON_CMD -m pip install --quiet customtkinter requests beautifulsoup4 dnspython websocket-client pyjwt cryptography

echo "[+] Paketlər hazırdır."
echo "[+] BIRKARTX işə salınır... (Bu bir az vaxt ala bilər)"

# Əsas proqramı işə sal
$PYTHON_CMD birkartx.py

# Əgər xəta verərsə ikinci cəhd
if [ $? -ne 0 ]; then
    echo "[!] Birinci cəhd uğursuz oldu. Yenidən cəhd edilir..."
    python birkartx.py
fi

echo -e "\n\033[92mBIRKARTX bağlandı. Sağ olun!\033[0m"