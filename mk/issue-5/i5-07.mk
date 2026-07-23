I5_07_FRAGMENT_MAKEFILE := $(abspath $(lastword $(MAKEFILE_LIST)))
I5_07_PRIMARY_MAKEFILE := $(abspath $(firstword $(MAKEFILE_LIST)))
I5_07_DIRECT_INVOCATION := $(filter $(I5_07_FRAGMENT_MAKEFILE),$(I5_07_PRIMARY_MAKEFILE))
I5_07_AUTHORIZED_GOALS := lake-contracts-check

ifneq ($(strip $(I5_07_DIRECT_INVOCATION)),)
.DEFAULT_GOAL := lake-contracts-check
I5_07_UNKNOWN_GOALS := $(filter-out $(I5_07_AUTHORIZED_GOALS),$(MAKECMDGOALS))
ifneq ($(strip $(I5_07_UNKNOWN_GOALS)),)
$(error unauthorized target(s): $(I5_07_UNKNOWN_GOALS))
endif
endif

.PHONY: $(I5_07_AUTHORIZED_GOALS)

lake-contracts-check:
	@env -u PYTHONPATH PYTHONDONTWRITEBYTECODE=1 python3 learning/labs/data-platform/verify_stage_a.py check
