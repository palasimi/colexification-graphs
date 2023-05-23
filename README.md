# colexification-graphs

Colexification graphs extracted from Wiktionary.

## Interpretation

A colexification graph is an undirected graph.

- Nodes represent meanings/sense-annotated words.
- The weight of an edge between two nodes is the number of languages where the same word is used for both meanings.

## Format

The graphs are available in TSV and JSON formats.

TSV columns:

1. node 1 word
2. node 1 sense
3. node 2 word
4. node 2 sense
5. weight of edge between node 1 and node 2

The JSON file is compatible with [Cytoscape.js](https://js.cytoscape.org/).

## Licenses

### Scripts

Copyright 2023 Levi Gruspe

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>. 

### Data

Copyright 2023 Levi Gruspe

The published colexification graphs are made available under the [Creative Commons Attribution-ShareAlike License](https://creativecommons.org/licenses/by-sa/3.0/).
This work is derived from Wiktionary.
The copyright of the original work belongs to Wiktionary's editors and contributors.
