import logging
from pathlib import Path
from chatbot.chatbot_base import BaseChatBot
import importlib
from typing import List

logger = logging.getLogger(__name__)


def list_chatbot_names() -> List[str]:
    """
    Discover chatbot implementations by scanning folders under chatbot/lessons
    Returns: a list of folder names
    """
    chatbot_names: List[str] = []
    lessons_path = Path(__file__).parent.parent / "chatbot" / "lessons"
    if lessons_path.exists():
        for lesson in lessons_path.iterdir():
            if lesson.is_dir() and (lesson / "chatbot.py").is_file():
                chatbot_names.append(lesson.name)
    return chatbot_names


def load_chatbot(name: str) -> BaseChatBot | None:
    """Returns the given chatbot implementation"""
    module_name = f"chatbot.lessons.{name}"
    try:
        # import the chatbot instance from the lessons' __main__.py
        module = importlib.import_module(f"{module_name}.__main__")
        chatbot = getattr(module, "chatbot")
        logger.info(f"Successfully loaded chatbot from {module_name}")
        return chatbot
    except Exception:
        logger.exception(f"Unable to load chatbot implementation from {module_name}")
        return None
