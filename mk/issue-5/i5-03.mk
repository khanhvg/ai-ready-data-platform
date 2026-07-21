.PHONY: learning-contracts-check lesson-check api-contracts-check evidence-verify

learning-contracts-check:
	@env -u PYTHONPATH PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/learning_contracts/runtime.py learning-contracts-check

lesson-check:
	@env -u PYTHONPATH PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/learning_contracts/runtime.py lesson-check --lesson "$(LESSON)"

api-contracts-check:
	@env -u PYTHONPATH PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/learning_contracts/runtime.py api-contracts-check

evidence-verify:
	@env -u PYTHONPATH PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/learning_contracts/runtime.py evidence-verify --evidence "$(EVIDENCE)"
