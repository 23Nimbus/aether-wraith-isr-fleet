#!/usr/bin/env python3
"""
audit_hash.py
-------------

Compute SHA‑256 checksums for a set of files and directories and
produce a JSON report.  This utility helps auditors verify the
integrity of generated artefacts and ensure reproducibility across
runs.  The output JSON lists each input path with its corresponding
digest and can be extended to include additional metadata.

Example:

    python audit_hash.py --paths missions compiled_output logs
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from typing import Dict, Any, List
import hmac

from utils.logging_utils import get_logger

logger = get_logger(__name__)


def sha256_of_file(path: str) -> str:
    """Compute the SHA-256 digest of a single file."""
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            h.update(chunk)
    return h.hexdigest()


def collect_files(path: str) -> List[str]:
    """Recursively collect files under a directory or return the file itself."""
    if os.path.isfile(path):
        return [path]
    files: List[str] = []
    for dirpath, _, filenames in os.walk(path):
        for name in filenames:
            files.append(os.path.join(dirpath, name))
    return files


def hash_paths(paths: List[str]) -> Dict[str, Any]:
    """Compute a mapping from file paths to SHA-256 digests."""
    digest_map: Dict[str, Any] = {}
    for p in paths:
        file_list = collect_files(p)
        for f in file_list:
            digest_map[f] = sha256_of_file(f)
    return digest_map


def main() -> None:
    parser = argparse.ArgumentParser(description='Generate a checksum report for audit purposes.')
    parser.add_argument('--paths', nargs='+', required=True, help='Files or directories to hash')
    parser.add_argument('--output', default='audit_report.json', help='Output JSON report path')
    parser.add_argument('--key', help='Path to a secret key file for signing the report')
    args = parser.parse_args()

    digest_map = hash_paths(args.paths)
    report: Dict[str, Any] = {'files': digest_map}

    # If a signing key is provided compute an HMAC signature over the JSON
    # representation of the digest map.  This signature can be used to
    # verify integrity and authenticity of the report.
    if args.key:
        with open(args.key, 'rb') as kf:
            secret = kf.read().strip()
        payload = json.dumps(digest_map, sort_keys=True).encode('utf-8')
        signature = hmac.new(secret, payload, hashlib.sha256).hexdigest()
        report['signature'] = signature
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2)
    logger.info('Wrote audit report to %s with %d entries', args.output, len(digest_map))


if __name__ == '__main__':
    main()