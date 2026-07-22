I5_06_PYTHON ?= python3.12

.PHONY: curriculum-check traceability-check

curriculum-check:
	@env -u PYTHONPATH PYTHONDONTWRITEBYTECODE=1 $(I5_06_PYTHON) -m learning.curriculum.tools.check_curriculum

traceability-check:
	@env -u PYTHONPATH PYTHONDONTWRITEBYTECODE=1 $(I5_06_PYTHON) -m learning.curriculum.tools.check_traceability
