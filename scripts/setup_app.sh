#!/bin/bash
# Script Setup Aplikasi Flask
# Pengembang: Athallah Budiman Devia Putra (NIM: 23076039)

set -e

echo "=========================================="
echo "  Setup Aplikasi - Brand Detection"
echo "=========================================="
echo ""

# Warna
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

# Cek apakah di folder yang benar
if [ ! -f "app.py" ]; then
    print_error "File app.py tidak ditemukan!"
    print_error "Pastikan Anda berada di folder root project"
    exit 1
fi

print_success "Berada di folder project yang benar"

# Buat virtual environment
print_info "Membuat virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    print_success "Virtual environment dibuat"
else
    print_warning "Virtual environment sudah ada"
fi

# Aktifkan virtual environment
print_info "Mengaktifkan virtual environment..."
source venv/bin/activate
print_success "Virtual environment aktif"

# Upgrade pip
print_info "Mengupgrade pip..."
pip install --upgrade pip
print_success "Pip diupgrade"

# Install dependencies
print_info "Menginstal Python packages dari requirements.txt..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    print_success "Python packages terinstal"
else
    print_error "File requirements.txt tidak ditemukan!"
    exit 1
fi

# Buat folder yang diperlukan
print_info "Membuat folder yang diperlukan..."
mkdir -p uploads
mkdir -p logs
mkdir -p static/images
print_success "Folder dibuat"

# Set permission
chmod 755 uploads
chmod 755 logs

# Cek file .env
if [ ! -f ".env" ]; then
    print_warning ".env file tidak ditemukan!"
    
    if [ -f ".env.example" ]; then
        print_info "Menyalin .env.example ke .env..."
        cp .env.example .env
        chmod 600 .env
        print_warning "File .env dibuat dari template"
        print_warning "PENTING: Edit file .env dan isi dengan kredensial Azure Anda!"
        echo ""
        print_info "Edit dengan: nano .env"
        echo ""
    else
        print_error ".env.example juga tidak ditemukan!"
        print_info "Buat file .env secara manual dengan kredensial Azure"
    fi
else
    print_success "File .env sudah ada"
    chmod 600 .env
fi

# Test import modules
print_info "Testing import modules..."
python3 -c "import flask; import azure.cognitiveservices.vision.computervision; import pyodbc; print('✓ All modules OK')" && print_success "Semua modules berhasil diimport"

echo ""
print_success "Setup aplikasi selesai!"
echo ""
print_info "Next steps:"
echo "  1. Edit file .env dengan kredensial Azure:"
echo "     nano .env"
echo "  2. Test aplikasi:"
echo "     python app.py"
echo "  3. Akses di browser: http://localhost:5000"
echo ""
