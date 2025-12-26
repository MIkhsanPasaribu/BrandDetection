# 🏗️ Struktur Proyek Brand Detection

```
BrandDetection/
│
├── 📄 app.py                           # Aplikasi Flask utama (entry point)
├── ⚙️ config.py                        # Konfigurasi aplikasi & Azure
├── 📦 requirements.txt                 # Python dependencies
├── 📚 README.md                        # Dokumentasi utama
├── � PANDUAN_SETUP_AZURE.md          # Panduan lengkap setup Azure
├── ✅ DEPLOYMENT_CHECKLIST.md         # Checklist deployment ke Azure
├── 📋 SETUP.md                         # Panduan instalasi lokal
├── 📊 RINGKASAN_PENGEMBANGAN.md       # Ringkasan lengkap proyek
├── 🔧 pyrightconfig.json              # Konfigurasi pyright
├── 🚫 .gitignore                      # Git ignore rules
├── 📝 .env.example                    # Template environment variables
│
├── 📂 .github/                        # GitHub configuration
│   └── copilot-instructions.md        # Instruksi Copilot
│
├── 🔧 services/                       # Layer service untuk Azure
│   ├── __init__.py
│   ├── computer_vision.py             # Azure Computer Vision service
│   └── database.py                    # Azure SQL Database service
│
├── 🛠️ utils/                          # Utility functions
│   ├── __init__.py
│   └── helpers.py                     # Helper functions
│
├── 🚀 scripts/                        # Deployment & maintenance scripts
│   ├── README.md                      # Dokumentasi scripts
│   ├── install_dependencies.sh        # Install dependencies di VM
│   ├── setup_app.sh                   # Setup aplikasi (venv, packages)
│   ├── deploy_production.sh           # Deploy dengan systemd & Nginx
│   ├── update_app.sh                  # Update aplikasi di production
│   └── check_health.sh                # Health check & monitoring
│
├── 🎨 templates/                      # Jinja2 HTML templates
│   ├── base.html                      # Base template (header, footer, nav)
│   ├── index.html                     # Halaman beranda (upload & deteksi)
│   ├── riwayat.html                   # Halaman riwayat deteksi
│   ├── statistik.html                 # Halaman statistik
│   ├── tim.html                       # Halaman tim pengembang
│   ├── 404.html                       # Error 404 page
│   └── 500.html                       # Error 500 page
│
├── 💅 static/                         # Static files
│   ├── css/
│   │   └── style.css                  # Main stylesheet (responsive)
│   ├── js/
│   │   ├── app.js                     # Main JavaScript
│   │   └── deteksi.js                 # Detection page JavaScript
│   └── images/                        # Image assets
│
├── 📤 uploads/                        # Uploaded images storage
│   └── .gitkeep
│
├── 📝 logs/                           # Application logs
│
└── 🐍 venv/                           # Python virtual environment

```

## 📊 Statistik File

| Kategori         | Jumlah File  | Deskripsi                          |
| ---------------- | ------------ | ---------------------------------- |
| Python (Backend) | 6 files      | app.py, config.py, services, utils |
| HTML Templates   | 7 files      | base, pages, error pages           |
| CSS              | 1 file       | Comprehensive responsive styling   |
| JavaScript       | 2 files      | Main app & detection logic         |
| Configuration    | 4 files      | requirements, .env, pyright, git   |
| Documentation    | 3 files      | README, SETUP, RINGKASAN           |
| **TOTAL**        | **23 files** | Production-ready aplikasi          |

## 🎯 Alur Kerja Aplikasi

```
┌─────────────────────────────────────────────────────────┐
│                     USER INTERFACE                       │
│  (HTML Templates + CSS + JavaScript di /templates)      │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│                  FLASK APPLICATION                       │
│              (app.py - Routes & Logic)                   │
│  • / (beranda)                                          │
│  • /riwayat                                             │
│  • /statistik                                           │
│  • /tim                                                 │
│  • /api/deteksi (POST)                                  │
│  • /api/riwayat (GET)                                   │
│  • /api/statistik (GET)                                 │
└──────────┬─────────────────────┬────────────────────────┘
           │                     │
           ▼                     ▼
┌──────────────────────┐  ┌──────────────────────────┐
│  COMPUTER VISION     │  │   DATABASE SERVICE       │
│  (services/)         │  │   (services/)            │
│  • deteksi_brand()   │  │  • simpan_hasil()       │
│  • info_gambar()     │  │  • dapatkan_riwayat()   │
└──────────┬───────────┘  └──────────┬───────────────┘
           │                         │
           ▼                         ▼
┌──────────────────────┐  ┌──────────────────────────┐
│  AZURE COMPUTER      │  │   AZURE SQL DATABASE     │
│  VISION API          │  │   (BrandDetection        │
│  (Cloud Service)     │  │    table)                │
└──────────────────────┘  └──────────────────────────┘
```

## 🔄 Flow Request Upload & Deteksi

```
1. USER → Upload gambar via form di index.html
              ↓
2. JavaScript (deteksi.js) → Validasi file & preview
              ↓
3. AJAX POST → /api/deteksi dengan FormData
              ↓
4. Flask (app.py) → Validasi & simpan file
              ↓
5. ComputerVisionService → Deteksi brand via Azure
              ↓
6. DatabaseService → Simpan hasil ke Azure SQL
              ↓
7. Flask → Return JSON response
              ↓
8. JavaScript → Tampilkan hasil ke user
```

## 📦 Dependencies Utama

| Package                                       | Version | Kegunaan                     |
| --------------------------------------------- | ------- | ---------------------------- |
| Flask                                         | 3.0.0   | Web framework                |
| azure-cognitiveservices-vision-computervision | 0.9.0   | Azure Computer Vision SDK    |
| pyodbc                                        | 5.0.1   | Azure SQL Database connector |
| python-dotenv                                 | 1.0.0   | Environment variables        |
| Pillow                                        | 10.1.0  | Image processing             |
| gunicorn                                      | 21.2.0  | Production WSGI server       |

## 🎨 Design System

### Color Palette

- **Primary**: Blue (#2563eb)
- **Secondary**: Green (#10b981)
- **Dark**: (#1f2937)
- **Light**: (#f3f4f6)

### Layout Components

- Responsive Grid System
- Card-based UI
- Sticky Navigation
- Animated Transitions
- Modal Notifications

## 🔐 Security Features

✅ Environment variables untuk credentials  
✅ File upload validation (type & size)  
✅ SQL parameterized queries  
✅ Secure filename handling  
✅ CORS protection  
✅ Error handling & logging

## 📱 Responsive Breakpoints

- **Mobile**: < 768px
- **Tablet**: 768px - 1024px
- **Desktop**: > 1024px

## 🚀 Production Checklist

- [x] Environment variables setup
- [x] Azure resources configured
- [x] Database table created
- [x] Error handling implemented
- [x] Logging configured
- [x] Security validations
- [x] Responsive design
- [x] Documentation complete

---

**Developed by**: Athallah Budiman Devia Putra  
**NIM**: 23076039  
**Program**: Pendidikan Teknik Informatika
