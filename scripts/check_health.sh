#!/bin/bash
# Script Health Check untuk Monitoring
# Pengembang: Athallah Budiman Devia Putra (NIM: 23076039)

echo "=========================================="
echo "  Health Check - Brand Detection"
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

# Check Systemd Service
print_info "Checking branddetection service..."
if sudo systemctl is-active --quiet branddetection; then
    print_success "Service is running"
    STATUS=$(sudo systemctl status branddetection --no-pager | grep "Active:" | awk '{print $2, $3}')
    echo "  Status: $STATUS"
else
    print_error "Service is NOT running!"
fi

# Check Nginx
print_info "Checking Nginx..."
if sudo systemctl is-active --quiet nginx; then
    print_success "Nginx is running"
else
    print_error "Nginx is NOT running!"
fi

# Check Port 5000 (Gunicorn)
print_info "Checking port 5000 (Gunicorn)..."
if netstat -tuln | grep -q ":5000"; then
    print_success "Port 5000 is listening"
else
    print_warning "Port 5000 is NOT listening"
fi

# Check Port 80 (Nginx)
print_info "Checking port 80 (Nginx)..."
if netstat -tuln | grep -q ":80"; then
    print_success "Port 80 is listening"
else
    print_warning "Port 80 is NOT listening"
fi

# Check Disk Space
print_info "Checking disk space..."
DISK_USAGE=$(df -h / | awk 'NR==2 {print $5}' | sed 's/%//')
if [ "$DISK_USAGE" -lt 80 ]; then
    print_success "Disk usage: ${DISK_USAGE}%"
else
    print_warning "Disk usage HIGH: ${DISK_USAGE}%"
fi

# Check Memory
print_info "Checking memory..."
MEMORY_USAGE=$(free | grep Mem | awk '{printf "%.0f", $3/$2 * 100.0}')
if [ "$MEMORY_USAGE" -lt 80 ]; then
    print_success "Memory usage: ${MEMORY_USAGE}%"
else
    print_warning "Memory usage HIGH: ${MEMORY_USAGE}%"
fi

# Check CPU Load
print_info "Checking CPU load..."
CPU_LOAD=$(uptime | awk -F'load average:' '{print $2}' | awk '{print $1}' | sed 's/,//')
echo "  Load average (1 min): $CPU_LOAD"

# Check Application Logs
print_info "Recent application logs (last 10 lines)..."
if [ -f "logs/app_$(date +%Y%m%d).log" ]; then
    echo "---"
    tail -n 10 "logs/app_$(date +%Y%m%d).log"
    echo "---"
else
    print_warning "Log file not found"
fi

# Check Nginx Error Logs
print_info "Recent Nginx errors (last 5 lines)..."
if [ -f "/var/log/nginx/branddetection_error.log" ]; then
    NGINX_ERRORS=$(sudo tail -n 5 /var/log/nginx/branddetection_error.log | wc -l)
    if [ "$NGINX_ERRORS" -gt 0 ]; then
        echo "---"
        sudo tail -n 5 /var/log/nginx/branddetection_error.log
        echo "---"
    else
        print_success "No recent errors"
    fi
fi

# HTTP Health Check
print_info "Testing HTTP endpoint..."
HTTP_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:5000/ 2>/dev/null || echo "failed")
if [ "$HTTP_RESPONSE" = "200" ]; then
    print_success "HTTP endpoint responding (200 OK)"
elif [ "$HTTP_RESPONSE" = "failed" ]; then
    print_error "Failed to connect to HTTP endpoint"
else
    print_warning "HTTP returned: $HTTP_RESPONSE"
fi

# Summary
echo ""
echo "=========================================="
echo "  Summary"
echo "=========================================="
echo "Timestamp: $(date '+%Y-%m-%d %H:%M:%S')"
echo "Uptime: $(uptime -p)"
echo ""

# Exit code berdasarkan health status
if sudo systemctl is-active --quiet branddetection && sudo systemctl is-active --quiet nginx; then
    print_success "Overall Status: HEALTHY"
    exit 0
else
    print_error "Overall Status: UNHEALTHY"
    exit 1
fi
