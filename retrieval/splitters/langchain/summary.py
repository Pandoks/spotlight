from typing import List, TypedDict
from langchain_core.language_models.llms import LLM
from langchain_core.prompts import PromptTemplate
from langchain_core.documents import Document
from retrieval.util import print_documents_in_json


class SummarySplitDocumentConfig(TypedDict):
    document: Document
    prompt: PromptTemplate
    llm: LLM


# template variables -> "{variable}"
# 2 possible variables: "{document_content}" & "{file_path}"
# TODO: support more variables
class SummaryPromptConfig(TypedDict):
    template: str


def create_summary_prompt(config: SummaryPromptConfig) -> PromptTemplate:
    return PromptTemplate(
        input_variables=["document_content", "filepath"], template=config["template"]
    )


def split_text(config: SummarySplitDocumentConfig) -> List[Document]:
    llm_sequence = config["prompt"] | config["llm"]
    document = config["document"].dict()
    page_content = document["page_content"]
    metadata = document["metadata"]
    summary = llm_sequence.invoke(
        {"document_content": page_content, "filepath": metadata["file_path"]}
    )
    new_document = Document(page_content=summary, metadata=metadata)
    documents = [config["document"], new_document]
    print_documents_in_json(documents)
    return documents
