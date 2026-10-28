# Menjalankan studio neon di komputer sendiri

Paket ini memuat **source OpenMontage, skills, panduan agen, profil kreator, dependency 3D, setup Piper Indonesia, dan tes MP4**. Tidak memuat `.env`, API key, sesi login, `.venv`, `node_modules`, atau model besar. Model diunduh terpisah dengan SHA-256 yang diperiksa. Tidak memerlukan MCP/plugin cloud yang dipakai di chat ini.

## 1. Yang disiapkan

| Komponen | Kebutuhan profil ini |
|---|---|
| OS | Linux; macOS; Windows lewat WSL2 Ubuntu 24.04 |
| Hardware | Rekomendasi 4 core, RAM 16 GB, disk kosong 10 GB. RAM 8 GB bisa dicoba dengan concurrency 2. GPU NVIDIA tidak wajib. |
| Python | **3.12+**, termasuk venv/pip. Upstream menerima 3.10+, tetapi helper aman ini memakai API tar Python 3.12. |
| Node.js | **22+**; Node 24 juga dipakai pada mesin pengujian. npm harus tersedia. |
| Media | FFmpeg dan ffprobe pada PATH; Chromium/Chrome atau browser yang diunduh Remotion |
| Suara | Piper 1.8.0 + model Indonesia `id_ID-news_tts-medium` (~67 MB archive) |
| Agen | Salah satu Codex, Claude Code, OpenCode; akun/provider LLM sesuai layanan masing-masing |
| Internet | Saat instalasi dependency/model dan menggunakan agen cloud. Sintesis Piper dan render lokal sesudah setup tidak memanggil API TTS. |

Gratisnya suara Piper **tidak berarti penggunaan Codex/Claude/model OpenCode gratis**. Biaya layanan agen mengikuti akun atau provider model yang dipilih. Tidak perlu ElevenLabs untuk profil ini.

## 2. Ambil source

Jika menerima `OpenMontage-portable-neon.zip`, ekstrak lalu masuk ke folder `OpenMontage`. Paket lengkap ini sudah menyertakan perubahan portable; **jangan hanya clone upstream dan mengira profil kreator ikut terbawa**. Jika bekerja melalui Git, simpan perubahan portable ini ke fork sendiri dan clone fork itu. Upstream: <https://github.com/calesthio/OpenMontage>.

Jangan menyalin `.env`, folder login agen, cache kredensial atau `node_modules` dari cloud ke komputer baru. Login pada CLI setempat. Menyalin `.venv` antar-OS juga tidak didukung.

## 3. Pasang prasyarat OS

### Ubuntu 24.04 / WSL2

Windows: jalankan `wsl --install -d Ubuntu-24.04` di PowerShell sebagai administrator, ikuti restart/setup WSL, lalu semua perintah berikut dijalankan **di terminal Ubuntu**. Simpan repo di `~/OpenMontage`, bukan `/mnt/c/...`, untuk performa file/render.

```bash
sudo apt update
sudo apt install -y git python3 python3-venv python3-pip ffmpeg build-essential
```

Pasang Node.js 22/24 melalui installer resmi atau version manager pilihanmu; pastikan `node --version` minimal 22. Paket Node bawaan beberapa distro masih terlalu lama. Referensi: <https://nodejs.org/en/download>.

Jika browser Remotion gagal karena library Linux hilang, Ubuntu 24.04 biasanya membutuhkan:

```bash
sudo apt install -y libnss3 libatk-bridge2.0-0t64 libatk1.0-0t64 libgbm1 libasound2t64 libcups2t64 libxkbcommon0 libxcomposite1 libxdamage1 libxrandr2 fonts-liberation
```

### macOS

Dengan Homebrew yang sudah terpasang:

```bash
brew install python@3.12 node@22 ffmpeg
export PATH="$(brew --prefix node@22)/bin:$PATH"
```

Gunakan `python3.12` untuk bootstrap. Apple Silicon harus memakai Python/Node dengan arsitektur yang konsisten. Jalur ini didokumentasikan tetapi belum diuji pada Mac dalam sesi ini; hasil smoke test pada komputer tersebut menentukan kesiapan.

