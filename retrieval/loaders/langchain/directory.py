from typing import List, TypedDict
from langchain_community.document_loaders import DirectoryLoader
from langchain_core.documents import Document
from retrieval.util import print_documents_in_json


class DirectoryLoadDocumentsConfig(TypedDict):
    path: str
    glob: str


def load_documents(config: DirectoryLoadDocumentsConfig) -> List[Document]:
    loader = DirectoryLoader(config["path"], glob=config["glob"])
    data = loader.load()
    print_documents_in_json(data)
    return data
