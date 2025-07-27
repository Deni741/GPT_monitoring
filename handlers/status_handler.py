import os
import hmac
import hashlib
from flask import Blueprint, request, abort

github_updater = Blueprint("github_updater", __name__)

GITHUB_SECRET = os.getenv("GITHUB_SECRET")
REPO_PATH = "/root/GPT_monitoring"

def verify_signature(secret, payload, signature):
    mac = hmac.new(secret.encode(), msg=payload, digestmod=hashlib.sha256)
    expected = f"sha256={mac.hexdigest()}"
    return hmac.compare_digest(expected, signature)

@github_updater.route("/webhook", methods=["POST"])
def webhook():
    signature = request.headers.get("X-Hub-Signature-256")
    if not signature:
        abort(400, "Missing signature")

    if not verify_signature(GITHUB_SECRET, request.data, signature):
        abort(403, "Invalid signature")

    try:
        os.system(f"cd {REPO_PATH} && git pull")
        return "Updated successfully", 200
    except Exception as e:
        return f"Update failed: {e}", 500
