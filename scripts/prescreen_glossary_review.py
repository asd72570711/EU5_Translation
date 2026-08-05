from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

from scan_glossary_candidates import (
    build_review_item,
    candidates,
    glossary_entries,
    parse_entries,
)


DIRECTIVE_RE = re.compile(
    r"^(begin|cancel|click|close|continue|do explain|left-?click|next|open|"
    r"read later|repeat|right-?click|skip lesson|tell me more|try|use|"
    r"select|switch|toggle|hover)\b",
    re.IGNORECASE,
)
ACTION_RE = re.compile(
    r"^(abandon|abolish|abort|absorb|accept|access|acquire|activate|add|affirm|appease|become|ban|break|build|call|claim|complete|conquer|corrupt|create|curb|deny|destroy|develop|disable|dismiss|"
    r"get|give|join|master|open|own|reach|restore|rule|take|win|clear|"
    r"cancel|cede|copy|decline|delete|demand|dissolve|enforce|force|release|"
    r"revoke|save|seize|select|send|spread|subjugate|switch|toggle|visit|"
    r"improve|increase|decrease|establish|declare|grant|appoint|remove|change|"
    r"lose|hold|accept|reject|annex|reform|reduce|raise|lower|end|enable|expand|"
    r"export|expel|favor|find|fortify|invite|limit|negotiate|offer|purchase|request|"
    r"share|sponsor|strengthen|support|suppress|transfer|vote|choose)\b",
    re.IGNORECASE,
)
RESULT_PHRASE_RE = re.compile(
    r"\b(abandoned|accepted|annexed|appointed|broken|cancelled|canceled|"
    r"changed|cleared|closed|completed|conquered|created|declared|defeated|"
    r"established|formed|gained|granted|integrated|lost|opened|owned|"
    r"reformed|rejected|removed|restored|retreating|lent|sold|visible|"
    r"converted|won)\s*$",
    re.IGNORECASE,
)
STATUS_PREFIX_RE = re.compile(
    r"^(abandoned|approved|cancelled|canceled|denied|granted|imposed|"
    r"integrated|reinstated|removed|restored|returned|revoked|supported|"
    r"terminated|withdrawn)\b.*\b(of|de|del|da|di|du|von|van)\b",
    re.IGNORECASE,
)
NARRATIVE_RE = re.compile(
    r"^(a|an|another|as|our|the|this|that|these|those|what|when|while|"
    r"if|although|instead|no|not|once|rather|we|you)\b",
    re.IGNORECASE,
)
PREDICATE_RE = re.compile(
    r"^(is|are|was|were|has|have|can|cannot|does|do|did|not|never|"
    r"exists|owns|owned|requires|allows|contains|includes)\b",
    re.IGNORECASE,
)
PAST_PARTICIPLE_RE = re.compile(r"^[A-Za-z]+ed$", re.IGNORECASE)
IRREGULAR_RESULT_WORDS = {"born", "given", "left", "lost", "won"}
COMMAND_RE = re.compile(
    r"^(open|close|click(?:ing)?|double[-‑]?click(?:ing)?|left[-‑]?click(?:ing)?|"
    r"right[-‑]?click(?:ing)?|select|toggle|switch|"
    r"cancel|load|save|start|show|hide|delete|copy)\b",
    re.IGNORECASE,
)
OBVIOUS_PREFIX_RE = re.compile(
    r"^(after|although|alternatively|always|another|any|are|as|aside|at|being|"
    r"between|for|from|if|in|instead|it|no|not|of|on|once|our|rather|that|"
    r"these|they|this|those|to|we|when|while|with|you)\b",
    re.IGNORECASE,
)
COMMON_WORDS = {
    "a", "all", "and", "are", "as", "at", "be", "been", "being", "can", "clear",
    "country", "create", "do", "for", "from", "get", "have", "if", "in", "is", "it",
    "of", "on", "or", "our", "the", "this", "to", "was", "we", "when", "with", "you",
}
STANDALONE_VERBS = {
    "abandon", "abolish", "abort", "absorb", "accept", "access", "acquire", "activate", "add", "begin", "become", "ban", "break", "build", "cancel", "claim", "clear",
    "click", "complete", "conquer", "confirm", "continue", "create", "decline",
    "delete", "demand", "discard", "dissolve", "employ", "enforce", "exit", "form",
    "gain", "get", "give", "improve", "increase", "integrate", "join", "load", "open",
    "own", "reach", "recruit", "reload", "remove", "restore", "revoke", "save", "select",
    "send", "seize", "skip", "spread", "start", "subjugate", "suggest", "switch", "take",
    "toggle", "use", "visit", "win", "choose", "appease", "call", "charter", "corrupt", "curb", "deny", "destroy", "develop", "disable", "dismiss", "enable", "end", "expand", "expel", "export", "favor", "find", "fortify", "grant", "invite", "limit", "negotiate", "offer", "purchase", "reduce", "reform", "request", "share", "sponsor", "spread", "strengthen", "support", "suppress", "transfer", "vote",
}
PHRASE_VERBS = STANDALONE_VERBS | {
    "abolish", "abort", "absorb", "affirm", "agree", "annex", "appease", "appoint", "apply", "assign", "await", "call", "cede", "charter", "change", "convert", "curb", "deselect", "disband", "disembark", "dismantle", "distribute", "embark", "embrace", "engage", "expel",
    "declare", "decrease", "enforce", "establish", "force", "hold", "lose", "lower",
    "colonize", "exchange", "extend", "fail", "fight", "finish", "grow", "hire", "insult", "leave", "lend", "master", "merge", "move", "need", "oppose", "pause", "profess", "recover", "reorganize", "remain", "remove", "repair", "repay", "reject", "respond", "restore", "return", "reset", "rule", "seize", "show", "surrender", "take", "trade",
    "transfer", "try", "upgrade", "vote",
}
FIXED_ACTION_TERMS = {"upgrade", "recruit", "integrate", "colonize", "convert"}
STANDALONE_PREDICATES = {"are", "exists", "never", "not", "owns", "requires"}
STANDALONE_COMMANDS = {
    "click", "clicking", "double-click", "double-clicking", "left-click", "left-clicking",
    "right-click", "right-clicking", "open", "select", "show", "toggle",
}
STANDALONE_ADJECTIVES = {
    "active", "available", "different", "easy", "excellent", "great", "hard",
    "historical", "important", "invalid", "local", "manual", "maximum", "minimum",
    "monthly", "possible", "recent", "strong", "weak",
}
STANDALONE_GENERIC_WORDS = {
    "all", "another", "any", "every", "her", "his", "how", "its", "my", "no",
    "our", "she", "some", "that", "their", "these", "this", "those", "us", "we",
    "what", "when", "where", "which", "who", "why", "you", "your",
}
GENERIC_DETERMINER_RE = re.compile(
    r"^(all|another|any|every|her|his|my|no|our|some|that|their|these|this|those|"
    r"what|when|where|which|who|why|you|your)\s+",
    re.IGNORECASE,
)
MECHANIC_RE = re.compile(
    r"\b(action|alert|army|balance|bureaucracy|building|cabinet|character|"
    r"country|culture|diplom|estate|government|law|location|market|mission|"
    r"modifier|parliament|production|religion|stability|subject|trade|"
    r"treaty|trigger|war|wealth|work|works?)\b",
    re.IGNORECASE,
)
PROTECTED_CATEGORY = {"event", "person", "person_or_place", "organization", "title_or_role", "work_title"}


