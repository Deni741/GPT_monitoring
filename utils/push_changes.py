import os
from git import Repo

# Завантажуємо шлях до репозиторію
repo_dir = os.path.dirname(os.path.abspath(__file__))
repo = Repo(repo_dir, search_parent_directories=True)

# Додаємо всі зміни
repo.git.add('--all')

# Комітимо з англомовним повідомленням
repo.index.commit("Autopush from server")

# Пушимо на GitHub
origin = repo.remote(name='origin')
origin.push()
