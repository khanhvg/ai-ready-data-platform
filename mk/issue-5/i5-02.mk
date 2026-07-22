I5_02_FRAGMENT_MAKEFILE := $(abspath $(lastword $(MAKEFILE_LIST)))
I5_02_PRIMARY_MAKEFILE := $(abspath $(firstword $(MAKEFILE_LIST)))
I5_02_DIRECT_INVOCATION := $(filter $(I5_02_FRAGMENT_MAKEFILE),$(I5_02_PRIMARY_MAKEFILE))
I5_02_AUTHORIZED_GOALS := i5-02-authority-check i5-02-protected-hash-check i5-02-toolchain-check i5-02-changed-path-check i5-02-security-check i5-02-credential-check i5-02-non-copy-check web-common-test learn-preview learn-preview-status learn-preview-reset-check learn-preview-down web-barrier-b-check web-astro-install web-astro-build web-astro-test web-astro-evidence web-next-install web-next-build web-next-test web-next-evidence web-vite-install web-vite-build web-vite-test web-vite-evidence web-real-fixture-rerun web-browser-evidence web-manual-a11y-check web-spike-scorecard-check web-retention-check web-winner-reproduce web-local-rollback-check web-vite-v3-preflight web-vite-v3-harness-test web-vite-v3-red web-vite-v3-gate web-vite-v3-scan web-vite-v3-retain web-vite-v3-rollback

ifneq ($(strip $(I5_02_DIRECT_INVOCATION)),)
.DEFAULT_GOAL := i5-02-authority-check
I5_02_UNKNOWN_GOALS := $(filter-out $(I5_02_AUTHORIZED_GOALS),$(MAKECMDGOALS))
ifneq ($(strip $(I5_02_UNKNOWN_GOALS)),)
$(error unauthorized target(s): $(I5_02_UNKNOWN_GOALS))
endif
endif

IMPLEMENTATION_INPUT_SHA ?=
LESSON ?= promotion-trust
PREVIEW_PORT ?= 4174
I5_01_MERGE_SHA ?=
export IMPLEMENTATION_INPUT_SHA
export LESSON
export PREVIEW_PORT
export I5_01_MERGE_SHA
I5_02_AUTHORITY = node spikes/web/harness/scripts/continuation-check.mjs --implementation-input "$$IMPLEMENTATION_INPUT_SHA"
I5_02_PREVIEW_CONTROL = node spikes/web/harness/scripts/preview-control.mjs
I5_02_VITE_V3 = node spikes/web/harness/scripts/simple-vite-v3.mjs

.PHONY: $(I5_02_AUTHORIZED_GOALS)

web-barrier-b-check:
	node spikes/web/harness/scripts/barrier-b-check.mjs --merge-sha "$$I5_01_MERGE_SHA"

web-astro-install:
	cd spikes/web/candidates/astro && npm ci --ignore-scripts --no-audit --no-fund --registry=https://registry.npmjs.org
web-astro-build:
	cd spikes/web/candidates/astro && npm run build
web-astro-test web-astro-evidence:
	cd spikes/web/candidates/astro && npm test
web-next-install:
	cd spikes/web/candidates/next && npm ci --ignore-scripts --no-audit --no-fund --registry=https://registry.npmjs.org
web-next-build:
	cd spikes/web/candidates/next && npm run build
web-next-test web-next-evidence:
	cd spikes/web/candidates/next && npm test
web-vite-install:
	cd spikes/web/candidates/vite && npm ci --ignore-scripts --no-audit --no-fund --registry=https://registry.npmjs.org
web-vite-build:
	cd spikes/web/candidates/vite && npm run build
web-vite-test web-vite-evidence:
	cd spikes/web/candidates/vite && npm test
web-real-fixture-rerun:
	node spikes/web/harness/scripts/gate-c-run.mjs
web-browser-evidence:
	node -e 'const v=require("./spikes/web/evidence/retained/gate-c/gate-c-20260721T0625Z/automated/automated-index.json");if(!v.comparisonComplete||v.results.length!==6)process.exit(1)'
web-manual-a11y-check:
	node -e 'const v=require("./spikes/web/evidence/retained/gate-c/gate-c-20260721T0625Z/manual/manual-evidence.json");if(!v.manualComplete)process.exit(1)'
