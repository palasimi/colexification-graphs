# Copyright 2023 Levi Gruspe
# Licensed under GNU GPLv3 or later
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


class SenseSchema(t.TypedDict):
    """Schema for values inside .senses."""
    # There are other fields, but we only need the translations.
    translations: t.NotRequired[list[TranslationSchema]]


class Schema(t.TypedDict):
    """Schema for each line in a kaikki.org dictionary."""
    word: str
    pos: str
    lang: str
    lang_code: str
    senses: list[SenseSchema]
    translations: t.NotRequired[list[TranslationSchema]]


__all__ = ["Schema", "SenseSchema", "TranslationSchema"]
