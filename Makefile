SHELL := /bin/bash

export GOOGLE_CLOUD_PROJECT=software-builds
export BADGES_BUCKET=$(GOOGLE_CLOUD_PROJECT)-badges

deploy:
	gcloud functions deploy \
		cloud-build-badge \
		--project=$(GOOGLE_CLOUD_PROJECT) \
		--source . \
		--runtime python39 \
		--entry-point build_badge \
		--service-account cloud-build-badge@$(GOOGLE_CLOUD_PROJECT).iam.gserviceaccount.com \
		--set-env-vars BADGES_BUCKET=$(GOOGLE_CLOUD_PROJECT)-badges \
		--trigger-topic=cloud-builds


unit:
	python -m pytest -W ignore::DeprecationWarning -v

integration:
	source tests/integration.sh && run_test
