DOCKER_IMAGE_NAME=sber-ios-install

run-docker-container:
	docker build -t sber-ios-install .
	docker run --privileged $(DOCKER_IMAGE_NAME)
	