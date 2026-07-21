LEARNING_RUNTIME_ROOT ?= /tmp/issue8-red-runtime/admitted
LEARNING_RUNTIME_CANDIDATE ?=
LEARNING_RUNTIME_INTERPRETER_SHA256 ?=
unexport LESSON EVIDENCE

# GNU Make 3.81 has no $(file ...) function. Keep command-line values raw with
# $(value), escape every single quote, and pass them as one argv element. The
# values are never exported or recursively expanded by Make.
learning_shell_quote = '$(subst ','"'"',$(value $(1)))'

.PHONY: learning-runtime-admit learning-contracts-check lesson-check api-contracts-check evidence-verify

define require-learning-runtime
	@test -n $(call learning_shell_quote,LEARNING_RUNTIME_INTERPRETER_SHA256) || (echo "LEARNING_RUNTIME_INTERPRETER_SHA256 is required" >&2; exit 2)
endef

learning-runtime-admit:
	@test -n $(call learning_shell_quote,LEARNING_RUNTIME_CANDIDATE) || (echo "LEARNING_RUNTIME_CANDIDATE is required" >&2; exit 2)
	$(require-learning-runtime)
	@env -u PYTHONPATH PYTHONDONTWRITEBYTECODE=1 python3 -m scripts.learning_contracts.runtime admit --runtime-root $(call learning_shell_quote,LEARNING_RUNTIME_ROOT) --candidate $(call learning_shell_quote,LEARNING_RUNTIME_CANDIDATE) --interpreter-sha256 $(call learning_shell_quote,LEARNING_RUNTIME_INTERPRETER_SHA256)

learning-contracts-check:
	$(require-learning-runtime)
	@env -u PYTHONPATH PYTHONDONTWRITEBYTECODE=1 python3 -m scripts.learning_contracts.runtime launch --runtime-root $(call learning_shell_quote,LEARNING_RUNTIME_ROOT) --interpreter-sha256 $(call learning_shell_quote,LEARNING_RUNTIME_INTERPRETER_SHA256) --timeout 120 -- check

lesson-check:
	$(require-learning-runtime)
	@env -u PYTHONPATH PYTHONDONTWRITEBYTECODE=1 python3 -m scripts.learning_contracts.runtime launch --runtime-root $(call learning_shell_quote,LEARNING_RUNTIME_ROOT) --interpreter-sha256 $(call learning_shell_quote,LEARNING_RUNTIME_INTERPRETER_SHA256) --timeout 60 -- lesson --lesson $(call learning_shell_quote,LESSON)

api-contracts-check:
	$(require-learning-runtime)
	@env -u PYTHONPATH PYTHONDONTWRITEBYTECODE=1 python3 -m scripts.learning_contracts.runtime launch --runtime-root $(call learning_shell_quote,LEARNING_RUNTIME_ROOT) --interpreter-sha256 $(call learning_shell_quote,LEARNING_RUNTIME_INTERPRETER_SHA256) --timeout 60 -- api

evidence-verify:
	$(require-learning-runtime)
	@env -u PYTHONPATH PYTHONDONTWRITEBYTECODE=1 python3 -m scripts.learning_contracts.runtime launch --runtime-root $(call learning_shell_quote,LEARNING_RUNTIME_ROOT) --interpreter-sha256 $(call learning_shell_quote,LEARNING_RUNTIME_INTERPRETER_SHA256) --timeout 60 -- evidence --evidence $(call learning_shell_quote,EVIDENCE)
