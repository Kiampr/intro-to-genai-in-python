import logging
import os
from langchain_openai.embeddings import AzureOpenAIEmbeddings
from pydantic import SecretStr
from chatbot.config import config

logger = logging.getLogger(__name__)


class RemoteEmbeddings(AzureOpenAIEmbeddings):
    """Represents a cloud-hosted OpenAI embeddings service
    Usage:
         embeddings_service = RemoteEmbeddings()
         text = "Hi"
         embeddings = embeddings_service.embed_query(text)
    """

    def __init__(self, **kwargs):
        # fetch service configuration from the config file
        service_config = config.get_embeddings_config()

        # retrieve API key from the environment variable
        auth_config = service_config["authentication"]
        api_key = os.getenv(auth_config["api_key_env_var"]) or ""

        # establish connection to service
        super().__init__(
            api_key=SecretStr(api_key),
            api_version=service_config["api_version"],
            azure_deployment=service_config["model"],
            azure_endpoint=service_config["endpoint"],
            default_headers=service_config["extra_headers"],
            **kwargs,
        )
