"""
Konfigurasi aplikasi Sistem Deteksi Merek.

Modul ini berisi semua konfigurasi yang diperlukan untuk menjalankan aplikasi,
termasuk kredensial Azure dan pengaturan aplikasi Flask.
"""

import os
from typing import Set
from dotenv import load_dotenv

# Muat environment variables dari file .env
load_dotenv()


class Config:
    """Kelas konfigurasi untuk aplikasi Flask."""

    # Konfigurasi Flask
    SECRET_KEY: str = os.getenv('SECRET_KEY', 'dev-secret-key-ubah-di-production')
    MAX_CONTENT_LENGTH: int = int(os.getenv('MAX_FILE_SIZE', 16 * 1024 * 1024))  # 16 MB default

    # Folder upload
    UPLOAD_FOLDER: str = os.getenv('UPLOAD_FOLDER', 'uploads')
    ALLOWED_EXTENSIONS: Set[str] = set(os.getenv('ALLOWED_EXTENSIONS', 'png,jpg,jpeg,gif').split(','))

    # Konfigurasi Azure Computer Vision
    COMPUTER_VISION_ENDPOINT: str = os.getenv('COMPUTER_VISION_ENDPOINT', '')
    COMPUTER_VISION_KEY: str = os.getenv('COMPUTER_VISION_KEY', '')

    # Konfigurasi Azure SQL Database
    SQL_SERVER: str = os.getenv('SQL_SERVER', '')
    SQL_DATABASE: str = os.getenv('SQL_DATABASE', '')
    SQL_USERNAME: str = os.getenv('SQL_USERNAME', '')
    SQL_PASSWORD: str = os.getenv('SQL_PASSWORD', '')

    # Connection string untuk Azure SQL
    SQL_CONNECTION_STRING: str = (
        f"Driver={{ODBC Driver 18 for SQL Server}};"
        f"Server=tcp:{SQL_SERVER},1433;"
        f"Database={SQL_DATABASE};"
        f"Uid={SQL_USERNAME};"
        f"Pwd={{password}};"
        f"Encrypt=yes;"
        f"TrustServerCertificate=no;"
    )

    # Informasi mahasiswa/pengembang
    INFO_PENGEMBANG = {
        'nama': 'Athallah Budiman Devia Putra',
        'nim': '23076039',
        'prodi': 'Pendidikan Teknik Informatika'
    }

    @staticmethod
    def validasi_konfigurasi() -> bool:
        """
        Validasi apakah semua konfigurasi penting sudah diset.

        Returns:
            bool: True jika semua konfigurasi valid, False jika ada yang kosong
        """
        konfigurasi_penting = [
            Config.COMPUTER_VISION_ENDPOINT,
            Config.COMPUTER_VISION_KEY,
            Config.SQL_SERVER,
            Config.SQL_DATABASE,
            Config.SQL_USERNAME,
            Config.SQL_PASSWORD
        ]

        return all(konfigurasi_penting)
