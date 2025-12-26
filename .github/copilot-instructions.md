# Instruksi Copilot - Sistem Deteksi Merek (Brand Detection)

## 📋 Ringkasan Proyek

Aplikasi web berbasis cloud computing untuk mendeteksi logo atau merek (brand) pada gambar menggunakan Azure Computer Vision API. Sistem ini memungkinkan pengguna mengunggah foto produk dan secara otomatis mendeteksi merek yang ada dalam gambar tersebut.

## Syarat

- **Bahasa**: Full Bahasa Indonesia untuk semua kode pada string, nama variabel, dan komentar (kecuali nama file dan library eksternal)
- **Code Quality**: Mengikuti best practices & pattern terbaik, readable, clean, maintainable, scalable, reliable, dan simple.

## 🎯 Tujuan Proyek

- Mendeteksi logo/merek secara otomatis dari gambar yang diunggah
- Menyimpan hasil deteksi ke database Azure SQL
- Melakukan eksperimen untuk menguji ketahanan AI terhadap berbagai kondisi gambar
- Deploy aplikasi ke Azure Virtual Machine

## 🏗️ Arsitektur Sistem

### Komponen Utama:

1. **Frontend**: Website untuk upload gambar dan menampilkan hasil
2. **Backend**: API server untuk memproses request dan komunikasi dengan Azure
3. **Azure Computer Vision**: Service AI untuk deteksi brand
4. **Azure SQL Database**: Penyimpanan data hasil deteksi
5. **Azure VM**: Hosting aplikasi

### Flow Kerja:

```
User Upload Gambar → Backend API → Azure Computer Vision
                                    ↓
                              Deteksi Brand
                                    ↓
                    JSON Response (brand, confidence)
                                    ↓
                          Azure SQL Database
                                    ↓
                        Tampilkan Hasil ke User
```

## 🛠️ Stack Teknologi

### Frontend:

- **HTML5/CSS3**: Struktur dan styling
- **JavaScript**: Interaksi user
- **Bootstrap/Tailwind CSS**: Framework UI (pilihan)
- **Fetch API/Axios**: HTTP requests

### Backend:

- **Python dengan Flask/FastAPI**: Framework web API (REKOMENDASI)
  - Atau **Node.js dengan Express**: Alternatif
- **Azure SDK**: Library untuk integrasi Azure services

### Database:

- **Azure SQL Database**: Relational database untuk menyimpan hasil

### Cloud Services:

- **Azure Computer Vision API**: Deteksi brand/logo
- **Azure Virtual Machine**: Hosting aplikasi
- **Azure Storage Account** (opsional): Penyimpanan gambar

## 📝 Panduan Pengembangan

### 1. Setup Azure Resources

#### Azure Computer Vision:

```python
# Buat resource Azure Computer Vision di Azure Portal
# Dapatkan endpoint dan subscription key
COMPUTER_VISION_ENDPOINT = "https://<your-resource>.cognitiveservices.azure.com/"
COMPUTER_VISION_KEY = "<your-subscription-key>"
```

#### Azure SQL Database:

```sql
-- Buat database dan tabel untuk menyimpan hasil deteksi
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

#### Connection String:

```python
# Format connection string untuk Azure SQL
SQL_CONNECTION_STRING = (
    "Driver={ODBC Driver 18 for SQL Server};"
    "Server=tcp:<server-name>.database.windows.net,1433;"
    "Database=<database-name>;"
    "Uid=<username>;"
    "Pwd=<password>;"
    "Encrypt=yes;"
    "TrustServerCertificate=no;"
)
```

### 2. Backend Development

#### Dependencies (requirements.txt):

```txt
Flask==3.0.0
azure-cognitiveservices-vision-computervision==0.9.0
msrest==0.7.1
pyodbc==5.0.1
python-dotenv==1.0.0
Pillow==10.1.0
```

#### Struktur Folder Backend:

```
backend/
├── app.py                 # Main aplikasi Flask
├── config.py              # Konfigurasi Azure credentials
├── services/
│   ├── computer_vision.py # Service untuk Azure Computer Vision
│   └── database.py        # Service untuk Azure SQL Database
├── routes/
│   └── api.py             # API endpoints
├── utils/
│   └── helpers.py         # Fungsi helper
├── uploads/               # Folder temporary untuk gambar
└── requirements.txt
```

#### Contoh Implementasi Computer Vision Service:

```python
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials

