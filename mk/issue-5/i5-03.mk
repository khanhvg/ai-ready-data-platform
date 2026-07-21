LEARNING_CONTRACTS_PY := $(lastword $(sort $(wildcard .artifacts/workspaces/golden/*/venv/bin/python)))

.PHONY: learning-contracts-check lesson-check api-contracts-check evidence-verify

define require-learning-runtime
	@test -n "$(LEARNING_CONTRACTS_PY)" || (echo "locked golden runtime missing; run make golden-clean PROFILE=small SEED=42" >&2; exit 2)
endef

learning-contracts-check:
	$(require-learning-runtime)
	@env -u PYTHONPATH PYTHONDONTWRITEBYTECODE=1 $(LEARNING_CONTRACTS_PY) -m scripts.learning_contracts.check check

lesson-check:
	$(require-learning-runtime)
	@env -u PYTHONPATH PYTHONDONTWRITEBYTECODE=1 $(LEARNING_CONTRACTS_PY) -m scripts.learning_contracts.check lesson

api-contracts-check:
	$(require-learning-runtime)
	@env -u PYTHONPATH PYTHONDONTWRITEBYTECODE=1 $(LEARNING_CONTRACTS_PY) -m scripts.learning_contracts.check api

evidence-verify:
	$(require-learning-runtime)
	@env -u PYTHONPATH PYTHONDONTWRITEBYTECODE=1 $(LEARNING_CONTRACTS_PY) -m scripts.learning_contracts.check evidence
