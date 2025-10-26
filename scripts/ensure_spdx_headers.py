#!/usr/bin/env python3
# SPDX-License-Identifier: MPL-2.0
"""Insert MPL-2.0 SPDX identifiers into source files."""
from __future__ import annotations

import argparse
import pathlib
import sys
from typing import Iterable

SPDX_LINE = "SPDX-License-Identifier: MPL-2.0"

LINE_COMMENT_EXTS = {
    ".py": "#",
    ".pyi": "#",
    ".sh": "#",
    ".bash": "#",
    ".zsh": "#",
    ".ps1": "#",
    ".psm1": "#",
    ".psd1": "#",
    ".c": "/*",
    ".h": "/*",
    ".cpp": "/*",
    ".hpp": "/*",
    ".cxx": "/*",
    ".hxx": "/*",
    ".java": "/*",
    ".cs": "//",
    ".js": "//",
    ".cjs": "//",
    ".mjs": "//",
    ".ts": "//",
    ".tsx": "//",
    ".jsx": "//",
    ".go": "//",
    ".rs": "//",
    ".swift": "//",
    ".dart": "//",
    ".kt": "//",
    ".kts": "//",
    ".gradle": "//",
    ".rb": "#",
    ".pl": "#",
    ".pm": "#",
    ".php": "//",
    ".scss": "//",
    ".css": "/*",
    ".scss": "//",
    ".sass": "//",
    ".less": "//",
    ".coffee": "#",
    ".toml": "#",
    ".ini": "#",
    ".cfg": "#",
    ".conf": "#",
    ".yaml": "#",
    ".yml": "#",
    ".env": "#",
    ".dockerfile": "#",
    ".ps": "#",
}

BLOCK_COMMENT_EXTS = {
    ".html": ("<!--", "-->"),
    ".htm": ("<!--", "-->"),
    ".xml": ("<!--", "-->"),
    ".md": ("<!--", "-->"),
}

SPECIAL_FILES = {
    "Dockerfile": "#",
    "Makefile": "#",
    "LICENSE": None,
}

SKIP_DIR_PARTS = {".git", "__pycache__", "build", "dist", "node_modules", ".mypy_cache"}


def iter_targets(paths: Iterable[pathlib.Path]) -> Iterable[pathlib.Path]:
    for path in paths:
        if not path.exists():
            continue
        if any(part in SKIP_DIR_PARTS for part in path.parts):
            continue
        if path.is_dir():
            yield from iter_targets(p for p in path.iterdir())
            continue
        if path.name in {"NOTICE", "LICENSE"}:
            continue
        yield path


def has_spdx(contents: str) -> bool:
    return any(SPDX_LINE in line for line in contents.splitlines()[:5])


def insert_for_file(path: pathlib.Path) -> bool:
    suffix = path.suffix.lower()
    comment = None
    block = None
    text = path.read_text(encoding="utf-8")

    if has_spdx(text):
        return False

    if path.name in SPECIAL_FILES:
        comment = SPECIAL_FILES[path.name]
    elif suffix in LINE_COMMENT_EXTS:
        comment = LINE_COMMENT_EXTS[suffix]
    elif suffix in BLOCK_COMMENT_EXTS:
        block = BLOCK_COMMENT_EXTS[suffix]
    elif text.startswith("#!"):
        comment = "#"
    elif path.match('scripts/*') and not suffix:
        comment = "#"
    elif path.stat().st_mode & 0o111:
        comment = "#"
    else:
        return False

    shebang = ""
    body = text
    if text.startswith("#!"):
        lines = text.splitlines()
        shebang = lines[0] + "\n"
        body = "\n".join(lines[1:])
        if body and not body.startswith("\n"):
            body = "\n" + body

    header = ""
    if block:
        start, end = block
        header = f"{start} {SPDX_LINE} {end}\n"
    elif comment == "/*":
        header = f"/* {SPDX_LINE} */\n"
    elif comment:
        header = f"{comment} {SPDX_LINE}\n"
    else:
        return False

    stripped = body.lstrip("\n")
    new_text = f"{shebang}{header}{stripped}"
    if not new_text.endswith("\n"):
        new_text += "\n"
    path.write_text(new_text, encoding="utf-8")
    return True


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Ensure SPDX headers are present.")
    parser.add_argument("paths", nargs="*", type=pathlib.Path, help="Paths to scan")
    parser.add_argument("--all", action="store_true", help="Process all tracked files")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.all or not args.paths:
        result = subprocess_run_git_ls()
        paths = [pathlib.Path(p.strip()) for p in result if p.strip()]
    else:
        paths = args.paths

    changed = False
    for target in iter_targets(paths):
        try:
            changed |= insert_for_file(target)
        except UnicodeDecodeError:
            continue
    return 0 if changed else 0


def subprocess_run_git_ls() -> list[str]:
    import subprocess

    result = subprocess.run(["git", "ls-files"], check=True, capture_output=True, text=True)
    return result.stdout.splitlines()


if __name__ == "__main__":
    sys.exit(main())
