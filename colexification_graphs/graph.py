# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright 2023 Levi Gruspe
# See https://www.gnu.org/licenses/gpl-3.0.en.html

# pylint: disable=duplicate-code, too-many-locals
"""Build colexification graph."""

from argparse import ArgumentParser, Namespace
from collections import Counter
from csv import reader, writer
from pathlib import Path
import sys
import typing as t


Language: t.TypeAlias = str
Word: t.TypeAlias = str
Translation: t.TypeAlias = tuple[Language, Word]
Sense: t.TypeAlias = tuple[str, str, str]   # ID, word and description
Edge: t.TypeAlias = tuple[Sense, Sense]


def parse_args() -> Namespace:
    """Parse command-line arguments."""
    parser = ArgumentParser(description=__doc__)
    parser.add_argument(
        "--edge-cutoff",
        dest="edge_cutoff",
        nargs=1,
        type=int,
        help="minimum weight required for edges in graph (default: 4)",

        # Removes > 2/3 of all edges
        default=[4],
    )

    parser.add_argument(
        "--sense-cutoff",
        dest="sense_cutoff",
        nargs=1,
        type=int,
        help="minimum languages required for word senses (default: 20)",

        # Removes > 80% of all word senses.
        default=[20],
    )

    parser.add_argument(
        "tsv",
        type=Path,
        help=(
            "path to TSV file "
            "(columns: language, word, concept ID, sense, gloss)"
        ),
    )
    args = parser.parse_args()
    args.edge_cutoff = args.edge_cutoff[0]
    args.sense_cutoff = args.sense_cutoff[0]
    return args


class InvalidRecord(Exception):
    """Raised when an invalid record is found in a TSV file."""


def get_rows(
    tsv: Path,
    silent: bool = True,
) -> t.Iterator[tuple[str, str, str, str, str]]:
    """Read rows from TSV file.

    If `silent` is `True`, silently ignores invalid rows.
    If not, raises `InvalidRecord`.
    """
    with open(tsv, encoding="utf-8") as file:
        for row in reader(file, delimiter="\t"):
            try:
                language, word, id_, sense, gloss = row
            except ValueError as exc:
                if silent:
                    continue
                raise InvalidRecord from exc

            yield language, word, id_, sense, gloss


def write_graph(graph: Counter[Edge]) -> None:
    """Write graph to stdout in TSV format."""
    out = writer(sys.stdout, delimiter="\t")
    for (source, target), weight in graph.most_common():
        id_s, sense_s, gloss_s = source
        id_t, sense_t, gloss_t = target
        row = (id_s, sense_s, gloss_s, id_t, sense_t, gloss_t, weight)
        out.writerow(row)


def main(args: Namespace) -> None:
    """Script entrypoint."""
    translation_senses: dict[Translation, set[Sense]] = {}
    sense_languages: dict[Sense, set[Language]] = {}
    for language, word, id_, sense, gloss in get_rows(args.tsv, silent=True):
        translation = (language, word)
        concept = (id_, sense, gloss)
        translation_senses.setdefault(translation, set()).add(concept)
        sense_languages.setdefault(concept, set()).add(language)

    # Only include word senses that are translated in enough languages.
    senses = {
        sense
        for sense, languages in sense_languages.items()
        if len(languages) >= args.sense_cutoff
    }

    # Create colexification graph.
    graph_languages: dict[Edge, set[Language]] = {}
    for (language, _), word_senses in translation_senses.items():
        nodes = sorted(sense for sense in word_senses if sense in senses)
        for i in range(1, len(nodes)):
            for j in range(i):
                graph_languages.setdefault(
                    (nodes[j], nodes[i]),
                    set(),
                ).add(language)

    write_graph(
        Counter({
            edge: weight
            for edge, languages in graph_languages.items()
            if (weight := len(languages)) >= args.edge_cutoff
        }),
    )


if __name__ == "__main__":
    main(parse_args())
