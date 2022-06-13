DOCKER_IMAGE_NAME=sber-ios-install

run-docker-container:
	docker build -t sber-ios-install .
	docker run -v /run:/run -v /dev/bus/usb:/dev/bus/usb --privileged --network="host" $(DOCKER_IMAGE_NAME)
	