import os
import subprocess
from datetime import datetime

# === Завантаження змінних ===
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO_URL = "https://github.com/Deni741/GPT_monitoring.git"
BRANCH = "main"
LOCAL_REPO_DIR = "/root/GPT_monitoring"

# === Ім'я безпечної версії .env (без секретів) ===
SAFE_ENV_PATH = os.path.join(LOCAL_REPO_DIR, ".env.safe")
ENV_PATH = os.path.join(LOCAL_REPO_DIR, ".env")

def prepare_safe_env():
    """
    Створює безпечну копію .env без чутливих токенів
    """
    if not os.path.exists(ENV_PATH):
        print("[ERROR] .env not found")
        return

    with open(ENV_PATH, "r") as f:
        lines = f.readlines()

    safe_lines = []
    for line in lines:
        if any(key in line for key in ["TELEGRAM_TOKEN", "OPENAI_API_KEY", "GITHUB_TOKEN", "GPT_CONTROLLER_TOKEN"]):
            continue
        safe_lines.append(line)

    with open(SAFE_ENV_PATH, "w") as f:
        f.writelines(safe_lines)

    print("[INFO] Created .env.safe without secrets")

def git_push():
    """
    Виконує git add → commit → push
    """
    try:
        os.chdir(LOCAL_REPO_DIR)
        subprocess.run(["git", "config", "user.email", "gpt_monitoring@auto.com"], check=True)
        subprocess.run(["git", "config", "user.name", "GPT Monitoring Bot"], check=True)

        subprocess.run(["git", "add", "."], check=True)

        commit_msg = f"Автопуш від GPT {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)

        repo_with_token = REPO_URL.replace("https://", f"https://{GITHUB_TOKEN}@")
        subprocess.run(["git", "push", repo_with_token, BRANCH], check=True)

        print("[INFO] Зміни запушено успішно.")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Git push failed: {e}")

if __name__ == "__main__":
    prepare_safe_env()
    git_push()
