from typing import List, TypedDict
from langchain_core.documents import Document
from langchain_core.vectorstores import VectorStore
from retrieval.util import print_documents_in_json


class VectorStoreRetrieveConfig(TypedDict):
    database: VectorStore
    search_type: str
    prompt: str


def retrieve(config: VectorStoreRetrieveConfig) -> List[Document]:
    database = config["database"]
    retriever = database.as_retriever(search_type=config["search_type"])
    documents = retriever.invoke(config["prompt"])
    print_documents_in_json(documents)
    return documents
