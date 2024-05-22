from typing import List, TypedDict
from langchain.chains.query_constructor.schema import AttributeInfo
from langchain.retrievers import SelfQueryRetriever
from langchain_core.documents import Document
from langchain_core.language_models.llms import LLM
from langchain_core.vectorstores import VectorStore
from retrieval.util import print_documents_in_json


class MetadataRetrieveConfig(TypedDict):
    llm: LLM
    database: VectorStore
    document_content_description: str
    metadata_field_info: List[AttributeInfo]
    prompt: str


def retrieve(config: MetadataRetrieveConfig) -> List[Document]:
    retriever = SelfQueryRetriever.from_llm(
        config["llm"],
        config["database"],
        config["document_content_description"],
        config["metadata_field_info"],
    )
    documents = retriever.invoke(config["prompt"])
    print_documents_in_json(documents)
    return documents
