from typing import Dict, List, Optional, TypedDict
from chromadb.api.types import Where
from langchain_community.vectorstores.chroma import Chroma
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from hashlib import sha256
from langchain_core.vectorstores import VectorStore


class ChromaSetupConfig(TypedDict):
    collection_name: str
    embedding_function: Optional[Embeddings]
    persistent_directory: Optional[str]


class ChromaAddConfig(TypedDict):
    documents: List[Document]
    database: Chroma


class ChromaDeleteConfig(TypedDict):
    metadatas: Optional[List[Dict]]
    database: Chroma


class ChromaUpdateConfig(TypedDict):
    documents: List[Document]
    database: Chroma


# https://python.langchain.com/v0.1/docs/integrations/vectorstores/chroma/
def setup_database(config: ChromaSetupConfig) -> VectorStore:
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


# WILL DELETE ALL contents inside of database if no metadata is provided
def delete(config: ChromaDeleteConfig) -> List[str]:
    database = config["database"]
    if not config["metadatas"]:
        to_be_deleted_documents = database.get()
        to_be_deleted_ids: List[str] = to_be_deleted_documents["ids"]
        database.delete(ids=to_be_deleted_ids)
        return to_be_deleted_ids

    to_be_deleted_ids = []
    for metadata in config["metadatas"]:
        query_filter_list: List[Dict[str, str]] = []
        for key, value in metadata.items():
            query_filter_list.append({key: value})
        query_filter: Dict | None = None
        if len(query_filter_list) == 1:
            query_filter = query_filter_list[0]
        else:
            query_filter = {"$and": query_filter_list}
        to_be_deleted_documents = database.get(where=query_filter)
        current_to_be_deleted_ids = to_be_deleted_documents["ids"]
        if not len(current_to_be_deleted_ids):
            continue
        to_be_deleted_ids.append(current_to_be_deleted_ids)
    return to_be_deleted_ids


def update(config: ChromaUpdateConfig) -> List[str] | None:
    database = config["database"]
    metadatas = []
    for document in config["documents"]:
        metadata = document.dict()["metadata"]
        if metadata not in metadatas:
            metadatas.append(metadata)
    delete({"database": database, "metadatas": metadatas})
    return add({"database": database, "documents": config["documents"]})
