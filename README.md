# Sistem Deteksi Merek (Brand Detection)

Aplikasi web berbasis cloud computing untuk mendeteksi logo atau merek (brand) pada gambar menggunakan Azure Computer Vision API.

## 👨‍💻 Informasi Pengembang

- **Nama**: Athallah Budiman Devia Putra
- **NIM**: 23076039
- **Prodi**: Pendidikan Teknik Informatika

## 📋 Deskripsi Proyek

Sistem ini memungkinkan pengguna mengunggah foto produk dan secara otomatis mendeteksi merek yang ada dalam gambar tersebut menggunakan teknologi AI dari Azure Computer Vision. Semua hasil deteksi disimpan ke Azure SQL Database untuk analisis lebih lanjut.

## 🎯 Fitur Utama

- ✅ **Deteksi Brand Otomatis**: Menggunakan Azure Computer Vision untuk mengenali logo dan merek
- ✅ **Upload Gambar**: Interface mudah untuk upload gambar (JPG, PNG, GIF)
- ✅ **Riwayat Deteksi**: Melihat semua deteksi yang pernah dilakukan
- ✅ **Statistik**: Analisis data deteksi dengan visualisasi
- ✅ **Responsive Design**: Dapat diakses dari desktop, tablet, dan mobile
- ✅ **Halaman Tim Pengembang**: Informasi lengkap tentang pengembang dan proyek

## 🛠️ Teknologi yang Digunakan

### Backend

- Python 3.8+
- Flask (Framework Web)
- Azure Computer Vision SDK
- Azure SQL Database (pyodbc)

### Frontend

- HTML5
- CSS3 (Custom styling dengan CSS Variables)
- JavaScript (Vanilla JS)

### Cloud Services

- Azure Computer Vision API
- Azure SQL Database
- Azure Virtual Machine (untuk deployment)

## � Quick Start

### Lokal Development

```bash
# Install dependencies
pip install -r requirements.txt

# Konfigurasi .env
cp .env.example .env
nano .env  # Edit dengan kredensial Azure Anda

# Jalankan aplikasi
python app.py

# Akses di browser
# http://localhost:5000
```

### Deployment ke Azure

Lihat panduan lengkap di [PANDUAN_SETUP_AZURE.md](PANDUAN_SETUP_AZURE.md) untuk:

- Setup Azure Computer Vision
- Setup Azure SQL Database
- Deploy ke Azure Virtual Machine
- Konfigurasi Nginx & Systemd

**Scripts otomasi deployment tersedia di folder [scripts/](scripts/)**

## �📁 Struktur Proyek

```
BrandDetection/
├── app.py                      # Aplikasi Flask utama
├── config.py                   # Konfigurasi aplikasi
├── requirements.txt            # Dependencies Python
├── .env.example               # Contoh environment variables
├── services/
│   ├── __init__.py
│   ├── computer_vision.py     # Service Azure Computer Vision
│   └── database.py            # Service Azure SQL Database
├── utils/
│   ├── __init__.py
│   └── helpers.py             # Fungsi helper
├── templates/                  # Template HTML
│   ├── base.html
│   ├── index.html
│   ├── riwayat.html
│   ├── statistik.html
│   ├── tim.html
│   ├── 404.html
│   └── 500.html
├── static/
│   ├── css/
│   │   └── style.css          # Stylesheet utama
│   ├── js/
│   │   ├── app.js             # JavaScript utama
│   │   └── deteksi.js         # JavaScript untuk deteksi
│   └── images/                # Gambar assets
├── uploads/                    # Folder untuk gambar yang diupload
└── logs/                       # Folder untuk log aplikasi
```

## ⚙️ Instalasi dan Setup

### 1. Clone atau Download Proyek

```bash
git clone <repository-url>
cd BrandDetection
```

### 2. Buat Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Setup Environment Variables

Salin file `.env.example` menjadi `.env`:

```bash
copy .env.example .env
```

Edit file `.env` dan isi dengan kredensial Azure Anda:

