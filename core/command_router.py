# core/command_router.py

def command_router(command: str) -> str:
    if command == "/ping":
        return "pong"
    return "Unknown command"
