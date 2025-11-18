import logging
import os
import subprocess
import socket
from typing import List, Dict
from chatbot.config import config, LLMType

logger = logging.getLogger(__name__)
_processes: Dict[str, subprocess.Popen | None] = {}


def is_port_open(host: str, port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        return sock.connect_ex((host, port)) == 0


def start_on_separate_process(
    name: str,
    cmd: List[str],
    host: str,
    port: int,
    env: Dict[str, str] = os.environ.copy(),
) -> None:
    # check if not already running
    if not is_port_open(host, port):
        logger.info(f"Launching {name}:\n{' '.join(cmd)}")
        _processes[name] = subprocess.Popen(
            cmd, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )


def start_on_this_process(
    name: str, cmd: List[str], env: Dict[str, str] = os.environ.copy()
) -> int:
    logger.info(f"Launching {name}:\n{' '.join(cmd)}")
    try:
        return subprocess.call(cmd, env=env)
    except KeyboardInterrupt:
        logger.warning("Interrupted by user. Shutting down...")
        return 130


def stop_chat_services():
    # stop the separate processes we started
    for name, process in _processes.items():
        if process and process.poll() is None:
            logger.info(f"Terminating process '{name}'...")
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                logger.warning(f"Process '{name}' did not exit in time. Killing...")
                process.kill()


def start_chat_services():
    if config.get_llm_type() == LLMType.LOCAL:
        # start ollama server to avoid latency on first prompt
        start_on_separate_process(
            name="ollama serve", cmd=["ollama", "serve"], host="localhost", port=11434
        )
        # pull requested model
        llm_config = config.get_llm_config()
        ollama_model = llm_config["model"]
        try:
            start_on_this_process(
                name="ollama pull", cmd=["ollama", "pull", ollama_model]
            )
        except Exception:
            logger.exception("Failed to pull local LLM")
