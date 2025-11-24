import yaml
from pathlib import Path
from enum import StrEnum
from typing import Any, Dict


class ServiceType(StrEnum):
    LOCAL = "local"
    REMOTE = "remote"


class Config:
    def __init__(self):
        config_path = Path(__file__).parent.parent / "config.yaml"
        with open(config_path, encoding="utf-8") as f:
            config: Dict[str, Any] = yaml.safe_load(f)
            self._llm_config: Dict[str, Any] = config["llm_config"]
            self._embeddings_config: Dict[str, Any] = config["embeddings_config"]
            self._log_level: str = config["log_level"]

    def get_llm_type(self) -> ServiceType:
        return ServiceType(self._llm_config["type"])

    def get_llm_config(self) -> Dict[str, Any]:
        return self._llm_config.copy()

    def get_embeddings_type(self) -> ServiceType:
        return ServiceType(self._embeddings_config["type"])

    def get_embeddings_config(self) -> Dict[str, Any]:
        return self._embeddings_config.copy()

    def get_log_level(self) -> str:
        return self._log_level


config = Config()