def detect_brand(image_path, endpoint, key):
    """
    Deteksi brand dari gambar menggunakan Azure Computer Vision

    Args:
        image_path: Path ke file gambar
        endpoint: Azure Computer Vision endpoint
        key: Subscription key

    Returns:
        dict: {'brand': str, 'confidence': float, 'rectangle': dict}
    """
    client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(key))

    with open(image_path, 'rb') as image_file:
        # Deteksi brand menggunakan analyze_image_in_stream
        features = ['brands']
        result = client.analyze_image_in_stream(image_file, visual_features=features)

    brands_detected = []
    if result.brands:
        for brand in result.brands:
            brands_detected.append({
                'brand': brand.name,
                'confidence': brand.confidence,
                'rectangle': {
                    'x': brand.rectangle.x,
                    'y': brand.rectangle.y,
                    'w': brand.rectangle.w,
                    'h': brand.rectangle.h
                }
            })

    return brands_detected
```

#### Contoh Database Service:

```python
import pyodbc
from datetime import datetime

def save_detection_result(connection_string, data):
    """
    Simpan hasil deteksi ke Azure SQL Database

    Args:
        connection_string: SQL connection string
        data: dict dengan keys: image_name, brand_name, confidence_score, dll
    """
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()

    query = """
    INSERT INTO BrandDetection
    (image_name, brand_name, confidence_score, image_path, resolution, position_type, notes)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """

    cursor.execute(query, (
        data['image_name'],
        data.get('brand_name'),
        data.get('confidence_score'),
        data.get('image_path'),
        data.get('resolution'),
        data.get('position_type'),
        data.get('notes')
    ))

    conn.commit()
    cursor.close()
    conn.close()
```

#### API Endpoints:

```python
from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/api/detect', methods=['POST'])
def detect_brand_api():
    """
    Endpoint untuk upload gambar dan deteksi brand

    Request: multipart/form-data dengan file gambar
    Response: JSON dengan hasil deteksi
    """
    if 'image' not in request.files:
        return jsonify({'error': 'Tidak ada file gambar'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'Nama file kosong'}), 400

    # Simpan file temporary
    filepath = os.path.join('uploads', file.filename)
    file.save(filepath)

    # Deteksi brand
    brands = detect_brand(filepath, COMPUTER_VISION_ENDPOINT, COMPUTER_VISION_KEY)

    # Simpan ke database
    for brand in brands:
        save_detection_result(SQL_CONNECTION_STRING, {
            'image_name': file.filename,
            'brand_name': brand['brand'],
            'confidence_score': brand['confidence'],
            'image_path': filepath
        })

    return jsonify({
        'success': True,
        'brands': brands
    })

@app.route('/api/history', methods=['GET'])
def get_history():
    """
    Endpoint untuk mengambil riwayat deteksi
    """
    conn = pyodbc.connect(SQL_CONNECTION_STRING)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM BrandDetection ORDER BY upload_timestamp DESC")
    rows = cursor.fetchall()

    results = []
    for row in rows:
        results.append({
            'id': row.id,
            'image_name': row.image_name,
            'brand_name': row.brand_name,
            'confidence': row.confidence_score,
            'timestamp': row.upload_timestamp.isoformat()
        })

    cursor.close()
    conn.close()

    return jsonify(results)
```

### 3. Frontend Development

#### Struktur Folder Frontend:

```
frontend/
├── index.html           # Halaman utama
├── css/
│   └── style.css        # Styling
├── js/
│   └── app.js           # JavaScript logic
└── assets/
    └── images/          # Gambar untuk UI
```

#### Contoh HTML (index.html):

```html
<!DOCTYPE html>
<html lang="id">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Sistem Deteksi Merek</title>
    <link rel="stylesheet" href="css/style.css" />
  </head>
  <body>
    <div class="container">
      <h1>Sistem Deteksi Merek (Brand Detection)</h1>

      <!-- Form Upload -->
      <div class="upload-section">
        <h2>Upload Gambar</h2>
        <input type="file" id="imageInput" accept="image/*" />
        <button onclick="uploadImage()">Deteksi Brand</button>

        <!-- Preview gambar -->
        <div id="imagePreview"></div>
      </div>

      <!-- Hasil Deteksi -->
      <div class="results-section">
        <h2>Hasil Deteksi</h2>
        <div id="results"></div>
      </div>

      <!-- Riwayat -->
      <div class="history-section">
        <h2>Riwayat Deteksi</h2>
        <button onclick="loadHistory()">Muat Riwayat</button>
        <div id="history"></div>
      </div>
    </div>

    <script src="js/app.js"></script>
  </body>
</html>
```

#### Contoh JavaScript (app.js):

```javascript
const API_URL = "http://localhost:5000/api";

