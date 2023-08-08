include envs/web

ACCOUNT_ID=817650998681
AWS_REGION=eu-west-2

# Docker
ECR_URL=$(ACCOUNT_ID).dkr.ecr.$(AWS_REGION).amazonaws.com
ECR_REPO_NAME=i-dot-ai-one-big-thing
ECR_REPO_URL=$(ECR_URL)/$(ECR_REPO_NAME)
IMAGE_TAG=$$(git rev-parse HEAD)
IMAGE=$(ECR_REPO_URL):$(IMAGE_TAG)


define _update_requirements
	docker-compose run requirements bash -c "pip install -U pip setuptools && pip install -U -r /app/$(1).txt && pip freeze > /app/$(1).lock"
endef

.PHONY: update-requirements
update-requirements:
	$(call _update_requirements,requirements)
	$(call _update_requirements,requirements-dev)

.PHONY: reset-db
reset-db:
	docker-compose up --detach ${POSTGRES_HOST}
	docker-compose run ${POSTGRES_HOST} dropdb -U ${POSTGRES_USER} -h ${POSTGRES_HOST} ${POSTGRES_DB}
	docker-compose run ${POSTGRES_HOST} createdb -U ${POSTGRES_USER} -h ${POSTGRES_HOST} ${POSTGRES_DB}
	docker-compose kill

# -------------------------------------- Code Style  -------------------------------------

.PHONY: check-python-code
check-python-code:
	isort --check .
	black --check .
	flake8
	bandit -ll -r ./one_big_thing

.PHONY: check-migrations
check-migrations:
	docker-compose build web
	docker-compose run web python manage.py migrate
	docker-compose run web python manage.py makemigrations --check

.PHONY: test
test:
	docker-compose down
	docker-compose build tests-one_big_thing one_big_thing-test-db && docker-compose run --rm tests-one_big_thing
	docker-compose down


# -------------------------------------- Docker  -------------------------------------

docker/login:
	aws ecr get-login-password --region $(AWS_REGION) | docker login --username AWS --password-stdin $(ECR_URL)

docker/build:
	docker build -t $(IMAGE) -f ./docker/web/Dockerfile .

docker/build-m1:
	docker buildx build --platform linux/amd64 -t $(IMAGE) -f ./docker/web/Dockerfile .

docker/push:
	docker push $(IMAGE)


# -------------------------------------- Terraform  -------------------------------------

tf_build_args=-var "image_tag=$(IMAGE_TAG)" -var-file=variables/${env}.tfvars

tf/new-workspace:
	terraform -chdir=terraform workspace new $(env)

tf/set-workspace:
	terraform -chdir=terraform workspace select $(env)

# Will create a new workspace if one does not already exist
# Note: only works in github actions
tf/set-or-create-workspace:
	make tf/set-workspace || make tf/new-workspace

tf/init:
	terraform -chdir=./terraform init -backend-config=backends/${env}.conf

tf/plan:
	make tf/set-workspace && \
	terraform -chdir=./terraform plan $(tf_build_args)

tf/apply:
	make tf/set-workspace && \
	terraform -chdir=./terraform apply ${tf_build_args}

tf/destroy:
	make tf/set-workspace && \
	terraform -chdir=./terraform destroy ${tf_build_args}
