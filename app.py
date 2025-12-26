"""
Aplikasi Flask untuk Sistem Deteksi Merek (Brand Detection).

Aplikasi full-stack yang menggunakan Azure Computer Vision untuk mendeteksi
brand/logo dalam gambar yang diupload dan menyimpan hasilnya ke Azure SQL Database.

Dibuat oleh: Athallah Budiman Devia Putra
NIM: 23076039
Prodi: Pendidikan Teknik Informatika
"""

import os
import logging
from datetime import datetime
from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
from werkzeug.utils import secure_filename

from config import Config
from services import ComputerVisionService, DatabaseService
from utils import (
    file_diizinkan,
    simpan_file_upload,
    format_confidence,
    validasi_ukuran_file
)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'logs/app_{datetime.now().strftime("%Y%m%d")}.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Inisialisasi Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Pastikan folder upload ada
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs('logs', exist_ok=True)

# Inisialisasi services
vision_service = ComputerVisionService(
    Config.COMPUTER_VISION_ENDPOINT,
    Config.COMPUTER_VISION_KEY
)

db_service = DatabaseService(
    Config.SQL_CONNECTION_STRING,
    Config.SQL_PASSWORD
)

# Inisialisasi database
db_service.inisialisasi_database()


@app.route('/')
def beranda():
    """
    Halaman beranda - upload dan deteksi gambar.

    Returns:
        Rendered template halaman beranda
    """
    logger.info("Mengakses halaman beranda")
    return render_template('index.html', info_pengembang=Config.INFO_PENGEMBANG)


@app.route('/riwayat')
def riwayat():
    """
    Halaman riwayat deteksi.

    Returns:
        Rendered template halaman riwayat dengan data dari database
    """
    logger.info("Mengakses halaman riwayat")
    data_riwayat = db_service.dapatkan_riwayat(limit=50)
    return render_template(
        'riwayat.html',
        riwayat=data_riwayat,
        info_pengembang=Config.INFO_PENGEMBANG
    )


@app.route('/tim')
def tim_pengembang():
    """
    Halaman tim pengembang.

    Returns:
        Rendered template halaman tim pengembang
    """
    logger.info("Mengakses halaman tim pengembang")
    return render_template('tim.html', info_pengembang=Config.INFO_PENGEMBANG)


@app.route('/statistik')
def statistik():
    """
    Halaman statistik deteksi.

    Returns:
        Rendered template halaman statistik
    """
    logger.info("Mengakses halaman statistik")
    data_statistik = db_service.dapatkan_statistik()
    return render_template(
        'statistik.html',
        statistik=data_statistik,
        info_pengembang=Config.INFO_PENGEMBANG
    )


@app.route('/api/deteksi', methods=['POST'])
def api_deteksi():
    """
    API endpoint untuk upload gambar dan deteksi brand.

    Request:
        - Method: POST
        - Content-Type: multipart/form-data
        - Body: file dengan key 'gambar'

    Returns:
        JSON response dengan hasil deteksi atau error message
    """
    logger.info("Request deteksi brand diterima")

    # Validasi ada file dalam request
    if 'gambar' not in request.files:
        logger.warning("Request tidak mengandung file gambar")
        return jsonify({
            'sukses': False,
            'pesan': 'Tidak ada file gambar dalam request'
        }), 400

    file = request.files['gambar']

    # Validasi nama file tidak kosong
    if not file.filename or file.filename == '':
        logger.warning("Nama file kosong")
        return jsonify({
            'sukses': False,
            'pesan': 'Nama file tidak boleh kosong'
        }), 400

    # Validasi ekstensi file
    if not file_diizinkan(file.filename, app.config['ALLOWED_EXTENSIONS']):
        logger.warning(f"Ekstensi file tidak diizinkan: {file.filename}")
        return jsonify({
            'sukses': False,
            'pesan': f"Ekstensi file tidak diizinkan. Gunakan: {', '.join(app.config['ALLOWED_EXTENSIONS'])}"
        }), 400

    # Validasi ukuran file
    if not validasi_ukuran_file(file, app.config['MAX_CONTENT_LENGTH']):
        logger.warning("Ukuran file melebihi batas")
        return jsonify({
            'sukses': False,
            'pesan': f"Ukuran file terlalu besar. Maksimal {app.config['MAX_CONTENT_LENGTH'] / (1024*1024)} MB"
        }), 400

    try:
        # Simpan file
        path_file = simpan_file_upload(file, app.config['UPLOAD_FOLDER'])
        if not path_file:
            raise Exception("Gagal menyimpan file")

        # Dapatkan info gambar
        info_gambar = vision_service.dapatkan_info_gambar(path_file)

        # Deteksi brand
        brand_terdeteksi = vision_service.deteksi_brand(path_file)

        # Simpan setiap brand yang terdeteksi ke database
        if brand_terdeteksi:
            for brand in brand_terdeteksi:
                data_simpan = {
                    'image_name': file.filename,
                    'brand_name': brand['brand'],
                    'confidence_score': brand['confidence'],
                    'image_path': path_file,
                    'resolution': info_gambar.get('resolusi', 'unknown'),
                    'notes': f"Deteksi otomatis - posisi: {brand['rectangle']}"
                }
                db_service.simpan_hasil_deteksi(data_simpan)
        else:
            # Simpan record tanpa brand jika tidak ada yang terdeteksi
            data_simpan = {
                'image_name': file.filename,
                'image_path': path_file,
                'resolution': info_gambar.get('resolusi', 'unknown'),
                'notes': 'Tidak ada brand yang terdeteksi'
            }
            db_service.simpan_hasil_deteksi(data_simpan)

        # Response sukses
        response = {
            'sukses': True,
            'pesan': f"Ditemukan {len(brand_terdeteksi)} brand" if brand_terdeteksi else "Tidak ada brand terdeteksi",
            'jumlah_brand': len(brand_terdeteksi),
            'brand': brand_terdeteksi,
            'info_gambar': info_gambar
        }

        logger.info(f"Deteksi berhasil: {len(brand_terdeteksi)} brand ditemukan")
        return jsonify(response), 200

    except Exception as e:
        logger.error(f"Error saat deteksi: {str(e)}")
        return jsonify({
            'sukses': False,
            'pesan': f"Terjadi kesalahan: {str(e)}"
        }), 500


