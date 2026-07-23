ifndef ISSUE_5_MAKE_FRAGMENTS
$(error mk/issue-5/i5-05.mk must be composed through the root Makefile)
endif

PORTAL_ROOT := apps/learning-portal

.PHONY: learn learn-status learn-down portal-test portal-a11y portal-e2e lesson-e2e local-journey-e2e portal-visual-review

learn:
	@test -n "$(value LESSON)" || (echo "LESSON is required" >&2; exit 2)
	@node $(PORTAL_ROOT)/scripts/portal-lifecycle.mjs start

learn-status:
	@node $(PORTAL_ROOT)/scripts/portal-lifecycle.mjs status

learn-down:
	@node $(PORTAL_ROOT)/scripts/portal-lifecycle.mjs down

portal-test:
	@npm --prefix $(PORTAL_ROOT) run test:unit
	@npm --prefix $(PORTAL_ROOT) run build

portal-a11y:
	@npm --prefix $(PORTAL_ROOT) run test:stage-a -- --workers=1 --retries=0

portal-e2e:
	@npm --prefix $(PORTAL_ROOT) run test:stage-a -- --workers=1 --retries=0

portal-visual-review:
	@npm --prefix $(PORTAL_ROOT) run test:visual -- --workers=1 --retries=0

lesson-e2e:
	@test -n "$(value LESSON)" || (echo "LESSON is required" >&2; exit 2)
	@node $(PORTAL_ROOT)/scripts/portal-lifecycle.mjs blocked lesson-e2e

local-journey-e2e:
	@node $(PORTAL_ROOT)/scripts/portal-lifecycle.mjs blocked local-journey-e2e