```env
COMPUTER_VISION_ENDPOINT=https://your-resource.cognitiveservices.azure.com/
COMPUTER_VISION_KEY=your-subscription-key-here

SQL_SERVER=your-server.database.windows.net
SQL_DATABASE=BrandDetectionDB
SQL_USERNAME=your-username
SQL_PASSWORD=your-password

SECRET_KEY=your-secret-key-here
```

### 5. Setup Azure Resources

**📘 Panduan lengkap tersedia di [PANDUAN_SETUP_AZURE.md](PANDUAN_SETUP_AZURE.md)**

Ringkasan singkat:

#### Azure Computer Vision:

1. Buat resource di Azure Portal
2. Salin endpoint dan key ke `.env`

#### Azure SQL Database:

1. Buat SQL Database di Azure Portal
2. Jalankan query untuk membuat tabel:

```sql
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
```

3. Update connection string di `.env`

**Untuk instruksi detail dengan screenshot dan troubleshooting, baca [PANDUAN_SETUP_AZURE.md](PANDUAN_SETUP_AZURE.md)**

### 6. Jalankan Aplikasi

```bash
python app.py
```

Aplikasi akan berjalan di `http://localhost:5000`

## 🧪 Testing

Untuk menjalankan type checking dengan pyright:

```bash
python -m pyright
```

Pastikan semua dependencies sudah terinstall dengan benar.

## 📖 Cara Penggunaan

1. **Upload Gambar**:

   - Buka halaman beranda
   - Klik "Pilih Gambar" dan pilih gambar yang mengandung logo/brand
   - Klik "Deteksi Brand"
   - Tunggu proses deteksi selesai

2. **Lihat Hasil**:

   - Hasil deteksi akan muncul di bawah form upload
   - Menampilkan brand yang terdeteksi beserta confidence score
   - Informasi posisi logo dalam gambar

3. **Lihat Riwayat**:

   - Klik menu "Riwayat" di navigasi
   - Lihat semua deteksi yang pernah dilakukan
   - Data ditampilkan dalam bentuk tabel

4. **Lihat Statistik**:

   - Klik menu "Statistik" di navigasi
   - Lihat total deteksi, brand populer, dll

5. **Info Pengembang**:
   - Klik menu "Tim Pengembang"
   - Lihat informasi lengkap tentang pengembang dan proyek

## 🔒 Keamanan

- Environment variables untuk menyimpan kredensial
- Validasi file upload (tipe dan ukuran)
- SQL parameterized queries untuk mencegah SQL injection
- HTTPS direkomendasikan untuk production

## 🚀 Deployment ke Azure VM

**📘 Panduan deployment lengkap: [PANDUAN_SETUP_AZURE.md](PANDUAN_SETUP_AZURE.md)**

### Quick Deployment dengan Scripts:

```bash
# 1. Setup dependencies di VM
./scripts/install_dependencies.sh

# 2. Setup aplikasi
./scripts/setup_app.sh

# 3. Deploy ke production
./scripts/deploy_production.sh

# 4. Health check
./scripts/check_health.sh
```

Lihat [scripts/README.md](scripts/README.md) untuk dokumentasi lengkap scripts.

### Manual Deployment:

1. ✅ Buat Azure VM (Ubuntu 22.04 LTS)
2. ✅ Install Python, pip, ODBC Driver, Nginx
3. ✅ Upload/clone kode ke VM
4. ✅ Setup virtual environment
5. ✅ Konfigurasi .env dengan kredensial Azure
6. ✅ Setup systemd service untuk Gunicorn
7. ✅ Konfigurasi Nginx sebagai reverse proxy
8. ✅ Setup firewall rules (UFW)
9. ✅ Test aplikasi

Langkah-langkah detail tersedia di [PANDUAN_SETUP_AZURE.md](PANDUAN_SETUP_AZURE.md)

## 📝 Logging

Aplikasi mencatat semua aktivitas ke file log di folder `logs/`:

- Format: `app_YYYYMMDD.log`
- Level: INFO, WARNING, ERROR
- Berguna untuk debugging dan monitoring

View logs:

```bash
# Application logs
tail -f logs/app_$(date +%Y%m%d).log

# Systemd logs (jika deployed)
journalctl -u branddetection -f
```

