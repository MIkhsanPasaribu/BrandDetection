# ✅ Deployment Checklist - Brand Detection

Checklist lengkap untuk deployment aplikasi Brand Detection ke Azure.

**Pengembang:** Athallah Budiman Devia Putra (NIM: 23076039)

---

## 📋 Pre-Deployment Checklist

### 1. Azure Account & Subscription

- [ ] Akun Azure aktif (Free Trial atau Student account)
- [ ] Credit tersedia ($200 free credit atau Azure for Students)
- [ ] Akses ke Azure Portal ([portal.azure.com](https://portal.azure.com))
- [ ] Verifikasi kartu kredit/debit selesai
- [ ] Subscription aktif

### 2. Development Environment

- [ ] Kode aplikasi sudah lengkap dan tested
- [ ] Pyright type checking passed (0 errors)
- [ ] File `.env.example` tersedia
- [ ] File `requirements.txt` up to date
- [ ] Dokumentasi lengkap
- [ ] Git repository ready (opsional tapi recommended)

### 3. Local Testing

- [ ] Aplikasi berjalan di local (`python app.py`)
- [ ] Upload gambar berfungsi
- [ ] Database connection tested
- [ ] Azure Computer Vision API tested
- [ ] Semua halaman loading dengan benar
- [ ] Responsive design verified di berbagai device

---

## 🔷 Phase 1: Azure Resources Setup

### Azure Computer Vision

- [ ] **Buat Resource**

  - [ ] Login ke Azure Portal
  - [ ] Create new resource → Search "Computer Vision"
  - [ ] Resource Group: `BrandDetection-RG` (buat baru)
  - [ ] Region: Southeast Asia atau East US
  - [ ] Name: `branddetection-vision`
  - [ ] Pricing tier: Free F0 atau Standard S1

- [ ] **Dapatkan Credentials**

  - [ ] Buka resource → Keys and Endpoint
  - [ ] Copy KEY 1
  - [ ] Copy Endpoint URL
  - [ ] Simpan di tempat aman

- [ ] **Test API**
  - [ ] Test dengan Quick Test di portal, ATAU
  - [ ] Test dengan Python script local

**Endpoint format:**

```
https://branddetection-vision.cognitiveservices.azure.com/
```

---

### Azure SQL Database

- [ ] **Buat SQL Database**

  - [ ] Create resource → Search "SQL Database"
  - [ ] Resource Group: `BrandDetection-RG` (sama dengan CV)
  - [ ] Database name: `BrandDetectionDB`

- [ ] **Buat SQL Server**

  - [ ] Server name: `branddetection-sql-server` (harus unik)
  - [ ] Region: Sama dengan Computer Vision
  - [ ] Authentication: SQL authentication
  - [ ] Admin login: `sqladmin`
  - [ ] Password: [Strong password - simpan!]

- [ ] **Konfigurasi Database**

  - [ ] Compute + Storage: Basic (5 DTU) atau Serverless
  - [ ] Networking: Public endpoint
  - [ ] Firewall rules: Allow Azure services ✅

- [ ] **Konfigurasi Firewall**

  - [ ] Add current client IP address
  - [ ] Add rule: Azure services (0.0.0.0)
  - [ ] Save firewall rules

- [ ] **Buat Tabel**

  - [ ] Buka Query Editor di portal
  - [ ] Login dengan sqladmin
  - [ ] Run query CREATE TABLE (lihat PANDUAN_SETUP_AZURE.md)
  - [ ] Verifikasi tabel berhasil dibuat

- [ ] **Dapatkan Connection String**

  - [ ] Buka Connection strings
  - [ ] Copy ODBC connection string
  - [ ] Replace `{your_password}` dengan password asli
  - [ ] Simpan di tempat aman

- [ ] **Test Connection**
  - [ ] Test dengan Azure Data Studio, ATAU
  - [ ] Test dengan Python script local

**Connection string format:**

```
Driver={ODBC Driver 18 for SQL Server};Server=tcp:branddetection-sql-server.database.windows.net,1433;Database=BrandDetectionDB;Uid=sqladmin;Pwd=YourPassword;Encrypt=yes;TrustServerCertificate=no;
```

---

### Azure Virtual Machine

- [ ] **Buat Virtual Machine**

  - [ ] Create resource → Search "Virtual Machine"
  - [ ] Resource Group: `BrandDetection-RG`
  - [ ] VM name: `branddetection-vm`
  - [ ] Region: Sama dengan resources lain
  - [ ] Image: Ubuntu Server 22.04 LTS
  - [ ] Size: B1s (dev) atau B2s (production)

- [ ] **Authentication**

  - [ ] Authentication type: SSH public key
  - [ ] Username: `azureuser`
  - [ ] SSH key: Generate new key pair
  - [ ] Key pair name: `branddetection-vm_key`

- [ ] **Networking**

  - [ ] Public IP: Yes (auto-create)
  - [ ] Inbound ports: SSH (22), HTTP (80), HTTPS (443)

- [ ] **Management**

  - [ ] Boot diagnostics: Enable
  - [ ] Auto-shutdown: Enable (untuk hemat biaya)
  - [ ] Shutdown time: 19:00 atau sesuai kebutuhan

- [ ] **Deployment**

  - [ ] Review + Create
  - [ ] Download private key (`.pem` file) → SIMPAN DENGAN AMAN!
  - [ ] Wait for deployment (3-5 menit)

- [ ] **Dapatkan IP Address**
  - [ ] Copy Public IP address dari resource
  - [ ] Simpan IP untuk akses SSH dan HTTP

**IP Address VM:**

```
13.229.XXX.XXX  (contoh)
```

---

## 💻 Phase 2: VM Configuration

### SSH ke VM

- [ ] **Koneksi SSH**
  - [ ] Windows: Move `.pem` ke `~/.ssh/` dan set permission
  - [ ] Linux/Mac: `chmod 400 ~/.ssh/branddetection-vm_key.pem`
  - [ ] Test SSH: `ssh -i ~/.ssh/branddetection-vm_key.pem azureuser@VM_IP`
  - [ ] Berhasil masuk ke VM

### Install Dependencies

- [ ] **Opsi A: Menggunakan Script (Recommended)**

  - [ ] Upload `install_dependencies.sh` ke VM
  - [ ] `chmod +x install_dependencies.sh`
  - [ ] `./install_dependencies.sh`
  - [ ] Verifikasi semua terinstall

- [ ] **Opsi B: Manual**

  - [ ] `sudo apt update && sudo apt upgrade -y`
  - [ ] Install Python 3 + pip
  - [ ] Install ODBC Driver 18
  - [ ] Install Nginx
  - [ ] Install Git
  - [ ] Setup firewall (ufw)

- [ ] **Verifikasi**
  - [ ] `python3 --version` → 3.10+
  - [ ] `pip3 --version` → 20+
  - [ ] `nginx -v` → 1.18+
  - [ ] `odbcinst -j` → ODBC Driver 18 for SQL Server

---

## 📦 Phase 3: Application Deployment

### Upload Kode

- [ ] **Pilih Metode Upload**

  - [ ] **Opsi A: Git Clone**
    - [ ] `git clone https://github.com/your-repo/BrandDetection.git`
  - [ ] **Opsi B: SCP Upload**
    - [ ] Compress project di local
    - [ ] `scp` ke VM
    - [ ] Extract di VM

- [ ] **Verifikasi**
  - [ ] `cd /home/azureuser/BrandDetection`
  - [ ] `ls` → ada file `app.py`, `config.py`, dll
  - [ ] File lengkap

### Setup Application

- [ ] **Opsi A: Menggunakan Script (Recommended)**

  - [ ] `chmod +x scripts/setup_app.sh`
  - [ ] `./scripts/setup_app.sh`
  - [ ] Verifikasi output: virtual environment created, packages installed

- [ ] **Opsi B: Manual**

  - [ ] `python3 -m venv venv`
  - [ ] `source venv/bin/activate`
  - [ ] `pip install -r requirements.txt`
  - [ ] `mkdir -p uploads logs`

- [ ] **Konfigurasi .env**

  - [ ] `cp .env.example .env` (jika setup script belum jalankan)
  - [ ] `nano .env`
  - [ ] Paste credentials Azure:
    - [ ] COMPUTER_VISION_ENDPOINT
    - [ ] COMPUTER_VISION_KEY
    - [ ] SQL_SERVER
    - [ ] SQL_DATABASE
    - [ ] SQL_USERNAME
    - [ ] SQL_PASSWORD
    - [ ] SECRET_KEY (generate random)
  - [ ] Save (Ctrl+O, Enter, Ctrl+X)
  - [ ] `chmod 600 .env`

- [ ] **Test Aplikasi**
  - [ ] `source venv/bin/activate`
  - [ ] `python app.py`
  - [ ] Check output: "Running on http://0.0.0.0:5000"
  - [ ] Test di browser: `http://VM_IP:5000`
  - [ ] Ctrl+C untuk stop

---

## 🚀 Phase 4: Production Deployment

### Systemd Service Setup

- [ ] **Opsi A: Menggunakan Script (Recommended)**

  - [ ] `chmod +x scripts/deploy_production.sh`
  - [ ] `./scripts/deploy_production.sh`
  - [ ] Verifikasi output: Service running, Nginx running

- [ ] **Opsi B: Manual**

  - [ ] Buat file `/etc/systemd/system/branddetection.service`
  - [ ] Copy konfigurasi dari PANDUAN_SETUP_AZURE.md
  - [ ] `sudo systemctl daemon-reload`
  - [ ] `sudo systemctl enable branddetection`
  - [ ] `sudo systemctl start branddetection`

- [ ] **Verifikasi Service**
  - [ ] `sudo systemctl status branddetection`
  - [ ] Status: Active (running)
  - [ ] No errors in logs

### Nginx Setup

- [ ] **Konfigurasi Nginx**

  - [ ] File: `/etc/nginx/sites-available/branddetection`
  - [ ] Copy konfigurasi dari PANDUAN_SETUP_AZURE.md
  - [ ] Ganti `server_name` dengan IP VM
  - [ ] Set `client_max_body_size 20M;`

- [ ] **Enable Site**

  - [ ] `sudo ln -s /etc/nginx/sites-available/branddetection /etc/nginx/sites-enabled/`
  - [ ] `sudo rm /etc/nginx/sites-enabled/default`
  - [ ] `sudo nginx -t` → "test is successful"
  - [ ] `sudo systemctl restart nginx`

- [ ] **Verifikasi Nginx**
  - [ ] `sudo systemctl status nginx`
  - [ ] Status: Active (running)

---

## ✅ Phase 5: Testing & Verification

### Functional Testing

- [ ] **Akses Aplikasi**

  - [ ] Buka browser: `http://VM_IP`
  - [ ] Halaman beranda loading ✅
  - [ ] Header menampilkan identitas mahasiswa ✅
  - [ ] Footer menampilkan identitas mahasiswa ✅

- [ ] **Test Upload & Deteksi**

  - [ ] Klik "Upload Gambar"
  - [ ] Pilih gambar dengan brand terkenal (Coca-Cola, Nike, dll)
  - [ ] Upload berhasil
  - [ ] Deteksi berjalan (loading indicator)
  - [ ] Hasil deteksi ditampilkan:
    - [ ] Nama brand
    - [ ] Confidence score
    - [ ] Gambar preview

- [ ] **Test Database**

  - [ ] Klik menu "Riwayat Deteksi"
  - [ ] Data hasil deteksi muncul di tabel
  - [ ] Informasi lengkap: nama file, brand, confidence, waktu

- [ ] **Test Statistik**

  - [ ] Klik menu "Statistik"
  - [ ] Data statistik ditampilkan:
    - [ ] Total deteksi
    - [ ] Total brand unik
    - [ ] Rata-rata confidence
    - [ ] Top brands

- [ ] **Test Halaman Tim**

  - [ ] Klik menu "Tim Pengembang"
  - [ ] Informasi pengembang ditampilkan lengkap

- [ ] **Test Responsive Design**
  - [ ] Resize browser window
  - [ ] Layout adjust untuk mobile/tablet
  - [ ] Test di device mobile jika memungkinkan

### Performance Testing

- [ ] **Upload Multiple Images**

  - [ ] Upload 5-10 gambar berbeda
  - [ ] Semua berhasil diproses
  - [ ] Tidak ada timeout

- [ ] **Load Testing (Opsional)**
  - [ ] Buka 3-5 browser tabs berbeda
  - [ ] Akses aplikasi bersamaan
  - [ ] Aplikasi tetap responsive

### Monitoring

- [ ] **Check Health**

  - [ ] `./scripts/check_health.sh`
  - [ ] Overall status: HEALTHY
  - [ ] Service running
  - [ ] Nginx running
  - [ ] Ports listening (5000, 80)

- [ ] **Check Logs**
  - [ ] `journalctl -u branddetection -n 50` → No critical errors
  - [ ] `sudo tail -f /var/log/nginx/branddetection_error.log` → No errors
  - [ ] `tail -f logs/app_$(date +%Y%m%d).log` → Logs tertulis

---

## 🔒 Phase 6: Security & Optimization

### Security

- [ ] **File Permissions**

  - [ ] `.env` permission: 600 (read/write owner only)
  - [ ] `.pem` key permission: 400 (read owner only)
  - [ ] `uploads/` folder: 755

- [ ] **Firewall**

  - [ ] `sudo ufw status` → Active
  - [ ] Allowed: SSH (22), HTTP (80), HTTPS (443), Nginx Full
  - [ ] Denied: semua port lain

- [ ] **Azure SQL Firewall**

  - [ ] Only VM IP dan development IP allowed
  - [ ] Test akses dari IP lain → Should be blocked

- [ ] **Environment Variables**
  - [ ] `.env` tidak di-commit ke Git
  - [ ] `.gitignore` includes `.env`
  - [ ] Credentials tidak hardcoded di kode

### Optimization (Opsional)

- [ ] **Gunicorn Workers**

  - [ ] Adjust workers based on CPU: `(2 x CPU) + 1`
  - [ ] Edit service file jika perlu

- [ ] **Nginx Caching**

  - [ ] Static files caching configured
  - [ ] `expires 30d` untuk CSS/JS/images

- [ ] **Auto-shutdown**
  - [ ] VM auto-shutdown enabled untuk hemat biaya
  - [ ] Waktu shutdown sesuai kebutuhan

---

## 📊 Phase 7: Documentation & Handoff

### Documentation Complete

- [ ] **README.md** up to date dengan deployment info
- [ ] **PANDUAN_SETUP_AZURE.md** lengkap
- [ ] **scripts/README.md** dokumentasi scripts lengkap
- [ ] **SETUP.md** instalasi local documented
- [ ] **STRUKTUR_PROYEK.md** struktur explained
- [ ] **RINGKASAN_PENGEMBANGAN.md** development summary

### Deployment Info

- [ ] **Catat informasi penting:**
  - [ ] VM Public IP: `_____________________`
  - [ ] VM Username: `azureuser`
  - [ ] SQL Server: `branddetection-sql-server.database.windows.net`
  - [ ] Database: `BrandDetectionDB`
  - [ ] Computer Vision endpoint: `_____________________`
  - [ ] Resource Group: `BrandDetection-RG`
  - [ ] Region: `_____________________`

### Access Info

- [ ] **URL Aplikasi:** `http://VM_IP`
- [ ] **SSH Command:** `ssh -i ~/.ssh/branddetection-vm_key.pem azureuser@VM_IP`
- [ ] **Azure Portal:** `https://portal.azure.com`

---

## 🎉 Final Verification

### Checklist Summary

- [ ] ✅ Azure Computer Vision: Running & tested
- [ ] ✅ Azure SQL Database: Connected & working
- [ ] ✅ Azure VM: Running & accessible
- [ ] ✅ Application: Deployed & functional
- [ ] ✅ Systemd Service: Running automatically
- [ ] ✅ Nginx: Reverse proxy working
- [ ] ✅ Upload: Functional & saving to database
- [ ] ✅ Detection: Working with Computer Vision API
- [ ] ✅ History: Displaying data from database
- [ ] ✅ Statistics: Calculating & displaying correctly
- [ ] ✅ Team Page: Showing developer info
- [ ] ✅ Responsive Design: Working on all devices
- [ ] ✅ Logs: Writing & accessible
- [ ] ✅ Security: Firewall, permissions, credentials secured
- [ ] ✅ Documentation: Complete & accurate

### Production Readiness

- [ ] Application accessible via HTTP
- [ ] All features working as expected
- [ ] No critical errors in logs
- [ ] Database connection stable
- [ ] API calls successful
- [ ] Performance acceptable
- [ ] Ready for demonstration

---

## 📝 Post-Deployment Tasks

### Ongoing Maintenance

- [ ] **Daily Health Checks**

  - [ ] Run `./scripts/check_health.sh`
  - [ ] Check error logs

- [ ] **Weekly Updates**

  - [ ] `sudo apt update && sudo apt upgrade`
  - [ ] Check Azure credits/costs

- [ ] **Monthly Review**
  - [ ] Review logs for patterns
  - [ ] Optimize queries if needed
  - [ ] Clean up old uploads

### Cost Management

- [ ] **Monitor Costs**

  - [ ] Azure Portal → Cost Management
  - [ ] Set budget alerts
  - [ ] Track spending

- [ ] **Optimize Usage**
  - [ ] Stop VM when not in use
  - [ ] Use auto-shutdown feature
  - [ ] Consider serverless SQL for dev/test

---

## 🎓 Demonstration Preparation

### Demo Checklist

- [ ] VM running dan accessible
- [ ] Prepare test images (5-10 brand logos)
- [ ] Test upload process sebelum demo
- [ ] Prepare slides/presentation (jika perlu)
- [ ] Note key points:
  - [ ] Architecture overview
  - [ ] Azure services used
  - [ ] Features implemented
  - [ ] Challenges & solutions
  - [ ] Future improvements

### Backup Plan

- [ ] Screenshot aplikasi running
- [ ] Record video demo (backup)
- [ ] Export database data (sample)
- [ ] Save example detection results

---

## ✨ Congratulations!

Jika semua checklist di atas sudah ✅, maka:

🎉 **Aplikasi Brand Detection Anda sudah berhasil di-deploy ke Azure!**

### Next Steps (Opsional):

1. 🌐 Setup custom domain
2. 🔒 Install SSL certificate (Let's Encrypt)
3. 📈 Setup Azure Application Insights untuk monitoring
4. 🔄 Setup CI/CD dengan GitHub Actions
5. 🧪 Implement automated testing
6. 📊 Enhanced analytics dashboard

---

**Pengembang:** Athallah Budiman Devia Putra  
**NIM:** 23076039  
**Prodi:** Pendidikan Teknik Informatika

**© 2025 - Brand Detection System - Cloud Computing Project**