## 4. Setup dan tes

Dari root repo (folder yang berisi AGENTS.md):

```bash
python3 portable/bootstrap.py
# macOS bila python3 belum versi 3.12: python3.12 portable/bootstrap.py
bash portable/run.sh python portable/doctor.py
bash portable/run.sh python portable/smoke.py
```

Bootstrap membuat/memakai `.venv`, memasang requirements, menjalankan **npm ci** dengan lockfile, mengunduh model bersertifikat checksum, lalu menyiapkan browser bila tidak ada browser sistem. Tidak menjalankan sudo, mengubah login agen, atau menimpa `.env`. `make setup` standar tetap ada, tetapi profil ini membutuhkan bootstrap portable untuk melengkapi 3D/model/alignment.

Hasil tes:

- `.runtime/portable-doctor.json`: modul/tool yang tersedia. Ini belum membuktikan browser dapat merender.
- `projects/portable-smoke/renders/smoke.mp4`: video nyata 1080×1920/30 fps, objek 3D bergerak dan suara Indonesia.
- `projects/portable-smoke/renders/frame.png`: periksa objek 3D tidak blank.
- `projects/portable-smoke/artifacts/readiness.json`: probe, durasi, alignment dan decode berhasil.

Dengarkan MP4 tes sebelum produksi. Pengujian mesin tidak dapat menjamin selera suara/visual. Profil suara ini mempertahankan model yang sudah dipilih kreator, bukan janji kualitas setara provider komersial. Bootstrap dan tes boleh diulang; gagal tetap menghasilkan exit code nonzero. Lihat `VALIDATION.md` untuk hasil yang benar-benar diuji di cloud.

## 5. Pilih agen

Pasang CLI dari dokumentasi resmi, lalu login/atur model pada CLI tersebut:

- Codex: <https://developers.openai.com/codex/cli/>
- Claude Code: <https://code.claude.com/docs/en/setup>
- OpenCode: <https://opencode.ai/docs/>

Jalankan dari root repo dengan environment video aktif:

```bash
bash portable/run.sh codex
# atau
bash portable/run.sh claude
# atau
bash portable/run.sh opencode
```

| Agen | Entry instruksi |
|---|---|
| Codex | `AGENTS.md` → `AGENT_GUIDE.md` + `portable/CREATOR_PROFILE.md`; skill native `.agents/skills/neon-reels/` |
| Claude Code | `CLAUDE.md` → guide/profile; skill `.claude/skills/neon-reels/` |
| OpenCode | `opencode.json` memuat guide/profile; `AGENTS.md` dan `.opencode/skills/neon-reels/` tersedia, skill juga bisa dibaca secara eksplisit |

Jika memakai aplikasi desktop atau extension IDE, buka folder root OpenMontage sebagai workspace. Minta agen menjalankan command Python melalui `bash portable/run.sh python ...`; tidak harus memulai aplikasi desktop lewat launcher CLI. File AGENTS/CLAUDE/profile tetap dibaca dari repo yang sama.

Deteksi skill otomatis dapat berbeda menurut versi CLI. Semua instruksi tetap dapat dipakai dengan meminta agen membaca file SKILL.md secara langsung. Tidak perlu mengandalkan slash command khusus atau cloud plugin. Jika memakai folder kerja lain, buka **root OpenMontage** agar instruksi/venv benar. Jangan menonaktifkan pemeriksaan permission secara global.

## 6. Prompt siap pakai

Salin isi `portable/START-HERE.txt` ke agen. Lampirkan naskah baru setelahnya. Untuk produksi tanpa berhenti di setiap gate, prompt tersebut menyediakan izin full-run yang terbatas pada produksi lokal dan biaya API nol. Upload/push memerlukan tujuan dan izin terpisah; tidak otomatis memakai repo publik sesi chat lama.

## 7. Skills dan berkas yang perlu ikut

