import re
import sys
from pathlib import Path


PATH = Path("translation_glossary.yml")
SECTION_NAMES = {"fixed", "aliases", "contextual", "reference_terms"}
ENTRY_RE = re.compile(r"^  (?! )([^:#][^:]*):")


def entry_name(block: list[str]) -> str:
    match = ENTRY_RE.match(block[0])
    if not match:
        raise ValueError(f"Cannot determine glossary entry name: {block[0]!r}")
    return match.group(1).strip()


def split_sections(lines: list[str]) -> tuple[list[str], dict[str, list[str]]]:
    headers: list[str] = []
    sections: dict[str, list[str]] = {}
    current = None
    for line in lines:
        if line and not line.startswith(" ") and line.rstrip(":") in SECTION_NAMES:
            current = line.rstrip(":")
            headers.append(current)
            sections[current] = []
            continue
        if current is None:
            headers.append(line)
        else:
            sections[current].append(line)
    return headers, sections


def split_blocks(lines: list[str]) -> list[list[str]]:
    blocks: list[list[str]] = []
    current: list[str] = []
    for line in lines:
        if ENTRY_RE.match(line):
            if current and any(part.strip() for part in current):
                blocks.append(current)
            current = [line]
        elif current:
            current.append(line)
        elif line.strip():
            raise ValueError(f"Unexpected content before first entry: {line!r}")
    if current and any(part.strip() for part in current):
        blocks.append(current)
    return blocks


def clean_block(block: list[str]) -> list[str]:
    while block and not block[0].strip():
        block.pop(0)
    while block and not block[-1].strip():
        block.pop()
    return block


def sort_fixed(lines: list[str]) -> list[str]:
    blocks = [clean_block(block) for block in split_blocks(lines)]
    blocks.sort(key=lambda block: entry_name(block).casefold())
    return [line for block in blocks for line in block]


def sort_alias_block(block: list[str]) -> list[str]:
    result = []
    also_start = None
    also_end = None
    for index, line in enumerate(block):
        if line == "    also:":
            also_start = index
            also_end = index + 1
            while also_end < len(block) and block[also_end].startswith("      - "):
                also_end += 1
            break
    if also_start is None:
        return block
    result.extend(block[:also_start + 1])
    variants = sorted(block[also_start + 1:also_end], key=lambda line: line[8:].casefold())
    result.extend(variants)
    result.extend(block[also_end:])
    return result


def sort_aliases(lines: list[str]) -> list[str]:
    blocks = [sort_alias_block(clean_block(block)) for block in split_blocks(lines)]
    blocks.sort(key=lambda block: entry_name(block).casefold())
    return [line for block in blocks for line in block]


def sort_contextual(lines: list[str]) -> list[str]:
    blocks = [clean_block(block) for block in split_blocks(lines)]
    blocks.sort(key=lambda block: entry_name(block).casefold())
    return [line for block in blocks for line in block]


def sort_reference_terms(lines: list[str]) -> list[str]:
    blocks = [clean_block(block) for block in split_blocks(lines)]
    blocks.sort(key=lambda block: entry_name(block).casefold())
    return [line for block in blocks for line in block]


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    original = PATH.read_text(encoding="utf-8-sig")
    lines = original.splitlines()
    prefix: list[str] = []
    sections: dict[str, list[str]] = {}
    current = None
    for line in lines:
        if line and not line.startswith(" ") and line.rstrip(":") in SECTION_NAMES:
            current = line.rstrip(":")
            sections[current] = []
            continue
        if current is None:
            prefix.append(line)
        else:
            sections[current].append(line)

    while prefix and not prefix[-1].strip():
        prefix.pop()
    output = prefix + [""]
    for name, sorter in (
        ("fixed", sort_fixed),
        ("aliases", sort_aliases),
        ("contextual", sort_contextual),
        ("reference_terms", sort_reference_terms),
    ):
        output.append(f"{name}:")
        output.extend(sorter(sections[name]))
        if name != "reference_terms":
            output.append("")
    new_text = "\n".join(output).rstrip() + "\n"
    if new_text == original:
        print("unchanged")
        return
    PATH.write_text(new_text, encoding="utf-8")
    print("sorted: translation_glossary.yml")


if __name__ == "__main__":
    main()
