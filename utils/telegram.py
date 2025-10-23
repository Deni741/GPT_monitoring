import os, requests

BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
CHAT_ID  = os.getenv("TELEGRAM_CHAT_ID", "").strip()

def notify(text: str) -> bool:
    """Відправити просте повідомлення в TG. Повертає True/False."""
    if not BOT_TOKEN or not CHAT_ID:
        return False
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        r = requests.post(url, json={"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"}, timeout=5)
        return r.ok
    except Exception:
        return False
