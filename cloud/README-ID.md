# Perbaikan runtime cloud — 30 Oktober 2026

Paket versi2 menyediakan setup terpisah di `/workspace/openmontage-runtime`. Source dan checksum diverifikasi; checkout Git, video lama, Secrets dan lockfile upstream tidak ditimpa. ZIP berisi source, bukan model/venv/node_modules/kredensial.

Dari checkout repo pengiriman ini, jalankan `python3 cloud/bootstrap_runtime.py --archive OpenMontage-portable-neon-v2.zip --sha256 7fa4ee1c9938c5255f802e0ffd4d678107d8ad4c4965f12311026b92f441dfb2`. Setup memasang dependency dari lock teruji, menjalankan npm ci dan render MP4 WebGL teknis empat detik. Tidak ada panggilan TTS berbayar. Prasyarat: Python3.12+, Node22+, FFmpeg/ffprobe; browser dapat disiapkan Remotion bila belum tersedia. Koneksi jaringan dan CA trust tetap mengikuti platform.

Bukti: [validation-2026-10-30.json](validation-2026-10-30.json). Instalasi dari direktori kosong, pip check, npm ci, full decode, pemeriksaan frame WebGL dan pemanggilan setup kedua berhasil di mesin sesi ini. Ini belum merupakan bukti pemulihan pada Cloud Task baru.

ElevenLabs telah diminta kembali. Secret bernama ELEVENLABS_API_KEY harus dipasang melalui environment settings untuk api.elevenlabs.io. Script `/workspace/openmontage-runtime/.venv/bin/python /workspace/openmontage-runtime/portable/elevenlabs_check.py` menguji autentikasi read-only tanpa sintesis/kredit. Saat perbaikan dibuat, key belum hadir sehingga autentikasi dan kualitas narasi belum diuji. Jangan memasukkan key ke chat, repo atau script.

Vol.4 telah disimpan dan mengganti antrean AI/Tech. Pengguna meminta jangan produksi dulu: [production-control.json](../production-control.json) tetap production_allowed=false. Jangan mengaktifkan batch atau fallback suara hanya karena interval empat jam berlalu.

Installer tidak membuat/menonaktifkan scheduler. Draft environment juga bukan Publish. Sesudah konfigurasi ditinjau dan dipublikasikan melalui produk, uji satu eksekusi Tasks di environment yang tepat sebelum menganggap jadwal berjalan. Jika UI Publish tetap menolak, simpan pesan error/waktu kejadian untuk dukungan platform; helper lokal tidak dapat memperbaiki layanan Publish.
