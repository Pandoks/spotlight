from typing import TypedDict
from langchain_community.document_loaders import DirectoryLoader


class DirectoryLoadDocumentsConfig(TypedDict):
    path: str
    glob: str


def load_documents(config):
    loader = DirectoryLoader(config["path"], glob=config["glob"])
    data = loader.load()
    return data
