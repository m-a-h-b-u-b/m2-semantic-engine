# m2-semantic-engine
# -----------------------------------------
# License : Dual License
#           - Apache 2.0 for open-source / personal use
#           - Commercial license required for closed-source use
# Author  : Md Mahbubur Rahman
# URL     : https://m-a-h-b-u-b.github.io
# GitHub  : https://github.com/m-a-h-b-u-b/m2-semantic-engine

"""
small CLI to ingest local text files into the indexer for testing.
"""
import argparse
import json
from src.semantic_engine.retrieval.retriever import Retriever

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="newline-delimited text file to ingest (one doc per line)")
    args = parser.parse_args()
    r = Retriever()
    docs = []
    with open(args.file, "r", encoding="utf-8") as fh:
        for i, line in enumerate(fh):
            line = line.strip()
            if not line:
                continue
            docs.append({"id": f"line-{i}", "text": line})
    r.index_documents(docs)
    print(f"Indexed {len(docs)} documents.")

if __name__ == "__main__":
    main()
