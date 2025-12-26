"""
Utilitas helper untuk aplikasi Brand Detection.

Modul ini berisi fungsi-fungsi helper yang digunakan di berbagai bagian aplikasi.
"""

import os
import logging
from typing import Optional
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage

# Setup logging
logger = logging.getLogger(__name__)


def file_diizinkan(nama_file: str, ekstensi_diizinkan: set) -> bool:
    """
    Cek apakah file memiliki ekstensi yang diizinkan.

    Args:
        nama_file: Nama file yang akan dicek
        ekstensi_diizinkan: Set ekstensi yang diizinkan (contoh: {'png', 'jpg'})

    Returns:
        bool: True jika ekstensi diizinkan, False jika tidak
    """
    return '.' in nama_file and \
        nama_file.rsplit('.', 1)[1].lower() in ekstensi_diizinkan


def simpan_file_upload(file: FileStorage, folder_upload: str) -> Optional[str]:
    """
    Simpan file yang diupload dengan nama yang aman.

    Args:
        file: File yang diupload dari request
        folder_upload: Path folder tempat menyimpan file

    Returns:
        str: Path lengkap file yang disimpan, atau None jika gagal
    """
    try:
        # Buat nama file yang aman
        nama_file_aman = secure_filename(file.filename or 'unknown.jpg')

        # Pastikan folder upload ada
        os.makedirs(folder_upload, exist_ok=True)

        # Path lengkap untuk menyimpan file
        path_file = os.path.join(folder_upload, nama_file_aman)

        # Simpan file
        file.save(path_file)
        logger.info(f"File berhasil disimpan: {path_file}")

        return path_file
    except Exception as e:
        logger.error(f"Gagal menyimpan file: {str(e)}")
        return None


def format_confidence(confidence: Optional[float]) -> str:
    """
    Format confidence score menjadi persentase string.

    Args:
        confidence: Nilai confidence (0.0 - 1.0)

    Returns:
        str: Confidence dalam format persentase (contoh: "95.5%")
    """
    if confidence is None:
        return "N/A"

    try:
        return f"{confidence * 100:.2f}%"
    except (ValueError, TypeError):
        return "N/A"


def format_ukuran_file(ukuran_bytes: int) -> str:
    """
    Format ukuran file dalam bytes menjadi format yang mudah dibaca.

    Args:
        ukuran_bytes: Ukuran file dalam bytes

    Returns:
        str: Ukuran dalam format KB/MB (contoh: "1.5 MB")
    """
    if ukuran_bytes < 1024:
        return f"{ukuran_bytes} B"
    elif ukuran_bytes < 1024 * 1024:
        return f"{ukuran_bytes / 1024:.2f} KB"
    else:
        return f"{ukuran_bytes / (1024 * 1024):.2f} MB"


def validasi_ukuran_file(file: FileStorage, max_size: int) -> bool:
    """
    Validasi ukuran file.

    Args:
        file: File yang diupload
        max_size: Ukuran maksimal dalam bytes

    Returns:
        bool: True jika ukuran file valid, False jika melebihi batas
    """
    try:
        # Simpan posisi saat ini
        posisi_awal = file.tell()

        # Pindah ke akhir file untuk mendapatkan ukuran
        file.seek(0, os.SEEK_END)
        ukuran_file = file.tell()

        # Kembalikan posisi ke awal
        file.seek(posisi_awal)

        return ukuran_file <= max_size
    except Exception as e:
        logger.error(f"Gagal memvalidasi ukuran file: {str(e)}")
        return False
