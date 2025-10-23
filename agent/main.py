import os
import json
import time
import sys
import logging
from logging.handlers import RotatingFileHandler
from dataclasses import dataclass
from dotenv import load_dotenv
from pathlib import Path
from utils.telegram import notify

# --- Шляхи ---
BASE_DIR = Path(__file__).resolve().parents[1]
LOGS_DIR = BASE_DIR / "logs"
LOGS_DIR.mkdir(exist_ok=True)

# --- Логер ---
def setup_logger() -> logging.Logger:
    logger = logging.getLogger("agent")
    logger.setLevel(logging.INFO)

    fmt = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(module)s:%(lineno)d - %(message)s")

    # Файл логів
    fh = RotatingFileHandler(LOGS_DIR / "agent.log", maxBytes=5 * 1024 * 1024, backupCount=10, encoding="utf-8")
    fh.setFormatter(fmt)
    fh.setLevel(logging.INFO)
    logger.addHandler(fh)

    # Консоль
    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(fmt)
    ch.setLevel(logging.INFO)
    logger.addHandler(ch)

    return logger


logger = setup_logger()

# --- ENV ---
load_dotenv(BASE_DIR / ".env")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini").strip()

# --- OpenAI клієнт ---
def do_llm_prompt(prompt: str) -> str:
    try:
        from openai import OpenAI
        client = OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "You are a helpful AI agent."},
                {"role": "user", "content": prompt},
            ],
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"[ERROR] {e}"

# --- Конфіг ---
CONFIG_PATH = BASE_DIR / "agent" / "instruction.json"
TASKS_PATH = BASE_DIR / "data" / "tasks.jsonl"

@dataclass
class Config:
    goals: list
    tick_seconds: int = 15
    dry_run: bool = False

    @classmethod
    def load(cls) -> "Config":
        if CONFIG_PATH.exists():
            data = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
            return cls(
                goals=data.get("goals", []),
                tick_seconds=int(data.get("tick_seconds", 15)),
                dry_run=bool(data.get("dry_run", False))
            )
        return cls(goals=[])

# --- Завдання ---
def read_task() -> dict | None:
    if TASKS_PATH.exists():
        try:
            with open(TASKS_PATH, "r", encoding="utf-8") as f:
                lines = f.readlines()
            if lines:
                task = json.loads(lines[-1])
                return task
        except Exception as e:
            logger.error(f"Read task error: {e}")
    return None

# --- Обробка завдань ---
def process_task(task: dict) -> None:
    task_type = task.get("type", "").strip().lower()
    logger.info(f"Processing task type: {task_type}")

    if task_type == "note":
    text = task.get("task", "")
    if text:
        logger.info(f"NOTE: {text}")
        # 🔔 Надсилаємо повідомлення в Telegram
        notify(f"🗒️ <b>Note отримано:</b>\n{text}")

        answer = do_llm_prompt(f"Коротко підтвердь отримання нотатки і дії: {text}")
        logger.info(f"LLM: {answer}")

    elif task_type == "test":
        logger.info(f"🧠 Test task received: {task}")
        print("✅ Agent test successful! The system is working correctly.")

    else:
        logger.warning(f"Unknown task type: {task_type}")

# --- Heartbeat ---
def heartbeat(cfg: Config) -> None:
    logger.info(f"Heartbeat | goals={cfg.goals} | dry_run={cfg.dry_run}")

# --- Основний цикл ---
def main_loop() -> None:
    logger.info("Agent started.")
    while True:
        try:
            cfg = Config.load()
            heartbeat(cfg)
            task = read_task()
            if task:
                logger.info(f"Processing task: {task}")
                process_task(task)
        except Exception as e:
            logger.exception(f"Main loop error: {e}")
        time.sleep(cfg.tick_seconds)

# --- Одноразовий запуск ---
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--once", action="store_true")
    args = parser.parse_args()

    logger.info("OpenAI client initialized.")

    if args.once:
        logger.info("🧩 Agent launched (single run mode).")
        cfg = Config.load()
        heartbeat(cfg)
        task = read_task()
        if task:
            process_task(task)
        else:
            logger.info("No tasks in queue.")
    else:
        main_loop()
