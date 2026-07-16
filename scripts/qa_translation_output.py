import argparse
import json
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path


ENTRY_RE = re.compile(r'^\s*([^#\s][^:]*):\s*(?:\d+\s+)?"((?:\\.|[^"\\])*)"')
HEADER_RE = re.compile(r'^\s*l_[a-z_]+:\s*$')
TOKEN_PATTERNS = {
    "placeholder": re.compile(r"\$[^$]+\$"),
    "scripted_localization": re.compile(r"\[[^\]]+\]"),
    "brace_variable": re.compile(r"\{[^}]+\}"),
    "percent_token": re.compile(r"%[A-Za-z0-9_]+"),
    "escape": re.compile(r"\\[nrt\\\"]"),
    "color_or_tag": re.compile(r"<[^>]+>"),
    "formatting_tag": re.compile(r"#!|#[A-Za-z_]+"),
    "icon_token": re.compile(r"@[A-Za-z0-9_]+!"),
}
CHINESE_RE = re.compile(r"[\u3400-\u9fff]")
LINK_RE = re.compile(r"\[Link\('([^']*)',\s*'([^']*)',\s*'([^']*)'\)\]")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def parse_localization(path: Path) -> dict[str, str]:
    entries: dict[str, str] = {}
    for line_number, line in enumerate(read_text(path).splitlines(), 1):
        if HEADER_RE.match(line):
            continue
        match = ENTRY_RE.match(line)
        if match:
            entries[match.group(1).strip()] = match.group(2)
    return entries


def unescape(value: str) -> str:
    return value.replace('\\"', '"').replace('\\\\', '\\')


def protected_tokens(value: str) -> dict[str, list[str]]:
    script_value = normalize_link_tokens(value)
    return {
        name: pattern.findall(script_value if name == "scripted_localization" else value)
        for name, pattern in TOKEN_PATTERNS.items()
    }


def normalize_link_tokens(value: str) -> str:
    def replace(match: re.Match[str]) -> str:
        first, second, display = match.groups()
        signature, _ = link_display_parts(display)
        if signature or first == "hints":
            return f"[Link('{first}','{second}','{signature or '__display_text__'}')]"
        return match.group(0)

    return LINK_RE.sub(replace, value)


def link_display_parts(display: str) -> tuple[str, str]:
    token_pattern = re.compile(r"\$[^$]+\$|@[A-Za-z0-9_]+!")
    matches = list(token_pattern.finditer(display))
    if not matches:
        if re.search(r"\s|>", display):
            return "__display_text__", display
        return "", ""
    signature = " ".join(match.group(0) for match in matches)
    visible = token_pattern.sub(" ", display).strip()
    return signature, visible


def mask_protected(value: str) -> str:
    def keep_link_display(match: re.Match[str]) -> str:
        display = match.group(3)
        signature, visible = link_display_parts(display)
        return visible if signature or match.group(1) == "hints" else " "

    masked = LINK_RE.sub(keep_link_display, value)
    for pattern in TOKEN_PATTERNS.values():
        masked = pattern.sub(lambda match: " " * len(match.group(0)), masked)
    return masked


def yaml_scalar_entries(path: Path) -> dict[str, str]:
    entries: dict[str, str] = {}
    section = None
    for line in read_text(path).splitlines():
        if line and not line.startswith(" "):
            section = line.rstrip(":")
            continue
        if section in {"fixed", "game_terms"}:
            match = re.match(r'^  (?! )([^:#][^:]*):\s*"([^"]*)"', line)
            if match:
                entries[match.group(1).strip()] = match.group(2)
    return entries