def source_paths(review: dict[str, Any], source_root: Path) -> list[Path]:
    paths = []
    for relative in review.get("source_file", []):
        path = source_root / relative
        if path.is_file():
            paths.append(path)
        elif path.is_dir():
            paths.extend(sorted(path.rglob("*.yml")))
    return paths


def is_tutorial(keys: list[str]) -> bool:
    return bool(keys) and all(k.lower().startswith(("lesson_", "tutorial_")) for k in keys)


def is_achievement(keys: list[str]) -> bool:
    return bool(keys) and all(k.upper().startswith("ACHIEVEMENT") for k in keys)


def is_inflected_action(word: str) -> bool:
    forms = {word.casefold()}
    if word.endswith("ing") and len(word) > 4:
        stem = word[:-3].casefold()
        forms.update({stem, stem + "e"})
        if len(stem) > 1 and stem[-1] == stem[-2]:
            forms.add(stem[:-1])
    if word.endswith("ed") and len(word) > 3:
        stem = word[:-2].casefold()
        forms.update({stem, stem + "e"})
        if stem.endswith("i"):
            forms.add(stem[:-1] + "y")
    if word.endswith("ies") and len(word) > 4:
        forms.add((word[:-3] + "y").casefold())
    elif word.endswith("s") and len(word) > 3:
        forms.add(word[:-1].casefold())
    return bool(forms & PHRASE_VERBS)


def is_generic_action_phrase(term: str) -> bool:
    words = [word.casefold() for word in re.findall(r"[A-Za-z]+(?:[-\u2011][A-Za-z]+)?", term)]
    if len(words) < 2:
        return False
    if is_inflected_action(words[0]):
        return True
    if re.fullmatch(r"order\s+(?:assault|full\s+retreat)", term, re.IGNORECASE):
        return True
    if PAST_PARTICIPLE_RE.fullmatch(words[-1]) and not words[-1].endswith("eed"):
        return True
    if words[0] == "constructing":
        return True
    if term.casefold() in {"gathering food", "dismantle the pest houses"}:
        return True
    return bool(RESULT_PHRASE_RE.search(term))


