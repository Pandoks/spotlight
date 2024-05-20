import sys
import argparse
import json
import importlib.util
from typing import List
from langchain_core.documents import Document


def main():
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers(dest="command")

    loader_parser = subparser.add_parser("loader")
    loader_parser.add_argument("--function", type=str, required=True)

    splitter_parser = subparser.add_parser("splitter")
    splitter_parser.add_argument("--function", type=str, required=True)

    embedding_parser = subparser.add_parser("embedding")
    embedding_parser.add_argument("--function", type=str, required=True)

    store_parser = subparser.add_parser("store")
    store_parser.add_argument("--function", type=str, required=True)

    retrieve_parser = subparser.add_parser("retrieve")
    retrieve_parser.add_argument("--function", type=str, required=True)

    args = parser.parse_args()
    stdin = sys.stdin.read()
    if not stdin:
        print(json.dumps({}))
        return
    data = json.loads(stdin)

    module_path = data["module_path"]
    if args not in ["loader", "splitter", "embedding", "store", "retriever"]:
        print(json.dumps({}))
        return
    module_name = args

    spec = importlib.util.spec_from_file_location(module_name, module_path)
    if not spec:
        print(json.dumps({}))
        return
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    loader = spec.loader
    if not loader:
        print(json.dumps({}))
        return
    loader.exec_module(module)

    config = data["config"]
    function_name = args["function"]

    try:
        function = getattr(module, function_name)
        if callable(function):
            match args:
                case "loader":
                    documents: List[Document] = function(config)
                    json_documents = []
                    for document in documents:
                        document = document.dict()
                        json_documents.append(
                            {
                                "page_content": document["page_content"],
                                "metadata": document["metadata"],
                            }
                        )
                    print(json.dumps(json_documents))
                    return

                case "splitter":
                    documents: List[Document] = function(config)
                    json_documents = []
                    for document in documents:
                        document = document.dict()
                        json_documents.append(
                            {
                                "page_content": document["page_content"],
                                "metadata": document["metadata"],
                            }
                        )
                    print(json.dumps(json_documents))
                    return

                case "embedding":
                    embeddings: List[List[float]] = function(config)
                    print(json.dumps(embeddings))
                    return

                case "store":
                    if function_name == "setup_database":
                        function(config)
                        print(
                            json.dumps(
                                {"database_location": config["persistent_directory"]}
                            )
                        )
                        return
                    elif function_name == "add":
                        added_ids: List[str] | None = function(config)
                        print(json.dumps(added_ids))
                        return
                    elif function_name == "delete":
                        deleted_ids: List[str] = function(config)
                        print(json.dumps(deleted_ids))
                        return
                    elif function_name == "update":
                        updated_ids: List[str] | None = function(config)
                        print(json.dumps(updated_ids))
                        return
                    else:
                        print(json.dumps({}))
                        return

                case "retriever":
                    documents: List[Document] = function(config)
                    json_documents = []
                    for document in documents:
                        document = document.dict()
                        json_documents.append(
                            {
                                "page_content": document["page_content"],
                                "metadata": document["metadata"],
                            }
                        )
                    print(json.dumps(json_documents))
                    return

                case _:
                    print(json.dumps({}))
                    return

        else:
            print(
                json.dumps({"error": f"'{function_name}' is not a callable function"})
            )
    except:
        print(json.dumps({}))
        return


if __name__ == "__main__":
    main()
