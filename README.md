# Terabox Telegram Downloader Bot (Python)

Ye bot Terabox links ko process karta hai, video ID normalize karta hai, xAPIverse API se stream nikalta hai, ffmpeg se MP4 banata hai aur Telegram par upload karta hai.

## ✅ New Additions
- Port support added: **`PORT=8080`**
- Keep-alive health URL added: `GET /health` (also `/` and `/ping`)
- Optional auto-ping support via `KEEP_ALIVE_URL`

---

## Supported Link Formats

- `https://1024terabox.com/s/<id>`
- `https://terabox.com/s/<id>`
- `https://teraboxlinke.com/v/<id>`

Bot `/s/` aur `/v/` ke baad wali ID extract karta hai aur canonical URL banata hai:

`https://1024terabox.com/s/<video_id>`

---

## Project Structure

```text
app/
├── main.py
├── config.py
├── bot/
│   ├── handlers.py
│   └── messages.py
├── services/
│   ├── terabox_api.py
│   ├── downloader.py
│   ├── telegram_uploader.py
│   ├── cleanup.py
│   └── keep_alive.py
└── utils/
    ├── validators.py
    └── logger.py
```

---

## Environment Variables

```env
API_ID=12345678
API_HASH=your_api_hash
BOT_TOKEN=123456:ABCDEF

XAPIVERSE_API_URL=https://xapiverse.com/api/terabox-pro
XAPIVERSE_KEY=your_xapiverse_key

TEMP_DIR=./temp
DEFAULT_QUALITY=480p
MAX_CONCURRENT_JOBS=2
REQUEST_TIMEOUT=45
FFMPEG_BIN=ffmpeg

PORT=8080
KEEP_ALIVE_URL=
KEEP_ALIVE_INTERVAL=300
```

---

## Local Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python -m app.main
```

---

## Keep Alive / Health Check

- Health endpoint: `http://<your-host>:8080/health`
- Same response: `/` and `/ping`
- Response: `{"status":"ok"}`

Agar `KEEP_ALIVE_URL` set karoge, bot background me har `KEEP_ALIVE_INTERVAL` seconds me us URL ko ping karega.

---

## Deploy se pehle kya kya karna hoga (Important)

1. **Telegram bot ready karo**
   - `BOT_TOKEN` from BotFather
   - `API_ID` + `API_HASH` from my.telegram.org

2. **xAPIverse key ready rakho**
   - `XAPIVERSE_KEY` valid hona chahiye

3. **Render service create karo**
   - `render.yaml` use karo (ab `type: web` + `PORT=8080`)

4. **Environment variables set karo**
   - `API_ID`, `API_HASH`, `BOT_TOKEN`, `XAPIVERSE_KEY`
   - Optional: `KEEP_ALIVE_URL` (e.g. your Render app `/health` URL)

5. **ffmpeg check**
   - Agar native build me issue aaye to Docker deploy use karo (`Dockerfile` included).

6. **Manual preflight test**
   - App logs me startup confirm karo
   - Browser/curl se `https://<render-domain>/health` hit karo
   - Telegram me `/start` bhejo
   - Ek valid Terabox link bhej kar full flow test karo

---

## Render Deploy

`render.yaml` included hai. Typical start command:

```bash
python -m app.main
```

Health check ke liye `https://<render-domain>/health` use kar sakte ho.

---

## Security Notes

- API keys kabhi repo me hardcode mat karo.
- `.env` local rakho, Render dashboard me secrets set karo.
- Invalid links reject hote hain, but production me rate limit add karna recommended hai.