def aliases(path: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    lines = read_text(path).splitlines()
    in_aliases = False
    term = None
    translation = None
    variants: list[str] = []

    def flush() -> None:
        if term and translation:
            for name in [term, *variants]:
                result[name] = translation

    for line in lines:
        if line == "aliases:":
            flush()
            in_aliases = True
            term = None
            translation = None
            variants = []
            continue
        if in_aliases and line and not line.startswith(" "):
            flush()
            in_aliases = False
            continue
        if not in_aliases:
            continue
        match = re.match(r"^  (?! )([^:#][^:]*):\s*$", line)
        if match:
            flush()
            term = match.group(1).strip()
            translation = None
            variants = []
            continue
        match = re.match(r'^    zh:\s*"([^"]*)"', line)
        if match:
            translation = match.group(1)
            continue
        match = re.match(r"^      -\s+(.+?)\s*$", line)
        if match and term:
            variants.append(match.group(1).strip())
    flush()
    return result


def contextual_terms(path: Path) -> set[str]:
    terms: set[str] = set()
    lines = read_text(path).splitlines()
    in_contextual = False
    for line in lines:
        if line == "contextual:":
            in_contextual = True
            continue
        if in_contextual and line and not line.startswith(" "):
            break
        if in_contextual:
            match = re.match(r"^  (?! )([^:#][^:]*):", line)
            if match:
                terms.add(match.group(1).strip())
    return terms


def term_in_text(term: str, text: str) -> bool:
    if " " in term:
        return term in text
    return re.search(r"(?<![A-Za-z])" + re.escape(term) + r"(?![A-Za-z])", text) is not None


def ordered_text_present(needle: str, haystack: str) -> bool:
    characters = [char for char in needle if not char.isspace()]
    position = 0
    for char in characters:
        position = haystack.find(char, position)
        if position < 0:
            return False
        position += 1
    return bool(characters)


def excerpt(text: str, needle: str = "", radius: int = 120) -> str:
    """Keep reports readable while retaining the relevant local context."""
    if len(text) <= radius * 2:
        return text
    position = text.find(needle) if needle else -1
    if position < 0:
        return text[: radius * 2] + "..."
    start = max(0, position - radius)
    end = min(len(text), position + len(needle) + radius)
    prefix = "..." if start else ""
    suffix = "..." if end < len(text) else ""
    return prefix + text[start:end] + suffix


def latin_words(value: str) -> list[str]:
    """Extract readable Latin-script words while preserving diacritics."""
    words: list[str] = []
    current: list[str] = []

    def is_latin(char: str) -> bool:
        name = unicodedata.name(char, "")
        return char.isascii() or "LATIN" in name

    def flush() -> None:
        if current:
            words.append("".join(current).strip(".-"))
            current.clear()

    for char in mask_protected(value):
        if is_latin(char) and char.isalpha():
            current.append(char)
        elif unicodedata.combining(char) and current:
            current.append(char)
        elif char in "'’.-" and current:
            current.append(char)
        else:
            flush()
    flush()
    return [word for word in words if word]


def untranslated_issues(
    source: dict[str, str],
    output: dict[str, str],
) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    for key, output_value in output.items():
        words = latin_words(unescape(output_value))
        if not words:
            continue
        text = " ".join(dict.fromkeys(words))
        first = words[0]
        issues.append(
            {
                "type": "untranslated_text",
                "key": key,
                "source": excerpt(unescape(source.get(key, "")), first),
                "output": excerpt(unescape(output_value), first),
                "text": text,
                "reason": "output 中仍保留疑似未翻譯英文",
            }
        )
    return issues


def punctuation_issues(
    key: str,
    source_value: str,
    output_value: str,
) -> list[dict[str, str]]:
    value = output_value
    plain = mask_protected(value)
    issues: list[dict[str, str]] = []
    if "／" in plain:
        issues.append(
            {
                "type": "style_warning",
                "key": key,
                "source": excerpt(source_value, "／"),
                "output": excerpt(output_value, "／"),
                "message": "使用了全形斜線／；專案規則要求半形斜線 /",
            }
        )
    if re.search(r"(?:\]|\$|@)\s+/|/\s+(?:\[|\$|@)", plain):
        issues.append(
            {
                "type": "style_warning",
                "key": key,
                "source": excerpt(source_value, "/"),
                "output": excerpt(output_value, "/"),
                "message": "placeholder 或 script token 與斜線之間可能有多餘空格",
            }
        )
    for symbol, message in (
        ("-", "普通連字號，請確認是否為英文複合詞或原文必要符號"),
        ("‑", "不斷行連字號，請確認是否用於複合人名、地名或避免換行"),
        ("——", "中文破折號，請確認是否用於標題或分類分隔"),
    ):
        if symbol in plain:
            issues.append(
                {
                    "type": "punctuation_review",
                    "key": key,
                    "source": excerpt(
                        source_value,
                        {"——": "-", "‑": "-", "／": "/"}.get(symbol, symbol),
                    ),
                    "output": excerpt(output_value, symbol),
                    "symbol": symbol,
                    "message": message,
                }
            )
    return issues


def glossary_mismatches(
    source: dict[str, str],
    output: dict[str, str],
    glossary: Path,
) -> list[dict[str, str]]:
    fixed = yaml_scalar_entries(glossary)
    fixed.update(aliases(glossary))
    contextual = contextual_terms(glossary)
    issues: list[dict[str, str]] = []
    for key, source_value in source.items():
        translated = output.get(key, "")
        for term, expected in fixed.items():
            source_plain = mask_protected(source_value)
            translated_plain = mask_protected(translated)
            if not expected or not term_in_text(term, source_plain):
                continue
            longer_term_used = any(
                longer != term
                and len(longer) > len(term)
                and term_in_text(longer, source_plain)
                for longer in fixed
            )
            if longer_term_used or term in contextual:
                continue
            if expected not in translated_plain and not ordered_text_present(expected, translated_plain):
                issues.append(
                    {
                        "type": "glossary_mismatch",
                        "key": key,
                        "term": term,
                        "expected": expected,
                        "actual": translated,
                    }
                )
    return issues


def run(source_path: Path, output_path: Path, glossary: Path) -> dict:
    source = parse_localization(source_path)
    output = parse_localization(output_path)
    issues: list[dict[str, str]] = []
    contextual = contextual_terms(glossary)

    source_header = next((line.strip() for line in read_text(source_path).splitlines() if line.strip()), "")
    output_header = next((line.strip() for line in read_text(output_path).splitlines() if line.strip()), "")
    if source_header != "l_english:":
        issues.append({"type": "format_error", "message": "來源檔 header 不是 l_english:"})
    if output_header != "l_simp_chinese:":
        issues.append({"type": "format_error", "message": "輸出檔 header 不是 l_simp_chinese:"})
    if source_path.name.endswith("_l_english.yml") and not output_path.name.endswith("_l_simp_chinese.yml"):
        issues.append({"type": "format_error", "message": "輸出檔 suffix 不是 _l_simp_chinese.yml"})

    source_order = list(source)
    output_order = list(output)
    if source_order != output_order:
        issues.append({"type": "key_order_warning", "message": "source 與 output 的 key 順序不同"})

    for key in sorted(set(source) - set(output)):
        issues.append({"type": "missing_key", "key": key})
    for key in sorted(set(output) - set(source)):
        issues.append({"type": "extra_key", "key": key})

    for key in sorted(set(source) & set(output)):
        source_tokens = protected_tokens(unescape(source[key]))
        output_tokens = protected_tokens(unescape(output[key]))
        for token_type in TOKEN_PATTERNS:
            if Counter(source_tokens[token_type]) != Counter(output_tokens[token_type]):
                issues.append(
                    {
                        "type": "token_mismatch",
                        "key": key,
                        "token_type": token_type,
                        "source": source_tokens[token_type],
                        "output": output_tokens[token_type],
                    }
                )
        value = mask_protected(unescape(output[key]))
        if re.search(r"\(\s*[^)]*\)", value) and CHINESE_RE.search(value):
            issues.append(
                {
                    "type": "style_warning",
                    "key": key,
                    "message": "中文值仍含半形括號，請確認是否屬於必要語法",
                }
            )
        if re.search(r"[\u3400-\u9fff]\s+(?:\$|\[|@)", value):
            issues.append(
                {
                    "type": "style_warning",
                    "key": key,
                    "message": "中文與 placeholder／script token 之間可能有多餘空格",
                }
            )

        issues.extend(
            punctuation_issues(
                key,
                unescape(source[key]),
                unescape(output[key]),
            )
        )

    for term in sorted(contextual, key=str.casefold):
        keys = [key for key, value in source.items() if term_in_text(term, mask_protected(value))]
        if keys:
            for key in keys:
                issues.append(
                    {
                        "type": "contextual_review",
                        "term": term,
                        "key": key,
                        "source": excerpt(source[key], term),
                        "output": excerpt(output.get(key, "")),
                        "message": "請依來源 key 與上下文人工確認 contextual 譯法",
                    }
                )

    issues.extend(glossary_mismatches(source, output, glossary))
    issues.extend(untranslated_issues(source, output))
    counts: dict[str, int] = {}
    for issue in issues:
        counts[issue["type"]] = counts.get(issue["type"], 0) + 1
    return {
        "source_file": str(source_path),
        "output_file": str(output_path),
        "summary": {
            "source_keys": len(source),
            "output_keys": len(output),
            "issues": len(issues),
            "by_type": counts,
        },
        "issues": issues,
    }


def output_relative_path(source_relative: Path) -> Path:
    name = source_relative.name
    if name.endswith("_l_english.yml"):
        name = name[: -len("_l_english.yml")] + "_l_simp_chinese.yml"
    return source_relative.with_name(name)


def source_relative_path(output_relative: Path) -> Path:
    name = output_relative.name
    if name.endswith("_l_simp_chinese.yml"):
        name = name[: -len("_l_simp_chinese.yml")] + "_l_english.yml"
    parts = list(output_relative.parts)
    parts[-1] = name
    parts = ["english" if part == "simp_chinese" else part for part in parts]
    return Path(*parts)


def run_recursive(
    source_root: Path,
    output_root: Path,
    glossary: Path,
    filename_pattern: re.Pattern[str] | None = None,
) -> dict:
    source_files = [
        path
        for path in sorted(source_root.rglob("*.yml"))
        if filename_pattern is None or filename_pattern.search(path.name)
    ]
    output_files = [
        path
        for path in sorted(output_root.rglob("*.yml"))
        if filename_pattern is None or filename_pattern.search(path.name)
    ] if output_root.exists() else []
    expected_output_names = {output_relative_path(path.relative_to(source_root)) for path in source_files}
    actual_output_names = {path.relative_to(output_root) for path in output_files}
    reports: list[dict] = []
    issues: list[dict] = []

    for source_path in source_files:
        relative = source_path.relative_to(source_root)
        output_path = output_root / output_relative_path(relative)
        if not output_path.exists():
            issues.append(
                {
                    "type": "missing_file",
                    "source_file": str(source_path),
                    "expected_output": str(output_path),
                }
            )
            continue
        report = run(source_path, output_path, glossary)
        reports.append(report)
        issues.extend(report["issues"])

    for relative in sorted(actual_output_names - expected_output_names):
        issues.append(
            {
                "type": "extra_file",
                "output_file": str(output_root / relative),
            }
        )

    counts: dict[str, int] = {}
    for issue in issues:
        counts[issue["type"]] = counts.get(issue["type"], 0) + 1
    return {
        "source_directory": str(source_root),
        "output_directory": str(output_root),
        "summary": {
            "source_files": len(source_files),
            "output_files": len(output_files),
            "files_checked": len(reports),
            "issues": len(issues),
            "by_type": counts,
        },
        "files": reports,
        # Recursive reports keep full issue details under each file. Do not
        # repeat the same issue list at the directory level.
        "directory_issues": [
            issue for issue in issues if issue.get("type") in {"missing_file", "extra_file"}
        ],
    }


def run_existing_outputs(
    source_root: Path,
    output_root: Path,
    glossary: Path,
    filename_pattern: re.Pattern[str] | None = None,
) -> dict:
    """Check only output files that already exist, without reporting untranslated source files."""
    output_files = [
        path
        for path in sorted(output_root.rglob("*.yml"))
        if filename_pattern is None or filename_pattern.search(path.name)
    ]
    reports: list[dict] = []
    issues: list[dict] = []
    for output_path in output_files:
        relative = output_path.relative_to(output_root)
        source_path = source_root / source_relative_path(relative)
        if not source_path.exists():
            issues.append(
                {
                    "type": "missing_source",
                    "output_file": str(output_path),
                    "expected_source": str(source_path),
                }
            )
            continue
        report = run(source_path, output_path, glossary)
        reports.append(report)
        issues.extend(report["issues"])

    counts: dict[str, int] = {}
    for issue in issues:
        counts[issue["type"]] = counts.get(issue["type"], 0) + 1
    return {
        "source_directory": str(source_root),
        "output_directory": str(output_root),
        "summary": {
            "source_files": 0,
            "output_files": len(output_files),
            "files_checked": len(reports),
            "issues": len(issues),
            "by_type": counts,
        },
        "files": reports,
        "directory_issues": [
            issue for issue in issues if issue.get("type") == "missing_source"
        ],
    }


def run_untranslated_only(
    source_root: Path,
    output_root: Path,
    filename_pattern: re.Pattern[str] | None = None,
) -> dict:
    """Fast scan for readable Latin text in existing output files only."""
    output_files = [
        path
        for path in sorted(output_root.rglob("*.yml"))
        if filename_pattern is None or filename_pattern.search(path.name)
    ]
    reports: list[dict] = []
    issues: list[dict] = []
    for output_path in output_files:
        relative = output_path.relative_to(output_root)
        source_path = source_root / source_relative_path(relative)
        source = parse_localization(source_path) if source_path.exists() else {}
        output = parse_localization(output_path)
        file_issues = untranslated_issues(source, output)
        reports.append(
            {
                "source_file": str(source_path),
                "output_file": str(output_path),
                "summary": {
                    "output_keys": len(output),
                    "issues": len(file_issues),
                    "by_type": {"untranslated_text": len(file_issues)}
                    if file_issues
                    else {},
                },
                "issues": file_issues,
            }
        )
        issues.extend(file_issues)

    return {
        "source_directory": str(source_root),
        "output_directory": str(output_root),
        "summary": {
            "source_files": 0,
            "output_files": len(output_files),
            "files_checked": len(reports),
            "issues": len(issues),
            "by_type": {"untranslated_text": len(issues)} if issues else {},
        },
        "files": reports,
        "directory_issues": [],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--glossary", default="translation_glossary.yml", type=Path)
    parser.add_argument("--report", default="work/reports/translation_qa.json", type=Path)
    parser.add_argument(
        "--filename-regex",
        help="Only check files whose basename matches this regular expression",
    )
    parser.add_argument(
        "--output-only",
        action="store_true",
        help="Only check existing output files; do not report missing output files",
    )
    parser.add_argument(
        "--untranslated-only",
        action="store_true",
        help="Only scan output human-readable text for untranslated Latin words",
    )
    args = parser.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    if args.source.is_dir():
        filename_pattern = re.compile(args.filename_regex, re.IGNORECASE) if args.filename_regex else None
        if args.untranslated_only:
            report = run_untranslated_only(args.source, args.output, filename_pattern)
        elif args.output_only:
            report = run_existing_outputs(args.source, args.output, args.glossary, filename_pattern)
        else:
            report = run_recursive(args.source, args.output, args.glossary, filename_pattern)
    else:
        report = run(args.source, args.output, args.glossary)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report["summary"], ensure_ascii=False, indent=2))
    print(f"wrote: {args.report}")


if __name__ == "__main__":
    main()
