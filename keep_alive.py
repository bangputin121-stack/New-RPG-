import os
from flask import Flask
from threading import Thread
import logging

app = Flask(__name__)
log = logging.getLogger("werkzeug")
log.setLevel(logging.ERROR)  # Suppress Flask request logs


@app.route("/")
def home():
    return "⚔️ Legends of Eternity Bot — Online!"


@app.route("/health")
def health():
    return {"status": "ok", "bot": "Legends of Eternity"}


def run():
    # Railway/Heroku inject PORT via env var; fallback 8080 untuk Replit/local
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=False, use_reloader=False)


def keep_alive():
    # Di Railway, keep_alive hanya dibutuhkan jika kamu deploy sebagai "Web Service".
    # Kalau deploy sebagai "Worker/Background Service", skip Flask (set env ENABLE_KEEP_ALIVE=0).
    if os.environ.get("ENABLE_KEEP_ALIVE", "1") == "0":
        return
    t = Thread(target=run, daemon=True)
    t.start()
