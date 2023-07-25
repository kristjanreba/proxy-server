# Variables
HTTP_PORT ?= 8081
TEST_SERVER_PORT ?= 8001
DOCKER_IMAGE_NAME ?= python-http-proxy
DOCKER_TEST_SERVER_IMAGE_NAME ?= python-test-server

.PHONY: build run test

build:
	docker build -t $(DOCKER_IMAGE_NAME) .
	docker build -t $(DOCKER_TEST_SERVER_IMAGE_NAME) -f DockerfileTestServer .

run:
	docker-compose up

test:
	docker-compose up -d
	docker-compose exec proxy pytest test_proxy_server.py
	docker-compose down
