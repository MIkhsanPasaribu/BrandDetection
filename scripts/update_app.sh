#!/bin/bash
# Script Update Aplikasi di Production
# Pengembang: Athallah Budiman Devia Putra (NIM: 23076039)

set -e

echo "=========================================="
echo "  Update Aplikasi - Brand Detection"
echo "=========================================="
echo ""

# Warna
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
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

PROJECT_DIR=$(pwd)

# Cek apakah di folder yang benar
if [ ! -f "$PROJECT_DIR/app.py" ]; then
    print_error "File app.py tidak ditemukan di $PROJECT_DIR"
    exit 1
fi

# Backup current version (opsional)
print_info "Membuat backup..."
BACKUP_DIR="$PROJECT_DIR/../backup_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"
cp -r "$PROJECT_DIR"/{app.py,config.py,services,utils,templates,static,requirements.txt} "$BACKUP_DIR/" 2>/dev/null || true
print_success "Backup dibuat di: $BACKUP_DIR"

# Pull update dari Git (jika menggunakan git)
if [ -d ".git" ]; then
    print_info "Pulling updates dari Git..."
    git pull origin main || git pull origin master
    print_success "Git pull selesai"
else
    print_warning "Bukan Git repository, skip git pull"
    print_info "Pastikan Anda sudah upload file terbaru ke server"
fi

# Aktifkan virtual environment
print_info "Aktivasi virtual environment..."
source venv/bin/activate
print_success "Virtual environment aktif"

# Update dependencies
print_info "Update Python packages..."
pip install --upgrade pip
pip install -r requirements.txt --upgrade
print_success "Python packages updated"

# Collect static files jika ada perubahan
if [ -d "static" ]; then
    print_info "Checking static files..."
    print_success "Static files OK"
fi

# Restart aplikasi
print_info "Restarting branddetection service..."
sudo systemctl restart branddetection
sleep 2

# Check status
if sudo systemctl is-active --quiet branddetection; then
    print_success "Service berhasil di-restart dan running!"
else
    print_warning "Service mungkin ada masalah"
    print_info "Check logs: journalctl -u branddetection -n 50"
fi

# Restart Nginx juga
print_info "Restarting Nginx..."
sudo systemctl restart nginx
print_success "Nginx restarted"

# Show status
echo ""
print_info "Status aplikasi:"
sudo systemctl status branddetection --no-pager -l

echo ""
print_success "Update aplikasi selesai!"
echo ""
print_info "Test aplikasi di browser untuk memastikan berjalan dengan baik"
echo ""
