import faiss
from langchain_community.vectorstores import FAISS
from langchain_community.vectorstores.utils import DistanceStrategy
from langchain_community.docstore.in_memory import InMemoryDocstore
from .embeddings import Embeddings
from chatbot.config import config, VectorDBSimilarityType
from typing import List
import math


class LocalVectorDB(FAISS):
    """Represents a locally-hosted vector store which supports semantic search
    Usage:
         vectordb_service = LocalVectorDB()
         text = "Hi"
         results = vectordb_service.invoke(text)
    """

    def __init__(self, **kwargs):
        # fetch service configuration from the config file
        service_config = config.get_vectordb_config()

        # define embedding function
        embeddings_service = Embeddings()

        def embedding_function(text: str) -> List[float]:
            embeddings = embeddings_service.embed_query(text)
            match service_config["similarity"]:
                case VectorDBSimilarityType.EUCLIDEAN_DISTANCE:
                    return embeddings
                case VectorDBSimilarityType.COSINE:
                    # embeddings need to be normalized for cosine
                    norm = math.sqrt(sum(x * x for x in embeddings))
                    if norm == 0:
                        return embeddings
                    return [x / norm for x in embeddings]
                case _:
                    raise NotImplementedError

        # define index and distance
        embeddings_size = len(embeddings_service.embed_query("dummy"))
        match service_config["similarity"]:
            case VectorDBSimilarityType.EUCLIDEAN_DISTANCE:
                index = faiss.IndexFlatL2(embeddings_size)
                distance_strategy = DistanceStrategy.EUCLIDEAN_DISTANCE
            case VectorDBSimilarityType.COSINE:
                index = faiss.IndexFlatIP(embeddings_size)
                distance_strategy = DistanceStrategy.COSINE
            case _:
                raise NotImplementedError

        # establish connection to service
        super().__init__(
            embedding_function=embedding_function,
            index=index,
            docstore=InMemoryDocstore(),
            index_to_docstore_id={},
            distance_strategy=distance_strategy,
            **kwargs,
        )
