from typing import Type
from langchain_core.language_models import BaseChatModel
from .local_llm import LocalLLM
from .remote_llm import RemoteLLM
from chatbot.config import config, LLMType

LLM: Type[BaseChatModel] = (
    LocalLLM if config.get_llm_type() == LLMType.LOCAL else RemoteLLM
)
