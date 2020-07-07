PROJECT_NAME = flask-app
CI_SERVER = jenkins
DOCKER = docker
DOCKER_COMPOSE = docker-compose

.PHONY: help test_pytest test_unittest

help:
	@echo "    test_pytest"
	@echo "        Run unit tests (pytest) on the application"
	@echo "    test_unittest"
	@echo "        Run unit tests (unittest) on the application"
	@echo "    clean"
	@echo "        Clean the Environment Docker Container"
	@echo "    system-prune"
	@echo "        Clean Environment  Docker Containers, volumes, images which are dangling"
	@echo "    remove"
	@echo "        Remove the Environment Docker Container"
	@echo "    stop"
	@echo "        Stop the Environment Docker Container"

test_pytest:
	python3 -m pytest -vv

test_unittest:
	python3 unittest_flaskapp.py

.PHONY: stop

stop:
	$(DOCKER) -p $(PROJECT_NAME) stop

.PHONY: remove

remove: stop
	$(DOCKER) -p $(PROJECT_NAME) rm --force -v

.PHONY: system-prune clean

system-prune:
	echo "y" | $(DOCKER) system prune

clean: remove system-prune