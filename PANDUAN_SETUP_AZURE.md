# 🔷 Panduan Lengkap Setup Azure untuk Brand Detection

## 📋 Daftar Isi

1. [Persiapan Akun Azure](#1-persiapan-akun-azure)
2. [Setup Azure Computer Vision](#2-setup-azure-computer-vision)
3. [Setup Azure SQL Database](#3-setup-azure-sql-database)
4. [Setup Azure Virtual Machine](#4-setup-azure-virtual-machine)
5. [Deployment Aplikasi ke VM](#5-deployment-aplikasi-ke-vm)
6. [Konfigurasi Domain & SSL (Opsional)](#6-konfigurasi-domain--ssl-opsional)
7. [Monitoring & Maintenance](#7-monitoring--maintenance)

---

## 1. Persiapan Akun Azure

### 1.1 Buat Akun Azure

1. Kunjungi [https://azure.microsoft.com/](https://azure.microsoft.com/)
2. Klik **"Start Free"** atau **"Try Azure for Free"**
3. Login dengan Microsoft Account atau buat akun baru
4. Isi informasi yang diperlukan:
   - Informasi pribadi
   - Nomor telepon (untuk verifikasi)
   - Kartu kredit/debit (untuk verifikasi, tidak akan dicharge untuk free tier)

### 1.2 Aktivasi Free Credits

Azure memberikan:

- **$200 kredit** untuk 30 hari pertama
- **12 bulan gratis** untuk layanan populer
- **Always free** untuk beberapa layanan

### 1.3 Verifikasi Akun

1. Cek email untuk verifikasi
2. Verifikasi nomor telepon dengan kode SMS
3. Verifikasi kartu kredit/debit

### 1.4 Akses Azure Portal

1. Buka [https://portal.azure.com/](https://portal.azure.com/)
2. Login dengan akun Azure Anda
3. Anda akan melihat **Dashboard Azure Portal**

---

## 2. Setup Azure Computer Vision

### 2.1 Buat Resource Computer Vision

#### Langkah-langkah:

1. **Login ke Azure Portal**

   - Buka [https://portal.azure.com/](https://portal.azure.com/)

2. **Create Resource**

   - Klik tombol **"+ Create a resource"** di kiri atas
   - Atau klik **"Create"** di dashboard

3. **Cari Computer Vision**

   - Di search bar, ketik: **"Computer Vision"**
   - Pilih **"Computer Vision"** dari hasil pencarian
   - Klik **"Create"**

4. **Konfigurasi Basic**

   **Subscription:**

   - Pilih subscription Anda (biasanya "Azure for Students" atau "Free Trial")

   **Resource Group:**

   - Klik **"Create new"**
   - Nama: `BrandDetection-RG`
   - Klik **"OK"**

   **Region:**

   - Pilih region terdekat, contoh:
     - `Southeast Asia` (Singapore)
     - `East Asia` (Hong Kong)
     - `East US` atau `West US`

   **Name:**

   - Nama unik untuk resource: `branddetection-vision`
   - Atau: `branddetection-cv-[nama-anda]`

   **Pricing Tier:**

   - Pilih **"Free F0"** (20 calls per minute, 5K calls per month)
   - Atau **"Standard S1"** jika butuh lebih (10 calls per second)

5. **Review + Create**
   - Klik **"Review + create"**
   - Tunggu validasi selesai
   - Klik **"Create"**
   - Tunggu deployment selesai (1-2 menit)

### 2.2 Dapatkan Keys dan Endpoint

1. **Buka Resource**

   - Setelah deployment selesai, klik **"Go to resource"**
   - Atau dari Home, cari resource `branddetection-vision`

2. **Keys and Endpoint**

   - Di menu sebelah kiri, klik **"Keys and Endpoint"**
   - Anda akan melihat:
     - **KEY 1** (Primary key)
     - **KEY 2** (Secondary key)
     - **Endpoint**

3. **Salin Informasi**

   **Endpoint:**

   ```
   https://branddetection-vision.cognitiveservices.azure.com/
   ```

   **Key:**

   ```
   abc123def456ghi789jkl012mno345pqr678stu901vwx
   ```

4. **Simpan ke File .env**

   Edit file `.env` di project:

   ```env
   COMPUTER_VISION_ENDPOINT=https://branddetection-vision.cognitiveservices.azure.com/
   COMPUTER_VISION_KEY=abc123def456ghi789jkl012mno345pqr678stu901vwx
   ```

### 2.3 Test Computer Vision API

#### Menggunakan Azure Portal (Quick Test):

1. Di resource Computer Vision, klik **"Quick test"** atau **"Try it"**
2. Upload gambar contoh yang mengandung logo brand terkenal
3. Lihat hasil deteksi di panel sebelah kanan

#### Menggunakan Python (Local Test):

```python
# test_computer_vision.py
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials

endpoint = "https://branddetection-vision.cognitiveservices.azure.com/"
key = "your-key-here"

client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(key))

# Test dengan gambar URL atau local file
with open('test_image.jpg', 'rb') as image:
    result = client.analyze_image_in_stream(image, visual_features=['brands'])

    if result.brands:
        for brand in result.brands:
            print(f"Brand: {brand.name}, Confidence: {brand.confidence}")
    else:
        print("No brands detected")
```

---

## 3. Setup Azure SQL Database

### 3.1 Buat SQL Database

#### Langkah-langkah:

1. **Create Resource**

   - Di Azure Portal, klik **"+ Create a resource"**
   - Cari: **"SQL Database"**
   - Klik **"Create"**

2. **Konfigurasi Basics**

   **Subscription:**

   - Pilih subscription Anda

   **Resource Group:**

   - Pilih: `BrandDetection-RG` (yang sudah dibuat sebelumnya)

   **Database Name:**

   - Nama: `BrandDetectionDB`

   **Server:**

   - Klik **"Create new"**

   **Server Configuration:**

   - **Server name:** `branddetection-sql-server` (harus unik secara global)
   - **Location:** Sama dengan Computer Vision (misal: Southeast Asia)
   - **Authentication method:** Pilih **"Use SQL authentication"**
   - **Server admin login:** `sqladmin`
   - **Password:** Buat password kuat (minimal 8 karakter, huruf besar, kecil, angka, simbol)
   - **Confirm password:** Ulangi password
   - Klik **"OK"**

   **Want to use SQL elastic pool:**

   - Pilih **"No"**

   **Compute + storage:**

   - Klik **"Configure database"**
   - Pilih **"Basic"** (untuk development/testing)
     - 5 DTUs
     - 2 GB storage
     - Biaya: ~$5/bulan
   - Atau pilih **"Serverless"** (pay-per-use, lebih hemat)
     - Min: 0.5 vCores
     - Max: 1 vCore
     - Auto-pause: 1 hour
   - Klik **"Apply"**

3. **Networking**

   **Connectivity method:**

   - Pilih **"Public endpoint"**

   **Firewall rules:**

   - ✅ **Allow Azure services and resources to access this server**
   - ✅ **Add current client IP address** (untuk akses dari komputer Anda)

   **Connection policy:**

   - Default

4. **Additional settings**

   **Data source:**

   - Pilih **"None"** (blank database)

   **Database collation:**

   - Default: `SQL_Latin1_General_CP1_CI_AS`

   **Enable Advanced Data Security:**

   - Pilih **"Not now"** (untuk development)

5. **Review + Create**
   - Klik **"Review + create"**
   - Klik **"Create"**
   - Tunggu deployment (3-5 menit)

### 3.2 Konfigurasi Firewall

1. **Buka SQL Server Resource**

   - Dari Home, cari `branddetection-sql-server`
   - Atau dari Database, klik nama server

2. **Firewall Settings**
   - Di menu kiri, klik **"Networking"** atau **"Firewalls and virtual networks"**
3. **Add Firewall Rules**

   **Untuk Development (IP Komputer Anda):**

   - Klik **"+ Add client IP"**
   - Nama rule: `MyComputer`
   - IP akan otomatis terdeteksi

   **Untuk Azure VM (nanti):**

   - Klik **"+ Add firewall rule"**
   - Nama: `AzureVM`
   - Start IP: `0.0.0.0`
   - End IP: `0.0.0.0`
   - (Atau IP spesifik VM setelah dibuat)

   **Allow Azure Services:**

   - Toggle **"Allow Azure services and resources to access this server"** = **ON**

4. **Save**
   - Klik **"Save"** di bagian atas

### 3.3 Buat Tabel Database

#### Menggunakan Query Editor di Azure Portal:

1. **Buka Database**

   - Klik database `BrandDetectionDB`

2. **Query Editor**

   - Di menu kiri, klik **"Query editor (preview)"**
   - Login dengan:
     - **Authentication type:** SQL authentication
     - **Login:** `sqladmin`
     - **Password:** (password yang Anda buat)
   - Klik **"OK"**

3. **Jalankan Query**

   Paste dan jalankan query berikut:

   ```sql
   -- Buat tabel BrandDetection
   CREATE TABLE BrandDetection (
       id INT IDENTITY(1,1) PRIMARY KEY,
       image_name NVARCHAR(255) NOT NULL,
       brand_name NVARCHAR(100),
       confidence_score FLOAT,
       upload_timestamp DATETIME DEFAULT GETDATE(),
       image_path NVARCHAR(500),
       resolution NVARCHAR(50),
       position_type NVARCHAR(50),
       notes NVARCHAR(MAX)
   );

   -- Buat index untuk performa
   CREATE INDEX idx_brand_name ON BrandDetection(brand_name);
   CREATE INDEX idx_upload_timestamp ON BrandDetection(upload_timestamp DESC);

   -- Verifikasi tabel sudah dibuat
   SELECT TABLE_NAME
   FROM INFORMATION_SCHEMA.TABLES
   WHERE TABLE_TYPE = 'BASE TABLE';
   ```

4. **Verifikasi**
   - Jika berhasil, Anda akan melihat message: "Query succeeded"
   - Hasilnya akan menampilkan: `BrandDetection`

### 3.4 Dapatkan Connection String

1. **Connection Strings**

   - Di menu database, klik **"Connection strings"**

2. **Copy Connection String**

   **ADO.NET:**

   ```
   Server=tcp:branddetection-sql-server.database.windows.net,1433;
   Initial Catalog=BrandDetectionDB;
   Persist Security Info=False;
   User ID=sqladmin;
   Password={your_password};
   MultipleActiveResultSets=False;
   Encrypt=True;
   TrustServerCertificate=False;
   Connection Timeout=30;
   ```

   **ODBC (untuk Python pyodbc):**

   ```
   Driver={ODBC Driver 18 for SQL Server};
   Server=tcp:branddetection-sql-server.database.windows.net,1433;
   Database=BrandDetectionDB;
   Uid=sqladmin;
   Pwd={your_password};
   Encrypt=yes;
   TrustServerCertificate=no;
   Connection Timeout=30;
   ```

3. **Simpan ke .env**

   ```env
   SQL_SERVER=branddetection-sql-server.database.windows.net
   SQL_DATABASE=BrandDetectionDB
   SQL_USERNAME=sqladmin
   SQL_PASSWORD=your_password_here
   ```

### 3.5 Test Connection

#### Menggunakan Azure Data Studio (Recommended):

1. Download [Azure Data Studio](https://docs.microsoft.com/sql/azure-data-studio/download)
2. Install dan buka aplikasi
3. Klik **"New Connection"**
4. Isi:
   - **Connection type:** Microsoft SQL Server
   - **Server:** `branddetection-sql-server.database.windows.net`
   - **Authentication type:** SQL Login
   - **User name:** `sqladmin`
   - **Password:** (password Anda)
   - **Database:** `BrandDetectionDB`
   - **Encrypt:** True
5. Klik **"Connect"**

#### Menggunakan Python (Local Test):

```python
# test_database.py
import pyodbc

server = 'branddetection-sql-server.database.windows.net'
database = 'BrandDetectionDB'
username = 'sqladmin'
password = 'your_password'

connection_string = f'''
    Driver={{ODBC Driver 18 for SQL Server}};
    Server=tcp:{server},1433;
    Database={database};
    Uid={username};
    Pwd={password};
    Encrypt=yes;
    TrustServerCertificate=no;
'''

try:
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()

    # Test query
    cursor.execute("SELECT @@VERSION")
    row = cursor.fetchone()
    print("✅ Database connection successful!")
    print(f"SQL Server version: {row[0]}")

    # Test tabel
    cursor.execute("SELECT COUNT(*) FROM BrandDetection")
    count = cursor.fetchone()[0]
    print(f"Total records in BrandDetection: {count}")

    conn.close()
except Exception as e:
    print(f"❌ Error: {e}")
```

---

## 4. Setup Azure Virtual Machine

### 4.1 Buat Virtual Machine

#### Langkah-langkah:

1. **Create Resource**

   - Di Azure Portal, klik **"+ Create a resource"**
   - Cari: **"Virtual Machine"**
   - Klik **"Create"**

2. **Konfigurasi Basics**

   **Subscription & Resource Group:**

   - **Subscription:** Pilih subscription Anda
   - **Resource group:** `BrandDetection-RG`

   **Instance Details:**

   - **Virtual machine name:** `branddetection-vm`
   - **Region:** Sama dengan resources lain (misal: Southeast Asia)
   - **Availability options:** No infrastructure redundancy required
   - **Security type:** Standard
   - **Image:** **Ubuntu Server 22.04 LTS - Gen2**
   - **Size:**
     - Klik **"See all sizes"**
     - Pilih **"B1s"** (1 vCPU, 1 GB RAM) untuk development
     - Atau **"B2s"** (2 vCPU, 4 GB RAM) untuk production
     - Estimated cost: $8-30/month

   **Administrator Account:**

   - **Authentication type:** SSH public key (Recommended)
   - **Username:** `azureuser`
   - **SSH public key source:** Generate new key pair
   - **Key pair name:** `branddetection-vm_key`

   **Inbound Port Rules:**

   - **Public inbound ports:** Allow selected ports
   - **Select inbound ports:**
     - ✅ SSH (22)
     - ✅ HTTP (80)
     - ✅ HTTPS (443)

3. **Disks**

   **OS Disk:**

   - **OS disk type:** Standard SSD (untuk hemat biaya)
   - **Delete with VM:** ✅ Yes

   **Data Disks:**

   - Tidak perlu (untuk aplikasi kecil)

4. **Networking**

   **Virtual network:**

   - Akan dibuat otomatis: `BrandDetection-RG-vnet`

   **Subnet:**

   - Default

   **Public IP:**

   - Akan dibuat otomatis: `branddetection-vm-ip`

   **NIC network security group:**

   - Basic

   **Public inbound ports:**

   - Allow selected ports: SSH, HTTP, HTTPS

   **Accelerated networking:**

   - Tidak perlu (untuk VM kecil)

5. **Management**

   **Monitoring:**

   - **Boot diagnostics:** Enable with managed storage account
   - **Guest OS diagnostics:** Disable

   **Auto-shutdown:**

   - ✅ Enable (untuk menghemat biaya)
   - **Time:** 19:00 (7 PM)
   - **Time zone:** (UTC+07:00) Bangkok, Hanoi, Jakarta

6. **Review + Create**
   - Klik **"Review + create"**
   - Tunggu validasi
   - Klik **"Create"**
7. **Download Private Key**

   - Pop-up akan muncul
   - Klik **"Download private key and create resource"**
   - File `branddetection-vm_key.pem` akan terdownload
   - **PENTING:** Simpan file ini dengan aman!

8. **Tunggu Deployment**
   - Proses deployment akan berlangsung 3-5 menit
   - Klik **"Go to resource"** setelah selesai

### 4.2 Koneksi ke VM

#### Untuk Windows (menggunakan PowerShell):

1. **Pindahkan Private Key**

   ```powershell
   # Pindahkan file .pem ke folder .ssh
   Move-Item -Path "$env:USERPROFILE\Downloads\branddetection-vm_key.pem" -Destination "$env:USERPROFILE\.ssh\"
   ```

2. **Set Permission**

   ```powershell
   # Windows tidak perlu chmod seperti Linux
   # Tapi pastikan file hanya readable oleh user Anda
   icacls "$env:USERPROFILE\.ssh\branddetection-vm_key.pem" /inheritance:r
   icacls "$env:USERPROFILE\.ssh\branddetection-vm_key.pem" /grant:r "$($env:USERNAME):(R)"
   ```

3. **SSH ke VM**

   ```powershell
   # Dapatkan IP public dari Azure Portal
   $VM_IP = "13.229.XXX.XXX"  # Ganti dengan IP VM Anda

   ssh -i "$env:USERPROFILE\.ssh\branddetection-vm_key.pem" azureuser@$VM_IP
   ```

#### Untuk Linux/Mac:

```bash
# Set permission untuk private key
chmod 400 ~/Downloads/branddetection-vm_key.pem

# SSH ke VM
ssh -i ~/Downloads/branddetection-vm_key.pem azureuser@13.229.XXX.XXX
```

### 4.3 Konfigurasi Awal VM

Setelah berhasil SSH ke VM:

```bash
# Update sistem
sudo apt update && sudo apt upgrade -y

# Install Python 3 dan pip
sudo apt install python3 python3-pip python3-venv -y

# Install ODBC Driver untuk SQL Server
curl https://packages.microsoft.com/keys/microsoft.asc | sudo apt-key add -
curl https://packages.microsoft.com/config/ubuntu/22.04/prod.list | sudo tee /etc/apt/sources.list.d/mssql-release.list
sudo apt update
sudo ACCEPT_EULA=Y apt install -y msodbcsql18

# Install unixODBC development headers
sudo apt install -y unixodbc-dev

# Install Nginx (web server)
sudo apt install nginx -y

# Install Git
sudo apt install git -y

# Verifikasi instalasi
python3 --version
pip3 --version
nginx -v
git --version
odbcinst -j
```

### 4.4 Setup Firewall

```bash
# Allow Nginx
sudo ufw allow 'Nginx Full'

# Allow SSH
sudo ufw allow OpenSSH

# Enable firewall
sudo ufw enable

# Check status
sudo ufw status
```

---

## 5. Deployment Aplikasi ke VM

### 5.1 Upload Kode ke VM

#### Opsi 1: Menggunakan Git (Recommended)

```bash
# Di VM, clone repository
cd /home/azureuser
git clone https://github.com/your-username/BrandDetection.git

# Atau jika belum di git, buat repository di GitHub dulu
# Lalu clone di VM
```

#### Opsi 2: Menggunakan SCP (dari komputer lokal)

```powershell
# Windows PowerShell
# Compress folder project
Compress-Archive -Path "C:\Users\mikhs\OneDrive\Documents\BrandDetection\*" -DestinationPath "$env:TEMP\branddetection.zip"

# Upload ke VM
scp -i "$env:USERPROFILE\.ssh\branddetection-vm_key.pem" "$env:TEMP\branddetection.zip" azureuser@13.229.XXX.XXX:/home/azureuser/

# SSH ke VM dan extract
ssh -i "$env:USERPROFILE\.ssh\branddetection-vm_key.pem" azureuser@13.229.XXX.XXX
unzip branddetection.zip -d BrandDetection
```

### 5.2 Setup Virtual Environment

```bash
# Masuk ke folder project
cd /home/azureuser/BrandDetection

# Buat virtual environment
python3 -m venv venv

# Aktifkan virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
```

### 5.3 Setup Environment Variables

```bash
# Buat file .env
nano .env

# Paste konfigurasi (ganti dengan kredensial Anda):
```

```env
# Azure Computer Vision
COMPUTER_VISION_ENDPOINT=https://branddetection-vision.cognitiveservices.azure.com/
COMPUTER_VISION_KEY=your_actual_key_here

# Azure SQL Database
SQL_SERVER=branddetection-sql-server.database.windows.net
SQL_DATABASE=BrandDetectionDB
SQL_USERNAME=sqladmin
SQL_PASSWORD=your_actual_password_here

# Flask Configuration
SECRET_KEY=generate_a_strong_random_key_here
MAX_FILE_SIZE=16777216
ALLOWED_EXTENSIONS=png,jpg,jpeg,gif
UPLOAD_FOLDER=uploads
```

```bash
# Simpan dengan Ctrl+O, Enter, Ctrl+X

# Set permission agar aman
chmod 600 .env
```

### 5.4 Test Aplikasi

```bash
# Pastikan virtual environment aktif
source venv/bin/activate

# Jalankan aplikasi (test mode)
python app.py

# Jika berhasil, Anda akan melihat:
# * Running on http://0.0.0.0:5000

# Test dari browser lokal:
# http://13.229.XXX.XXX:5000

# Tekan Ctrl+C untuk stop
```

### 5.5 Setup Gunicorn (Production Server)

```bash
# Install gunicorn (jika belum ada di requirements.txt)
pip install gunicorn

# Test gunicorn
gunicorn --bind 0.0.0.0:5000 app:app

# Jika berhasil, stop dengan Ctrl+C
```

### 5.6 Setup Systemd Service

```bash
# Buat service file
sudo nano /etc/systemd/system/branddetection.service
```

Paste konfigurasi berikut:

```ini
[Unit]
Description=Brand Detection Flask Application
After=network.target

[Service]
Type=simple
User=azureuser
WorkingDirectory=/home/azureuser/BrandDetection
Environment="PATH=/home/azureuser/BrandDetection/venv/bin"
ExecStart=/home/azureuser/BrandDetection/venv/bin/gunicorn --workers 3 --bind 0.0.0.0:5000 --timeout 300 --access-logfile /home/azureuser/BrandDetection/logs/access.log --error-logfile /home/azureuser/BrandDetection/logs/error.log app:app
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
# Simpan dengan Ctrl+O, Enter, Ctrl+X

# Reload systemd
sudo systemctl daemon-reload

# Enable service (auto-start on boot)
sudo systemctl enable branddetection

# Start service
sudo systemctl start branddetection

# Check status
sudo systemctl status branddetection

# Jika ada error, lihat log:
journalctl -u branddetection -n 50 --no-pager
```

### 5.7 Konfigurasi Nginx

```bash
# Buat konfigurasi Nginx
sudo nano /etc/nginx/sites-available/branddetection
```

Paste konfigurasi:

```nginx
server {
    listen 80;
    server_name 13.229.XXX.XXX;  # Ganti dengan IP VM Anda

    client_max_body_size 20M;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Timeout untuk upload gambar besar
        proxy_connect_timeout 300;
        proxy_send_timeout 300;
        proxy_read_timeout 300;
        send_timeout 300;
    }

    # Static files (opsional, untuk performa)
    location /static {
        alias /home/azureuser/BrandDetection/static;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # Logs
    access_log /var/log/nginx/branddetection_access.log;
    error_log /var/log/nginx/branddetection_error.log;
}
```

```bash
# Simpan dengan Ctrl+O, Enter, Ctrl+X

# Enable site
sudo ln -s /etc/nginx/sites-available/branddetection /etc/nginx/sites-enabled/

# Remove default site
sudo rm /etc/nginx/sites-enabled/default

# Test konfigurasi
sudo nginx -t

# Jika OK, restart Nginx
sudo systemctl restart nginx

# Check status
sudo systemctl status nginx
```

### 5.8 Test Deployment

1. **Buka browser**
2. **Akses:** `http://13.229.XXX.XXX` (ganti dengan IP VM Anda)
3. **Test fitur:**
   - Upload gambar
   - Lihat hasil deteksi
   - Cek halaman riwayat
   - Cek halaman statistik
   - Cek halaman tim

---

## 6. Konfigurasi Domain & SSL (Opsional)

### 6.1 Setup Domain

#### Jika Anda punya domain:

1. **DNS Configuration**

   - Login ke domain provider Anda (GoDaddy, Namecheap, dll)
   - Tambah A Record:
     - **Type:** A
     - **Name:** @ (untuk root) atau www
     - **Value:** IP VM Anda (13.229.XXX.XXX)
     - **TTL:** 600 atau Auto

2. **Update Nginx Config**

   ```bash
   sudo nano /etc/nginx/sites-available/branddetection
   ```

   Ganti:

   ```nginx
   server_name 13.229.XXX.XXX;
   ```

   Menjadi:

   ```nginx
   server_name branddetection.yourdomain.com www.branddetection.yourdomain.com;
   ```

   ```bash
   sudo nginx -t
   sudo systemctl restart nginx
   ```

### 6.2 Setup SSL dengan Let's Encrypt

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Obtain SSL certificate
sudo certbot --nginx -d branddetection.yourdomain.com -d www.branddetection.yourdomain.com

# Ikuti instruksi:
# - Masukkan email
# - Agree to terms
# - Pilih redirect HTTP to HTTPS (recommended)

# Certbot akan otomatis update Nginx config

# Test renewal
sudo certbot renew --dry-run

# Auto-renewal sudah dikonfigurasi otomatis via cron/systemd timer
```

---

## 7. Monitoring & Maintenance

### 7.1 Monitoring Aplikasi

#### Check Application Status:

```bash
# Service status
sudo systemctl status branddetection

# Recent logs
journalctl -u branddetection -n 100 --no-pager

# Follow logs (real-time)
journalctl -u branddetection -f

# Application logs
tail -f /home/azureuser/BrandDetection/logs/app_*.log

# Nginx access logs
sudo tail -f /var/log/nginx/branddetection_access.log

# Nginx error logs
sudo tail -f /var/log/nginx/branddetection_error.log
```

#### Check Resource Usage:

```bash
# CPU & Memory
htop
# (Install: sudo apt install htop)

# Disk usage
df -h

# Network
netstat -tuln | grep :80
netstat -tuln | grep :5000
```

### 7.2 Restart Services

```bash
# Restart aplikasi
sudo systemctl restart branddetection

# Restart Nginx
sudo systemctl restart nginx

# Restart semua
sudo systemctl restart branddetection nginx
```

### 7.3 Update Aplikasi

```bash
# SSH ke VM
ssh -i ~/.ssh/branddetection-vm_key.pem azureuser@13.229.XXX.XXX

# Masuk ke folder project
cd /home/azureuser/BrandDetection

# Backup database (opsional)
# (Backup otomatis ada di Azure SQL)

# Pull update dari git
git pull origin main

# Atau upload file baru via SCP

# Activate venv
source venv/bin/activate

# Update dependencies jika ada perubahan
pip install -r requirements.txt

# Restart aplikasi
sudo systemctl restart branddetection

# Check status
sudo systemctl status branddetection
```

### 7.4 Backup & Recovery

#### Backup Database (Otomatis):

Azure SQL Database sudah otomatis backup:

- Point-in-time restore: 7-35 hari
- Long-term retention: hingga 10 tahun (konfigurasi manual)

#### Backup Manual:

```bash
# Export database dari Azure Portal
# SQL Database → Export → Export to .bacpac file
```

#### Backup Files:

```bash
# Backup folder uploads
cd /home/azureuser/BrandDetection
tar -czf uploads_backup_$(date +%Y%m%d).tar.gz uploads/

# Download ke local
# scp -i ~/.ssh/branddetection-vm_key.pem azureuser@IP:/home/azureuser/BrandDetection/uploads_backup_*.tar.gz .
```

### 7.5 Cost Management

#### Monitor Biaya di Azure Portal:

1. **Cost Management + Billing**

   - Menu utama → **Cost Management + Billing**
   - **Cost analysis** → Lihat breakdown biaya per resource

2. **Set Budget Alert**

   - **Budgets** → **+ Add**
   - Set budget bulanan (misal: $20)
   - Set alert ketika mencapai 80%, 100%

3. **Stop VM ketika tidak digunakan**

   ```bash
   # Dari Azure Portal:
   # VM → Stop (deallocated)
   # Untuk menghemat biaya compute

   # Atau set auto-shutdown schedule
   ```

---

## 📊 Checklist Deployment

### ✅ Phase 1: Azure Resources Setup

- [ ] Akun Azure aktif dengan credit/subscription
- [ ] Resource Group `BrandDetection-RG` dibuat
- [ ] Azure Computer Vision resource dibuat
  - [ ] Endpoint disimpan
  - [ ] Key disimpan
  - [ ] Test API berhasil
- [ ] Azure SQL Database dibuat
  - [ ] Server & database ready
  - [ ] Firewall dikonfigurasi
  - [ ] Tabel `BrandDetection` dibuat
  - [ ] Connection string disimpan
  - [ ] Test connection berhasil
- [ ] Azure Virtual Machine dibuat
  - [ ] VM running
  - [ ] SSH access berhasil
  - [ ] Dependencies terinstall

### ✅ Phase 2: Application Deployment

- [ ] Kode aplikasi di VM
- [ ] Virtual environment dibuat
- [ ] Dependencies terinstall
- [ ] File `.env` dikonfigurasi dengan kredensial yang benar
- [ ] Folder `uploads/` dan `logs/` ada dan writable
- [ ] Test aplikasi dengan `python app.py` berhasil
- [ ] Gunicorn berjalan
- [ ] Systemd service `branddetection` aktif
- [ ] Nginx dikonfigurasi dan running
- [ ] Aplikasi accessible via browser

### ✅ Phase 3: Testing & Validation

- [ ] Halaman beranda loading
- [ ] Upload gambar berhasil
- [ ] Deteksi brand berfungsi
- [ ] Hasil tersimpan di database
- [ ] Halaman riwayat menampilkan data
- [ ] Halaman statistik menampilkan data
- [ ] Halaman tim pengembang loading
- [ ] Identitas mahasiswa tampil di semua halaman
- [ ] Responsive design berfungsi di mobile

### ✅ Phase 4: Optional (Production)

- [ ] Domain dikonfigurasi
- [ ] SSL certificate terinstall (HTTPS)
- [ ] Auto-shutdown VM dikonfigurasi untuk hemat biaya
- [ ] Monitoring logs berfungsi
- [ ] Budget alert di Azure diset

---

## 🎉 Selesai!

Aplikasi **Brand Detection** Anda sekarang:

- ✅ Running di Azure Virtual Machine
- ✅ Menggunakan Azure Computer Vision untuk deteksi
- ✅ Menyimpan data ke Azure SQL Database
- ✅ Production-ready dengan Nginx + Gunicorn
- ✅ Accessible via HTTP (atau HTTPS jika setup SSL)

### 📱 Akses Aplikasi:

**URL:** `http://13.229.XXX.XXX` (atau domain Anda)

### 👨‍💻 Informasi Pengembang:

**Nama:** Athallah Budiman Devia Putra  
**NIM:** 23076039  
**Prodi:** Pendidikan Teknik Informatika

---

## 📚 Referensi & Resources

- [Azure Portal](https://portal.azure.com/)
- [Azure Computer Vision Documentation](https://learn.microsoft.com/azure/cognitive-services/computer-vision/)
- [Azure SQL Database Documentation](https://learn.microsoft.com/azure/azure-sql/)
- [Azure VM Documentation](https://learn.microsoft.com/azure/virtual-machines/)
- [Flask Deployment Guide](https://flask.palletsprojects.com/en/latest/deploying/)
- [Nginx Documentation](https://nginx.org/en/docs/)
- [Let's Encrypt](https://letsencrypt.org/)

---

**© 2025 - Brand Detection System - Cloud Computing Project**
