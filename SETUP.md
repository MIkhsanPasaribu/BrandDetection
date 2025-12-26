# Script Setup untuk Sistem Deteksi Merek

## Panduan Instalasi Dependencies

Untuk menjalankan aplikasi dan testing dengan pyright, ikuti langkah berikut:

### 1. Buat Virtual Environment

```bash
python -m venv venv
```

### 2. Aktifkan Virtual Environment

**Windows:**

```bash
venv\Scripts\activate
```

**Linux/Mac:**

```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install Pyright (untuk testing)

```bash
pip install pyright
```

### 5. Jalankan Type Checking

```bash
python -m pyright
```

## Catatan Testing

Pyright akan menampilkan error "reportMissingImports" jika dependencies belum terinstall di virtual environment yang aktif.

**Solusi:**

1. Pastikan virtual environment sudah diaktifkan
2. Install semua dependencies dengan `pip install -r requirements.txt`
3. Jalankan kembali `python -m pyright`

Jika semua dependencies terinstall dengan benar, pyright seharusnya tidak menampilkan error atau hanya menampilkan warning minor.

## Dependencies yang Dibutuhkan

- Flask==3.0.0
- azure-cognitiveservices-vision-computervision==0.9.0
- msrest==0.7.1
- pyodbc==5.0.1
- python-dotenv==1.0.0
- Pillow==10.1.0
- gunicorn==21.2.0

## Testing Aplikasi

Setelah dependencies terinstall:

1. **Setup environment variables:**

   ```bash
   copy .env.example .env
   # Edit .env dengan kredensial Azure Anda
   ```

2. **Jalankan aplikasi:**

   ```bash
   python app.py
   ```

3. **Akses aplikasi:**
   Buka browser dan akses `http://localhost:5000`

## Troubleshooting

### Error: Module not found

- Pastikan virtual environment aktif
- Install dependencies dengan `pip install -r requirements.txt`

### Error: pyright not found

- Install pyright dengan `pip install pyright`

### Error: Azure credentials not configured

- Edit file `.env` dan isi dengan kredensial Azure yang valid
