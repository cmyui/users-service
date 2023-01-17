#!/usr/bin/make

REPO_DIR = ..

build: # build all containers
	@docker build -t beatmap-ids-service:latest $(REPO_DIR)/beatmap-ids-service

clone: # clone all containers
	@if [ ! -d $(REPO_DIR)/beatmap-ids-service ]; then git clone git@github.com:akatsuki-v2/beatmap-ids-service.git $(REPO_DIR)/beatmap-ids-service; fi

pull: # pull all containers
	cd $(REPO_DIR)/beatmap-ids-service && git pull

run-bg: # run all containers in the background
	@docker-compose up -d \
		beatmap-ids-service \
		mysql

run: # run all containers in the foreground
	@docker-compose up \
		beatmap-ids-service \
		mysql

logs: # attach to the containers live to view their logs
	@docker-compose logs -f

test: # run the tests
	@docker-compose exec beatmap-ids-service /scripts/run-tests.sh

test-dbg: # run the tests in debug mode
	@docker-compose exec beatmap-ids-service /scripts/run-tests.sh --dbg
