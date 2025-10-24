#!/usr/bin/env python3
import os
import sys
from pathlib import Path
from typing import List

try:
    from huggingface_hub import HfApi, upload_folder
except Exception as e:
    print("huggingface_hub is not installed. Install it with: pip install huggingface_hub", file=sys.stderr)
    raise

SPACE_ID = "NiloyMondal/TDS_Project_1"
SPACE_URL = f"https://huggingface.co/spaces/{SPACE_ID}"


def get_token() -> str:
    token = os.environ.get("HF_TOKEN") or os.environ.get("HUGGINGFACE_TOKEN")
    if not token:
        print("Error: Please set HF_TOKEN (or HUGGINGFACE_TOKEN) environment variable with your Hugging Face API token.", file=sys.stderr)
        sys.exit(1)
    return token


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    token = get_token()

    api = HfApi(token=token)

    # Ensure repo exists and is a Space (won't overwrite if exists)
    api.create_repo(
        repo_id=SPACE_ID,
        repo_type="space",
        exist_ok=True,
        space_sdk="docker",  # Our project ships a Dockerfile
    )

    # Ignore typical local/dev files
    ignore_patterns: List[str] = [
        ".git*",
        "**/__pycache__/**",
        "venv/**",
        ".venv/**",
        "**/.pytest_cache/**",
        "**/.mypy_cache/**",
        "**/.DS_Store",
        "**/*:Zone.Identifier",
    ]

    print(f"Uploading folder {repo_root} to {SPACE_URL} ...")
    upload_folder(
        repo_id=SPACE_ID,
        repo_type="space",
        token=token,
        folder_path=str(repo_root),
        path_in_repo="/",
        commit_message="Deploy from local workspace",
        ignore_patterns=ignore_patterns,
    )

    print("Upload complete. Your Space will start building shortly:")
    print(SPACE_URL)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
