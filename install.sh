#!/bin/bash
# AetherVault Installation Script for Linux
# Copyright (c) 2024 - MIT License

set -e

echo "AetherVault - Installation Script"
echo "=================================="
echo ""

# Check Python version
echo "[1/4] Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Install with: sudo apt install python3 python3-pip"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "Found Python $PYTHON_VERSION"

# Check Python version meets minimum requirement
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d'.' -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d'.' -f2)

if [ "$PYTHON_MAJOR" -lt 3 ] || { [ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 9 ]; }; then
    echo "WARNING: Python 3.9 or higher is recommended"
    echo "Current version: $PYTHON_VERSION"
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Install dependencies
echo ""
echo "[2/4] Installing Python dependencies..."
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi
echo "Dependencies installed successfully"

# Get absolute path
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
AETHER_PATH="$SCRIPT_DIR/aether_vault.py"

# Create desktop entry
echo ""
echo "[3/4] Creating desktop entry..."
mkdir -p ~/.local/share/applications

cat > ~/.local/share/applications/aether-vault.desktop << EOF
[Desktop Entry]
Type=Application
Name=Aether Vault
Comment=Secure File Encryption & Steganography
Exec=python3 "$AETHER_PATH" %F
Icon=security-high
Terminal=false
Categories=Utility;Security;Encryption;
MimeType=application/octet-stream;image/png;
EOF

echo "Desktop entry created"

# Update desktop database
echo ""
echo "[4/4] Updating desktop database..."
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database ~/.local/share/applications/ 2>/dev/null || true
    echo "Desktop database updated"
else
    echo "Note: update-desktop-database not found, skipping"
fi

# Make script executable
chmod +x "$AETHER_PATH"

# Success message
echo ""
echo "=================================="
echo "Installation completed successfully"
echo "=================================="
echo ""
echo "Usage:"
echo "  GUI Mode:  python3 aether_vault.py"
echo "  CLI Mode:  python3 aether_vault.py <file>"
echo ""
echo "For right-click integration:"
echo "  Right-click any file"
echo "  Select 'Open With' > 'Aether Vault'"
echo ""
