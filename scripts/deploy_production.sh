#!/bin/bash
# Script Deployment Production dengan Systemd & Nginx
# Pengembang: Athallah Budiman Devia Putra (NIM: 23076039)

set -e

echo "=========================================="
echo "  Deployment Production - Brand Detection"
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

# Dapatkan current user dan directory
CURRENT_USER=$(whoami)
PROJECT_DIR=$(pwd)

print_info "User: $CURRENT_USER"
print_info "Project directory: $PROJECT_DIR"

# Cek apakah di folder yang benar
if [ ! -f "$PROJECT_DIR/app.py" ]; then
    print_error "File app.py tidak ditemukan di $PROJECT_DIR"
    exit 1
fi

# Cek apakah virtual environment ada
if [ ! -d "$PROJECT_DIR/venv" ]; then
    print_error "Virtual environment tidak ditemukan!"
    print_error "Jalankan setup_app.sh terlebih dahulu"
    exit 1
fi

print_success "Project directory valid"

# Setup Systemd Service
print_info "Membuat systemd service file..."

sudo tee /etc/systemd/system/branddetection.service > /dev/null <<EOF
[Unit]
Description=Brand Detection Flask Application
After=network.target

[Service]
Type=simple
User=$CURRENT_USER
WorkingDirectory=$PROJECT_DIR
Environment="PATH=$PROJECT_DIR/venv/bin"
ExecStart=$PROJECT_DIR/venv/bin/gunicorn --workers 3 --bind 0.0.0.0:5000 --timeout 300 --access-logfile $PROJECT_DIR/logs/access.log --error-logfile $PROJECT_DIR/logs/error.log app:app
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

print_success "Systemd service file dibuat"

# Reload systemd
print_info "Reload systemd daemon..."
sudo systemctl daemon-reload
print_success "Systemd daemon reloaded"

# Enable service
print_info "Enable branddetection service..."
sudo systemctl enable branddetection
print_success "Service enabled (auto-start on boot)"

# Start service
print_info "Starting branddetection service..."
sudo systemctl start branddetection
sleep 2
print_success "Service started"

# Check status
print_info "Checking service status..."
if sudo systemctl is-active --quiet branddetection; then
    print_success "Service is running!"
else
    print_error "Service failed to start!"
    print_info "Check logs with: journalctl -u branddetection -n 50"
    exit 1
fi

# Get VM IP (public IP dari Azure metadata service atau local IP)
VM_IP=$(curl -H Metadata:true --noproxy "*" "http://169.254.169.254/metadata/instance/network/interface/0/ipv4/ipAddress/0/publicIpAddress?api-version=2021-02-01&format=text" 2>/dev/null || hostname -I | awk '{print $1}')

print_info "VM IP Address: $VM_IP"

# Setup Nginx
print_info "Konfigurasi Nginx..."

sudo tee /etc/nginx/sites-available/branddetection > /dev/null <<EOF
server {
    listen 80;
    server_name $VM_IP;

    client_max_body_size 20M;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        
        # Timeout untuk upload gambar besar
        proxy_connect_timeout 300;
        proxy_send_timeout 300;
        proxy_read_timeout 300;
        send_timeout 300;
    }

    # Static files
    location /static {
        alias $PROJECT_DIR/static;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # Logs
    access_log /var/log/nginx/branddetection_access.log;
    error_log /var/log/nginx/branddetection_error.log;
}
EOF

print_success "Nginx config file dibuat"

# Enable site
print_info "Enable Nginx site..."
sudo ln -sf /etc/nginx/sites-available/branddetection /etc/nginx/sites-enabled/

# Remove default site
if [ -f "/etc/nginx/sites-enabled/default" ]; then
    sudo rm /etc/nginx/sites-enabled/default
    print_success "Default site removed"
fi

# Test Nginx config
print_info "Testing Nginx configuration..."
if sudo nginx -t; then
    print_success "Nginx configuration is valid"
else
    print_error "Nginx configuration error!"
    exit 1
fi

# Restart Nginx
print_info "Restarting Nginx..."
sudo systemctl restart nginx
print_success "Nginx restarted"

# Check Nginx status
if sudo systemctl is-active --quiet nginx; then
    print_success "Nginx is running!"
else
    print_error "Nginx failed to start!"
    exit 1
fi

echo ""
echo "=========================================="
echo "  Deployment Berhasil!"
echo "=========================================="
echo ""
print_success "Aplikasi Brand Detection sudah running di production mode"
echo ""
print_info "Akses aplikasi di:"
echo "  http://$VM_IP"
echo ""
print_info "Management commands:"
echo "  • Status service:    sudo systemctl status branddetection"
echo "  • Restart service:   sudo systemctl restart branddetection"
echo "  • Stop service:      sudo systemctl stop branddetection"
echo "  • View logs:         journalctl -u branddetection -f"
echo "  • Nginx logs:        sudo tail -f /var/log/nginx/branddetection_access.log"
echo ""
print_info "Pengembang:"
echo "  Nama: Athallah Budiman Devia Putra"
echo "  NIM:  23076039"
echo "  Prodi: Pendidikan Teknik Informatika"
echo ""
