from typing import List, Optional, TypedDict

from langchain.storage import InMemoryStore, LocalFileStore, create_kv_docstore
from langchain_core.documents import Document
from langchain_core.stores import BaseStore


class KeyValueStoreSetupConfig(TypedDict):
    persistent_directory: Optional[str]


class KeyValueStoreAddConfig(TypedDict):
    documents: List[Document]
    database: BaseStore


class KeyValueStoreDeleteConfig(TypedDict):
    file_path: Optional[List[str]]
    database: BaseStore


class KeyValueStoreUpdateConfig(TypedDict):
    documents: List[Document]
    database: BaseStore


def setup_database(config: KeyValueStoreSetupConfig) -> BaseStore:
    persistent_directory = config["persistent_directory"]
    if not persistent_directory:
        store = InMemoryStore()
        return store

    file_store = LocalFileStore(persistent_directory)
    store = create_kv_docstore(file_store)
    return store


# Will automatically override so it can be used as a pseudo update
def add(config: KeyValueStoreAddConfig) -> List[str] | None:
    added_files = []
    database = config["database"]
    for document in config["documents"]:
        document_dict = document.dict()
        database.mset([(document_dict["metadata"]["file_location"], document)])
        added_files.append(document_dict["metadata"]["file_location"])

    if not len(added_files):
        return None
    return added_files


def delete(config: KeyValueStoreDeleteConfig) -> List[str]:
    database = config["database"]
    if not config["file_path"]:
        all_keys = list(database.yield_keys())
        database.mdelete(all_keys)
        return all_keys

    deleted_files = []
    for file_path in config["file_path"]:
        document = database.mget(file_path)
        if not document:
            continue
        database.mdelete(file_path)
        deleted_files.append(file_path)

    return deleted_files


def update(config: KeyValueStoreUpdateConfig) -> List[str] | None:
    return add(config)