async function uploadImage() {
  const fileInput = document.getElementById("imageInput");
  const file = fileInput.files[0];

  if (!file) {
    alert("Silakan pilih gambar terlebih dahulu");
    return;
  }

  // Tampilkan preview
  const preview = document.getElementById("imagePreview");
  preview.innerHTML = `<img src="${URL.createObjectURL(file)}" alt="Preview">`;

  // Upload ke backend
  const formData = new FormData();
  formData.append("image", file);

  try {
    const response = await fetch(`${API_URL}/detect`, {
      method: "POST",
      body: formData,
    });

    const data = await response.json();
    displayResults(data);
  } catch (error) {
    console.error("Error:", error);
    alert("Terjadi kesalahan saat mendeteksi brand");
  }
}

function displayResults(data) {
  const resultsDiv = document.getElementById("results");

  if (data.brands && data.brands.length > 0) {
    let html = "<h3>Brand Terdeteksi:</h3><ul>";
    data.brands.forEach((brand) => {
      html += `
                <li>
                    <strong>${brand.brand}</strong> 
                    (Confidence: ${(brand.confidence * 100).toFixed(2)}%)
                    <br>Posisi: X=${brand.rectangle.x}, Y=${brand.rectangle.y}
                </li>
            `;
    });
    html += "</ul>";
    resultsDiv.innerHTML = html;
  } else {
    resultsDiv.innerHTML = "<p>Tidak ada brand yang terdeteksi</p>";
  }
}

async function loadHistory() {
  try {
    const response = await fetch(`${API_URL}/history`);
    const data = await response.json();

    const historyDiv = document.getElementById("history");
    let html =
      "<table><tr><th>Gambar</th><th>Brand</th><th>Confidence</th><th>Waktu</th></tr>";

    data.forEach((item) => {
      html += `
                <tr>
                    <td>${item.image_name}</td>
                    <td>${item.brand_name || "N/A"}</td>
                    <td>${
                      item.confidence
                        ? (item.confidence * 100).toFixed(2) + "%"
                        : "N/A"
                    }</td>
                    <td>${new Date(item.timestamp).toLocaleString("id-ID")}</td>
                </tr>
            `;
    });

    html += "</table>";
    historyDiv.innerHTML = html;
  } catch (error) {
    console.error("Error:", error);
  }
}
```

### 4. Deployment ke Azure VM

#### Langkah-langkah Deployment:

1. **Buat Azure VM**:

   - Pilih OS: Ubuntu 22.04 LTS (rekomendasi) atau Windows Server
   - Size: Standard B2s atau lebih tinggi
   - Buka port: 80 (HTTP), 443 (HTTPS), 22 (SSH)

2. **Setup VM (Ubuntu)**:

```bash
# Update sistem
sudo apt update && sudo apt upgrade -y

# Install Python dan dependencies
sudo apt install python3 python3-pip python3-venv -y

# Install ODBC Driver untuk SQL Server
curl https://packages.microsoft.com/keys/microsoft.asc | sudo apt-key add -
curl https://packages.microsoft.com/config/ubuntu/22.04/prod.list | sudo tee /etc/apt/sources.list.d/mssql-release.list
sudo apt update
sudo ACCEPT_EULA=Y apt install msodbcsql18 -y

# Install Nginx (web server)
sudo apt install nginx -y
```

3. **Deploy Aplikasi**:

```bash
# Clone atau upload kode ke VM
cd /home/azureuser
mkdir brand-detection
cd brand-detection

# Setup virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
nano .env
# Isi dengan:
# COMPUTER_VISION_ENDPOINT=your_endpoint
# COMPUTER_VISION_KEY=your_key
# SQL_CONNECTION_STRING=your_connection_string
```

4. **Setup Service dengan Systemd**:

```bash
# Buat service file
sudo nano /etc/systemd/system/brand-detection.service
```

Isi file:

```ini
[Unit]
Description=Brand Detection API
After=network.target

[Service]
User=azureuser
WorkingDirectory=/home/azureuser/brand-detection
Environment="PATH=/home/azureuser/brand-detection/venv/bin"
ExecStart=/home/azureuser/brand-detection/venv/bin/gunicorn -w 4 -b 0.0.0.0:5000 app:app

