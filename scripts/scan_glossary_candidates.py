from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from functools import lru_cache
from pathlib import Path
from typing import Any


# Cover common Latin, IPA, and Latin Extended blocks, including Vietnamese,
# historical names, and combining accents without per-language exceptions.
LATIN_UPPER = (
    r"A-Z\u00C0-\u02AF\u1D00-\u1DFF\u1E00-\u1EFF"
    r"\u2C60-\u2C7F\uA720-\uA7FF\uAB30-\uAB6F"
    r"\U00010780-\U000107BF\U0001DF00-\U0001DFFF"
)
LATIN_LETTER = (
    r"A-Za-z\u00C0-\u02AF\u0300-\u036F\u1D00-\u1DFF\u1E00-\u1EFF"
    r"\u2C60-\u2C7F\uA720-\uA7FF\uAB30-\uAB6F"
    r"\U00010780-\U000107BF\U0001DF00-\U0001DFFF"
)
APOSTROPHE = r"'\u2019"
QUOTE_CHARS = "\"'\u201c\u201d"

REFERENCE_GENERIC_WORDS = {
    "a", "an", "and", "at", "by", "cost", "country", "countries", "detail",
    "for", "from", "in", "of", "on", "or", "sea", "state", "system", "the",
    "to", "treaty", "type", "types", "war", "with",
}
REFERENCE_DOMAIN_WORDS = {
    "academy", "artillery", "bishop", "bishopric", "cathedral", "cavalry",
    "church", "commune", "groschen", "infantry", "marquis", "marquisate",
    "militia", "monastery", "mosque", "parliament", "patriarchate", "regiment",
    "republic", "school", "temple", "university", "workshop",
}
PROPER_DERIVATION_PAIRS = {
    "abkhazia": {"abkhazian", "abkhazians"},
    "bologna": {"bolognese"},
    "catalonia": {"catalan"},
    "china": {"chinese"},
    "croatia": {"croatian", "croatians"},
    "england": {"english"},
    "france": {"french"},
    "germany": {"german", "germans"},
    "italy": {"italian", "italians"},
    "netherlands": {"dutch"},
    "poland": {"polish"},
    "portugal": {"portuguese"},
    "piedmont": {"piedmontese"},
    "russia": {"russian"},
    "sardinia": {"sardinian"},
    "scotland": {"scottish"},
    "spain": {"spanish"},
    "sundan": {"sundanese"},
    "sweden": {"swedish"},
    "turkey": {"turkish"},
    "venice": {"venetian"},
    "vijayanagar": {"vijayanagari"},
}

