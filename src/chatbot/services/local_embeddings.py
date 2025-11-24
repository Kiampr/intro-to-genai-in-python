from langchain_openai.embeddings import OpenAIEmbeddings
from pydantic import SecretStr
from chatbot.config import config


class LocalEmbeddings(OpenAIEmbeddings):
    """Represents a locally-hosted Ollama embeddings service
    Usage:
         embeddings_service = LocalEmbeddings()
         text = "Hi"
         embeddings = embeddings_service.embed_query(text)
    """

    def __init__(self, **kwargs):
        # fetch service configuration from the config file
        service_config = config.get_embeddings_config()

        # establish connection to service
        super().__init__(
            model=service_config["model"],
            base_url="http://127.0.0.1:11434/v1",
            api_key=SecretStr("dummy"),
            **kwargs,
        )
