from abc import ABC, abstractmethod


class Embeddings(ABC):
    @abstractmethod
    def embed_documents(self):
        pass
