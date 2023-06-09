# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright 2023 Levi Gruspe
# See https://www.gnu.org/licenses/gpl-3.0.en.html
"""kaikki.org dictionary word schema."""

import typing as t


class TranslationSchema(t.TypedDict):
    """Schema for values inside .senses[*].translations."""
    lang: str
    code: t.NotRequired[str]    # Some translations have missing codes :(
    word: t.NotRequired[str]    # Some translations have missing words :(
    roman: t.NotRequired[str]
    sense: t.NotRequired[str]   # If `None`, treat as equal to `word`.


class SynonymSchema(t.TypedDict):
    """Schema for values inside .senses[*].synonyms."""
    word: str


class SenseSchema(t.TypedDict):
    """Schema for values inside .senses."""
    # There are other fields, but we only need translations and synonyms.
    translations: t.NotRequired[list[TranslationSchema]]
    synonyms: t.NotRequired[list[SynonymSchema]]


class Schema(t.TypedDict):
    """Schema for each line in a kaikki.org dictionary."""
    word: str
    pos: str
    lang: str
    lang_code: str
    senses: list[SenseSchema]
    translations: t.NotRequired[list[TranslationSchema]]


__all__ = ["Schema", "SenseSchema", "SynonymSchema", "TranslationSchema"]