- `AGENT_GUIDE.md`, `PROJECT_CONTEXT.md`: aturan dan arsitektur repo.
- `pipeline_defs/`, `skills/pipelines/explainer/`, `skills/meta/`, `schemas/`: tahapan produksi, pemeriksaan dan checkpoint.
- `.agents/skills/`: knowledge tool/provider, termasuk Remotion, 3D, audio dan FFmpeg. `.claude/skills/` memuat skill untuk Claude.
- `portable/CREATOR_PROFILE.md`, custom skill `neon-reels`: identitas neon, suara, tempo, hook, subtitle dan MP4.
- `portable/runtime.json`, requirements dan composer lockfile: versi serta pengaturan yang dapat diulang.
- `portable/examples/calendar-neon/`: contoh source video kalender terakhir untuk mempelajari mekanik. Audio/render tidak ikut; ini tidak otomatis menghasilkan video baru.

Folder `projects/` dan `remotion-composer/projects/` diabaikan Git. Jika ingin melanjutkan proyek tertentu pada komputer lain, arsipkan folder proyek tersebut secara sadar beserta source/artifact/aset yang diperlukan; paket dasar ini tidak membawa seluruh riwayat produksi. Jangan mengira `git push` biasa menyertakan proyek yang di-ignore.

## 8. Masalah yang sering muncul

| Gejala | Perbaikan |
|---|---|
| Piper unavailable di registry | Jalankan agen lewat `portable/run.sh`; `.venv/bin` harus ada pada PATH. |
| Suara robotik seperti eSpeak | Pastikan model neural `.onnx` di `.runtime/piper/`; jangan pakai fallback eSpeak. |
| `No module named onnx` / alignment kosong | Ulang bootstrap; profil memasang optional dependency ONNX untuk native alignment. |
| Model gagal download | Periksa koneksi/proxy, akses `github.com` dan `release-assets.githubusercontent.com`; jangan mematikan TLS. |
| npm/Node gagal | Cek Node22+, npm dan akses registry.npmjs.org; ulang npm ci dari composer. Jangan hapus lockfile agar "lolos". |
| Browser tidak ditemukan | Jalankan `npx --no-install remotion browser ensure` dari `remotion-composer`, atau tentukan `REMOTION_BROWSER_EXECUTABLE` sebagai path browser lokal. |
| Browser Linux gagal startup | Pasang library browser di atas; periksa render.log. Tidak perlu menyalin `/usr/bin/chromium` dari cloud. |
| WebGL blank/kehabisan RAM | Gunakan `--gl=swangle`, concurrency2, dan periksa frame tes. |
| Angka kalender berkedip | Pisahkan kedalaman tekstur dari permukaan backing; jangan buat bidang coplanar. |
| Save environment cloud gagal | Tidak relevan pada setup lokal; `.venv` dan `.runtime` dikelola di filesystem komputer. |
| Error API ElevenLabs | Profil default tidak memanggil ElevenLabs. Periksa decision_log agar agen tidak memakai keputusan lama. |

Untuk jaringan terbatas, tujuan setup umumnya github.com/release-assets.githubusercontent.com, pypi.org/files.pythonhosted.org, registry.npmjs.org dan host browser yang diminta Remotion. Login/LLM membutuhkan domain provider CLI yang dipilih. Izinkan lewat kebijakan jaringan yang didukung, bukan bypass proxy.

## 9. Lisensi dan batas verifikasi

Lisensi source OpenMontage tetap ada di `LICENSE` (AGPL-3.0); sertakan saat mendistribusikan paket. Engine Piper, package lain dan model suara memiliki lisensi masing-masing. Archive resmi model yang dipakai memiliki MODEL_CARD yang tampaknya tersalin dari bahasa/model lain; checksum dan identitas bahasa Indonesia terverifikasi, tetapi **izin komersial model ini belum dikonfirmasi dari kartu tersebut**. Konfirmasi kepada distributor/pemilik model sebelum menjadikannya dasar penggunaan komersial, atau pilih model dengan hak yang jelas melalui persetujuan baru. Checksum membuktikan integritas file, bukan izin lisensinya.

Tes sesi ini berjalan di Linux cloud. Instalasi baru macOS/WSL2, login ketiga CLI, biaya akun, dan akses provider harus diverifikasi di komputer tujuan; tidak diklaim sudah diuji hanya karena guide tersedia.
