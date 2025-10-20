from flask import Flask, request, abort
import hmac, hashlib, subprocess, os, sys, datetime

app = Flask(__name__)

REPO_DIR = "/root/GPT_monitoring"
LOG_FILE = f"{REPO_DIR}/logs/webhook.log"
SECRET = os.getenv("GITHUB_WEBHOOK_SECRET", "").encode()

def log(msg):
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{ts}] {msg}\n")
    print(msg, flush=True)

@app.route("/webhook", methods=["POST"])
def webhook():
    signature = request.headers.get("X-Hub-Signature-256")
    if not signature or not SECRET:
        log("⚠️ Missing signature or secret")
        abort(403)

    sha_name, signature = signature.split("=")
    mac = hmac.new(SECRET, msg=request.data, digestmod=hashlib.sha256)
    if not hmac.compare_digest(mac.hexdigest(), signature):
        log("❌ Invalid signature — possible spoofed request")
        abort(403)

    event = request.headers.get("X-GitHub-Event")
    if event != "push":
        log(f"ℹ️ Ignored non-push event: {event}")
        return "ignored", 200

    try:
        log("🔄 Received push event — running git pull...")
        result = subprocess.run(
            ["git", "-C", REPO_DIR, "pull", "--rebase"],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            log(f"✅ Git pull successful:\n{result.stdout}")
        else:
            log(f"❗️ Git pull failed:\n{result.stderr}")
    except Exception as e:
        log(f"🔥 Exception during git pull: {e}")
        abort(500)

    return "ok", 200

if __name__ == "__main__":
    log("🚀 Webhook server started on port 5000")
    app.run(host="0.0.0.0", port=5000)
