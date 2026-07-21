.PHONY: help golden-clean data-contracts-check evidence-contracts-check migration-contracts-check architecture-check architecture-render

help:
	@env -u PYTHONPATH PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/golden/command_registry.py

golden-clean:
	@env -u PYTHONPATH PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/golden/golden_run.py --profile "$(PROFILE)" --seed "$(SEED)"

data-contracts-check:
	@env -u PYTHONPATH PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/golden/locked_test.py data-contracts

evidence-contracts-check:
	@env -u PYTHONPATH PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/golden/locked_test.py evidence-contracts

migration-contracts-check:
	@env -u PYTHONPATH PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/golden/locked_test.py migration-contracts

architecture-check:
	@env -u PYTHONPATH PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/golden/architecture_pipeline.py check

architecture-render:
	@env -u PYTHONPATH PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/golden/architecture_pipeline.py render
