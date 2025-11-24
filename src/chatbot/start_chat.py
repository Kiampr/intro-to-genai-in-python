import logging
import os
import requests
import subprocess
import socket
from typing import List, Dict
from chatbot.config import config, ServiceType

logger = logging.getLogger(__name__)
_processes: Dict[str, subprocess.Popen | None] = {}


def is_port_open(host: str, port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        return sock.connect_ex((host, port)) == 0


def run_on_separate_process(
    name: str,
    cmd: List[str],
    host: str,
    port: int,
    env: Dict[str, str] = os.environ.copy(),
) -> None:
    # check if not already running
    if not is_port_open(host, port):
        logger.info(f"Running new process `{name}` with command: {' '.join(cmd)}")
        _processes[name] = subprocess.Popen(
            cmd, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )


def run_on_this_process(cmd: List[str], env: Dict[str, str] = os.environ.copy()) -> int:
    logger.info(f"Running command: {' '.join(cmd)}")
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
    # preload local services to avoid latency on first prompt
    service_configs = [config.get_llm_config(), config.get_embeddings_config()]
    service_endpoint_paths = ["api/generate", "api/embeddings"]
    service_endpoint_host = "127.0.0.1"
    service_endpoint_port = 11434
    service_test_payloads = [
        {"messages": [{"role": "user", "content": "Hi"}], "stream": False},
        {"input": "Hi"},
    ]
    for service_config, service_endpoint_path, service_test_payload in zip(
        service_configs, service_endpoint_paths, service_test_payloads
    ):
        if service_config["type"] == ServiceType.LOCAL:
            # download the model, if not present
            model = service_config["model"]
            cmd = ["ollama", "pull", model]
            exit_code = run_on_this_process(cmd=cmd)
            if exit_code != 0:
                logger.error(f"Failed to fetch model `{model}`: exit code {exit_code}")
            else:
                # send a dummy test query
                url = f"http://{service_endpoint_host}:{service_endpoint_port}/{service_endpoint_path}"
                payload = {"model": model, **service_test_payload}
                response = requests.post(url=url, json=payload, timeout=360)
                response.raise_for_status()
