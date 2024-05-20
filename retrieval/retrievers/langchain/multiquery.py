from typing import List, TypedDict
from langchain_core.documents import Document
from langchain_core.language_models.llms import LLM
from langchain_core.retrievers import RetrieverLike
from langchain_core.prompts import PromptTemplate


class MultiQueryRetrieveConfig(TypedDict):
    retriever: RetrieverLike
    prompt_generator: PromptTemplate
    llm: LLM
    prompt: str


class RunPromptsConfig(TypedDict):
    retriever: RetrieverLike
    prompts: List[str]


def parse_questions(questions: str) -> List[str]:
    lines = questions.strip().split("\n")
    filtered_lines = [line for line in lines if line]
    return filtered_lines


def run_prompts(config: RunPromptsConfig):
    documents = []
    for prompt in config["prompts"]:
        documents.extend(config["retriever"].invoke(prompt))
    return documents


def retrieve(config: MultiQueryRetrieveConfig) -> List[Document]:
    llm_sequence = (
        config["prompt_generator"] | config["llm"] | parse_questions | run_prompts
    )
    documents = llm_sequence.invoke({"question": config["prompt"]})
    return documents
