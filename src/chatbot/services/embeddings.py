from typing import Type
from langchain_core.embeddings import Embeddings as BaseEmbeddingsModel
from .local_embeddings import LocalEmbeddings
from .remote_embeddings import RemoteEmbeddings
from chatbot.config import config, ServiceType

Embeddings: Type[BaseEmbeddingsModel] = (
    LocalEmbeddings
    if config.get_embeddings_type() == ServiceType.LOCAL
    else RemoteEmbeddings
)
