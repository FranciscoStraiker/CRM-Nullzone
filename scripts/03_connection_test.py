from __future__ import annotations

import argparse
import base64
import json
from pathlib import Path
from urllib import request


DEFAULT_API_URL = "https://content-receiver.replit.app/api/upload-content"
DEFAULT_SOURCE_PATH = Path("/home/node").expanduser()


def upload_file(file_path: Path, base_path: Path, url: str) -> None:
    relative_name = file_path.relative_to(base_path)

    payload = {
        "filename": str(relative_name),  # mantiene estructura de carpetas
        "content_base64": base64.b64encode(file_path.read_bytes()).decode("ascii"),
    }

    body = json.dumps(payload).encode("utf-8")
    req = request.Request(
        url,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    with request.urlopen(req) as response:
        print(f"[+] Uploaded: {relative_name}")
        print(response.read().decode("utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Upload a file or directory to the upload-content API."
    )
    parser.add_argument(
        "--url",
        default=DEFAULT_API_URL,
        help="Target upload-content API URL.",
    )
    parser.add_argument(
        "--path",
        default=str(DEFAULT_SOURCE_PATH),
        help="Local file or directory to upload.",
    )
    args = parser.parse_args()

    source_path = Path(args.path).expanduser()
    if not source_path.exists():
        raise SystemExit(f"Path does not exist: {source_path}")

    if source_path.is_file():
        upload_file(source_path, source_path.parent, args.url)
    else:
        for file in source_path.rglob("*"):
            if file.is_file():
                upload_file(file, source_path, args.url)


if __name__ == "__main__":
    main()
