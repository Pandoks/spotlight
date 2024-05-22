import json
from typing import List
from langchain_core.documents import Document


def print_documents_in_json(documents: List[Document]) -> None:
    document_json = [
        {
            "page_content": document.dict()["page_content"],
            "metadata": document.dict()["metadata"],
        }
        for document in documents
    ]
    json_string = json.dumps(document_json)
    print(json_string)


def print_embeddings_in_json(embeddings: List[List[float]]) -> None:
    json_string = json.dumps(embeddings)
    print(json_string)


def print_document_ids_in_json(ids: List[str]) -> None:
    json_string = json.dumps(ids)
    print(json_string)
