I5_06_PYTHON := $(firstword $(wildcard .artifacts/workspaces/golden/*/venv/bin/python))

.PHONY: curriculum-check traceability-check

curriculum-check:
	@test -n "$(I5_06_PYTHON)" || (echo "I5-06 admitted runtime is missing" >&2; exit 2)
	@env -u PYTHONPATH PYTHONDONTWRITEBYTECODE=1 $(I5_06_PYTHON) -m learning.curriculum.tools.check_curriculum

traceability-check:
	@test -n "$(I5_06_PYTHON)" || (echo "I5-06 admitted runtime is missing" >&2; exit 2)
	@env -u PYTHONPATH PYTHONDONTWRITEBYTECODE=1 $(I5_06_PYTHON) -m learning.curriculum.tools.check_traceability
