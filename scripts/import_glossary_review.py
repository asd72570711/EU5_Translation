from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


DEFAULT_REVIEW = Path("work/glossary_review/review.json")
DEFAULT_GLOSSARY = Path("translation_glossary.yml")

CONTEXTUAL_DERIVED_TERMS = {
    "Aretine",
    "Basque",
    "Breton",
    "British",
    "Byzantine",
    "Castilian",
    "Catalan",
    "Corsican",
    "Ferrarese",
    "Florentine",
    "Irish",
    "Japanese",
    "Neapolitan",
    "Piscan",
    "Roman",
    "Scottish",
    "Venetian",
    "Welsh",
    "Beja",
    "Circassian",
    "Coptic",
    "Egyptian",
    "Finnish",
    "Malagasy",
    "Mazovian",
    "Mecklenburgian",
    "Pomeranian",
    "Saxon",
    "Shan",
    "Silesian",
    "Cog",
    "Control",
    "Devotion",
}

LANGUAGE_TERMS = {
    "Basque",
    "Castilian",
    "Catalan",
    "Irish",
    "Japanese",
    "Welsh",
}

WHEN_ADJECTIVE = "\u4f5c\u5f62\u5bb9\u8a5e\uff0c\u4fee\u98fe\u5730\u5340\u3001\u6587\u5316\u3001\u52e2\u529b\u6216\u4e8b\u7269"
WHEN_PEOPLE = "\u6307\u4eba\u6216\u65cf\u7fa4"
WHEN_LANGUAGE = "\u6307\u8a9e\u8a00"
PERSON_SUFFIX = "\u4eba"
LANGUAGE_SUFFIX = "\u8a9e"
CONTROL_VALUES = {"ai", "cont", "skip"}

