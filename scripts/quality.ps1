$ErrorActionPreference = "Stop"

uv sync --locked
uv run ruff format --check .
uv run ruff check .
uv run pyright
uv run nbdev-export
git diff --exit-code
uv run nbdev-test --path notebooks/00_environment_contract.ipynb
uv run transformer-env --json --require-canonical-gpu
