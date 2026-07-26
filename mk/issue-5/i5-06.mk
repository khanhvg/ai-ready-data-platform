.PHONY: curriculum-check traceability-check

curriculum-check:
	@env -u PYTHONPATH PYTHONDONTWRITEBYTECODE=1 python3.12 -m learning.curriculum.tools.content_io launch curriculum

traceability-check:
	@env -u PYTHONPATH PYTHONDONTWRITEBYTECODE=1 python3.12 -m learning.curriculum.tools.content_io launch traceability
