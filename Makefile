SHELL := /bin/bash

test: venv requirements-test.txt
	( \
		clear; \
		echo "┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
		echo "┣╾> Installing TEST requirements"; \
		echo "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
		. .venv/bin/activate; \
		pip install -r requirements-test.txt; \
		clear; \
		echo "┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
		echo "┣╾> Running Tests... "; \
		echo "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
		env $$(cat local.env | grep -v '#' | xargs) \
		COMMIT=$$(git rev-parse HEAD) \
		ptw ; \
	)

local: venv requirements-dev.txt
	( \
		clear; \
		echo "┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
		echo "┣╾> Installing DEV/LOCAL requirements"; \
		echo "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
		. .venv/bin/activate; \
		pip install -r requirements-dev.txt; \
		clear ;\
		echo "┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
		echo "┣╾> Running local dev ... "; \
		echo "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
		env $$(cat local.env | grep -v '#' | xargs) \
		COMMIT=$$(git rev-parse HEAD) \
		./infrastructure/bin/app.sh -l -r; \
	)

docker:
	clear
	@echo "┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "┣╾> Starting containerized environment..."
	@echo "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	docker run -it --rm --env-file infrastructure/container/docker.env

compose: compose-build
	clear
	@echo "┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "┣╾> Starting containerized environment..."
	@echo "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	docker-compose -f infrastructure/container/local.docker-compose.yml up

compose-test: compose-build
	clear
	@echo "┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "┣╾> Starting test container...  "
	@echo "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	docker-compose -f infrastructure/container/local.docker-compose.yml up test

compose-dev: compose-build
	clear
	@echo "┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "┣╾> Starting app and db containers...  "
	@echo "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	docker-compose -f infrastructure/container/local.docker-compose.yml up -d db
	docker-compose -f infrastructure/container/local.docker-compose.yml up app

compose-up: compose-build
	docker-compose -f infrastructure/container/local.docker-compose.yml up

compose-down:
	docker-compose -f infrastructure/container/local.docker-compose.yml down

compose-build:
	( \
		clear; \
		echo "┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
		echo "┣╾> Building containers... "; \
		echo "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
		docker-compose -f infrastructure/container/local.docker-compose.yml \
		build --build-arg COMMIT=$$(git rev-parse HEAD) \
	)

run: venv requirements.txt
	( \
		clear; \
		echo "┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
		echo "┣╾> Installing APPLICATION requirements"; \
		echo "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
		. .venv/bin/activate; \
		pip install -r requirements.txt; \
		clear ;\
		./infrastructure/bin/app.sh; \
	)

venv: venv_exists
	@echo " "
	@echo "Activating virtualenv..."
	. .venv/bin/activate;

venv_exists: prepare
	test -d .venv || ( \
		clear; \
		echo "┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
		echo "┣╾> Verifying and Creating Virtual Env   "; \
		echo "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
		echo " "; \
		echo "Verifying and Creating Virtual Environment if not exists..."; \
		virtualenv --python="$$HOME/.pyenv/versions/3.7.9/bin/python3.7" .venv \
	)

prepare:
	test -d ~/.pyenv || ( \
		clear; \
		echo "┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
		echo "┣╾> Installing PYENV to python versions"; \
		echo "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
		echo "Installing pyenv to manage python versions"; \
		curl https://pyenv.run | bash \
	)

	( \
		clear; \
		echo "┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
		echo "┣╾> Installing python 3.7.9 "; \
		echo "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
		export PATH="$$HOME/.pyenv/bin:$$PATH" ; \
		eval "$$(pyenv init -)" ; \
		eval "$$(pyenv virtualenv-init -)" ; \
		pyenv install -v 3.7.9 -s ; \
	)
	clear

install: venv
	( \
		clear; \
		. .venv/bin/activate; \
		echo "┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
		echo "┣╾> Installing ALL requirements"; \
		echo "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
		pip install -r requirements.txt; \
		pip install -r requirements-test.txt; \
		pip install -r requirements-dev.txt; \
	)

clean_all: clean
	echo "┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
	echo "┣╾> Removing pyenv and python versions "; \
	echo "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
	rm -rf ~/.pyenv

clean: compose-down
	echo "┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
	echo "┣╾> Cleaning virtual environment  "; \
	echo "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
	rm -rf .venv
	find . -iname "*.log" -delete
	find . -iname "*.pyc" -delete
	find . -type d -iname ".pytest_cache" -print0 | xargs -0 -I {} rm -rf {} +