ENTRY_RE = re.compile(r'^\s*([^#\s][^:]*):\s*"(.*)"\s*(?:#.*)?$')
PROTECTED_RE = re.compile(
    r"\$[^$]+\$|\[[^\]]+\]|#\w+|#!|\\n|@[A-Za-z0-9_]+!|<[^>]+>"
)
# Keep protected fragments out of candidate text without turning them into
# ordinary whitespace that could join words across a placeholder or \n.
PROTECTED_SEPARATOR = "\uE000"
WORD_RE = re.compile(r"[^\W\d_][\w'._-]*", re.UNICODE)
TITLE_CASE_RE = re.compile(
    rf"\b[{LATIN_UPPER}][{LATIN_LETTER}{APOSTROPHE}.-]+"
    rf"(?:\s+(?:of|de|del|da|di|du|von|van|the|and|la|le|des|"
    rf"d[{APOSTROPHE}][{LATIN_UPPER}][{LATIN_LETTER}{APOSTROPHE}.-]+|"
    rf"l[{APOSTROPHE}][{LATIN_UPPER}][{LATIN_LETTER}{APOSTROPHE}.-]+|"
    rf"d[{APOSTROPHE}]|"
    r"I|II|III|IV|V|VI|VII|VIII|IX|X|XI|XII|"
    rf"[{LATIN_UPPER}][{LATIN_LETTER}{APOSTROPHE}.-]+))*\b"
)
ENTITY_HEAD_RE = re.compile(
    rf"\b(?:Board|Corps|Order|Company|League|Treaty|Academy|University|"
    rf"Institute|Council|House|Dynasty|Kingdom|Republic|Empire|Army|Navy)"
    rf"(?:\s+(?:of|de|del|da|di|du|von|van|the|la|le|des|"
    rf"d[{APOSTROPHE}][{LATIN_UPPER}][{LATIN_LETTER}{APOSTROPHE}.-]+|"
    rf"l[{APOSTROPHE}][{LATIN_UPPER}][{LATIN_LETTER}{APOSTROPHE}.-]+|"
    rf"[{LATIN_UPPER}][{LATIN_LETTER}{APOSTROPHE}.-]+))*\b"
)
POSSESSIVE_NAME_RE = re.compile(
    rf"\b([{LATIN_UPPER}][{LATIN_LETTER}{APOSTROPHE}.-]+"
    rf"(?:\s+[{LATIN_UPPER}][{LATIN_LETTER}{APOSTROPHE}.-]+){{0,3}})[{APOSTROPHE}]s\b"
)
CONNECTOR_NAME_RE = re.compile(
    rf"\b(?:of|de|del|da|di|du|von|van)\s+"
    rf"([{LATIN_UPPER}][{LATIN_LETTER}{APOSTROPHE}.-]+)\b"
)
CONNECTOR_PHRASE_RE = re.compile(
    rf"\b([{LATIN_UPPER}][{LATIN_LETTER}{APOSTROPHE}.-]+"
    rf"(?:\s+[{LATIN_UPPER}][{LATIN_LETTER}{APOSTROPHE}.-]+){{0,3}}"
    rf"\s+(?:of|de|del|da|di|du|von|van)\s+"
    rf"[{LATIN_UPPER}][{LATIN_LETTER}{APOSTROPHE}.-]+"
    rf"(?:\s+[{LATIN_UPPER}][{LATIN_LETTER}{APOSTROPHE}.-]+){{0,3}})\b"
)

IGNORE_TERMS = {
    "A",
    "Air",
    "All",
    "And",
    "As",
    "Can",
    "Christ",
    "Christian",
    "Christianity",
    "Christendom",
    "Church",
    "Earth",
    "England",
    "English",
    "For",
    "French",
    "German",
    "God",
    "Great Spirit",
    "Greeks",
    "Here",
    "If",
    "In",
    "Italian",
    "King",
    "Latins",
    "Lord",
    "Man",
    "No",
    "Nothing",
    "On",
    "Or",
    "Our",
    "Papal",
    "Pope",
    "Rather",
    "Spanish",
    "Spaniard",
    "The",
    "These",
    "Those",
    "Turkish",
    "What",
}

