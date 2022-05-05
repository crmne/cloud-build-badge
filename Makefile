requirements.txt: pyproject.toml poetry.lock
	poetry export -f requirements.txt --output requirements.txt --without-hashes

.PHONY: test
test:
	poetry run pytest -v

.PHONY: setup.bucket
setup.bucket:
	gsutil mb gs://${GOOGLE_CLOUD_PROJECT}-badges/
	gsutil defacl ch -u AllUsers:R gs://${GOOGLE_CLOUD_PROJECT}-badges/
	gsutil -m -h "Cache-Control:no-cache,max-age=0" cp ./badges/*.svg gs://${GOOGLE_CLOUD_PROJECT}-badges/badges/

.PHONY: setup.iam
setup.iam:
	gcloud iam service-accounts create cloud-build-badge
	gsutil iam ch serviceAccount:cloud-build-badge@${GOOGLE_CLOUD_PROJECT}.iam.gserviceaccount.com:legacyObjectReader,legacyBucketWriter gs://${GOOGLE_CLOUD_PROJECT}-badges/

.PHONY: setup
setup: setup.bucket setup.iam

.PHONY: deploy
deploy: requirements.txt
	gcloud functions deploy cloud-build-badge \
		--source . \
		--runtime python39 \
		--entry-point build_badge \
		--service-account cloud-build-badge@${GOOGLE_CLOUD_PROJECT}.iam.gserviceaccount.com \
		--trigger-topic=cloud-builds \
		--set-env-vars BADGES_BUCKET=${GOOGLE_CLOUD_PROJECT}-badges
