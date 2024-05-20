import sys
import argparse
import json


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


if __name__ == "__main__":
    main()