TRAILING_CONNECTORS = {
    "and",
    "da",
    "de",
    "del",
    "des",
    "di",
    "du",
    "la",
    "le",
    "of",
    "the",
    "van",
    "von",
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def parse_entries(path: Path) -> list[tuple[str, str]]:
    entries: list[tuple[str, str]] = []
    for line in read_text(path).splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        match = ENTRY_RE.match(line)
        if match:
            entries.append((match.group(1).strip(), match.group(2)))
    return entries


def glossary_entries(glossary_path: Path) -> dict[str, str]:
    entries: dict[str, str] = {}
    current_term: str | None = None
    alias_term: str | None = None
    alias_translation: str | None = None
    alias_names: list[str] = []
    in_aliases = False
    in_contextual = False
    contextual_term: str | None = None
    contextual_default: str | None = None
    contextual_senses: list[str] = []

    def flush_alias() -> None:
        if alias_term and alias_translation:
            entries[alias_term] = alias_translation
            for alias in alias_names:
                entries[alias] = alias_translation

    def flush_contextual() -> None:
        nonlocal contextual_term, contextual_default, contextual_senses
        if contextual_term:
            values: list[str] = []
            for value in contextual_senses:
                if value and value not in values:
                    values.append(value)
            entries[contextual_term] = "、".join(values) if values else (contextual_default or "")
        contextual_term = None
        contextual_default = None
        contextual_senses = []

    for line in read_text(glossary_path).splitlines():
        if line == "aliases:":
            flush_contextual()
            flush_alias()
            in_aliases = True
            in_contextual = False
            alias_term = None
            alias_translation = None
            alias_names = []
            continue
        if line == "contextual:":
            flush_alias()
            flush_contextual()
            in_aliases = False
            in_contextual = True
            current_term = None
            continue
        if in_contextual and line and not line.startswith(" "):
            flush_contextual()
            in_contextual = False
        if in_aliases and line and not line.startswith(" "):
            flush_alias()
            in_aliases = False
            alias_term = None
            alias_translation = None
            alias_names = []

        if in_aliases:
            alias = re.match(r"^  (?! )([^:#][^:]+):\s*$", line)
            if alias:
                flush_alias()
                alias_term = alias.group(1).strip()
                alias_translation = None
                alias_names = []
                continue
            zh = re.match(r'^    zh:\s*"([^"]*)"', line)
            if zh and alias_term:
                alias_translation = zh.group(1)
                continue
            also = re.match(r"^      -\s+(.+?)\s*$", line)
            if also and alias_term:
                alias_names.append(also.group(1).strip())
            continue

        if in_contextual:
            block = re.match(r"^  (?! )([^:#][^:]+):(?:\s+#.*)?\s*$", line)
            if block:
                flush_contextual()
                contextual_term = block.group(1).strip()
                continue
            default = re.match(r'^    default:\s*"([^"]*)"', line)
            if default and contextual_term:
                contextual_default = default.group(1)
                continue
            sense = re.match(r'^      - zh:\s*"([^"]*)"', line)
            if sense and contextual_term:
                contextual_senses.append(sense.group(1))
            continue

        scalar = re.match(r'^  (?! )([^:#][^:]+):\s*"([^"]*)"', line)
        if scalar:
            entries[scalar.group(1).strip()] = scalar.group(2)
            current_term = None
            continue

        block = re.match(r"^  (?! )([^:#][^:]+):(?:\s+#.*)?\s*$", line)
        if block:
            current_term = block.group(1).strip()
            continue

        if current_term:
            default = re.match(r'^    (?:default|zh):\s*"([^"]*)"', line)
            if default and current_term not in entries:
                entries[current_term] = default.group(1)

    flush_alias()
    flush_contextual()
    return entries


def alias_group_key(term: str) -> str:
    return " ".join(term.split()).casefold()


def glossary_alias_groups(glossary_path: Path) -> dict[str, str]:
    """Map each aliases term to its canonical group without flattening variants."""
    groups: dict[str, str] = {}
    in_aliases = False
    canonical: str | None = None
    aliases: list[str] = []

    def flush() -> None:
        if canonical:
            group = alias_group_key(canonical)
            groups[group] = group
            groups[normalized_reference_term(canonical)] = group
            for alias in aliases:
                groups[alias_group_key(alias)] = group
                groups[normalized_reference_term(alias)] = group

    for line in read_text(glossary_path).splitlines():
        if line == "aliases:":
            flush()
            in_aliases = True
            canonical = None
            aliases = []
            continue
        if in_aliases and line and not line.startswith(" "):
            flush()
            in_aliases = False
            canonical = None
            aliases = []
        if not in_aliases:
            continue
        block = re.match(r"^  (?! )([^:#][^:]+):\s*$", line)
        if block:
            flush()
            canonical = block.group(1).strip()
            aliases = []
            continue
        also = re.match(r"^      -\s+(.+?)\s*$", line)
        if also and canonical:
            aliases.append(also.group(1).strip())
    flush()
    return groups


def reference_entries(glossary_path: Path) -> dict[str, str]:
    """Read reference-only terms without treating them as enforced terms."""
    entries: dict[str, str] = {}
    in_reference_terms = False
    current_term: str | None = None

    for line in read_text(glossary_path).splitlines():
        if line == "reference_terms:":
            in_reference_terms = True
            current_term = None
            continue
        if in_reference_terms and line and not line.startswith(" "):
            break
        if not in_reference_terms:
            continue

        term = re.match(r"^  (?! )([^:#][^:]+):(?:\s+#.*)?$", line)
        if term:
            current_term = term.group(1).strip()
            continue
        suggestion = re.match(r'^\s{6,8}-\s*"([^"]*)"', line)
        if suggestion and current_term and current_term not in entries:
            entries[current_term] = suggestion.group(1)

    return entries


def candidates(entries: list[tuple[str, str]]) -> dict[str, set[str]]:
    found: dict[str, set[str]] = {}
    prepared: list[tuple[str, str, str, list[tuple[str, re.Match[str], str]]]] = []

    for key, value in entries:
        clean = PROTECTED_RE.sub(
            lambda match: PROTECTED_SEPARATOR * len(match.group(0)), value
        )
        matches: list[tuple[str, re.Match[str], str]] = []
        for pattern in (TITLE_CASE_RE, ENTITY_HEAD_RE):
            for match in pattern.finditer(clean):
                term = normalize_candidate(match.group(0))
                if term:
                    matches.append((pattern.pattern, match, term))
        prepared.append((key, clean, value, matches))


    for key, clean, value, matches in prepared:
        for _, match, term in matches:
            if is_sentence_fragment(term):
                continue
            found.setdefault(term, set()).add(key)
            for embedded in embedded_candidates(match.group(0)):
                embedded_term = normalize_candidate(embedded)
                if embedded_term:
                    found.setdefault(embedded_term, set()).add(key)
    return found


def embedded_candidates(term: str) -> set[str]:
    """Return likely named subterms hidden inside a larger title or phrase."""
    found: set[str] = set()
    for match in POSSESSIVE_NAME_RE.finditer(term):
        found.add(match.group(1))
    for match in CONNECTOR_NAME_RE.finditer(term):
        found.add(match.group(1))
    for match in CONNECTOR_PHRASE_RE.finditer(term):
        found.add(match.group(1))
    for word in re.findall(rf"[{LATIN_UPPER}][{LATIN_LETTER}{APOSTROPHE}.-]+", term):
        if any(ord(char) > 127 for char in word):
            found.add(word)
    return found


def normalize_candidate(term: str) -> str | None:
    term = term.strip(f" ,.;:!?{QUOTE_CHARS}()[]")
    parts = term.split()
    while parts and parts[-1].lower() in TRAILING_CONNECTORS:
        parts.pop()
    term = " ".join(parts)
    # Treat a leading article as a surface-form variant for review purposes.
    # The canonical term still matches both "Wakō" and "The Wakō" later.
    if len(parts) > 1 and parts[0].lower() == "the":
        term = " ".join(parts[1:])
    if len(term) < 3 or term in IGNORE_TERMS:
        return None
    return term


def is_sentence_fragment(term: str) -> bool:
    return bool(re.search(r"\.\s+[A-Z]", term))


@lru_cache(maxsize=20000)
def words(term: str) -> set[str]:
    ignored = {
        "a",
        "an",
        "and",
        "by",
        "de",
        "del",
        "of",
        "the",
        "to",
        "van",
        "von",
        "i",
        "ii",
        "iii",
        "iv",
        "v",
        "vi",
        "vii",
        "viii",
        "ix",
        "x",
        "xi",
        "xii",
    }
    return {
        word_key
        for raw_word in WORD_RE.findall(term)
        for word_key in (normalize_word_token(raw_word),)
        if word_key not in ignored and len(word_key) > 1
    }


@lru_cache(maxsize=20000)
def normalized_reference_term(term: str) -> str:
    normalized = unicodedata.normalize("NFKD", term)
    normalized = "".join(char for char in normalized if not unicodedata.combining(char))
    normalized = normalized.replace("\u2019", "'").replace("`", "'")
    normalized = re.sub(r"['\u2019]s\b", "", normalized, flags=re.IGNORECASE)
    normalized = re.sub(r"[^A-Za-z0-9]+", " ", normalized).strip().lower()
    return normalized


@lru_cache(maxsize=20000)
def normalize_word_token(token: str) -> str:
    normalized = unicodedata.normalize("NFKD", token)
    return "".join(
        char.lower()
        for char in normalized
        if not unicodedata.combining(char)
        and unicodedata.category(char)[0] in {"L", "N"}
        and unicodedata.category(char) != "Lm"
    )


@lru_cache(maxsize=20000)
def word_forms(word: str) -> set[str]:
    variants = {word}
    # Some Greek/Byzantine transliterations use -ai/-ais as a plural-like
    # pair, for example Akritai/Akritais. Only an exact glossary counterpart
    # can consume this conservative variant during reference matching.
    if word.endswith("ais") and len(word) > 4:
        variants.add(word[:-1])
    if word.endswith("ies") and len(word) > 4:
        variants.add(word[:-3] + "y")
    if word.endswith("es") and len(word) > 3:
        variants.add(word[:-2])
    if word.endswith("s") and not word.endswith(("ss", "us", "is")) and len(word) > 3:
        variants.add(word[:-1])
    if word.endswith("ied") and len(word) > 4:
        variants.add(word[:-3] + "y")
    if word.endswith("ed") and len(word) > 4:
        variants.add(word[:-1])
        variants.add(word[:-2])
    if word.endswith("ing") and len(word) > 5:
        stem = word[:-3]
        variants.add(stem)
        variants.add(stem + "e")
    return variants


def phrase_contains_inflected(longer: str, shorter: str) -> bool:
    longer_words = longer.split()
    shorter_words = shorter.split()
    if not longer_words or not shorter_words or len(shorter_words) > len(longer_words):
        return False
    width = len(shorter_words)
    for index in range(len(longer_words) - width + 1):
        window = longer_words[index : index + width]
        if all(
            left == right or left in word_forms(right) or right in word_forms(left)
            for left, right in zip(window, shorter_words)
        ):
            return True
    return False


@lru_cache(maxsize=20000)
def reference_forms(term: str) -> set[str]:
    normalized = normalized_reference_term(term)
    parts = normalized.split()
    if not parts:
        return set()
    forms = {normalized}
    for index, part in enumerate(parts):
        for variant in word_forms(part):
            form_parts = parts.copy()
            form_parts[index] = variant
            forms.add(" ".join(form_parts))
    return forms


def phrase_contains(longer: str, shorter: str) -> bool:
    """Match complete words in a phrase, never a character substring."""
    longer_words = longer.split()
    shorter_words = shorter.split()
    if not longer_words or not shorter_words or len(shorter_words) > len(longer_words):
        return False
    width = len(shorter_words)
    return any(
        longer_words[index : index + width] == shorter_words
        for index in range(len(longer_words) - width + 1)
    )


def generated_proper_derivations(base: str) -> set[str]:
    """Generate conservative country/region adjective forms for known pairs."""
    if " " in base or "-" in base or len(base) < 4:
        return set()
    candidates = {base + "ian", base + "ese", base + "ish", base + "i"}
    if base.endswith("ia"):
        candidates.add(base[:-1] + "an")
    if base.endswith("a"):
        candidates.add(base[:-1] + "an")
        candidates.add(base[:-1] + "ian")
    if base.endswith("o"):
        candidates.add(base[:-1] + "an")
    if base.endswith("y"):
        candidates.add(base[:-1] + "an")
        candidates.add(base[:-1] + "ian")
    return candidates


def generated_concept_derivations(base: str) -> set[str]:
    """Generate conservative -ist/-ism concept pairs."""
    if len(base) < 6:
        return set()
    if base.endswith("ist"):
        return {base[:-3] + "ism"}
    if base.endswith("ism"):
        return {base[:-3] + "ist"}
    return set()


def proper_derivation_match(first: str, second: str) -> bool:
    if first == second or " " in first or " " in second:
        return False
    if second in PROPER_DERIVATION_PAIRS.get(first, set()) or first in PROPER_DERIVATION_PAIRS.get(second, set()):
        return True
    first_forms = word_forms(first)
    second_forms = word_forms(second)
    return bool(
        generated_proper_derivations(first).intersection(second_forms)
        or generated_proper_derivations(second).intersection(first_forms)
        or generated_concept_derivations(first).intersection(second_forms)
        or generated_concept_derivations(second).intersection(first_forms)
    )


_REFERENCE_PROFILE_CACHE: dict[
    tuple[int, int], tuple[list[tuple[str, str, str, set[str], set[str], str | None]], set[str]]
] = {}


def glossary_refs(
    term: str,
    glossary: dict[str, str],
    limit: int = 12,
    core_limit: int = 3,
    alias_groups: dict[str, str] | None = None,
) -> list[dict[str, str]]:
    term_normalized = normalized_reference_term(term)
    term_forms = reference_forms(term)
    term_words = words(term)
    term_head = term_normalized.split()[0] if term_normalized else ""
    refs: list[tuple[int, int, int, str, str, set[str], str | None]] = []
    alias_groups = alias_groups or {}
    cache_key = (id(glossary), id(alias_groups))
    cached = _REFERENCE_PROFILE_CACHE.get(cache_key)
    if cached is None:
        known_profiles = [
            (
                known_term,
                translation,
                normalized_reference_term(known_term),
                reference_forms(known_term),
                words(known_term),
                alias_groups.get(alias_group_key(known_term))
                or alias_groups.get(normalized_reference_term(known_term)),
            )
            for known_term, translation in glossary.items()
        ]
        family_counts: dict[str, int] = {}
        for _, _, _, _, known_words, _ in known_profiles:
            if len(known_words) > 1:
                for word in known_words:
                    if word not in REFERENCE_GENERIC_WORDS:
                        family_counts[word] = family_counts.get(word, 0) + 1
        family_cores = {word for word, count in family_counts.items() if count >= 2}
        cached = (known_profiles, family_cores)
        _REFERENCE_PROFILE_CACHE[cache_key] = cached
    known_profiles, family_cores = cached
    for known_term, translation, known_normalized, known_forms, known_words, alias_group in known_profiles:
        score = 0
        if known_normalized == term_normalized:
            score = 1000
        elif known_normalized in term_forms or term_normalized in known_forms:
            score = 850
        elif proper_derivation_match(term_normalized, known_normalized):
            score = 825
        elif phrase_contains_inflected(term_normalized, known_normalized) or phrase_contains_inflected(
            known_normalized, term_normalized
        ):
            if known_words and not known_words.issubset(REFERENCE_GENERIC_WORDS):
                # A longer complete phrase with more matched words outranks
                # entries that merely share one head word, while staying below
                # exact, alias, and explicit word-form matches.
                score = min(840, 760 + 40 * len(known_normalized.split()))

        overlap = term_words & known_words
        domain_overlap = set()
        known_head = known_normalized.split()[0] if known_normalized else ""
        if overlap and len(term_words) > 1 and len(known_words) > 1:
            domain_overlap = overlap & REFERENCE_DOMAIN_WORDS
            meaningful_overlap = overlap - REFERENCE_GENERIC_WORDS
            if term_head == known_head and term_head not in REFERENCE_GENERIC_WORDS:
                # Shared proper-name heads, such as "Sofa", keep a term family together.
                score = max(score, 760)
            elif domain_overlap:
                # Shared concrete domain heads, such as "Groschen", connect related phrases.
                score = max(score, 700 + 25 * len(domain_overlap))
            elif overlap & family_cores:
                # Repeated proper/domain cores, such as "Sofa", connect a term family.
                score = max(score, 575 + 15 * len(overlap & family_cores))
            elif len(meaningful_overlap) >= 2:
                score = max(score, 400 + 20 * len(meaningful_overlap))
        if score:
            candidate_cores = set()
            if score < 850:
                candidate_cores = overlap - REFERENCE_GENERIC_WORDS
                if domain_overlap:
                    candidate_cores = domain_overlap
                elif term_head == known_head and term_head not in REFERENCE_GENERIC_WORDS:
                    candidate_cores = {term_head}
                elif overlap & family_cores:
                    candidate_cores = overlap & family_cores
            alias_rank = 0 if alias_group and alias_group == alias_group_key(known_term) else 1
            refs.append((score, len(known_term), alias_rank, known_term, translation, candidate_cores, alias_group))

    refs.sort(key=lambda item: (-item[0], item[2], -item[1], item[3].lower()))
    selected: list[tuple[int, int, int, str, str, set[str], str | None]] = []
    core_counts: dict[str, int] = {}
    selected_alias_groups: set[str] = set()
    for candidate in refs:
        score, _, _, _, _, candidate_cores, alias_group = candidate
        if alias_group and alias_group in selected_alias_groups:
            continue
        if score < 850 and candidate_cores and any(
            core_counts.get(core, 0) >= core_limit for core in candidate_cores
        ):
            continue
        selected.append(candidate)
        if alias_group:
            selected_alias_groups.add(alias_group)
        for core in candidate_cores:
            core_counts[core] = core_counts.get(core, 0) + 1
        if len(selected) >= limit:
            break
    return [
        {"term": known_term, "translation": translation}
        for _, _, _, known_term, translation, _, _ in selected
    ]


def guess_category(term: str) -> str:
    lowered = term.lower()
    if any(word in lowered for word in ("battle", "siege", "war")):
        return "event"
    if any(
        word in lowered
        for word in ("declaration", "theses", "essay", "discourse", "books", "histories")
    ):
        return "work_title"
    if any(word in lowered for word in ("order", "commonwealth", "church")):
        return "organization"
    if any(
        word in lowered
        for word in ("king", "emperor", "pope", "marquis", "archbishop", "admiral", "captain")
    ):
        return "title_or_role"
    if re.search(r"\b(of|de|del|da|di|du|von|van|d['\u2019])", term):
        return "person_or_place"
    if re.search(r"\b[IVX]+\b", term):
        return "person"
    return "unknown"


def existing_review_items(path: Path) -> dict[str, dict[str, Any]]:
    if not path.exists():
        return {}
    text = path.read_text(encoding="utf-8")
    if not text.strip():
        return {}
    data = json.loads(text)
    return {
        normalize_candidate(item["term"]) or item["term"]: item
        for item in data.get("items", [])
        if isinstance(item, dict) and item.get("term")
    }


def build_review_item(
    term: str,
    keys: list[str],
    glossary: dict[str, str],
    existing: dict[str, Any] | None,
    alias_groups: dict[str, str] | None = None,
) -> dict[str, Any]:
    item = {
        "term": term,
        "translation": "",
        "status": "todo",
        "category": guess_category(term),
        "keys": keys,
        "note": "",
        "glossary_refs": glossary_refs(term, glossary, alias_groups=alias_groups),
    }
    if existing:
        for field in ("translation", "category", "status", "note"):
            if field in existing:
                item[field] = existing[field]
        if "keys" in existing:
            item["keys"] = sorted(set(existing["keys"]) | set(keys))
    return item


def write_review_json(
    output_path: Path,
    source_file: list[str],
    rows: list[tuple[str, str, list[str]]],
    glossary: dict[str, str],
    known_glossary: dict[str, str] | None = None,
    alias_groups: dict[str, str] | None = None,
) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    existing_data: dict[str, Any] = {}
    if output_path.exists():
        existing_text = output_path.read_text(encoding="utf-8") if output_path.exists() else ""
        existing_data = json.loads(existing_text) if existing_text.strip() else {"files": []}
    known_terms = set(known_glossary if known_glossary is not None else glossary)
    existing_items = {
        term: item
        for term, item in existing_review_items(output_path).items()
        if term not in known_terms
    }
    new_items = []
    for status, term, keys in rows:
        if status != "review":
            continue
        item = build_review_item(term, keys, glossary, existing_items.get(term), alias_groups=alias_groups)
        new_items.append(item)
    merged_items = dict(existing_items)
    for item in new_items:
        merged_items[item["term"]] = item
    existing_source_files = existing_data.get("source_file", [])
    if not isinstance(existing_source_files, list):
        existing_source_files = []
    review = {
        "source_file": sorted(set(existing_source_files) | set(source_file)),
        "status": "todo",
        "instructions": (
            "Status values: todo=fill translation manually, "
            "ai=let Codex suggest translation in review.json, "
            "cont=have Codex propose a contextual glossary rule from source contexts, "
            "skip=ignore. glossary_refs are references only."
        ),
        "items": sorted(merged_items.values(), key=lambda item: str(item.get("term", "")).lower()),
    }
    output_path.write_text(json.dumps(review, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", required=True, action="append")
    parser.add_argument("--source-root", default="source/english")
    parser.add_argument("--glossary", default="translation_glossary.yml")
    parser.add_argument("--review-only", action="store_true")
    parser.add_argument("--write-review", action="store_true")
    parser.add_argument("--review-output", default="work/glossary_review/review.json")
    args = parser.parse_args()

    sys.stdout.reconfigure(encoding="utf-8")

    glossary_path = Path(args.glossary)
    glossary = glossary_entries(glossary_path)
    alias_groups = glossary_alias_groups(glossary_path)
    reference_glossary = reference_entries(glossary_path)
    glossary_for_refs = {**glossary, **reference_glossary}
    known = set(glossary_for_refs)
    candidate_terms: dict[str, list[str]] = {}
    scanned_files: list[str] = []
    for source_file in args.file:
        source_path = Path(args.source_root) / source_file
        paths = sorted(source_path.rglob("*.yml")) if source_path.is_dir() else [source_path]
        for path in paths:
            relative = path.relative_to(Path(args.source_root)).as_posix()
            scanned_files.append(relative)
            for term, keys in candidates(parse_entries(path)).items():
                candidate_terms.setdefault(term, []).extend(keys)

    rows = []
    for term, keys in sorted(candidate_terms.items(), key=lambda x: x[0].lower()):
        keys = sorted(set(keys))
        status = "known" if term in known else "review"
        if args.review_only and status == "known":
            continue
        rows.append((status, term, sorted(keys)))

    if args.write_review:
        review_rows = [row for row in rows if row[0] == "review"]
        write_review_json(
            Path(args.review_output),
            scanned_files,
            review_rows,
            glossary_for_refs,
            known_glossary=glossary_for_refs,
            alias_groups=alias_groups,
        )
        print(f"wrote: {args.review_output}")
        print(f"review_items: {len(review_rows)}")
        return 0

    print(f"files: {', '.join(scanned_files)}")
    print(f"candidates: {len(rows)}")
    print("status\tterm\tkeys\tglossary_refs")
    for status, term, keys in rows:
        refs = glossary_refs(term, glossary_for_refs, alias_groups=alias_groups)
        ref_text = "; ".join(f"{ref['term']}={ref['translation']}" for ref in refs[:5])
        print(f"{status}\t{term}\t{', '.join(keys)}\t{ref_text}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
