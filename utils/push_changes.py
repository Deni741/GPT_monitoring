import os
import subprocess
from dotenv import load_dotenv

load_dotenv(dotenv_path='.env')

def push_changes(commit_message="Автоматичний push з сервера"):
    repo_path = os.getcwd()
    github_token = os.getenv("GITHUB_TOKEN")

    if not github_token:
        print("❌ GITHUB_TOKEN не знайдено в .env")
        return

    try:
        subprocess.run(["git", "add", "."], cwd=repo_path, check=True)
        subprocess.run(["git", "commit", "-m", commit_message], cwd=repo_path, check=True)
        subprocess.run(["git", "push"], cwd=repo_path, check=True)
        print("✅ Зміни успішно запушені на GitHub.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Помилка при пуші: {e}")

if __name__ == "__main__":
    push_changes()
