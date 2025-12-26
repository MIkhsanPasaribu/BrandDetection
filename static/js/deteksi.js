/**
 * JavaScript untuk halaman deteksi brand
 *
 * Menangani upload gambar, preview, dan menampilkan hasil deteksi
 */

document.addEventListener("DOMContentLoaded", function () {
  const formUpload = document.getElementById("formUpload");
  const inputGambar = document.getElementById("inputGambar");
  const previewGambar = document.getElementById("previewGambar");
  const imgPreview = document.getElementById("imgPreview");
  const btnDeteksi = document.getElementById("btnDeteksi");
  const hasilDeteksi = document.getElementById("hasilDeteksi");
  const containerHasil = document.getElementById("containerHasil");

  // Event listener untuk preview gambar saat file dipilih
  inputGambar.addEventListener("change", function (e) {
    const file = e.target.files[0];

    if (file) {
      // Validasi ukuran file (16 MB)
      const maxSize = 16 * 1024 * 1024; // 16 MB
      if (file.size > maxSize) {
        tampilkanNotifikasi(
          "Ukuran file terlalu besar! Maksimal 16 MB.",
          "error"
        );
        inputGambar.value = "";
        previewGambar.style.display = "none";
        return;
      }

      // Validasi tipe file
      const allowedTypes = [
        "image/jpeg",
        "image/jpg",
        "image/png",
        "image/gif",
      ];
      if (!allowedTypes.includes(file.type)) {
        tampilkanNotifikasi(
          "Tipe file tidak didukung! Gunakan JPG, PNG, atau GIF.",
          "error"
        );
        inputGambar.value = "";
        previewGambar.style.display = "none";
        return;
      }

      // Tampilkan preview
      const reader = new FileReader();
      reader.onload = function (e) {
        imgPreview.src = e.target.result;
        previewGambar.style.display = "block";
        previewGambar.classList.add("fade-in");
      };
      reader.readAsDataURL(file);

      // Tampilkan info file
      tampilkanNotifikasi(
        `File dipilih: ${file.name} (${formatUkuranFile(file.size)})`,
        "info"
      );
    }
  });

  // Event listener untuk form submit
  formUpload.addEventListener("submit", async function (e) {
    e.preventDefault();

    const file = inputGambar.files[0];
    if (!file) {
      tampilkanNotifikasi("Pilih gambar terlebih dahulu!", "warning");
      return;
    }

    // Disable button dan tampilkan loading
    btnDeteksi.disabled = true;
    btnDeteksi.querySelector(".btn-text").style.display = "none";
    btnDeteksi.querySelector(".btn-loading").style.display = "inline";

    // Buat FormData
    const formData = new FormData();
    formData.append("gambar", file);

    try {
      // Kirim request ke API
      const response = await fetch("/api/deteksi", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (response.ok && data.sukses) {
        // Tampilkan hasil
        tampilkanHasil(data);
        tampilkanNotifikasi(data.pesan, "success");
      } else {
        tampilkanNotifikasi(data.pesan || "Terjadi kesalahan", "error");
      }
    } catch (error) {
      console.error("Error:", error);
      tampilkanNotifikasi("Gagal menghubungi server", "error");
    } finally {
      // Enable button dan sembunyikan loading
      btnDeteksi.disabled = false;
      btnDeteksi.querySelector(".btn-text").style.display = "inline";
      btnDeteksi.querySelector(".btn-loading").style.display = "none";
    }
  });

  // Fungsi untuk menampilkan hasil deteksi
  function tampilkanHasil(data) {
    hasilDeteksi.style.display = "block";
    hasilDeteksi.classList.add("fade-in");

    if (data.brand && data.brand.length > 0) {
      // Ada brand yang terdeteksi
      let html = '<div class="brand-list">';

      data.brand.forEach((brand, index) => {
        html += `
                    <div class="brand-item fade-in" style="animation-delay: ${
                      index * 0.1
                    }s">
                        <h4 class="brand-name">🏷️ ${brand.brand}</h4>
                        <div class="brand-details">
                            <p>
                                <strong>Confidence:</strong> 
                                <span class="confidence-badge" style="background: ${getConfidenceColor(
                                  brand.confidence
                                )}">
                                    ${formatConfidence(brand.confidence)}
                                </span>
                            </p>
                            <p>
                                <strong>Posisi:</strong> 
                                X: ${brand.rectangle.x}, 
                                Y: ${brand.rectangle.y}, 
                                W: ${brand.rectangle.w}, 
                                H: ${brand.rectangle.h}
                            </p>
                        </div>
                    </div>
                `;
      });

      html += "</div>";

      // Tambahkan info gambar
      if (data.info_gambar) {
        html += `
                    <div class="image-info" style="margin-top: 1.5rem; padding: 1rem; background: #f3f4f6; border-radius: 0.5rem;">
                        <h4 style="margin-bottom: 0.5rem;">ℹ️ Informasi Gambar</h4>
                        <p><strong>Resolusi:</strong> ${data.info_gambar.resolusi}</p>
                        <p><strong>Format:</strong> ${data.info_gambar.format}</p>
                    </div>
                `;
      }

      containerHasil.innerHTML = html;
    } else {
      // Tidak ada brand yang terdeteksi
      containerHasil.innerHTML = `
                <div class="no-brand-found" style="text-align: center; padding: 2rem;">
                    <div style="font-size: 3rem; margin-bottom: 1rem;">❌</div>
                    <h3>Tidak Ada Brand Terdeteksi</h3>
                    <p style="color: #6b7280; margin-top: 0.5rem;">
                        Gambar ini tidak mengandung brand atau logo yang dapat dikenali oleh sistem.
                    </p>
                </div>
            `;
    }

    // Scroll ke hasil
    hasilDeteksi.scrollIntoView({ behavior: "smooth", block: "nearest" });
  }

  // Fungsi untuk mendapatkan warna berdasarkan confidence
  function getConfidenceColor(confidence) {
    if (confidence >= 0.8) return "#10b981"; // Hijau
    if (confidence >= 0.6) return "#f59e0b"; // Kuning
    return "#ef4444"; // Merah
  }
});
