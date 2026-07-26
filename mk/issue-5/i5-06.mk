I5_06_RUNTIME := .artifacts/workspaces/golden/i11-stage-a-v3
I5_06_PYTHON := $(I5_06_RUNTIME)/venv/bin/python
I5_06_ADMISSION := $(I5_06_RUNTIME)/runtime-admission.json

.PHONY: curriculum-check traceability-check

curriculum-check:
	@test -f "$(I5_06_ADMISSION)" -a -x "$(I5_06_PYTHON)" || (echo "I5-06 exact admitted runtime is missing" >&2; exit 2)
	@env -u PYTHONPATH PYTHONDONTWRITEBYTECODE=1 $(I5_06_PYTHON) -m learning.curriculum.tools.check_curriculum

traceability-check:
	@test -f "$(I5_06_ADMISSION)" -a -x "$(I5_06_PYTHON)" || (echo "I5-06 exact admitted runtime is missing" >&2; exit 2)
	@env -u PYTHONPATH PYTHONDONTWRITEBYTECODE=1 $(I5_06_PYTHON) -m learning.curriculum.tools.check_traceability
