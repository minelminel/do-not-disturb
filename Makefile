.DEFAULT_GOAL := help
.PHONY: help
TEST_PATH=./
PACKAGE=do-not-disturb
PORT=5000
REGISTRY=localhost:32000
AUTHOR=minelminel

help:
	@echo "==> Available Commands"
	@echo " make build      --      Build an updated Docker image and tag it as :latest"
	@echo " make run        --      Run the latest Docker image (non-daemon mode)"
	@echo " make tag        --      Tag the latest image in preparation for pushing to registry"
	@echo " make push       --      Push the latest image to the registry"
	@echo " make publish    --      Perform all the above steps, in order to create an updated published image"

build:
	@echo "==> build"
	docker build -t ${PACKAGE}:latest .

exec: build
	@echo "==> exec"
	docker run -it --entrypoint=/bin/bash ${PACKAGE}:latest

run: build
	@echo "==> run"
	docker run -p ${PORT}:80 ${PACKAGE}:latest

tag: build
	@echo "==> tag"
	docker tag ${PACKAGE}:latest ${REGISTRY}/${AUTHOR}/${PACKAGE}:latest

push: build tag
	@echo "==> push"
	docker push ${REGISTRY}/${AUTHOR}/${PACKAGE}:latest

publish: build tag push
	@echo "==> publish"
	@echo "Updated image available for rollout"