## 🐛 Troubleshooting

### Error Koneksi Azure Computer Vision:

- Periksa endpoint dan subscription key di `.env`
- Pastikan resource Azure aktif
- Cek firewall dan network settings
- Test dengan script: `python -c "from services.computer_vision import ComputerVisionService; svc = ComputerVisionService(); print('OK')"`

### Error Koneksi Database:

- Pastikan firewall rule mengizinkan IP Anda di Azure SQL
- Periksa connection string di `.env`
- Verifikasi username dan password
- Test dengan Azure Data Studio atau Query Editor

### Service Failed to Start (Production):

```bash
# Check status
sudo systemctl status branddetection

# View logs
journalctl -u branddetection -n 50

# Common fixes:
# - Check .env file exists and has correct values
# - Verify virtual environment path in service file
# - Ensure port 5000 is not in use
```

Lihat [PANDUAN_SETUP_AZURE.md](PANDUAN_SETUP_AZURE.md) section "Troubleshooting" untuk solusi lengkap.

### Brand Tidak Terdeteksi:

- Azure Computer Vision hanya mengenali brand terkenal
- Pastikan logo cukup jelas dan tidak terlalu kecil
- Coba dengan gambar yang lebih berkualitas

## 📚 Dokumentasi Tambahan

### Dokumentasi Proyek:

- 📘 **[PANDUAN_SETUP_AZURE.md](PANDUAN_SETUP_AZURE.md)** - Panduan lengkap setup Azure (Computer Vision, SQL Database, VM)
- 🚀 **[scripts/README.md](scripts/README.md)** - Dokumentasi scripts deployment dan maintenance
- 📝 **[SETUP.md](SETUP.md)** - Panduan instalasi dan setup lokal
- 📊 **[STRUKTUR_PROYEK.md](STRUKTUR_PROYEK.md)** - Penjelasan struktur folder dan file
- 📋 **[RINGKASAN_PENGEMBANGAN.md](RINGKASAN_PENGEMBANGAN.md)** - Ringkasan proses pengembangan

### Referensi External:

- [Azure Computer Vision Documentation](https://learn.microsoft.com/azure/cognitive-services/computer-vision/)
- [Azure SQL Database Documentation](https://learn.microsoft.com/azure/azure-sql/)
- [Azure Virtual Machines Documentation](https://learn.microsoft.com/azure/virtual-machines/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Python pyodbc Documentation](https://github.com/mkleehammer/pyodbc/wiki)

## 🎓 Konteks Akademik

Proyek ini adalah tugas akhir untuk mata kuliah **Cloud Computing** dengan fokus pada:

1. ✅ **Infrastructure as a Service (IaaS)** - Azure Virtual Machine
2. ✅ **Platform as a Service (PaaS)** - Azure SQL Database
3. ✅ **Software as a Service (SaaS)** - Azure Computer Vision API
4. ✅ **Full-stack Web Development** - Flask + HTML/CSS/JS
5. ✅ **DevOps Practices** - Deployment scripts, systemd, Nginx
6. ✅ **Database Management** - Azure SQL, query optimization
7. ✅ **API Integration** - RESTful API dengan Azure SDK

### Eksperimen yang Dapat Dilakukan:

- 🔬 Uji ketahanan AI terhadap berbagai orientasi logo (tegak, miring, terbalik)
- 🔬 Uji pengaruh resolusi gambar terhadap akurasi deteksi
- 🔬 Uji dengan berbagai kondisi pencahayaan
- 🔬 Analisis confidence score berdasarkan kondisi gambar
- 🔬 Perbandingan brand yang paling sering terdeteksi

## 📧 Kontak

Untuk pertanyaan atau masalah terkait proyek ini, silakan hubungi:

**Athallah Budiman Devia Putra**

- NIM: 23076039
- Prodi: Pendidikan Teknik Informatika

## 📄 Lisensi

Proyek ini dibuat untuk keperluan tugas akademik Cloud Computing.

---

**© 2025 Athallah Budiman Devia Putra - Tugas Cloud Computing**