web-spike-scorecard-check:
	node -e 'const v=require("./docs/decisions/evidence/adr-0005-web-stack-scorecard.json");if(v.status!=="Proposed"||v.decision!=="no-winner"||v.acceptanceCanAdvance!==false||Object.values(v.candidates).some(c=>c.numericScore!==null))process.exit(1)'
web-retention-check:
	test -f spikes/web/evidence/retention-index.json
web-winner-reproduce:
	@echo "no-winner: retained neutral preview only" >&2; exit 1
web-local-rollback-check:
	test ! -e apps/learning-portal && test ! -e apps/lab-runner

web-vite-v3-preflight:
	$(I5_02_VITE_V3) preflight --implementation-input "$$IMPLEMENTATION_INPUT_SHA"

web-vite-v3-harness-test:
	node --test spikes/web/harness/tests/simple-vite-v3.test.mjs

web-vite-v3-red:
	$(I5_02_VITE_V3) red --implementation-input "$$IMPLEMENTATION_INPUT_SHA"

web-vite-v3-gate:
	$(I5_02_VITE_V3) gate --implementation-input "$$IMPLEMENTATION_INPUT_SHA"

web-vite-v3-scan:
	$(I5_02_VITE_V3) scan --implementation-input "$$IMPLEMENTATION_INPUT_SHA"

web-vite-v3-retain:
	$(I5_02_VITE_V3) retain --implementation-input "$$IMPLEMENTATION_INPUT_SHA"

web-vite-v3-rollback:
	$(I5_02_VITE_V3) rollback --implementation-input "$$IMPLEMENTATION_INPUT_SHA"

i5-02-authority-check:
	$(I5_02_AUTHORITY) --check authority

i5-02-protected-hash-check:
	$(I5_02_AUTHORITY) --check protected-hash

i5-02-toolchain-check:
	$(I5_02_AUTHORITY) --check toolchain

i5-02-changed-path-check:
	$(I5_02_AUTHORITY) --check changed-path

i5-02-security-check:
	$(I5_02_AUTHORITY) --check security

i5-02-credential-check:
	$(I5_02_AUTHORITY) --check credential

i5-02-non-copy-check:
	$(I5_02_AUTHORITY) --check non-copy

web-common-test:
	$(I5_02_AUTHORITY) --check authority
	node --test spikes/web/common/tests/contract-schema.test.mjs spikes/web/common/tests/four-grain.test.mjs spikes/web/common/tests/preview-label.test.mjs spikes/web/common/tests/preview-authority.test.mjs spikes/web/common/tests/state-navigation.test.mjs spikes/web/common/tests/state-reset.test.mjs spikes/web/common/tests/failure-taxonomy.test.mjs spikes/web/common/tests/static-facts.test.mjs spikes/web/common/tests/journey-contract.test.mjs spikes/web/common/tests/browser-authority.test.mjs spikes/web/common/tests/non-copy.test.mjs

learn-preview:
	$(I5_02_AUTHORITY) --check authority
	@test "$$LESSON" = promotion-trust
	@case "$$PREVIEW_PORT" in ''|*[!0-9]*) exit 2;; esac
	$(I5_02_PREVIEW_CONTROL) start --lesson "$$LESSON" --port "$$PREVIEW_PORT" --implementation-input "$$IMPLEMENTATION_INPUT_SHA"

learn-preview-status:
	$(I5_02_AUTHORITY) --check authority
	@case "$$PREVIEW_PORT" in ''|*[!0-9]*) exit 2;; esac
	$(I5_02_PREVIEW_CONTROL) status --port "$$PREVIEW_PORT" --implementation-input "$$IMPLEMENTATION_INPUT_SHA"

learn-preview-reset-check:
	$(I5_02_AUTHORITY) --check authority
	@test "$$LESSON" = promotion-trust
	$(I5_02_PREVIEW_CONTROL) reset-check --lesson "$$LESSON" --implementation-input "$$IMPLEMENTATION_INPUT_SHA"

learn-preview-down:
	$(I5_02_AUTHORITY) --check authority
	@case "$$PREVIEW_PORT" in ''|*[!0-9]*) exit 2;; esac
	$(I5_02_PREVIEW_CONTROL) down --port "$$PREVIEW_PORT" --implementation-input "$$IMPLEMENTATION_INPUT_SHA"
