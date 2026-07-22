ifneq ($(abspath $(firstword $(MAKEFILE_LIST))),$(abspath $(lastword $(MAKEFILE_LIST))))

.PHONY: learn learn-status learn-down portal-test portal-a11y portal-e2e portal-visual-review lesson-e2e local-journey-e2e

learn:
	@npm --prefix apps/learning-portal run build
	@node apps/learning-portal/scripts/portal-lifecycle.mjs start

learn-status:
	@node apps/learning-portal/scripts/portal-lifecycle.mjs status

learn-down:
	@node apps/learning-portal/scripts/portal-lifecycle.mjs down

portal-test:
	@npm --prefix apps/learning-portal run test:unit
	@npm --prefix apps/learning-portal run build

portal-a11y:
	@npm --prefix apps/learning-portal run test:stage-a -- --workers=1 --retries=0

portal-e2e:
	@npm --prefix apps/learning-portal run test:stage-a -- --workers=1 --retries=0

portal-visual-review:
	@npm --prefix apps/learning-portal run test:visual -- --workers=1 --retries=0
	@node apps/learning-portal/scripts/write-review-artifacts.mjs

lesson-e2e local-journey-e2e:
	@node apps/learning-portal/scripts/verify-stage-a-release.mjs --stage-b-block $@

else
.DEFAULT_GOAL := i5-05-direct-invocation-denied
.PHONY: i5-05-direct-invocation-denied
i5-05-direct-invocation-denied:
	@echo "I5-05_FRAGMENT_DIRECT_INVOCATION_DENIED" >&2
	@exit 2
endif
