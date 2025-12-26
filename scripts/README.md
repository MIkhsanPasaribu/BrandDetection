# 🚀 Scripts Deployment - Brand Detection

Kumpulan script bash untuk otomasi deployment dan maintenance aplikasi Brand Detection di Azure VM.

**Pengembang:** Athallah Budiman Devia Putra  
**NIM:** 23076039  
**Prodi:** Pendidikan Teknik Informatika

---

## 📋 Daftar Scripts

| Script                    | Deskripsi                                                    | Kapan Digunakan                 |
| ------------------------- | ------------------------------------------------------------ | ------------------------------- |
| `install_dependencies.sh` | Install semua dependencies sistem (Python, Nginx, ODBC, dll) | Pertama kali setup VM baru      |
| `setup_app.sh`            | Setup virtual environment dan install Python packages        | Setelah upload/clone kode ke VM |
| `deploy_production.sh`    | Deploy aplikasi dengan Systemd + Nginx                       | Deployment pertama kali         |
| `update_app.sh`           | Update aplikasi yang sudah running                           | Setiap ada perubahan kode       |
| `check_health.sh`         | Health check dan monitoring status aplikasi                  | Monitoring rutin                |

---

## 🎯 Alur Deployment Lengkap

### Step 1: Setup VM Baru

```bash
# SSH ke VM
ssh -i ~/.ssh/branddetection-vm_key.pem azureuser@YOUR_VM_IP

# Download dan jalankan script install dependencies
cd /home/azureuser
curl -O https://raw.githubusercontent.com/your-repo/BrandDetection/main/scripts/install_dependencies.sh
chmod +x install_dependencies.sh
./install_dependencies.sh
```

**Output yang diharapkan:**

- ✓ Python 3.x terinstall
- ✓ Nginx terinstall
- ✓ ODBC Driver terinstall
- ✓ Git terinstall
- ✓ Firewall dikonfigurasi

### Step 2: Upload Kode Aplikasi

**Opsi A: Menggunakan Git (Recommended)**

```bash
cd /home/azureuser
git clone https://github.com/your-username/BrandDetection.git
cd BrandDetection
```

**Opsi B: Menggunakan SCP dari komputer lokal**

```powershell
# Windows PowerShell
# Compress folder
Compress-Archive -Path "C:\Users\mikhs\OneDrive\Documents\BrandDetection\*" -DestinationPath "$env:TEMP\branddetection.zip"

# Upload
scp -i "$env:USERPROFILE\.ssh\branddetection-vm_key.pem" "$env:TEMP\branddetection.zip" azureuser@YOUR_VM_IP:/home/azureuser/

# Di VM, extract
ssh -i "$env:USERPROFILE\.ssh\branddetection-vm_key.pem" azureuser@YOUR_VM_IP
cd /home/azureuser
unzip branddetection.zip -d BrandDetection
cd BrandDetection
```

### Step 3: Setup Aplikasi

```bash
# Jalankan script setup
chmod +x scripts/*.sh
./scripts/setup_app.sh
```

**Output yang diharapkan:**

- ✓ Virtual environment dibuat
- ✓ Python packages terinstall
- ✓ Folder uploads/ dan logs/ dibuat
- ✓ File .env dibuat dari template

**PENTING:** Edit file `.env` dengan kredensial Azure Anda:

```bash
nano .env
```

Isi dengan:

```env
COMPUTER_VISION_ENDPOINT=https://your-resource.cognitiveservices.azure.com/
COMPUTER_VISION_KEY=your_actual_key_here
SQL_SERVER=your-server.database.windows.net
SQL_DATABASE=BrandDetectionDB
SQL_USERNAME=sqladmin
SQL_PASSWORD=your_password_here
SECRET_KEY=generate_random_key_here
```

### Step 4: Test Aplikasi (Opsional)

```bash
# Aktifkan virtual environment
source venv/bin/activate

# Test run
python app.py

# Jika berhasil, akan muncul:
# * Running on http://0.0.0.0:5000

# Test di browser: http://YOUR_VM_IP:5000

# Tekan Ctrl+C untuk stop
```

### Step 5: Deploy ke Production

