from typing import List, TypedDict
from langchain_community.embeddings.ollama import OllamaEmbeddings


class OllamaEmbedDocumentsConfig(TypedDict):
    texts: List[str]
    model: str


def embed_documents(config: OllamaEmbedDocumentsConfig) -> List[List[float]]:
    embedder = OllamaEmbeddings(model=config["model"])
    embeddings = embedder.embed_documents(config["texts"])
    return embeddings
