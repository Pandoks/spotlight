from typing import List, Optional, TypedDict
from chromadb.api import ClientAPI
from chromadb.api.models.Collection import Collection
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
import chromadb


class ChromaSetupConfig(TypedDict):
    collection_name: str
    embedding_function: Optional[Embeddings]
    persistent_directory: Optional[str]


class ChromaStoreConfig(TypedDict):
    documents: List[Document]
    database: Chroma


# https://python.langchain.com/v0.1/docs/integrations/vectorstores/chroma/
def setup_database(config: ChromaSetupConfig) -> ClientAPI:
    database_client = None
    if config["persistent_directory"]:
        database_client = chromadb.PersistentClient(path=config["persistent_directory"])
    else:
        database_client = chromadb.Client()
    database_client.get_or_create_collection(config["collection_name"])
    return database_client


def upsert(config: ChromaStoreConfig) -> List[str]:
    return config["database"].add_documents(config["documents"])