def should_skip(item: dict[str, Any]) -> bool:
    term = str(item.get("term", "")).strip()
    keys = [str(key) for key in item.get("keys", [])]

    # Tutorial instructions are one-off directions, not reusable terminology.
    if is_tutorial(keys) and DIRECTIVE_RE.search(term):
        return True

    # Predicate and command labels are code-like conditions or UI actions,
    # even when category guessing mistakes a connector for a proper name.
    if PREDICATE_RE.search(term) and len(term.split()) >= 2:
        return True
    if COMMAND_RE.search(term) and (len(term.split()) >= 2 or "-" in term or "‑" in term):
        return True
    if term.lower() in STANDALONE_COMMANDS or term.lower() in STANDALONE_PREDICATES:
        return True
    if term.lower() in STANDALONE_ADJECTIVES:
        return True
    if term.lower() in STANDALONE_GENERIC_WORDS:
        return True
    if GENERIC_DETERMINER_RE.search(term) and len(term.split()) >= 2:
        return True

    # Generic action/result phrases are translated from context rather than
    # stored as glossary entries. The scanner separately preserves embedded
    # proper-name candidates such as "Confession of Biljno Polje".
    if is_generic_action_phrase(term):
        return True

    # Status/result modifiers before a connector phrase, for example
    # "Abandoned Exemption of Sound Toll", are usually one-off labels.
    # The connector phrase is extracted separately by the candidate scanner.
    if STATUS_PREFIX_RE.search(term):
        return True

    if item.get("category") in PROTECTED_CATEGORY:
        return False

    # Standalone past participles are normally message/status labels rather
    # than reusable glossary terms. Exclude noun-like words ending in -eed.
    if len(term.split()) == 1 and PAST_PARTICIPLE_RE.fullmatch(term) and not term.lower().endswith("eed"):
        return True
    if len(term.split()) == 1 and term.casefold() in IRREGULAR_RESULT_WORDS:
        return True

    # Construction and maintenance localization keys use action labels as
    # resource/status names; translate the full sentence from context.
    key_text = " ".join(keys).lower()
    if (
        ("_construction" in key_text or "_maintenance" in key_text)
        and re.match(r"^(constructing|distill)\b", term, re.IGNORECASE)
    ):
        return True

    if term.casefold().startswith("detach ") and item.get("category") == "unknown":
        return True

    # Achievement titles are retained only when they look like a mechanic,
    # historical name, work title, organization, or other reusable term.
    if is_achievement(keys):
        if MECHANIC_RE.search(term):
            return False
        if ACTION_RE.search(term) or len(term.split()) >= 3:
            return True

    words = {word.lower() for word in re.findall(r"[A-Za-z]+", term)}
    if OBVIOUS_PREFIX_RE.search(term) and len(term.split()) >= 2 and not MECHANIC_RE.search(term):
        return True
    if len(words) >= 2 and words and words <= COMMON_WORDS:
        return True
    if len(words) == 1 and term.lower() in STANDALONE_VERBS:
        return term.lower() not in FIXED_ACTION_TERMS
    if len(words) == 1 and is_inflected_action(term):
        return term.lower() not in FIXED_ACTION_TERMS
    if PREDICATE_RE.search(term) and len(term.split()) >= 2:
        return True

    # Generic narrative fragments are not glossary terms. Short noun phrases
    # remain pending because they may still be UI terms or historical names.
    if NARRATIVE_RE.search(term) and len(term.split()) >= 4 and not MECHANIC_RE.search(term):
        return True

    return False


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--review", default="work/glossary_review/review.json")
    parser.add_argument("--source-root", default="source/english")
    parser.add_argument("--glossary", default="translation_glossary.yml")
    parser.add_argument("--write", action="store_true")
    parser.add_argument(
        "--existing-only",
        action="store_true",
        help="only update existing todo/cont items; do not rescan source files",
    )
    args = parser.parse_args()

    review_path = Path(args.review)
    review = json.loads(review_path.read_text(encoding="utf-8"))
    glossary = glossary_entries(Path(args.glossary))
    existing = {item.get("term"): item for item in review.get("items", []) if item.get("term")}

    scanned: dict[str, set[str]] = {}
    if not args.existing_only:
        for source_file in source_paths(review, Path(args.source_root)):
            for term, keys in candidates(parse_entries(source_file)).items():
                scanned.setdefault(term, set()).update(keys)

    added = 0
    for term, keys in scanned.items():
        if term in glossary or term in existing:
            continue
        candidate = build_review_item(term, sorted(keys), glossary, None)
        if should_skip(candidate):
            candidate["status"] = "skip"
        existing[term] = candidate
        added += 1

    marked = 0
    for item in existing.values():
        if item.get("status") in {"todo", "cont"} and should_skip(item):
            item["status"] = "skip"
            marked += 1

    review["items"] = sorted(existing.values(), key=lambda item: str(item.get("term", "")).lower())
    if args.write:
        review_path.write_text(json.dumps(review, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    counts: dict[str, int] = {}
    for item in review["items"]:
        status = str(item.get("status", ""))
        counts[status] = counts.get(status, 0) + 1
    print(json.dumps({"added_candidates": added, "marked_skip": marked, "counts": counts}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
