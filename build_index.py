import json

from rag_core import build_index


if __name__ == "__main__":
    print(json.dumps(build_index(force=True), ensure_ascii=False, indent=2))
