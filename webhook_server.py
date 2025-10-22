#from future import annotations
from flask import Flask, request, jsonify
import hmac, hashlib, os, logging, subprocess, json
from pathlib import Path

# ---------- базові речі ----------
BASE_DIR = Path(__file__).resolve().parent
LOGS_DIR = BASE_DIR / "logs"
LOGS_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    handlers=[
        logging.FileHandler(LOGS_DIR / "webhook.log", encoding="utf-8"),
        logging.StreamHandler()
    ],
)
log = logging.getLogger("webhook_server")

# .env (не обов'язково; просто не падаємо, якщо відсутній)
try:
    from dotenv import load_dotenv
    load_dotenv(BASE_DIR / ".env")
except Exception:
    pass

# ---------- налаштування ----------
# Секрет з GitHub webhook (якщо порожній — підпис перевіряти не будемо)
SECRET_RAW = os.getenv("GITHUB_WEBHOOK_SECRET", "") or ""
VERIFY = (os.getenv("VERIFY_SIGNATURE", "true").lower() not in {"0","false","no","off"})
SECRET = SECRET_RAW.encode() if SECRET_RAW else b""

# Повний шлях до скрипту оновлення
UPDATE_SCRIPT = str(BASE_DIR / "scripts" / "git_update.sh")

# Яку гілку приймаємо
TARGET_REF = os.getenv("WEBHOOK_BRANCH", "refs/heads/main")

# ---------- хелпери ----------
def _verify_signature(req) -> bool:
    """Перевіряємо X-Hub-Signature-256. Якщо VERIFY=false або секрет порожній — пропускаємо (діагностика/стенд)."""
    if not VERIFY or not SECRET:
        log.warning("Signature verification is DISABLED for diagnostics.")
        return True

    sig = req.headers.get("X-Hub-Signature-256", "")
    if not sig.startswith("sha256="):
        log.error("Missing/invalid X-Hub-Signature-256 header.")
        return False

    digest = "sha256=" + hmac.new(SECRET, req.data, hashlib.sha256).hexdigest()
    ok = hmac.compare_digest(digest, sig)
    if not ok:
        log.error(f"Signature mismatch. expected={digest} got={sig}")
    return ok


def _run_update_async() -> None:
    """
    Запускаємо скрипт оновлення неблокуюче.
    Використовуємо systemd-run якщо є, інакше — subprocess.Popen.
    """
    try:
        # спроба через systemd-run (гарно логується в journalctl)
        subprocess.Popen(
            ["systemd-run", "--unit=gpt-webhook-update", "--same-dir", UPDATE_SCRIPT],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        log.info("Triggered git_update via systemd-run.")
    except FileNotFoundError:
        # fallback: просто фонова команда
        subprocess.Popen(
            [UPDATE_SCRIPT],
            cwd=str(BASE_DIR),
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        log.info("Triggered git_update via subprocess (fallback).")


# ---------- Flask ----------
app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    # 1) перевірка підпису
    if not _verify_signature(request):
        return "Invalid signature", 401

    # 2) витягуємо тип події
    event = request.headers.get("X-GitHub-Event", "")
    payload = request.get_json(silent=True) or {}

    # 3) обробляємо тільки push у потрібну гілку
    if event == "push":
        ref = payload.get("ref", "")
        log.info(f"Webhook OK: event=push ref={ref}")
        if ref == TARGET_REF:
            _run_update_async()
            return jsonify(ok=True), 200
        else:
            log.info(f"Ignored: ref {ref} != {TARGET_REF}")
            return jsonify(ignored=True), 200

    # Інші події можна ігнорити/логувати
    log.info(f"Ignored event type: {event}")
    return jsonify(ignored=True), 200


if __name__ == "__main__":
    # Локальний запуск (systemd і так підніме через ExecStart)
    app.run(host="0.0.0.0", port=5000)
