from langchain_openai import ChatOpenAI
from pydantic import SecretStr
from chatbot.config import config


class LocalLLM(ChatOpenAI):
    """Represents a locally-hosted LLM service orchestrated by Ollama
    Usage:
         llm_service = LocalLLM()
         messages = [user_message(content="Hi")]
         answer = llm_service.invoke(messages)
    """

    def __init__(self, **kwargs):
        # fetch service configuration from the config file
        service_config = config.get_llm_config()

        # establish connection to service
        super().__init__(
            model=service_config["model"],
            base_url="http://127.0.0.1:11434/v1",
            api_key=SecretStr("dummy"),
            **kwargs,
        )
