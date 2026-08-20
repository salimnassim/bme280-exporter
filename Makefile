.PHONY: ci

ci:
	uv lock --check
	uv sync --locked --dev
	uv run ruff check .
	uv run ruff format --check .
