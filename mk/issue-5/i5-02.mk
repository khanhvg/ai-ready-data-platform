.DEFAULT_GOAL := i5-02-authority-check

AUTHORIZED_GOALS := i5-02-authority-check i5-02-protected-hash-check i5-02-toolchain-check i5-02-changed-path-check i5-02-security-check i5-02-credential-check i5-02-non-copy-check web-common-test learn-preview learn-preview-status learn-preview-reset-check learn-preview-down web-barrier-b-check web-astro-install web-astro-build web-astro-test web-astro-evidence web-next-install web-next-build web-next-test web-next-evidence web-vite-install web-vite-build web-vite-test web-vite-evidence web-real-fixture-rerun web-browser-evidence web-manual-a11y-check web-spike-scorecard-check web-retention-check web-winner-reproduce web-local-rollback-check
UNKNOWN_GOALS := $(filter-out $(AUTHORIZED_GOALS),$(MAKECMDGOALS))
ifneq ($(strip $(UNKNOWN_GOALS)),)
$(error unauthorized target(s): $(UNKNOWN_GOALS))
endif

IMPLEMENTATION_INPUT_SHA ?=
LESSON ?= promotion-trust
PREVIEW_PORT ?= 4174
I5_01_MERGE_SHA ?=
export IMPLEMENTATION_INPUT_SHA
export LESSON
export PREVIEW_PORT
export I5_01_MERGE_SHA
AUTHORITY = node spikes/web/harness/scripts/continuation-check.mjs --implementation-input "$$IMPLEMENTATION_INPUT_SHA"
PREVIEW_CONTROL = node spikes/web/harness/scripts/preview-control.mjs

.PHONY: $(AUTHORIZED_GOALS)

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
