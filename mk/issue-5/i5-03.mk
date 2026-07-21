LEARNING_CONTRACTS_PY := $(lastword $(sort $(wildcard .artifacts/workspaces/golden/*/venv/bin/python)))
unexport LESSON EVIDENCE

# GNU Make 3.81 has no $(file ...) function. Keep command-line values raw with
# $(value), escape every single quote, and pass them as one argv element. The
# values are never exported or recursively expanded by Make.
learning_shell_quote = '$(subst ','"'"',$(value $(1)))'

.PHONY: learning-contracts-check lesson-check api-contracts-check evidence-verify

define require-learning-runtime
	@test -n "$(LEARNING_CONTRACTS_PY)" || (echo "locked golden runtime missing; run make golden-clean PROFILE=small SEED=42" >&2; exit 2)
endef

learning-contracts-check:
	$(require-learning-runtime)
	@env -u PYTHONPATH PYTHONDONTWRITEBYTECODE=1 $(LEARNING_CONTRACTS_PY) -m scripts.learning_contracts.check check

lesson-check:
	$(require-learning-runtime)
	@env -u PYTHONPATH PYTHONDONTWRITEBYTECODE=1 $(LEARNING_CONTRACTS_PY) -m scripts.learning_contracts.check lesson --lesson $(call learning_shell_quote,LESSON)

api-contracts-check:
	$(require-learning-runtime)
	@env -u PYTHONPATH PYTHONDONTWRITEBYTECODE=1 $(LEARNING_CONTRACTS_PY) -m scripts.learning_contracts.check api

evidence-verify:
	$(require-learning-runtime)
	@env -u PYTHONPATH PYTHONDONTWRITEBYTECODE=1 $(LEARNING_CONTRACTS_PY) -m scripts.learning_contracts.check evidence --evidence $(call learning_shell_quote,EVIDENCE)
