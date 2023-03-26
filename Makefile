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

stop: # stop all containers
	docker-compose down

logs: # attach to the containers live to view their logs
	docker-compose logs -f

test: # run the tests
	docker-compose exec example-service /scripts/run-tests.sh

test-dbg: # run the tests in debug mode
	docker-compose exec example-service /scripts/run-tests.sh --dbg

view-cov: # open the coverage report in the browser
	if grep -q WSL2 /proc/sys/kernel/osrelease; then \
		wslview mount/tests/htmlcov/index.html; \
	else \
		xdg-open mount/tests/htmlcov/index.html; \
	fi

up-migrations: # apply up migrations from current state
	docker-compose exec example-service /scripts/migrate-db.sh up

down-migrations: # apply down migrations from current state
	docker-compose exec example-service /scripts/migrate-db.sh down
