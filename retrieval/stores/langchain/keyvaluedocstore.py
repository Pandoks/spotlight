from langchain.storage._lc_store import create_kv_docstore
from langchain.storage import LocalFileStore

fs = LocalFileStore("./store_location")
store = create_kv_docstore(fs)

vectorstore = Chroma(
    collection_name="split_parents",
    embedding_function=embeddings,
    persist_directory="./db",
)
retriever = ParentDocumentRetriever(
    vectorstore=vectorstore,
    docstore=store,
    child_splitter=child_splitter,
    parent_splitter=parent_splitter,
)
retriever.add_documents(documents, ids=None)
