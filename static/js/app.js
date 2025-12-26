/**
 * JavaScript Utama untuk Sistem Deteksi Merek
 *
 * Dibuat oleh: Athallah Budiman Devia Putra
 * NIM: 23076039
 * Prodi: Pendidikan Teknik Informatika
 */

// Fungsi untuk menampilkan notifikasi
function tampilkanNotifikasi(pesan, tipe = "info") {
  const warna = {
    success: "#10b981",
    error: "#ef4444",
    warning: "#f59e0b",
    info: "#3b82f6",
  };

  const notifikasi = document.createElement("div");
  notifikasi.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${warna[tipe] || warna.info};
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 0.5rem;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        z-index: 1000;
        animation: slideIn 0.3s ease;
        max-width: 400px;
    `;
  notifikasi.textContent = pesan;

  document.body.appendChild(notifikasi);

  // Hapus notifikasi setelah 5 detik
  setTimeout(() => {
    notifikasi.style.animation = "slideOut 0.3s ease";
    setTimeout(() => notifikasi.remove(), 300);
  }, 5000);
}

// Fungsi untuk format ukuran file
function formatUkuranFile(bytes) {
  if (bytes === 0) return "0 B";
  const k = 1024;
  const sizes = ["B", "KB", "MB", "GB"];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + " " + sizes[i];
}

// Fungsi untuk format confidence sebagai persentase
function formatConfidence(confidence) {
  return (confidence * 100).toFixed(2) + "%";
}

// Animasi CSS
const styleElement = document.createElement("style");
styleElement.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
    
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .fade-in {
        animation: fadeIn 0.5s ease;
    }
`;
document.head.appendChild(styleElement);

// Export fungsi untuk digunakan di file lain
if (typeof module !== "undefined" && module.exports) {
  module.exports = {
    tampilkanNotifikasi,
    formatUkuranFile,
    formatConfidence,
  };
}
