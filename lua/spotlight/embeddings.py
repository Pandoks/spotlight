import ollama
import chromadb
import argparse
import uuid
from chromadb.utils.embedding_functions import OllamaEmbeddingFunction

chromadb_client = None
embedding_function = None
collection = None


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")

    store_parser = subparsers.add_parser("store")
    store_parser.add_argument("--text", type=str, required=True)
    store_parser.add_argument("--collection-name", type=bool, required=True)
    store_parser.add_argument("--model", type=str, required=True)
    store_parser.add_argument("--db-location", type=str)
    store_parser.add_argument("--file-location", type=str, required=True)

    retrieve_parser = subparsers.add_parser("retrieve")
    retrieve_parser.add_argument("--text", type=str, required=True)
    retrieve_parser.add_argument("--collection-name", type=str, required=True)
    retrieve_parser.add_argument("--model", type=str, required=True)
    retrieve_parser.add_argument("--result_amount", type=int, required=True)
    retrieve_parser.add_argument("--file-location", type=str, required=True)
    retrieve_parser.add_argument("--db-location", type=str)

    setup_parser = subparsers.add_parser("setup")
    setup_parser.add_argument("--db-location", type=str)
    setup_parser.add_argument("--collection-name", type=str, required=True)

    args = parser.parse_args()

    if args.db_location:
        chromadb_client = chromadb.PersistentClient(path=args.db_location)
    else:
        chromadb_client = chromadb.Client()
    if args.command != "setup":
        embedding_function = OllamaEmbeddingFunction(
            url="http://localhost:11434/api/embeddings", model_name=args.model
        )
        collection = chromadb_client.get_collection(name=args.collection_name)

    if args.command == "setup":
        collection = chromadb_client.create_collection(name=args.collection_name)

    elif args.command == "store":
        try:
            collection.add(
                documents=[args.text],
                metadatas=[{"file": args.file_location}],
                ids=[str(uuid.uuid4())],
            )
            return True
        except:
            return False

    elif args.command == "retrieve":
        collection.query(query_texts=[args.text], n_results=args.result_amount)


if __name__ == "__main__":
    main()
