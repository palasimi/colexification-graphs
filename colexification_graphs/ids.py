# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright 2023 Levi Gruspe
# See https://www.gnu.org/licenses/gpl-3.0.en.html
"""Compute concept IDs."""

from base58 import b58encode

from colexification_graphs.fnv import fnv_1a_64 as fnv_hash


def compute_concept_id(word: str, sense: str) -> str:
    """Compute concept ID for word-sense."""
    key = f"{word}\t{sense}".encode()
    return b58encode(fnv_hash(key)).decode()


__all__ = ["compute_concept_id"]
