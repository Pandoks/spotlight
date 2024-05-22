from typing import List, Optional, TypedDict
from langchain_core.documents import Document
from langchain_core.stores import BaseStore
from langchain_core.vectorstores import VectorStore
from langchain_text_splitters import TextSplitter
from langchain.retrievers import ParentDocumentRetriever
from retrieval.util import print_documents_in_json


class ParentRetrieveConfig(TypedDict):
    database: VectorStore
    document_database: BaseStore
    prompt: str
    child_splitter: TextSplitter
    parent_splitter: Optional[TextSplitter]


# Make sure to use the child_splitter and parent_splitter before storing documents in their respective databases
def retrieve(config: ParentRetrieveConfig) -> List[Document]:
    retriever = ParentDocumentRetriever(
        vectorstore=config["database"],
        docstore=config["document_database"],
        child_splitter=config["child_splitter"],
        parent_splitter=config["parent_splitter"],
    )
    documents = retriever.invoke(config["prompt"])
    print_documents_in_json(documents)
    return documents
