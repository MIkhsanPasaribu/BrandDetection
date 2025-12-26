"""
Service untuk Azure SQL Database.

Modul ini berisi fungsi-fungsi untuk berinteraksi dengan Azure SQL Database
untuk menyimpan dan mengambil hasil deteksi brand.
"""

import logging
from typing import List, Dict, Optional
from datetime import datetime
import pyodbc # type: ignore

# Setup logging
logger = logging.getLogger(__name__)


class DatabaseService:
    """Service untuk berinteraksi dengan Azure SQL Database."""

    def __init__(self, connection_string: str, password: str):
        """
        Inisialisasi Database Service.

        Args:
            connection_string: String koneksi ke Azure SQL Database (dengan placeholder password)
            password: Password untuk database
        """
        # Ganti placeholder password dengan password sebenarnya
        self.connection_string = connection_string.replace('{password}', password)
        logger.info("Database Service berhasil diinisialisasi")

    def dapatkan_koneksi(self) -> Optional[pyodbc.Connection]:
        """
        Buat koneksi baru ke database.

        Returns:
            pyodbc.Connection atau None jika gagal
        """
        try:
            koneksi = pyodbc.connect(self.connection_string)
            logger.info("Koneksi database berhasil dibuat")
            return koneksi
        except Exception as e:
            logger.error(f"Gagal membuat koneksi database: {str(e)}")
            return None

    def inisialisasi_database(self) -> bool:
        """
        Buat tabel BrandDetection jika belum ada.

        Returns:
            bool: True jika berhasil, False jika gagal
        """
        query_create_table = """
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='BrandDetection' AND xtype='U')
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
        """

        koneksi = self.dapatkan_koneksi()
        if not koneksi:
            return False

        try:
            cursor = koneksi.cursor()
            cursor.execute(query_create_table)
            koneksi.commit()
            cursor.close()
            koneksi.close()
            logger.info("Tabel BrandDetection berhasil diinisialisasi")
            return True
        except Exception as e:
            logger.error(f"Gagal membuat tabel: {str(e)}")
            return False

    def simpan_hasil_deteksi(self, data: Dict) -> bool:
        """
        Simpan hasil deteksi brand ke database.

        Args:
            data: Dictionary dengan keys:
                  - image_name: Nama file gambar
                  - brand_name: Nama brand yang terdeteksi (optional)
                  - confidence_score: Skor confidence (optional)
                  - image_path: Path file gambar (optional)
                  - resolution: Resolusi gambar (optional)
                  - position_type: Tipe posisi untuk eksperimen (optional)
                  - notes: Catatan tambahan (optional)

        Returns:
            bool: True jika berhasil, False jika gagal
        """
        query = """
        INSERT INTO BrandDetection
        (image_name, brand_name, confidence_score, image_path, resolution, position_type, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """

        koneksi = self.dapatkan_koneksi()
        if not koneksi:
            return False

        try:
            cursor = koneksi.cursor()
            cursor.execute(
                query,
                (
                    data.get('image_name', ''),
                    data.get('brand_name'),
                    data.get('confidence_score'),
                    data.get('image_path'),
                    data.get('resolution'),
                    data.get('position_type'),
                    data.get('notes')
                )
            )
            koneksi.commit()
            cursor.close()
            koneksi.close()
            logger.info(f"Hasil deteksi berhasil disimpan untuk: {data.get('image_name')}")
            return True
        except Exception as e:
            logger.error(f"Gagal menyimpan hasil deteksi: {str(e)}")
            return False

    def dapatkan_riwayat(self, limit: int = 100) -> List[Dict]:
        """
        Ambil riwayat deteksi dari database.

        Args:
            limit: Jumlah maksimal record yang diambil (default 100)

        Returns:
            List[Dict]: Daftar hasil deteksi
        """
        query = f"""
        SELECT TOP {limit}
            id, image_name, brand_name, confidence_score,
            upload_timestamp, image_path, resolution, position_type, notes
        FROM BrandDetection
        ORDER BY upload_timestamp DESC
        """

        koneksi = self.dapatkan_koneksi()
        if not koneksi:
            return []

        try:
            cursor = koneksi.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()

            hasil: List[Dict] = []
            for row in rows:
                hasil.append({
                    'id': row.id,
                    'image_name': row.image_name,
                    'brand_name': row.brand_name,
                    'confidence': row.confidence_score,
                    'timestamp': row.upload_timestamp.isoformat() if row.upload_timestamp else None,
                    'image_path': row.image_path,
                    'resolution': row.resolution,
                    'position_type': row.position_type,
                    'notes': row.notes
                })

            cursor.close()
            koneksi.close()
            logger.info(f"Berhasil mengambil {len(hasil)} record riwayat")
            return hasil
        except Exception as e:
            logger.error(f"Gagal mengambil riwayat: {str(e)}")
            return []

    def dapatkan_statistik(self) -> Dict:
        """
        Dapatkan statistik deteksi dari database.

        Returns:
            Dict: Statistik seperti total deteksi, brand populer, rata-rata confidence
        """
        query = """
        SELECT
            COUNT(*) as total_deteksi,
            COUNT(DISTINCT brand_name) as jumlah_brand_unik,
            AVG(confidence_score) as rata_confidence
        FROM BrandDetection
        WHERE brand_name IS NOT NULL
        """

        query_brand_populer = """
        SELECT TOP 5 brand_name, COUNT(*) as jumlah
        FROM BrandDetection
        WHERE brand_name IS NOT NULL
        GROUP BY brand_name
        ORDER BY jumlah DESC
        """

        koneksi = self.dapatkan_koneksi()
        if not koneksi:
            return {}

        try:
            cursor = koneksi.cursor()

            # Ambil statistik umum
            cursor.execute(query)
            row = cursor.fetchone()

            statistik = {
                'total_deteksi': row.total_deteksi if row else 0,
                'jumlah_brand_unik': row.jumlah_brand_unik if row else 0,
                'rata_confidence': round(row.rata_confidence, 4) if row and row.rata_confidence else 0
            }

            # Ambil brand populer
            cursor.execute(query_brand_populer)
            rows = cursor.fetchall()
            brand_populer = [
                {'brand': row.brand_name, 'jumlah': row.jumlah}
                for row in rows
            ]
            statistik['brand_populer'] = brand_populer

            cursor.close()
            koneksi.close()
            logger.info("Berhasil mengambil statistik")
            return statistik
        except Exception as e:
            logger.error(f"Gagal mengambil statistik: {str(e)}")
            return {}
