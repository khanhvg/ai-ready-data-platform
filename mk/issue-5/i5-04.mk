.PHONY: runner-test runner-security-test runner-race-test

runner-test:
	@env -u PYTHONPATH RUNNER_GATE_MODE=verify PYTHONDONTWRITEBYTECODE=1 python3.12 apps/lab-runner/tools/run-gate.py

runner-security-test:
	@env -u PYTHONPATH RUNNER_GATE_MODE=verify PYTHONDONTWRITEBYTECODE=1 python3.12 apps/lab-runner/tools/run-gate.py

runner-race-test:
	@env -u PYTHONPATH RUNNER_GATE_MODE=verify PYTHONDONTWRITEBYTECODE=1 python3.12 apps/lab-runner/tools/run-gate.py
