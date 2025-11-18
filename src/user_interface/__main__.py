import logging
import sys
from pathlib import Path
from typing import List
from chatbot.utils.logging import configure_logging
from chatbot.start_chat import (
    start_chat_services,
    stop_chat_services,
    start_on_this_process,
)

logger = logging.getLogger(__name__)


def start_streamlit(argv: List[str] | None = None) -> int:
    streamlit_app_path = Path(__file__).parent / "app.py"
    streamlit_cmd = [
        "streamlit",
        "run",
        str(streamlit_app_path),
        "--server.address",
        "localhost",
    ]
    if argv:
        streamlit_cmd += ["--"] + argv
    return start_on_this_process(name="streamlit", cmd=streamlit_cmd)


def main() -> int:
    configure_logging()
    try:
        start_chat_services()
        exit_code = start_streamlit()
    except Exception:
        logger.exception("Unhandled exception")
        exit_code = 1
    finally:
        stop_chat_services()
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
