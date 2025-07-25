import os

def save_code_to_file(code: str, file_path: str) -> str:
    try:
        # Забезпечуємо, що директорія існує
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Записуємо код у файл
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(code.strip() + '\n')

        return f"✅ Файл успішно створено: {file_path}"
    except Exception as e:
        return f"❌ Помилка під час збереження файлу: {e}"
