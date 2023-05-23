DATE=$(shell date '+%Y.%m.%d')
PARENT="colexification-graphs-$(DATE)"

# Expects build/kaikki.jsonl to exist.
# Download from https://kaikki.org/dictionary/All%20languages%20combined/kaikki.org-dictionary-all.json
.PHONY:	build
build:	build/graph.json

build/wordsenses.tsv:	build/kaikki.jsonl
	python -m colexification_graphs.wordsenses $< > $@ 2> build/wordsenses.err

build/graph.tsv:	build/wordsenses.tsv
	python -m colexification_graphs.graph $< > $@

build/graph.json:	build/graph.tsv
	python -m colexification_graphs.post $< > $@

.PHONY:	check
check:
	flake8 colexification_graphs
	pylint colexification_graphs
	mypy --strict colexification_graphs

.PHONY:	dist
dist:	build
	mkdir -p dist
	cd build; \
		mkdir -p "$(PARENT)"; \
		cp ../README.md graph.json graph.tsv "$(PARENT)"; \
		tar -czvf "$(PARENT).tar.gz" "$(PARENT)"; \
		mv "$(PARENT).tar.gz" ../dist
