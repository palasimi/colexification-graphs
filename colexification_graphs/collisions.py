# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright 2023 Levi Gruspe
# See https://www.gnu.org/licenses/gpl-3.0.en.html
"""Check for collisions in concept hashes."""

from argparse import ArgumentParser, Namespace
from csv import reader
from pathlib import Path
import sys

from colexification_graphs.ids import compute_concept_id


def parse_args() -> Namespace:
    """Parse command-line arguments."""
    parser = ArgumentParser(description=__doc__)
    parser.add_argument(
        "tsv",
        type=Path,
        help="path to TSV file (columns: language, word, sense, gloss)",
    )
    return parser.parse_args()


def main(args: Namespace) -> None:
    """Script entrypoint."""
    # Get concepts.
    concepts = set()
    with open(args.tsv, encoding="utf-8") as file:
        for _, _, word, sense in reader(file, delimiter="\t"):
            concepts.add((word, sense))

    # Compute IDs.
    ids: dict[str, set[tuple[str, str]]] = {}
    for concept in concepts:
        id_ = compute_concept_id(concept[0], concept[1])
        ids.setdefault(id_, set()).add(concept)

    # Look for collisions.
    total = 0
    for id_, collisions in ids.items():
        if len(collisions) > 1:
            total += 1
            print(collisions, file=sys.stdout)

    if total > 0:
        print("Found", total, "collisions", file=sys.stdout)


if __name__ == "__main__":
    main(parse_args())
