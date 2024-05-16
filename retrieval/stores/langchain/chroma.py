from typing import List, Optional, TypedDict
from chromadb.api.types import Where, WhereDocument
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings


class ChromaSetupConfig(TypedDict):
    collection_name: str
    embedding_function: Optional[Embeddings]
    persistent_directory: Optional[str]


class ChromaStoreConfig(TypedDict):
    documents: List[Document]
    database: Chroma


# https://python.langchain.com/v0.1/docs/integrations/vectorstores/chroma/
def setup_database(config: ChromaSetupConfig) -> Chroma:
    database = Chroma(
        collection_name=config["collection_name"],
        embedding_function=config["embedding_function"],
        persist_directory=config["persistent_directory"],
    )
    return database


# def upsert(config: ChromaStoreConfig) -> List[str]:
#     return config["database"].add_documents(config["documents"]\)
