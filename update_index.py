import json
import sys

from rag_core import UPDATE_LOG_PATH, append_jsonl, build_index, utc_now


if __name__ == "__main__":
    try:
        print(json.dumps(build_index(), ensure_ascii=False, indent=2))
    except Exception as error:
        append_jsonl(
            UPDATE_LOG_PATH,
            {
                "started_at": utc_now(),
                "finished_at": utc_now(),
                "status": "failed",
                "errors": [f"{type(error).__name__}: {error}"],
            },
        )
        print(f"index update failed: {error}", file=sys.stderr)
        raise
