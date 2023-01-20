#!/usr/bin/make

REPO_DIR = ..

build: # build all containers
	@docker build -t example-service:latest $(REPO_DIR)/example-service

clone: # clone all containers
	@if [ ! -d $(REPO_DIR)/example-service ]; then git clone git@github.com:akatsuki-v2/example-service.git $(REPO_DIR)/example-service; fi

pull: # pull all containers
	cd $(REPO_DIR)/example-service && git pull

run-bg: # run all containers in the background
	@docker-compose up -d \
		example-service \
		mysql

run: # run all containers in the foreground
	@docker-compose up \
		example-service \
		mysql

logs: # attach to the containers live to view their logs
	@docker-compose logs -f

test: # run the tests
	@docker-compose exec example-service /scripts/run-tests.sh

test-dbg: # run the tests in debug mode
	@docker-compose exec example-service /scripts/run-tests.sh --dbg
