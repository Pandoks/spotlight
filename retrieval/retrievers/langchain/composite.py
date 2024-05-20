from typing import List, TypedDict
from langchain.retrievers import EnsembleRetriever
from langchain_core.documents import Document
from langchain_core.retrievers import RetrieverLike


class CompositeRetrieveConfig(TypedDict):
    retrievers: List[RetrieverLike]
    weights: List[float]
    prompt: str


def retrieve(config: CompositeRetrieveConfig) -> List[Document]:
    retriever = EnsembleRetriever(
        retrievers=config["retrievers"], weights=config["weights"]
    )
    documents = retriever.invoke(config["prompt"])
    return documents
