import os
from langchain_core.utils import convert_to_secret_str
from langchain_openai import AzureChatOpenAI
from chatbot.config import config


class RemoteLLM(AzureChatOpenAI):
    """Represents a cloud-hosted OpenAI LLM
    Usage:
         llm = RemoteLLM()
         messages = [user_message(content="Hi")]
         answer = llm.invoke(messages)
    """

    def __init__(self, **kwargs):
        # the API key is retrieved from an environment variable
        # this is more secure than storing it in a (version controlled) file
        llm_api_key = os.getenv("OPENAI_API_KEY") or ""
        # non-confidential configuration for the LLM is retrieved from the config file
        llm_config = config.get_llm_config()
        super().__init__(
            api_key=convert_to_secret_str(llm_api_key),
            api_version=llm_config["api_version"],
            azure_deployment=llm_config["model"],
            azure_endpoint=llm_config["endpoint"],
            default_headers=llm_config["extra_headers"],
            include_response_headers=True,
            **kwargs,
        )
