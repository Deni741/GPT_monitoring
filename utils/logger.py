import datetime

def log_and_print(message: str):
    """Виводить повідомлення в консоль і лог (можна розширити на файл)"""
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted = f"[{now}] {message}"
    print(formatted)
