# Copyright 2023 Levi Gruspe
# Licensed under GNU GPLv3 or later
# See https://www.gnu.org/licenses/gpl-3.0.en.html

# pylint: disable=invalid-name
"""Extract sense-annotated words from Wiktionary data."""

from argparse import ArgumentParser, Namespace
from csv import writer
from logging import warning
from pathlib import Path
import sys
import typing as t

from orjson import loads    # pylint: disable=no-name-in-module

from colexification_graphs.schema import (
    Schema,
    SenseSchema,
    SynonymSchema,
    TranslationSchema,
)


TranslationError: t.TypeAlias = t.Literal[
    "missing-code",
    "missing-sense",
    "missing-word",
]


def get_words(dictionary: Path) -> t.Iterator[Schema]:
    """Get words from a kaikki dictionary file."""
    with open(dictionary, encoding="utf-8") as file:
        for line in file:
            data: Schema = loads(line)

            assert data["pos"]
            assert data["lang"]
            assert data["senses"]

            yield data


def get_word_senses(data: Schema) -> t.Iterator[SenseSchema]:
    """Get different senses of word."""
    yield from data["senses"]


def get_synonyms(sense: SenseSchema) -> list[SynonymSchema]:
    """Get synonyms from word sense."""
    synonyms = []
    for synonym in sense.get("synonyms", []):
        # If there's an error in one synonym, there's probably an error in
        # other synonyms, too.
        if not synonym["word"]:
            return []
        synonyms.append(synonym)
    return synonyms


def warn(
    kind: TranslationError,
    language: str,
    word: str,
    translation: TranslationSchema,
) -> None:
    """Log warning about possible error in translation data."""
    message = f"{kind}\t{language}\t{word}\t{translation}"
    warning(message)


def check_translation(
    translation: TranslationSchema,
) -> TranslationError | None:
    """Check if translation data is okay (no missing fields).

    The result is the type of error, or `None` if there are no errors.
    """
    if not translation.get("code"):
        return "missing-code"
    if not translation.get("word"):
        return "missing-word"

    # Empty string is okay.
    if translation.get("sense") is None:
        return "missing-sense"
    return None


def get_translations(data: Schema) -> t.Iterator[TranslationSchema]:
    """Get translations of a word in different languages.

    The translations in the return value are guaranteed to have non-empty code,
    word and sense values.
    A word is not considered a translation of itself.
    """
    language_name = data["lang"]
    language = data["lang_code"]
    word = data["word"]

    for translation in data.get("translations", []):
        error = check_translation(translation)
        if error is not None:
            warn(error, language, word, translation)
        if error in ("missing-code", "missing-word"):
            continue
        yield translation

    for sense in get_word_senses(data):
        # Get sense description of first translation.
        # The translations may have different senses, but the assumption is
        # they're all roughly the same.
        # But to be sure, we won't change the sense values of translations.
        # We'll only use `sense_description` for synonyms.
        sense_description = None

        # Yield translations.
        for translation in sense.get("translations", []):
            error = check_translation(translation)
            if error is not None:
                warn(error, language, word, translation)
            if error in ("missing-code", "missing-word"):
                continue
            yield translation

            # Set sense description.
            if sense_description is None:
                sense_description = translation.get("sense")

        # Treat synonyms as translations.
        if sense_description is not None:
            for synonym in get_synonyms(sense):
                yield {
                    "lang": language_name,
                    "code": language,
                    "word": synonym["word"],
                    "sense": sense_description,
                }


def fix_whitespace(text: str) -> tuple[bool, str]:
    """Fix whitespace characters in text.

    The result is a tuple containing a:
    - `bool` value to indicate success
    - `str` of the modified text.
    """
    ok = True

    newline = text.find("\n")
    if newline >= 0:
        # Strip text after the newline, because the following line is probably
        # a comment.
        text = text[:newline]
        ok = False

    if "\t" in text:
        text = text.replace("\t", " ")
        ok = False
    return ok, text


def get_records(dictionary: Path) -> t.Iterator[tuple[str, str, str, str]]:
    """Get relevant records from the kaikki dictionary.

    Generates 4-tuples: (language, word, sense, gloss).
    """
    for data in get_words(dictionary):
        word = data["word"]
        language = data["lang_code"]
        glosses = set()

        for translation in get_translations(data):
            gloss = translation.get("sense", word)
            if gloss == "Translations":
                gloss = word
            glosses.add(gloss)
            yield translation["code"], translation["word"], word, gloss

        for gloss in glosses:
            yield language, word, word, gloss


def write_rows(rows: t.Iterable[tuple[str, ...]]) -> None:
    """Write rows to stdout in TSV format.

    Tabs are replace with a space, and text after newlines are truncated.
    """
    out = writer(sys.stdout, delimiter="\t")
    for row in rows:
        record = []
        for entry in row:
            ok, replacement = fix_whitespace(entry)
            record.append(replacement)
            if not ok:
                warning(f"invalid-whitespace\t{entry!r}")
        out.writerow(record)


def parse_args() -> Namespace:
    """Parse command-line arguments."""
    parser = ArgumentParser(description=__doc__)
    parser.add_argument(
        "dictionary",
        type=Path,
        help="path to kaikki dictionary (.jsonl file)",
    )
    return parser.parse_args()


def main(args: Namespace) -> None:
    """Script entrypoint."""
    try:
        write_rows(get_records(args.dictionary))
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main(parse_args())