```bash
# Jalankan script deployment
./scripts/deploy_production.sh
```

**Output yang diharapkan:**

- ✓ Systemd service dibuat dan running
- ✓ Nginx dikonfigurasi dan running
- ✓ Aplikasi accessible via HTTP

**Akses aplikasi:** `http://YOUR_VM_IP`

---

## 🔄 Update Aplikasi

Ketika ada perubahan kode dan ingin update aplikasi yang sudah running:

```bash
# SSH ke VM
ssh -i ~/.ssh/branddetection-vm_key.pem azureuser@YOUR_VM_IP

# Masuk ke folder project
cd /home/azureuser/BrandDetection

# Jika menggunakan Git
git pull origin main

# Atau upload file baru via SCP

# Jalankan script update
./scripts/update_app.sh
```

Script ini akan:

1. ✓ Backup versi sekarang
2. ✓ Pull update dari Git (jika ada)
3. ✓ Update Python packages
4. ✓ Restart service
5. ✓ Verify status

---

## 🔍 Monitoring & Troubleshooting

### Health Check

```bash
# Jalankan health check
./scripts/check_health.sh
```

Output akan menampilkan:

- Status service (branddetection & nginx)
- Status port (5000 & 80)
- Disk usage
- Memory usage
- CPU load
- Recent logs
- HTTP endpoint test

### Manual Checks

#### Check Service Status

```bash
# Status branddetection service
sudo systemctl status branddetection

# Status nginx
sudo systemctl status nginx
```

#### View Logs

```bash
# Application logs (live)
journalctl -u branddetection -f

# Application logs (last 100 lines)
journalctl -u branddetection -n 100 --no-pager

# Nginx access logs
sudo tail -f /var/log/nginx/branddetection_access.log

# Nginx error logs
sudo tail -f /var/log/nginx/branddetection_error.log

# Application file logs
tail -f logs/app_$(date +%Y%m%d).log
```

#### Restart Services

```bash
# Restart aplikasi
sudo systemctl restart branddetection

# Restart Nginx
sudo systemctl restart nginx

# Restart both
sudo systemctl restart branddetection nginx
```

#### Check Network

```bash
# Check port 5000 (Gunicorn)
netstat -tuln | grep :5000

# Check port 80 (Nginx)
netstat -tuln | grep :80

# Check firewall
sudo ufw status

# Test HTTP endpoint
curl -I http://localhost:5000
curl -I http://localhost
```

---

## 🛠️ Common Issues & Solutions

### Issue 1: Service Failed to Start

**Gejala:**

```
● branddetection.service - Brand Detection Flask Application
   Loaded: loaded (/etc/systemd/system/branddetection.service; enabled)
   Active: failed (Result: exit-code)
```

**Solusi:**

```bash
# Check detailed error
journalctl -u branddetection -n 50

# Common causes:
# 1. Virtual environment path salah
# 2. File .env tidak ada atau salah
# 3. Dependencies tidak terinstall
# 4. Port 5000 sudah dipakai

# Fix dan restart
sudo systemctl restart branddetection
```

### Issue 2: Nginx 502 Bad Gateway

**Gejala:**
Browser menampilkan "502 Bad Gateway"

**Solusi:**

```bash
# Check apakah Gunicorn running
sudo systemctl status branddetection

# Check port 5000
netstat -tuln | grep :5000

# Jika tidak running, restart
sudo systemctl restart branddetection

# Check Nginx error log
sudo tail -f /var/log/nginx/branddetection_error.log
```

### Issue 3: Database Connection Error

**Gejala:**
Error log menampilkan "Failed to connect to database"

**Solusi:**

```bash
# Check .env file
cat .env

# Verify kredensial benar
# Test connection manually
source venv/bin/activate
python3 -c "from services.database import DatabaseService; db = DatabaseService(); print('Connected!' if db.inisialisasi_database() else 'Failed')"

# Check Azure SQL firewall rules
# - Pastikan IP VM sudah diizinkan
# - Atau enable "Allow Azure services"
```

### Issue 4: Upload Gambar Gagal

**Gejala:**
Error saat upload: "413 Request Entity Too Large"

**Solusi:**

