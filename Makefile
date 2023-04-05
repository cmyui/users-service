#!/usr/bin/make

build: # build all containers
	sudo chmod -R 755 pgdata
	docker build -t users-service:latest -t registry.digitalocean.com/akatsuki/users-service:latest .

run-bg: # run all containers in the background
	docker-compose up -d \
		users-service \
		postgres

run: # run all containers in the foreground
	docker-compose up \
		users-service \
		postgres

stop: # stop all containers
	docker-compose down

logs: # attach to the containers live to view their logs
	docker-compose logs -f

test: # run the tests
	docker-compose exec users-service /scripts/run-tests.sh

test-dbg: # run the tests in debug mode
	docker-compose exec users-service /scripts/run-tests.sh --dbg

view-cov: # open the coverage report in the browser
	if grep -q WSL2 /proc/sys/kernel/osrelease; then \
		wslview mount/tests/htmlcov/index.html; \
	else \
		xdg-open mount/tests/htmlcov/index.html; \
	fi

up-migrations: # apply up migrations from current state
	docker-compose exec users-service /scripts/migrate-db.sh up

down-migrations: # apply down migrations from current state
	docker-compose exec users-service /scripts/migrate-db.sh down

push:
	docker push registry.digitalocean.com/akatsuki/users-service:latest

install:
	helm install --values chart/values.yaml users-service-staging ../akatsuki/common-helm-charts/microservice-base/

uninstall:
	helm uninstall users-service-staging

diff-upgrade:
	helm diff upgrade --allow-unreleased --values chart/values.yaml users-service-staging ../akatsuki/common-helm-charts/microservice-base/

upgrade:
	helm upgrade --atomic --values chart/values.yaml users-service-staging ../akatsuki/common-helm-charts/microservice-base/
