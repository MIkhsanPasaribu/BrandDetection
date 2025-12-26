"""
Service untuk Azure Computer Vision API.

Modul ini berisi fungsi-fungsi untuk berinteraksi dengan Azure Computer Vision API
untuk mendeteksi brand/logo pada gambar yang diunggah.
"""

import logging
from typing import List, Dict, Optional
from azure.cognitiveservices.vision.computervision import ComputerVisionClient # type: ignore
from msrest.authentication import CognitiveServicesCredentials # type: ignore
from PIL import Image # type: ignore

# Setup logging
logger = logging.getLogger(__name__)


class ComputerVisionService:
    """Service untuk berinteraksi dengan Azure Computer Vision API."""

    def __init__(self, endpoint: str, key: str):
        """
        Inisialisasi Computer Vision Service.

        Args:
            endpoint: URL endpoint Azure Computer Vision
            key: Subscription key untuk autentikasi
        """
        self.endpoint = endpoint
        self.key = key
        self.client: Optional[ComputerVisionClient] = None

        if endpoint and key:
            try:
                kredensial = CognitiveServicesCredentials(key)
                self.client = ComputerVisionClient(endpoint, kredensial)
                logger.info("Computer Vision Client berhasil diinisialisasi")
            except Exception as e:
                logger.error(f"Gagal menginisialisasi Computer Vision Client: {str(e)}")
                self.client = None

    def deteksi_brand(self, path_gambar: str) -> List[Dict]:
        """
        Deteksi brand/logo dari gambar menggunakan Azure Computer Vision.

        Args:
            path_gambar: Path lengkap ke file gambar yang akan dianalisis

        Returns:
            List[Dict]: Daftar brand yang terdeteksi dengan informasi lengkap
                       Setiap dict berisi: brand, confidence, rectangle

        Raises:
            Exception: Jika terjadi error saat memanggil API
        """
        if not self.client:
            logger.error("Computer Vision Client belum diinisialisasi")
            return []

        brand_terdeteksi: List[Dict] = []

        try:
            logger.info(f"Memulai deteksi brand untuk gambar: {path_gambar}")

            # Buka file gambar dalam mode binary
            with open(path_gambar, 'rb') as file_gambar:
                # Panggil API untuk menganalisis gambar
                fitur = ['brands']
                hasil = self.client.analyze_image_in_stream(
                    file_gambar,
                    visual_features=fitur
                )

            # Proses hasil deteksi
            # Type guard: pastikan hasil memiliki attribute brands
            # type: ignore digunakan karena Azure SDK tidak memiliki type stubs lengkap
            if hasil and hasattr(hasil, 'brands') and hasil.brands:  # type: ignore[attr-defined]
                logger.info(f"Ditemukan {len(hasil.brands)} brand dalam gambar")  # type: ignore[attr-defined]

                for brand in hasil.brands:  # type: ignore[attr-defined]
                    info_brand = {
                        'brand': brand.name,
                        'confidence': brand.confidence,
                        'rectangle': {
                            'x': brand.rectangle.x,
                            'y': brand.rectangle.y,
                            'w': brand.rectangle.w,
                            'h': brand.rectangle.h
                        }
                    }
                    brand_terdeteksi.append(info_brand)
                    logger.info(
                        f"Brand terdeteksi: {brand.name} "
                        f"(confidence: {brand.confidence:.2%})"
                    )
            else:
                logger.info("Tidak ada brand yang terdeteksi dalam gambar")

        except FileNotFoundError:
            logger.error(f"File gambar tidak ditemukan: {path_gambar}")
            raise Exception("File gambar tidak ditemukan")
        except Exception as e:
            logger.error(f"Error saat deteksi brand: {str(e)}")
            raise Exception(f"Gagal mendeteksi brand: {str(e)}")

        return brand_terdeteksi

    def dapatkan_info_gambar(self, path_gambar: str) -> Dict:
        """
        Dapatkan informasi tambahan tentang gambar (resolusi, format, ukuran).

        Args:
            path_gambar: Path lengkap ke file gambar

        Returns:
            Dict: Informasi gambar (width, height, format, size)
        """
        try:
            with Image.open(path_gambar) as img:
                info = {
                    'width': img.width,
                    'height': img.height,
                    'format': img.format,
                    'mode': img.mode,
                    'resolusi': f"{img.width}x{img.height}"
                }
                logger.info(f"Info gambar: {info}")
                return info
        except Exception as e:
            logger.error(f"Error mendapatkan info gambar: {str(e)}")
            return {
                'width': 0,
                'height': 0,
                'format': 'unknown',
                'mode': 'unknown',
                'resolusi': 'unknown'
            }
