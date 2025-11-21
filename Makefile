IMAGE_NAME = stt-microservice
PORT = 33000

.PHONY: build run stop clean

build:
	docker build -t $(IMAGE_NAME) .

run:
	docker run -d -p $(PORT):$(PORT) --name $(IMAGE_NAME) $(IMAGE_NAME)

stop:
	docker stop $(IMAGE_NAME) || true
	docker rm $(IMAGE_NAME) || true

clean: stop
	docker rmi $(IMAGE_NAME) || true

logs:
	docker logs -f $(IMAGE_NAME)
