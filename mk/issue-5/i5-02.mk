.DEFAULT_GOAL := i5-02-authority-check

AUTHORIZED_GOALS := i5-02-authority-check i5-02-protected-hash-check i5-02-toolchain-check i5-02-changed-path-check i5-02-security-check i5-02-credential-check i5-02-non-copy-check web-common-test learn-preview learn-preview-status learn-preview-reset-check learn-preview-down
UNKNOWN_GOALS := $(filter-out $(AUTHORIZED_GOALS),$(MAKECMDGOALS))
ifneq ($(strip $(UNKNOWN_GOALS)),)
$(error unauthorized target(s): $(UNKNOWN_GOALS))
endif

IMPLEMENTATION_INPUT_SHA ?=
LESSON ?= promotion-trust
PREVIEW_PORT ?= 4174
export IMPLEMENTATION_INPUT_SHA
export LESSON
export PREVIEW_PORT
AUTHORITY = node spikes/web/harness/scripts/authority-check.mjs --implementation-input "$$IMPLEMENTATION_INPUT_SHA"
PREVIEW_CONTROL = node spikes/web/harness/scripts/preview-control.mjs

.PHONY: i5-02-authority-check i5-02-protected-hash-check i5-02-toolchain-check i5-02-changed-path-check i5-02-security-check i5-02-credential-check i5-02-non-copy-check web-common-test learn-preview learn-preview-status learn-preview-reset-check learn-preview-down

i5-02-authority-check:
	$(AUTHORITY) --check authority

i5-02-protected-hash-check:
	$(AUTHORITY) --check protected-hash

i5-02-toolchain-check:
	$(AUTHORITY) --check toolchain

i5-02-changed-path-check:
	$(AUTHORITY) --check changed-path

i5-02-security-check:
	$(AUTHORITY) --check security

i5-02-credential-check:
	$(AUTHORITY) --check credential

i5-02-non-copy-check:
	$(AUTHORITY) --check non-copy

web-common-test:
	$(AUTHORITY) --check authority
	node --test spikes/web/common/tests/contract-schema.test.mjs spikes/web/common/tests/four-grain.test.mjs spikes/web/common/tests/preview-label.test.mjs spikes/web/common/tests/preview-authority.test.mjs spikes/web/common/tests/state-navigation.test.mjs spikes/web/common/tests/state-reset.test.mjs spikes/web/common/tests/failure-taxonomy.test.mjs spikes/web/common/tests/static-facts.test.mjs spikes/web/common/tests/journey-contract.test.mjs spikes/web/common/tests/browser-authority.test.mjs spikes/web/common/tests/non-copy.test.mjs

learn-preview:
	$(AUTHORITY) --check authority
	@test "$$LESSON" = promotion-trust
	@case "$$PREVIEW_PORT" in ''|*[!0-9]*) exit 2;; esac
	$(PREVIEW_CONTROL) start --lesson "$$LESSON" --port "$$PREVIEW_PORT" --implementation-input "$$IMPLEMENTATION_INPUT_SHA"

learn-preview-status:
	$(AUTHORITY) --check authority
	@case "$$PREVIEW_PORT" in ''|*[!0-9]*) exit 2;; esac
	$(PREVIEW_CONTROL) status --port "$$PREVIEW_PORT" --implementation-input "$$IMPLEMENTATION_INPUT_SHA"

learn-preview-reset-check:
	$(AUTHORITY) --check authority
	@test "$$LESSON" = promotion-trust
	$(PREVIEW_CONTROL) reset-check --lesson "$$LESSON" --implementation-input "$$IMPLEMENTATION_INPUT_SHA"

learn-preview-down:
	$(AUTHORITY) --check authority
	@case "$$PREVIEW_PORT" in ''|*[!0-9]*) exit 2;; esac
	$(PREVIEW_CONTROL) down --port "$$PREVIEW_PORT" --implementation-input "$$IMPLEMENTATION_INPUT_SHA"
