.PHONY: learning-contracts-check lesson-check api-contracts-check evidence-verify

I5_03_ENV := env -u PYTHONPATH -u AWS_ACCESS_KEY_ID -u AWS_SECRET_ACCESS_KEY -u AWS_SESSION_TOKEN -u AWS_PROFILE -u AWS_DEFAULT_PROFILE -u GOOGLE_APPLICATION_CREDENTIALS -u AZURE_CLIENT_ID -u AZURE_CLIENT_SECRET PYTHONDONTWRITEBYTECODE=1

learning-contracts-check:
	@$(I5_03_ENV) python3.12 -m scripts.learning_contracts.check learning-contracts-check

lesson-check:
	@$(I5_03_ENV) python3.12 -m scripts.learning_contracts.check lesson-check --lesson "$(LESSON)"

api-contracts-check:
	@$(I5_03_ENV) python3.12 -m scripts.learning_contracts.check api-contracts-check

evidence-verify:
	@$(I5_03_ENV) python3.12 -m scripts.learning_contracts.check evidence-verify --evidence "$(EVIDENCE)"