@app.route('/api/riwayat', methods=['GET'])
def api_riwayat():
    """
    API endpoint untuk mengambil riwayat deteksi.

    Query parameters:
        - limit (optional): Jumlah maksimal record (default: 100)

    Returns:
        JSON response dengan list riwayat deteksi
    """
    logger.info("Request riwayat deteksi diterima")

    try:
        limit = request.args.get('limit', 100, type=int)
        data_riwayat = db_service.dapatkan_riwayat(limit=limit)

        return jsonify({
            'sukses': True,
            'jumlah': len(data_riwayat),
            'data': data_riwayat
        }), 200

    except Exception as e:
        logger.error(f"Error mengambil riwayat: {str(e)}")
        return jsonify({
            'sukses': False,
            'pesan': f"Terjadi kesalahan: {str(e)}"
        }), 500


@app.route('/api/statistik', methods=['GET'])
def api_statistik():
    """
    API endpoint untuk mengambil statistik deteksi.

    Returns:
        JSON response dengan statistik deteksi
    """
    logger.info("Request statistik diterima")

    try:
        data_statistik = db_service.dapatkan_statistik()

        return jsonify({
            'sukses': True,
            'data': data_statistik
        }), 200

    except Exception as e:
        logger.error(f"Error mengambil statistik: {str(e)}")
        return jsonify({
            'sukses': False,
            'pesan': f"Terjadi kesalahan: {str(e)}"
        }), 500


@app.errorhandler(404)
def halaman_tidak_ditemukan(e):
    """Handler untuk error 404 - halaman tidak ditemukan."""
    logger.warning(f"Halaman tidak ditemukan: {request.url}")
    return render_template('404.html', info_pengembang=Config.INFO_PENGEMBANG), 404


@app.errorhandler(500)
def error_server(e):
    """Handler untuk error 500 - internal server error."""
    logger.error(f"Internal server error: {str(e)}")
    return render_template('500.html', info_pengembang=Config.INFO_PENGEMBANG), 500


@app.context_processor
def utility_processor():
    """
    Tambahkan fungsi utility ke context template.

    Returns:
        Dict dengan fungsi-fungsi helper untuk template
    """
    return {
        'format_confidence': format_confidence,
        'tahun_sekarang': datetime.now().year
    }


if __name__ == '__main__':
    # Validasi konfigurasi sebelum menjalankan
    if not Config.validasi_konfigurasi():
        logger.warning(
            "⚠️  PERINGATAN: Beberapa konfigurasi Azure belum diset. "
            "Aplikasi mungkin tidak berfungsi dengan baik. "
            "Silakan cek file .env"
        )

    logger.info("🚀 Memulai aplikasi Brand Detection")
    logger.info(f"📁 Folder upload: {app.config['UPLOAD_FOLDER']}")
    logger.info(f"👨‍💻 Pengembang: {Config.INFO_PENGEMBANG['nama']}")

    # Jalankan aplikasi dalam mode development
    app.run(debug=True, host='0.0.0.0', port=5000)
