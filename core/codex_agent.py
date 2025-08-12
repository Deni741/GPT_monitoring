import os
import requests

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO_OWNER = "Deni741"
REPO_NAME = "GPT_monitoring"

def github_api(method, endpoint, data=None):
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}{endpoint}"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    response = requests.request(method, url, headers=headers, json=data)
    if response.status_code >= 300:
        raise Exception(f"GitHub API error: {response.status_code}, {response.text}")
    return response.json()

def push_file(file_path, commit_message):
    with open(file_path, "r") as f:
        content = f.read()
    from base64 import b64encode
    b64_content = b64encode(content.encode()).decode()
    github_api(
        "PUT",
        f"/contents/{file_path}",
        {
            "message": commit_message,
            "content": b64_content,
            "branch": "main"
        }
    )
