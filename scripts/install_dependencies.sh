#!/bin/bash
# Script Instalasi Dependencies untuk Azure VM
# Pengembang: Athallah Budiman Devia Putra (NIM: 23076039)

set -e  # Exit jika ada error

echo "=========================================="
echo "  Instalasi Dependencies - Brand Detection"
echo "=========================================="
echo ""

# Warna untuk output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Fungsi untuk print dengan warna
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

# Update sistem
print_info "Mengupdate sistem..."
sudo apt update -y
sudo apt upgrade -y
print_success "Sistem berhasil diupdate"

# Install Python 3 dan pip
print_info "Menginstal Python 3 dan pip..."
sudo apt install -y python3 python3-pip python3-venv
print_success "Python 3 dan pip terinstal"

# Verifikasi Python
PYTHON_VERSION=$(python3 --version)
print_info "Python version: $PYTHON_VERSION"

# Install ODBC Driver untuk SQL Server
print_info "Menginstal ODBC Driver untuk SQL Server..."
curl https://packages.microsoft.com/keys/microsoft.asc | sudo apt-key add -
curl https://packages.microsoft.com/config/ubuntu/22.04/prod.list | sudo tee /etc/apt/sources.list.d/mssql-release.list
sudo apt update
sudo ACCEPT_EULA=Y apt install -y msodbcsql18
sudo apt install -y unixodbc-dev
print_success "ODBC Driver terinstal"

# Install Nginx
print_info "Menginstal Nginx..."
sudo apt install -y nginx
print_success "Nginx terinstal"

# Verifikasi Nginx
NGINX_VERSION=$(nginx -v 2>&1)
print_info "Nginx version: $NGINX_VERSION"

# Install Git
print_info "Menginstal Git..."
sudo apt install -y git
print_success "Git terinstal"

# Install utilities
print_info "Menginstal utilities..."
sudo apt install -y htop curl wget unzip
print_success "Utilities terinstal"

# Setup firewall
print_info "Mengkonfigurasi firewall..."
sudo ufw allow 'Nginx Full'
sudo ufw allow OpenSSH
sudo ufw --force enable
print_success "Firewall dikonfigurasi"

# Verifikasi semua instalasi
echo ""
echo "=========================================="
echo "  Verifikasi Instalasi"
echo "=========================================="
python3 --version
pip3 --version
nginx -v
git --version
odbcinst -j

echo ""
print_success "Semua dependencies berhasil terinstal!"
echo ""
print_info "Next steps:"
echo "  1. Clone atau upload kode aplikasi"
echo "  2. Setup virtual environment"
echo "  3. Install Python packages"
echo "  4. Konfigurasi .env file"
echo ""