CONTEXTUAL_RULES = {
    "Autonomy": [
        ("自治", "指自治運動、分權方向或一般自治概念"),
        ("自治權", "指政治實體、地區、階層或群體所擁有的自治權利或權限"),
    ],
    "Advance": [
        ("革新", "指科技、知識或制度的革新"),
        ("推進", "指推進流程、計畫或行動，而非科技名詞"),
    ],
    "Capital": [
        ("首都", "指政治實體的首都或首府"),
        ("資本", "指經濟、金融或資產語境"),
    ],
    "Irrigation": [
        ("灌溉設施", "指遊戲中的灌溉建設、設施或投資"),
        ("灌溉", "指一般農業活動、政策或過程"),
    ],
    "Favors": [
        ("人情", "指政治、階層或外交關係中的可用人情資源"),
        ("恩惠", "指一般敘事中的個人恩惠或情分"),
    ],
    "Favor": [
        ("人情", "指政治、階層或外交關係中的可用人情資源"),
        ("恩惠", "指一般敘事中的個人恩惠或情分"),
    ],
    "Islamic": [
        ("伊斯蘭的", "作形容詞，修飾文化、制度、學院、教義或事物"),
        ("伊斯蘭教的", "明確修飾宗教、信仰或教派語境"),
    ],
    "Location": [
        ("地點", "指遊戲中的地點、位置或 location 物件"),
    ],
    "Mason": [
        ("石匠", "指從事砌石或建築工作的職業、人物或群體"),
        ("磚窯", "指遊戲中的 mason 建築類型或相關建築物"),
    ],
    "Rival": [
        ("宿敵", "指遊戲中被指定為 rival 的國家、角色或勢力"),
        ("競爭對手", "指一般競爭關係，且未被指定為遊戲 rival"),
    ],
    "Bahan": [
        ("八幡", "指日本文化或宗教相關的八幡概念"),
        ("八幡貿易", "指文本中的 Bahan Trade，即以海盜劫掠為主的貿易活動"),
    ],
    "Cannon": [
        ("火炮", "指大砲、砲兵武器或軍事裝備"),
        ("炮灰", "出現在 cannon fodder 詞組中，指被當作消耗品投入戰鬥的人員"),
    ],
    "Catholic": [
        ("天主教的", "作形容詞，修飾教會、宗教、信仰、人物或相關事物"),
        ("天主教徒", "指信仰天主教的人或天主教族群"),
    ],
    "Bavarian": [
        ("巴伐利亞的", "作形容詞，修飾巴伐利亞的地區、政體、文化或人物"),
        ("巴伐利亞人", "指巴伐利亞人或巴伐利亞族群"),
    ],
    "General": [
        ("將軍", "指軍事階級或軍事指揮官"),
        ("一般", "作形容詞，表示普遍、概括或非特定的情況"),
    ],
    "Mandate": [
        ("天命", "指 Mandate of Heaven 等中國政治或宗教概念"),
        ("命令", "作動詞或一般政治語境，表示下令、授權或要求執行"),
    ],
    "Mossi": [
        ("莫西", "作地區、政體或相關名稱的修飾語"),
        ("莫西人", "指莫西人或莫西族群"),
    ],
    "Protestant": [
        ("新教的", "作形容詞，修飾新教信仰、教派、人物或事物"),
        ("新教徒", "指新教徒或新教信仰者"),
    ],
    "Puritan": [
        ("清教徒", "指清教徒或清教徒群體"),
        ("清教的", "作形容詞，修飾清教信仰、價值或相關事物"),
    ],
    "Mary": [
        ("瑪利亞", "指基督教或聖經語境中的耶穌之母"),
        ("瑪莉", "指一般西式人名，且語境採用此譯名"),
        ("瑪麗", "指一般西式人名，且語境採用此譯名"),
    ],
    "Norman": [
        ("諾曼", "作形容詞，修飾諾曼文化、制度或事物"),
        ("諾曼人", "指諾曼人或諾曼族群"),
        ("諾曼語", "指諾曼語言"),
    ],
    "Patriarchy": [
        ("牧首區", "指東正教等宗教體系中的牧首管轄區或宗教組織"),
        ("父權制", "指一般政治、社會或家庭制度中的 patriarchy"),
    ],
    "Beja": [
        ("貝雅", "指非洲的貝雅民族、文化或政體"),
        ("貝賈", "指葡萄牙地名或相關政體"),
    ],
    "Circassian": [
        ("切爾克西亞的", "作形容詞，修飾切爾克西亞地區、文化、政體或相關事物"),
        ("切爾克西亞人", "指切爾克西亞人或其族群"),
    ],
    "Coptic": [
        ("科普特的", "作形容詞，修飾科普特文化、宗教或相關事物"),
        ("科普特人", "指科普特人或科普特族群"),
        ("科普特語", "指科普特語言"),
    ],
    "Egyptian": [
        ("埃及的", "作形容詞，修飾埃及地區、政體、文化或相關事物"),
        ("埃及人", "指埃及人或埃及族群"),
        ("埃及語", "指埃及語言"),
    ],
    "Finnish": [
        ("芬蘭的", "作形容詞，修飾芬蘭地區、文化、政體或相關事物"),
        ("芬蘭人", "指芬蘭人或芬蘭族群"),
        ("芬蘭語", "指芬蘭語言"),
    ],
    "Malagasy": [
        ("馬拉加斯的", "作形容詞，修飾馬拉加斯地區、政體、文化或相關事物"),
        ("馬拉加斯人", "指馬拉加斯人或其族群"),
        ("馬拉加斯語", "指馬拉加斯語言"),
    ],
    "Mazovian": [
        ("馬佐維亞的", "作形容詞，修飾馬佐維亞地區、政體、文化或相關事物"),
        ("馬佐維亞人", "指馬佐維亞人或其族群"),
    ],
    "Mecklenburgian": [
        ("梅克倫堡的", "作形容詞，修飾梅克倫堡地區、政體、文化或相關事物"),
        ("梅克倫堡人", "指梅克倫堡人或其族群"),
    ],
    "Pomeranian": [
        ("波美拉尼亞的", "作形容詞，修飾波美拉尼亞地區、政體、文化或相關事物"),
        ("波美拉尼亞人", "指波美拉尼亞人或其族群"),
    ],
    "Saxon": [
        ("薩克森的", "作形容詞，修飾德意志薩克森地區、政體、文化或相關事物"),
        ("薩克森人", "指德意志薩克森人或其族群"),
        ("薩克森語", "指薩克森語言"),
    ],
    "Shan": [
        ("撣族", "指撣族、撣族文化或相關政體"),
        ("撣語", "指撣語言"),
        ("撣族的", "作形容詞，修飾撣族地區、文化或事物"),
    ],
    "Silesian": [
        ("西里西亞的", "作形容詞，修飾西里西亞地區、政體、文化或相關事物"),
        ("西里西亞人", "指西里西亞人或其族群"),
    ],
    "Cog": [
        ("齒輪", "指 UI 中的齒輪圖示或齒輪按鈕"),
        ("柯克船", "指中世紀帆船類型 cog"),
    ],
    "Control": [
        ("控制力", "指遊戲中的地區、社會或政治控制力數值"),
        ("控制", "指一般控制、支配或管理行為"),
    ],
    "Devotion": [
        ("奉獻度", "指遊戲中的宗教或政府數值、機制或指標"),
        ("虔誠", "指一般宗教語境中的虔誠、敬虔或信仰投入"),
    ],
    "Ivan": [
        ("伊凡", "指俄羅斯、保加利亞等東歐歷史人物姓名，或 Novgorod 的 Ivan's Hundred"),
        ("伊萬", "指專案既有譯名或特定人物語境採用伊萬的音譯"),
    ],
    "Lombard": [
        ("倫巴底的", "作形容詞，修飾倫巴底的王國、地區、文化、勢力或事物"),
        ("倫巴底人", "指倫巴底族群或人物"),
        ("倫巴底語", "指 Lombard 語言"),
    ],
    "Bubu": [
        ("魚籠", "指 Bubu 建築或當地魚籠陷阱"),
        ("布布", "指人物姓名或其他專有名詞"),
    ],
    "Dock": [
        ("船塢", "指遊戲中的 Dock 建築或建造、修理船隻的設施"),
        ("停靠", "作動詞，指船隻停靠港口或船塢"),
    ],
    "Sect": [
        ("宗派", "指遊戲中的宗教宗派或 Sect 國際組織"),
        ("教派", "指一般宗教語境中的 sect，且不作為遊戲機制名稱"),
    ],
    "Siberian": [
        ("西伯利亞", "作地理或環境修飾語，例如 Siberian wilds、Siberian forests"),
        ("西伯利亞的", "作一般形容詞，修飾西伯利亞相關的地區、文化或事物"),
        ("西伯利亞人", "指西伯利亞文化或族群"),
        ("西伯利亞語", "指西伯利亞語言"),
    ],
    "Yamashiro": [
        ("山城", "指日本山地的土木與木柵防禦建築"),
        ("山城國", "指日本歷史上的山城國、相關省份或政體"),
        ("山城氏", "指 Yamashiro 家族或王朝名稱"),
    ],
    "Andean": [
        ("安地斯的", "作形容詞，修飾安地斯地區、文化、宗教或相關事物"),
        ("安地斯人", "指安地斯地區人民或族群"),
    ],
    "Arabian": [
        ("阿拉伯的", "作形容詞，修飾阿拉伯地區、文化、海域、馬匹或相關事物"),
        ("阿拉伯人", "指阿拉伯人或阿拉伯族群"),
    ],
    "Chancery": [
        ("秘書室", "指遊戲中的 Chancery 建築或政府文書辦公機構"),
        ("文書署", "指歷史或行政語境中的 chancery 文書機關"),
    ],
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def yaml_quote(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def glossary_terms(text: str) -> set[str]:
    terms: set[str] = set()
    alias_term: str | None = None
    alias_names: list[str] = []
    in_aliases = False

    def flush_alias() -> None:
        if alias_term:
            terms.add(alias_term)
            terms.update(alias_names)

    for line in text.splitlines():
        if line == "aliases:":
            flush_alias()
            in_aliases = True
            alias_term = None
            alias_names = []
            continue
        if in_aliases and line and not line.startswith(" "):
            flush_alias()
            in_aliases = False
            alias_term = None
            alias_names = []

        if in_aliases:
            alias = re.match(r"^  (?! )([^:#][^:]+):\s*$", line)
            if alias:
                flush_alias()
                alias_term = alias.group(1).strip()
                alias_names = []
                continue
            also = re.match(r"^      -\s+(.+?)\s*$", line)
            if also and alias_term:
                alias_names.append(also.group(1).strip())
            continue

        match = re.match(r"^  (?! )([^:#][^:]+):", line)
        if match:
            terms.add(match.group(1).strip())
    flush_alias()
    return terms


def importable_items(
    review: dict[str, Any],
    resolved_only: bool,
    include_cont: bool,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    items = []
    contextual_items = []
    for item in review.get("items", []):
        status = item.get("status")
        translation = item.get("translation", "").strip()
        if status == "skip":
            continue
        if status == "cont":
            if not include_cont:
                continue
            if not translation:
                if resolved_only:
                    continue
                raise ValueError(f"Missing translation for {item.get('term')}")
            if item.get("term") in CONTEXTUAL_RULES or item.get("term") in CONTEXTUAL_DERIVED_TERMS:
                contextual_items.append(item)
            else:
                items.append(item)
            continue
        if status not in {"todo", "ai"}:
            if resolved_only:
                # Keep malformed or user-entered statuses for manual repair.
                continue
            raise ValueError(f"Unsupported status for {item.get('term')}: {status}")
        if status == "todo" and translation.lower() in CONTROL_VALUES:
            raise ValueError(
                f"Control value used as translation for {item.get('term')}; use status instead"
            )
        if not translation:
            if resolved_only:
                continue
            raise ValueError(f"Missing translation for {item.get('term')}")
        if resolved_only and status not in {"todo", "ai"}:
            continue
        items.append(item)
    return items, contextual_items


def remove_processed_items(review: dict[str, Any], imported_terms: set[str]) -> dict[str, int]:
    retained = []
    removed_skip = 0
    removed_imported = 0
    for item in review.get("items", []):
        if item.get("status") == "skip":
            removed_skip += 1
            continue
        if item.get("term") in imported_terms and item.get("status") in {"todo", "ai", "cont"}:
            removed_imported += 1
            continue
        retained.append(item)
    review["items"] = retained
    return {"removed_skip": removed_skip, "removed_imported": removed_imported}


def yaml_inline_comment(note: str) -> str:
    return " / ".join(line.strip() for line in note.splitlines() if line.strip())


def person_or_group(translation: str) -> str:
    if translation.endswith(PERSON_SUFFIX):
        return translation
    return translation + PERSON_SUFFIX


def contextual_block(term: str, translation: str, note: str) -> list[str]:
    heading = f"  {term}:"
    if note:
        heading += f"  # {yaml_inline_comment(note)}"
    senses = CONTEXTUAL_RULES.get(
        term,
        [
            (translation, WHEN_ADJECTIVE),
            (person_or_group(translation), WHEN_PEOPLE),
        ],
    )
    default = senses[0][0] if term in CONTEXTUAL_RULES else translation
    lines = [heading, f"    default: {yaml_quote(default)}", "    senses:"]
    for zh, when in senses:
        lines.extend([f"      - zh: {yaml_quote(zh)}", f"        when: {yaml_quote(when)}"])
    if term in LANGUAGE_TERMS:
        lines.extend(
            [
                f"      - zh: {yaml_quote(translation + LANGUAGE_SUFFIX)}",
                f"        when: {yaml_quote(WHEN_LANGUAGE)}",
            ]
        )
    return lines


def apply_import(
    glossary_text: str,
    items: list[dict[str, Any]],
    contextual_items: list[dict[str, Any]],
) -> tuple[str, dict[str, int]]:
    existing = glossary_terms(glossary_text)
    fixed_items: list[tuple[str, str, str]] = []
    contextual_lines: list[str] = []
    skipped_existing = 0

    for item in contextual_items:
        term = item["term"]
        if term in existing:
            skipped_existing += 1
            continue
        contextual_lines.extend(
            contextual_block(term, item["translation"].strip(), item.get("note", "").strip())
        )
        existing.add(term)

    for item in items:
        term = item["term"]
        translation = item["translation"].strip()
        if term in existing:
            skipped_existing += 1
            continue
        if term in CONTEXTUAL_DERIVED_TERMS:
            note = item.get("note", "").strip()
            contextual_lines.extend(contextual_block(term, translation, note))
        else:
            fixed_items.append((term, translation, item.get("note", "").strip()))
        existing.add(term)

    lines = glossary_text.splitlines()
    if fixed_items:
        fixed_lines: list[str] = []
        # Preserve review order; glossary sorting is an explicit separate operation.
        for term, translation, note in fixed_items:
            line = f"  {term}: {yaml_quote(translation)}"
            if note:
                line += f"  # {yaml_inline_comment(note)}"
            fixed_lines.append(line)
        aliases_index = next(i for i, line in enumerate(lines) if line.startswith("aliases:"))
        lines[aliases_index:aliases_index] = fixed_lines + [""]

    if contextual_lines:
        reference_index = next(
            i for i, line in enumerate(lines) if line == "reference_terms:"
        )
        lines[reference_index:reference_index] = [""] + contextual_lines

    stats = {
        "fixed_added": len(fixed_items),
        "contextual_added": sum(1 for line in contextual_lines if re.match(r"^  [^ ].*:$", line)),
        "skipped_existing": skipped_existing,
    }
    return "\n".join(lines) + "\n", stats


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--review", default=str(DEFAULT_REVIEW))
    parser.add_argument("--glossary", default=str(DEFAULT_GLOSSARY))
    parser.add_argument(
        "--resolved-only",
        action="store_true",
        help="Import filled todo items and remove them plus skip items from the review",
    )
    parser.add_argument(
        "--include-cont",
        action="store_true",
        help="Import cont items only after AI has completed contextual judgment",
    )
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    sys.stdout.reconfigure(encoding="utf-8")

    review_path = Path(args.review)
    glossary_path = Path(args.glossary)
    review = json.loads(review_path.read_text(encoding="utf-8"))
    glossary_text = read_text(glossary_path)
    items, contextual_items = importable_items(
        review,
        args.resolved_only,
        args.include_cont,
    )
    new_text, stats = apply_import(glossary_text, items, contextual_items)

    stats["importable_items"] = len(items)
    stats["pending_contextual"] = len(contextual_items)
    stats["contextual_terms"] = [item.get("term") for item in contextual_items]
    stats["resolved_only"] = args.resolved_only
    print(json.dumps(stats, ensure_ascii=False, indent=2))
    if args.write:
        if new_text != glossary_text:
            glossary_path.write_text(new_text, encoding="utf-8")
            print(f"wrote: {glossary_path}")
        else:
            print(f"unchanged: {glossary_path}")
        if args.resolved_only:
            cleanup = remove_processed_items(
                review,
                {item["term"] for item in items + contextual_items},
            )
            review_path.write_text(
                json.dumps(review, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            print(json.dumps(cleanup, ensure_ascii=False, indent=2))
    else:
        print("dry-run only; pass --write to update glossary")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
