#!/usr/bin/make

build: # build all containers
	docker build -t example-service:latest .

run-bg: # run all containers in the background
	docker-compose up -d \
		example-service \
		postgres

run: # run all containers in the foreground
	docker-compose up \
		example-service \
		postgres

logs: # attach to the containers live to view their logs
	docker-compose logs -f

test: # run the tests
	docker-compose exec example-service /scripts/run-tests.sh

test-dbg: # run the tests in debug mode
	docker-compose exec example-service /scripts/run-tests.sh --dbg
