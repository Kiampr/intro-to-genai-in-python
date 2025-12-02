from typing import Type
from langchain_core.vectorstores import VectorStore as BaseVectorStore
from .local_vectordb import LocalVectorDB

VectorDB: Type[BaseVectorStore] = LocalVectorDB
