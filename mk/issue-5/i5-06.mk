I506_RUNTIME_CANDIDATE ?=
I506_RUNTIME_INTERPRETER_SHA256 ?=

I506_RUNTIME_CANDIDATE := $(if $(value LEARNING_RUNTIME_CANDIDATE),$(value LEARNING_RUNTIME_CANDIDATE),$(value I506_RUNTIME_CANDIDATE))
I506_RUNTIME_INTERPRETER_SHA256 := $(if $(value LEARNING_RUNTIME_INTERPRETER_SHA256),$(value LEARNING_RUNTIME_INTERPRETER_SHA256),$(value I506_RUNTIME_INTERPRETER_SHA256))

i506_shell_quote = '$(subst ','"'"',$(value $(1)))'

.PHONY: curriculum-check traceability-check

define require-i506-runtime
	@test -n $(call i506_shell_quote,I506_RUNTIME_CANDIDATE) || (echo "LEARNING_RUNTIME_CANDIDATE is required" >&2; exit 2)
	@test -n $(call i506_shell_quote,I506_RUNTIME_INTERPRETER_SHA256) || (echo "LEARNING_RUNTIME_INTERPRETER_SHA256 is required" >&2; exit 2)
endef

curriculum-check:
	$(require-i506-runtime)
	@$(call i506_shell_quote,I506_RUNTIME_CANDIDATE)/venv/bin/python -m learning.curriculum.tools.check_curriculum

traceability-check:
	$(require-i506-runtime)
	@$(call i506_shell_quote,I506_RUNTIME_CANDIDATE)/venv/bin/python -m learning.curriculum.tools.check_traceability
