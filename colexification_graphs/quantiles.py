# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright 2023 Levi Gruspe
# See https://www.gnu.org/licenses/gpl-3.0.en.html

# pylint: disable=invalid-name
"""Compute quantile scores of edge weights."""

from argparse import ArgumentParser, Namespace
from csv import reader
from pathlib import Path
from statistics import quantiles


def parse_args() -> Namespace:
    """Parse command-line arguments."""
    parser = ArgumentParser(description=__doc__)
    parser.add_argument(
        "graph",
        type=Path,
        help="path to graph .tsv file (edge weights in 5th column)",
    )
    return parser.parse_args()


def main(args: Namespace) -> None:
    """Script entrypoint."""
    with open(args.graph, encoding="utf-8") as file:
        weights = [int(row[4]) for row in reader(file, delimiter="\t")]
    weights.sort()
    print(weights)

    for n in [2, 3, 4, 5, 10, 100, 1000]:
        print(n, quantiles(weights, n=n))


if __name__ == "__main__":
    main(parse_args())