[Install]
WantedBy=multi-user.target
```

```bash
# Enable dan start service
sudo systemctl enable brand-detection
sudo systemctl start brand-detection
```

5. **Konfigurasi Nginx**:

```bash
sudo nano /etc/nginx/sites-available/brand-detection
```

Isi file:

```nginx
server {
    listen 80;
    server_name your_vm_ip_or_domain;

    location / {
        root /home/azureuser/brand-detection/frontend;
        index index.html;
    }

    location /api {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

```bash
# Enable site dan restart nginx
sudo ln -s /etc/nginx/sites-available/brand-detection /etc/nginx/sites-enabled/
sudo systemctl restart nginx
```

## 🧪 Eksperimen dan Testing

### 1. Uji Posisi Logo

#### Tujuan:

Menguji ketahanan AI terhadap berbagai orientasi logo

#### Metodologi:

```python
# Tambahkan parameter position_type saat menyimpan ke database
test_positions = ['tegak_lurus', 'miring_45', 'terbalik_180', 'rotasi_90']

for position in test_positions:
    # Upload gambar dengan posisi berbeda
    # Catat confidence score
    # Simpan ke database dengan label position_type
```

#### Variabel yang Diukur:

- Confidence score untuk setiap posisi
- Apakah brand tetap terdeteksi
- Waktu proses deteksi

### 2. Uji Resolusi

#### Tujuan:

Menguji pengaruh kualitas gambar terhadap akurasi deteksi

#### Metodologi:

```python
from PIL import Image

def test_resolution(original_image_path):
    """
    Test deteksi dengan berbagai resolusi
    """
    resolutions = [
        (1920, 1080, 'HD'),
        (1280, 720, 'HD_720'),
        (640, 480, 'SD'),
        (320, 240, 'Low'),
        (160, 120, 'Very_Low')
    ]

    results = []
    img = Image.open(original_image_path)

    for width, height, label in resolutions:
        # Resize gambar
        resized = img.resize((width, height))
        test_path = f'test_{label}.jpg'
        resized.save(test_path)

        # Deteksi brand
        brands = detect_brand(test_path, endpoint, key)

        results.append({
            'resolution': label,
            'dimensions': f'{width}x{height}',
            'brands_detected': len(brands),
            'confidence': brands[0]['confidence'] if brands else 0
        })

    return results
```

### 3. Uji Gangguan Visual

#### Tujuan:

Menguji ketahanan terhadap noise dan blur

#### Metodologi:

```python
from PIL import Image, ImageFilter

def add_noise(image_path, level):
    """Tambahkan noise ke gambar"""
    img = Image.open(image_path)
    # Implementasi noise addition
    return noisy_img

def add_blur(image_path, radius):
    """Tambahkan blur ke gambar"""
    img = Image.open(image_path)
    blurred = img.filter(ImageFilter.GaussianBlur(radius))
    return blurred

# Test dengan berbagai level gangguan
noise_levels = [0, 10, 25, 50, 75]
blur_levels = [0, 2, 5, 10, 15]
```

### 4. Analisis Hasil

#### Query untuk Analisis:

```sql
-- Rata-rata confidence berdasarkan posisi
SELECT position_type, AVG(confidence_score) as avg_confidence
FROM BrandDetection
GROUP BY position_type
ORDER BY avg_confidence DESC;

-- Perbandingan resolusi
SELECT resolution,
       COUNT(*) as total_detections,
       AVG(confidence_score) as avg_confidence
FROM BrandDetection
GROUP BY resolution;

-- Brand paling sering terdeteksi
SELECT brand_name, COUNT(*) as detection_count
FROM BrandDetection
WHERE brand_name IS NOT NULL
GROUP BY brand_name
ORDER BY detection_count DESC;
```

## 📊 Struktur Laporan

### 1. Pendahuluan

- Latar belakang
- Tujuan penelitian
- Manfaat penelitian

### 2. Tinjauan Pustaka

- Cloud Computing
- Computer Vision
- Azure Computer Vision API
- Brand Detection Technology

### 3. Metodologi

- Arsitektur sistem
- Tools dan teknologi yang digunakan
- Desain eksperimen

### 4. Implementasi

- Setup Azure resources
- Pengembangan aplikasi web
- Deployment ke Azure VM

### 5. Hasil dan Pembahasan

- Hasil uji posisi logo
- Hasil uji resolusi
- Hasil uji gangguan visual
- Analisis performa Azure Computer Vision

### 6. Kesimpulan

- Temuan utama
- Kontribusi penelitian
- Saran untuk pengembangan

## 🔒 Best Practices Keamanan

### 1. Environment Variables

```python
# Jangan hardcode credentials di kode
# Gunakan .env file atau Azure Key Vault
from dotenv import load_dotenv
import os

load_dotenv()

COMPUTER_VISION_KEY = os.getenv('COMPUTER_VISION_KEY')
SQL_PASSWORD = os.getenv('SQL_PASSWORD')
```

### 2. Azure SQL Security

- Gunakan Firewall rules untuk membatasi akses
- Enable SSL/TLS untuk koneksi
- Gunakan managed identity jika memungkinkan

### 3. File Upload Security

```python
# Validasi tipe file
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Batasi ukuran file
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB
```

## 📈 Monitoring dan Logging

### Setup Logging:

```python
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(
    filename=f'logs/app_{datetime.now().strftime("%Y%m%d")}.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Log setiap request
@app.before_request
def log_request():
    logging.info(f'Request: {request.method} {request.path}')

# Log hasil deteksi
def detect_and_log(image_path):
    logging.info(f'Processing image: {image_path}')
    brands = detect_brand(image_path, endpoint, key)
    logging.info(f'Brands detected: {len(brands)}')
    return brands
```

## 🎨 Pengembangan Lanjutan (Opsional)

### Fitur Tambahan:

1. **Visualisasi Bounding Box**:

   - Gambar kotak di sekitar logo yang terdeteksi
   - Gunakan HTML5 Canvas atau library seperti fabric.js

2. **Batch Processing**:

   - Upload multiple images sekaligus
   - Queue system untuk processing

3. **Dashboard Analytics**:

   - Chart untuk statistik deteksi
   - Gunakan Chart.js atau D3.js

4. **Export Report**:

   - Export hasil eksperimen ke PDF/Excel
   - Gunakan library seperti reportlab atau openpyxl

5. **API Authentication**:
   - JWT token untuk secure API access
   - Rate limiting untuk mencegah abuse

## 🐛 Troubleshooting

### Common Issues:

1. **Error koneksi ke Azure Computer Vision**:

   - Periksa endpoint dan key
   - Periksa firewall dan network security group

2. **Error koneksi ke Azure SQL**:

   - Pastikan firewall rule mengizinkan IP VM
   - Periksa connection string

3. **Brand tidak terdeteksi**:

   - Azure Computer Vision hanya mengenali brand terkenal
   - Pastikan logo cukup jelas dan besar

4. **Performance lambat**:
   - Resize gambar sebelum upload ke API
   - Gunakan async processing untuk multiple images

## 📚 Resources dan Dokumentasi

### Dokumentasi Azure:

- [Azure Computer Vision Documentation](https://learn.microsoft.com/azure/cognitive-services/computer-vision/)
- [Azure SQL Database Documentation](https://learn.microsoft.com/azure/azure-sql/)
- [Azure VM Documentation](https://learn.microsoft.com/azure/virtual-machines/)

### Tutorial dan Guides:

- Python Flask Tutorial
- Azure SDK for Python
- Computer Vision API Reference

---

## ⚙️ Panduan untuk GitHub Copilot

Saat mengembangkan kode untuk proyek ini, pastikan:

1. **Gunakan bahasa Indonesia** untuk komentar dan dokumentasi
2. **Ikuti struktur folder** yang sudah ditentukan
3. **Implementasikan error handling** yang proper
4. **Tambahkan logging** untuk debugging
5. **Validasi input** dari user
6. **Gunakan environment variables** untuk credentials
7. **Ikuti best practices** Python/JavaScript
8. **Buat kode yang modular** dan mudah di-maintain
9. **Tambahkan docstring** untuk setiap fungsi
10. **Test setiap fitur** sebelum deployment

### Contoh Format Komentar:

```python
def detect_brand(image_path, endpoint, key):
    """
    Mendeteksi brand/logo dari gambar menggunakan Azure Computer Vision API.

    Parameter:
        image_path (str): Path lengkap ke file gambar yang akan dianalisis
        endpoint (str): URL endpoint Azure Computer Vision
        key (str): Subscription key untuk autentikasi

    Return:
        list: Daftar brand yang terdeteksi dengan confidence score

    Raises:
        Exception: Jika terjadi error saat memanggil API
    """
    # Implementasi...
```

### Prioritas Development:

1. ✅ Setup Azure resources (Computer Vision, SQL Database)
2. ✅ Buat struktur folder dan file dasar
3. ✅ Implementasi backend API untuk deteksi brand
4. ✅ Implementasi koneksi ke Azure SQL Database
5. ✅ Buat frontend untuk upload dan display hasil
6. ✅ Testing lokal
7. ✅ Deployment ke Azure VM
8. ✅ Implementasi eksperimen (posisi, resolusi, gangguan)
9. ✅ Analisis dan dokumentasi hasil

---

**Catatan Penting**: File instruksi ini akan menjadi panduan utama untuk GitHub Copilot dalam membantu pengembangan aplikasi. Pastikan untuk selalu mengikuti panduan ini agar kode yang dihasilkan konsisten dan sesuai dengan kebutuhan proyek.
