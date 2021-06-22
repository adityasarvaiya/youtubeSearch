.PHONY: version all

VIRTUALENV_FOLDER?=venv
CURDIR:=$(shell pwd)
BIN_DIR:=$(CURDIR)/$(VIRTUALENV_FOLDER)/bin

PYTHON:=$(BIN_DIR)/python
PIP:=$(BIN_DIR)/pip
PYLINT:=$(BIN_DIR)/pylint
COVERAGE:=$(BIN_DIR)/coverage
PRE_COMMIT:=$(BIN_DIR)/pre-commit
REQUIREMENTS:=$(CURDIR)/reqs/dev.txt


HOST=0.0.0.0:8000

TESTSUITE=data_center
TEST_SETTINGS=data_center.settings.test
COV_CONFIG:=$(CURDIR)/.coveragerc
COV_REPORT_FORMAT=

.PHONY: help
help: ## Show this help message
help: version
	@echo 'Usage: make <target>'
	@echo
	@echo 'Targets:'
	@echo "$$(grep -hE '^\S+:.*##' $(MAKEFILE_LIST) | sed -e 's/:.*##\s*/:/' -e 's/^\(.\+\):\(.*\)/\1:\2/' | column -c2 -t -s:)"

.PHONY: venv_create
venv_create:
	test -f $(VIRTUALENV_FOLDER)/bin/activate ||  $(shell which python3) -m venv $(VIRTUALENV_FOLDER)

.PHONY: clean_pyc
clean_pyc: ## Clean all *.pyc files
	find . -name '*.pyc' -delete

.PHONY: clean
clean: clean_pyc

.PHONY: pylint
pylint:
	$(PYLINT) $(TESTSUITE)

.PHONY: update
update: ## Update all necessary requirements and migrate
update: requirements_update migrate

.PHONY: install
install: ## Install all necessary requirements
install: venv_create
	$(PIP) install -r "$(REQUIREMENTS)"
	$(PRE_COMMIT) install
	$(PYTHON) manage.py migrate

.PHONY: requirements_update
requirements_update: requirements

requirements:
	@echo -e "Installing/Updating backend requirements"
	$(PIP) install -r "$(REQUIREMENTS)"

.PHONY: migrations
migrations:
migrations: ## Make migrations
	$(PYTHON) manage.py makemigrations

.PHONY: migrate
migrate:
migrate: ## Apply migration files
	$(PYTHON) manage.py migrate

.PHONY: test
test: ## Run tests
test: clean_pyc unittest

.PHONY: test-cov
test-cov: ## Run tests with coverage
test-cov: clean_pyc unittest-cov report

.PHONY: unittest
unittest:
	yes yes | $(PYTHON) $(CURDIR)/manage.py test --settings=$(TEST_SETTINGS)
	$(PYTHON) $(CURDIR)/manage.py test --settings=$(TEST_SETTINGS) --keepdb

.PHONY: report
report: ## Coverage report
	$(COVERAGE) report -m

.PHONY: unittest-cov
unittest-cov:
	yes yes | $(COVERAGE) run  $(CURDIR)/manage.py test --settings=$(TEST_SETTINGS)
	$(COVERAGE) run $(CURDIR)/manage.py test --settings=$(TEST_SETTINGS) --keepdb

.PHONY: unittest-ci
unittest-ci:
	$(COVERAGE) run $(CURDIR)/manage.py test --settings=$(TEST_SETTINGS)

.PHONY: build
build: ## Build
build: install pre_commit collectstatic

.PHONY: pre_commit
pre_commit: ## Pre commit
pre_commit: requirements_update
	$(PRE_COMMIT) install

.PHONY: collectstatic
collectstatic: ## Collects static files
	$(PYTHON) manage.py collectstatic --no-input

.PHONY: server
server: ## Run python server only
server: requirements
	$(PYTHON) $(CURDIR)/manage.py runserver $(HOST)

.PHONY: createadmin
admin: ## Creates Administrator account
admin: update
	$(PYTHON) $(CURDIR)/manage.py initadmin

.PHONY: version
version: ## Print version information
	@echo $$(echo "version commit@" && git rev-parse --short HEAD)

## Shortcuts
.PHONY: b
b: build

.PHONY: t
t: test

.PHONY: v
v: version

.PHONY: h
h: help

.PHONY: i
i: install

.PHONY: u
u: update

.PHONY: tc
tc: test-cov