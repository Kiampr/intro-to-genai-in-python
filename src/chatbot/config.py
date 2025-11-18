import yaml
from pathlib import Path
from enum import Enum
from typing import Dict


class LLMType(Enum):
    LOCAL = "local"
    REMOTE = "remote"


class Config:
    def __init__(self):
        config_path = Path(__file__).parent.parent / "config.yaml"
        with open(config_path, encoding="utf-8") as f:
            config = yaml.safe_load(f)
            self._llm_config = config["llm_config"]
            self._log_level = config["log_level"]

    def get_llm_type(self) -> LLMType:
        return LLMType(self._llm_config["type"])

    def get_llm_config(self) -> Dict:
        return self._llm_config

    def get_log_level(self) -> str:
        return self._log_level


config = Config()
