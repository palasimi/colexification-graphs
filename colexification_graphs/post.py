# Copyright 2023 Levi Gruspe
# Licensed under GNU GPLv3 or later
# See https://www.gnu.org/licenses/gpl-3.0.en.html

# pylint: disable=too-few-public-methods
"""Turn TSV file of graph edges into a cytoscape JSON file."""

from argparse import ArgumentParser, Namespace
from csv import reader
from json import dumps
from pathlib import Path

import networkx as nx   # type: ignore


def parse_args() -> Namespace:
    """Parse command-line arguments."""
    parser = ArgumentParser(description=__doc__)
    parser.add_argument(
        "tsv",
        type=Path,
        help=(
            "path to TSV file "
            "(columns: word 1, sense 1, word 2, sense 2, weight)"
        ),
    )
    return parser.parse_args()


class NodeDirectory:
    """Maps word senses to IDs."""
    def __init__(self) -> None:
        self.counter = 0
        self.ids: dict[tuple[str, str], int] = {}

    def get(self, sense: tuple[str, str]) -> int:
        """Return sense ID."""
        self.counter += 1
        return self.ids.setdefault(sense, self.counter)


def load_graph(tsv: Path) -> nx.Graph:
    """Create graph from weighted edges in TSV file.

    Minimum edge weight to include in the graph.
    """
    graph = nx.Graph()
    nodes = NodeDirectory()
    with open(tsv, encoding="utf-8") as file:
        for row in reader(file, delimiter="\t"):
            (
                source_word,
                source_sense,
                target_word,
                target_sense,
                weight,
            ) = row
            source = nodes.get((source_word, source_sense))
            target = nodes.get((target_word, target_sense))

            graph.add_node(
                source,
                word=source_word,
                sense=source_sense,
            )
            graph.add_node(
                target,
                word=target_word,
                sense=target_sense,
            )
            graph.add_edge(source, target, weight=int(weight))
    return graph


def to_cytoscape(graph: nx.Graph) -> str:
    """Convert networkx graph into a cytoscape JSON file."""
    nodes = [
        {
            "data": {
                **data,
                "id": node,
            },
        }
        for node, data in graph.nodes(data=True)
    ]
    edges = [
        {
            "data": {
                **data,
                "source": source,
                "target": target,
            },
        }
        for source, target, data in graph.edges(data=True)
    ]
    return dumps({
        "elements": {
            "nodes": nodes,
            "edges": edges,
        },
    })


def main(args: Namespace) -> None:
    """Script entrypoint."""
    graph = load_graph(args.tsv)
    print(to_cytoscape(graph))


if __name__ == "__main__":
    main(parse_args())
