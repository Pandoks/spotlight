from typing import List, Optional, TypedDict
from langchain_core.documents import Document
from langchain_text_splitters import Language, RecursiveCharacterTextSplitter


class CodeSplitTextConfig(TypedDict):
    text: str
    language: Language
    chunk_size: Optional[int]
    chunk_overlap: Optional[int]


# https://python.langchain.com/v0.1/docs/modules/data_connection/document_transformers/code_splitter/
def split_text(config: CodeSplitTextConfig) -> List[Document]:
    chunk_size = config.get("chunk_size", 50)
    chunk_overlap = config.get("chunk_overlap", 0)
    splitter = RecursiveCharacterTextSplitter.from_language(
        language=config["language"], chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )
    docs = splitter.create_documents([config["text"]])
    return docs
