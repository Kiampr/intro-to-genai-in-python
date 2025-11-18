from langchain_openai import ChatOpenAI
from langchain_core.utils import convert_to_secret_str
from chatbot.config import config


class LocalLLM(ChatOpenAI):
    """Represents a locally-hosted Ollama LLM
    Usage:
         llm = LocalLLM()
         messages = [user_message(content="Hi")]
         answer = llm.invoke(messages)
    """

    def __init__(self, **kwargs):
        # fetch LLM configuration from the config file
        llm_config = config.get_llm_config()
        super().__init__(
            model=llm_config["model"],
            base_url="http://localhost:11434/v1",
            api_key=convert_to_secret_str("dummy"),
            **kwargs,
        )