```bash
# Edit Nginx config
sudo nano /etc/nginx/sites-available/branddetection

# Pastikan ada baris:
# client_max_body_size 20M;

# Restart Nginx
sudo systemctl restart nginx
```

### Issue 5: Permission Denied pada uploads/

**Gejala:**
Error: "[Errno 13] Permission denied: 'uploads/image.jpg'"

**Solusi:**

```bash
# Set permission folder uploads
chmod 755 uploads/
chown azureuser:azureuser uploads/

# Verify
ls -la uploads/
```

---

## 📊 Cron Jobs untuk Maintenance

### Auto Health Check (Setiap 30 menit)

```bash
# Edit crontab
crontab -e

# Tambahkan:
*/30 * * * * /home/azureuser/BrandDetection/scripts/check_health.sh >> /home/azureuser/BrandDetection/logs/health_check.log 2>&1
```

### Log Rotation

```bash
# Buat file logrotate config
sudo nano /etc/logrotate.d/branddetection

# Isi:
/home/azureuser/BrandDetection/logs/*.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
}

/var/log/nginx/branddetection_*.log {
    daily
    rotate 14
    compress
    delaycompress
    missingok
    notifempty
    sharedscripts
    postrotate
        [ -f /var/run/nginx.pid ] && kill -USR1 `cat /var/run/nginx.pid`
    endscript
}
```

### Database Backup (Setiap hari jam 2 pagi)

```bash
# Edit crontab
crontab -e

# Tambahkan:
0 2 * * * /home/azureuser/BrandDetection/scripts/backup_database.sh
```

---

## 🔐 Security Checklist

- [ ] File `.env` permission 600 (hanya owner yang bisa read)
- [ ] Private key `.pem` permission 400
- [ ] Folder `uploads/` tidak di-commit ke Git
- [ ] `SECRET_KEY` di-generate random dan strong
- [ ] Azure SQL firewall hanya allow IP VM dan development
- [ ] UFW firewall enabled dan configured
- [ ] Nginx configured dengan proper headers
- [ ] SSL/TLS certificate installed (untuk production)
- [ ] Regular security updates: `sudo apt update && sudo apt upgrade`

---

## 📈 Performance Tuning

### Gunicorn Workers

Default: 3 workers

Untuk adjust berdasarkan CPU:

```bash
# Formula: (2 x CPU cores) + 1
# Check CPU cores
nproc

# Edit service file
sudo nano /etc/systemd/system/branddetection.service

# Ubah --workers sesuai kebutuhan:
# --workers 5  (untuk 2 CPU cores)

# Reload dan restart
sudo systemctl daemon-reload
sudo systemctl restart branddetection
```

### Nginx Caching (Opsional)

```nginx
# Edit Nginx config
sudo nano /etc/nginx/sites-available/branddetection

# Tambahkan caching untuk static files:
location /static {
    alias /home/azureuser/BrandDetection/static;
    expires 30d;
    add_header Cache-Control "public, immutable";
    access_log off;
}
```

---

## 📞 Support

Jika ada masalah yang tidak bisa diselesaikan dengan panduan ini:

1. **Check Logs** - Selalu mulai dengan melihat logs
2. **Health Check** - Jalankan `check_health.sh`
3. **Dokumentasi** - Baca `PANDUAN_SETUP_AZURE.md`
4. **GitHub Issues** - Buat issue di repository

---

## 📚 Referensi Script

### install_dependencies.sh

- Update sistem
- Install Python 3 + pip
- Install ODBC Driver untuk SQL Server
- Install Nginx
- Install Git & utilities
- Konfigurasi firewall

### setup_app.sh

- Buat virtual environment
- Install Python packages
- Buat folder uploads/ dan logs/
- Setup file .env

### deploy_production.sh

- Buat systemd service
- Enable dan start service
- Konfigurasi Nginx
- Setup reverse proxy

### update_app.sh

- Backup versi sekarang
- Pull update dari Git
- Update dependencies
- Restart service

### check_health.sh

- Check service status
- Check port listening
- Check disk & memory
- Check logs
- HTTP endpoint test

---

**© 2025 - Brand Detection System**  
**Cloud Computing Project - Athallah Budiman Devia Putra (23076039)**
