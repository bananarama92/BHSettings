"""A script for getting the SHA256 hash of a file."""

from __future__ import annotations

import argparse
import hashlib


def main(filename: str) -> str:
    with open(filename, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(usage="python ./get_hash.py room_settings.yaml", description=__doc__)
    parser.add_argument("path", help="Path to the file")
    args = parser.parse_args()
    print(main(args.path))
