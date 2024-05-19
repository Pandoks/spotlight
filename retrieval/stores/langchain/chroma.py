from typing import List, Optional, TypedDict
from chromadb.api.types import Where, WhereDocument
from langchain_community.vectorstores.chroma import Chroma
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from hashlib import sha256


class ChromaSetupConfig(TypedDict):
    collection_name: str
    embedding_function: Optional[Embeddings]
    persistent_directory: Optional[str]


class ChromaAddConfig(TypedDict):
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


# will automatically ignore duplicate documents
def add(config: ChromaAddConfig) -> List[str] | None:
    documents_with_hashes = []
    for document in config["documents"]:
        document = document.dict()
        page_content = document["page_content"]
        hashed_page_content = sha256(page_content.encode("utf-8").hexdigest())

        new_metadata = document["metadata"]
        new_metadata["hash"] = hashed_page_content

        query_filter: Where = {
            "$and": [
                {"source": new_metadata["source"]},
                {"file_path": new_metadata["file_path"]},
                {"file_name": new_metadata["file_name"]},
                {"file_type": new_metadata["file_type"]},
                {"hash": new_metadata["hash"]},
            ]
        }
        existing_documents = config["database"].get(where=query_filter)
        if not len(existing_documents["ids"]):
            documents_with_hashes.append(Document(page_content, metadata=new_metadata))

    if not len(documents_with_hashes):
        return None

    return config["database"].add_documents(documents_with_hashes)
