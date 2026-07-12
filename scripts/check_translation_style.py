#!/usr/bin/env python3
"""Check common Traditional Chinese localization style problems."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


HAN = r"\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff"
BOUNDARY_RE = re.compile(
    rf"(?:[{HAN}]\s+[A-Za-z0-9_$\[\]#]|[A-Za-z0-9_$\[\]#]\s+[{HAN}])"
)
PLACEHOLDER_SPACE_RE = re.compile(
    rf"(?:[{HAN}]\s+(?:\$[^$]+\$|\[[^\]]+\])|(?:\$[^$]+\$|\[[^\]]+\])\s+[{HAN}])"
)
ASCII_PAREN_RE = re.compile(r"\([^\r\n]*\)")
PROTECTED_TOKEN_RE = re.compile(r"\[[^\]]+\]|\$[^$]+\$|#!|#[A-Za-z_][A-Za-z0-9_]*\s?")


def load_translations(path: Path) -> dict[str, str]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or not all(
        isinstance(key, str) and isinstance(value, str) for key, value in data.items()
    ):
        raise ValueError("translations JSON must map strings to strings")
    return data


def check_value(key: str, value: str) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    unprotected_value = PROTECTED_TOKEN_RE.sub("", value)
    if BOUNDARY_RE.search(unprotected_value):
        issues.append(
            {
                "key": key,
                "type": "unnecessary_boundary_space",
                "message": "中文與英文、數字或 code-like token 之間有空格",
            }
        )
    if PLACEHOLDER_SPACE_RE.search(unprotected_value):
        issues.append(
            {
                "key": key,
                "type": "placeholder_boundary_space",
                "message": "中文與 placeholder 或 scripted localization 之間有空格",
            }
        )
    if ASCII_PAREN_RE.search(unprotected_value) and any(
        "\u3400" <= char <= "\u9fff" for char in unprotected_value
    ):
        issues.append(
            {
                "key": key,
                "type": "ascii_parentheses",
                "message": "含中文的翻譯仍使用半形括號，請確認是否應改為全形括號",
            }
        )
    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--translations", required=True, type=Path)
    args = parser.parse_args()

    translations = load_translations(args.translations)
    issues = [issue for key, value in translations.items() for issue in check_value(key, value)]
    result = {
        "translation_file": str(args.translations),
        "translation_count": len(translations),
        "issues": issues,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
