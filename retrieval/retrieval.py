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

    match args:
        case "loader":
            module_path = data["module_path"]
            module_name = "loader"
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
                else:
                    print(
                        json.dumps(
                            {"error": f"'{function_name}' is not a callable function"}
                        )
                    )
            except:
                print(json.dumps({}))
                return

        case "splitter":
            module_path = data["module_path"]
            module_name = "splitter"
        case "embedding":
            module_path = data["module_path"]
            module_name = "embedding"
        case "store":
            module_path = data["module_path"]
            module_name = "store"
        case "retriever":
            module_path = data["module_path"]
            module_name = "retriever"
        case _:
            print(json.dumps({}))


if __name__ == "__main__":
    main()
