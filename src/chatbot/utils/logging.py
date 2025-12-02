import logging
from rich.logging import RichHandler
from chatbot.config import config


def configure_logging() -> None:
    # setup console log coloring handler
    handler = RichHandler(
        rich_tracebacks=True,  # Enable rich tracebacks
        show_time=False,  # Disable timestamps
        show_level=True,  # Show log levels
        show_path=False,  # Disable file path display
    )

    level = logging.getLevelNamesMapping().get(config.get_log_level().upper())
    logging.basicConfig(level=level, format="%(message)s", handlers=[handler])

    # suppress some the 3rd party packages INFO logging, to reduce clutter
    for logger_name in ["httpx", "mcp"]:
        logging.getLogger(logger_name).setLevel(logging.ERROR)
