import logging
import sys
from pathlib import Path
from typing import List
from chatbot.utils.logging import configure_logging
from chatbot.start_chat import (
    start_chat_services,
    stop_chat_services,
    run_on_this_process,
)

logger = logging.getLogger(__name__)


def start_streamlit(argv: List[str] | None = None) -> int:
    streamlit_app_path = Path(__file__).parent / "app.py"
    streamlit_cmd = [
        "streamlit",
        "run",
        str(streamlit_app_path.resolve()),
        "--server.address",
        "127.0.0.1",
    ]
    if argv:
        streamlit_cmd += ["--"] + argv
    return run_on_this_process(cmd=streamlit_cmd)


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
