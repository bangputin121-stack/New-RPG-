# 🚂 Panduan Deploy ke Railway

Bot ini sekarang **siap di-deploy ke Railway**. Ikuti langkah di bawah berurutan.

---

## ⚠️ LAKUKAN DULU SEBELUM APA-APA

### 1. Revoke token lama (WAJIB)
Token lama di file `env.` sudah bocor. Generate baru:

1. Buka [@BotFather](https://t.me/BotFather) di Telegram
2. Ketik `/mybots` → pilih bot kamu → **API Token** → **Revoke**
3. BotFather kasih token baru. **Salin, jangan ditempel ke file apa pun.**

### 2. Ganti Telegram ID super admin
Edit `database.py` baris ~13:
```python
SUPER_ADMIN_IDS = [
    123456789,  # ← ganti dengan ID Telegram kamu
]
```
Cara cek ID Telegram: chat [@userinfobot](https://t.me/userinfobot), dia akan balas ID-nya.

---

## 🚀 Deploy ke Railway (cara paling mudah: GitHub)

### Langkah 1 — Push ke GitHub
```bash
cd fixed_bot
git init
git add .
git commit -m "Initial deploy"
git remote add origin https://github.com/username/nama-repo.git
git push -u origin main
```

File `.gitignore` sudah saya siapkan — `env.`, `.env`, dan folder `data/` tidak akan ikut ter-push.

### Langkah 2 — Buat project Railway
1. Buka [railway.app](https://railway.app) → **New Project** → **Deploy from GitHub repo**
2. Pilih repo bot kamu → Railway otomatis deteksi Python dari `requirements.txt`

### Langkah 3 — Set environment variable
Di project Railway → tab **Variables** → tambahkan:

| Variable | Value |
|---|---|
| `BOT_TOKEN` | Token baru dari BotFather |
| `ENABLE_KEEP_ALIVE` | `0` |
| `TZ` | `Asia/Jakarta` (biar reset daily/weekly sesuai WIB) |

### Langkah 4 — WAJIB: Bikin Volume untuk data persisten
Ini paling penting. **Tanpa Volume, semua data pemain (player, market, admin, ban) akan hilang setiap kali redeploy!**

1. Di project Railway → klik service kamu → tab **Settings**
2. Scroll ke **Volumes** → **+ New Volume**
3. Mount Path: `/app/data`
4. Save → Railway akan redeploy otomatis

### Langkah 5 — Verify
Tab **Deployments** → lihat log. Kalau muncul:
```
⚔️  Legends of Eternity v9.0 — READY!
✅ Bot commands registered.
```
→ bot sudah jalan. Coba `/start` di Telegram.

---

## 🔧 Konfigurasi yang sudah saya siapkan di folder `fixed_bot/`

| File | Fungsi |
|---|---|
| `Procfile` | Bilang ke Railway: jalankan `python3 bot.py` sebagai worker |
| `railway.toml` | Auto-restart kalau crash (max 10x) |
| `runtime.txt` | Lock Python ke 3.11.9 (versi stabil untuk python-telegram-bot 20.7) |
| `.gitignore` | Blokir file rahasia dari git |
| `.env.example` | Template env var untuk developer lain |
| `keep_alive.py` | Sudah support `PORT` dinamis Railway + bisa di-disable via env |

---

## ❓ Troubleshooting

### Bot langsung crash dengan "BOT_TOKEN belum diset"
→ Kamu belum set `BOT_TOKEN` di Variables. Cek lagi tab Variables di Railway.

### Bot jalan tapi pesan tidak di-response
→ Mungkin token sudah di-revoke di sisi Telegram tapi Railway masih pakai yang lama. Update variable `BOT_TOKEN` dengan token baru → Railway auto-redeploy.

### Data hilang setiap deploy
→ Volume belum di-mount ke `/app/data`. Ikuti Langkah 4 di atas.

### Reset daily quest nggak tepat jam 00:00 WIB
→ Set env var `TZ=Asia/Jakarta`. Railway container default UTC.

### Error "conflict: terminated by other getUpdates request"
→ Bot sedang jalan di 2 tempat sekaligus (misal: di laptop lokal & Railway). Matikan yang lokal. Telegram cuma izinkan 1 polling per bot.

### RAM/CPU kepake banyak
→ `python-telegram-bot` dengan polling normal cukup di ~200 MB RAM. Railway free tier ($5 credit/bulan) cukup untuk bot skala kecil-menengah.

---

## 💡 Tips tambahan

- **Pakai Railway CLI** biar bisa lihat log real-time: `npm i -g @railway/cli` → `railway login` → `railway logs`
- **Backup data rutin** — walaupun sudah pakai Volume, tetap copy `players.json` manual sesekali lewat Railway Shell
- **Health check URL** — kalau mau deploy sebagai "Web Service" untuk monitoring (UptimeRobot dsb), set `ENABLE_KEEP_ALIVE=1`, Railway akan expose URL publik `/health`

Selamat deploy! 🚀
