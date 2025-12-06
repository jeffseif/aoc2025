SHELL = /bin/bash

.PHONY: all
all:
	@uv run --no-dev python -m aoc2025

.PHONY: lint
lint:
	uv run --dev pre-commit run --all-files

.PHONY: clean
clean:
	@git clean -fdfx
