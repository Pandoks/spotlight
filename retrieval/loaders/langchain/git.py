from langchain_community.document_loaders import GitLoader
from typing import Callable, List, Optional, TypedDict
from langchain_core.documents import Document
from retrieval.util import print_documents_in_json


class GitLoadDocumentsConfig(TypedDict):
    path: str
    branch: str
    file_filter: Optional[Callable[[str], bool]]


# https://python.langchain.com/v0.1/docs/integrations/document_loaders/git/#load-existing-repository-from-disk
def load_documents(config: GitLoadDocumentsConfig) -> List[Document]:
    loader = GitLoader(
        repo_path=config["path"],
        branch=config["branch"],
        file_filter=config["file_filter"],
    )
    data = loader.load()
    print_documents_in_json(data)
    return data
