SHELL=/bin/bash



# Project.

PROJECT_NAME=belaster

BELASTER_CLI_NAME=belaster
SRC_BELASTER_CLI_PATH=exe/$(BELASTER_CLI_NAME)

SRC_BASH_COMPLETER_HELPER_NAME=bash-completer-helper
SRC_BASH_COMPLETER_HELPER_PATH=exe/$(SRC_BASH_COMPLETER_HELPER_NAME)

DEST_BASH_COMPLETER_HELPER_NAME=bash-completer-helper-for-belaster


# Dev environment.

## Python version used for development.
PYTHON_VERSION=3.13

## pyenv environment.
PYENV_ROOT:=$(shell pyenv root)
PYENV_ENVIRONMENT_NAME=$(PROJECT_NAME)
PYENV_ENVIRONMENT_PATH=$(PYENV_ROOT)/versions/$(PYENV_ENVIRONMENT_NAME)

## venv environment.
VIRTUAL_ENVIRONMENT_PATH=.venv

## Command-line belaster for development.
DEV_BELASTER_CLI_PATH=$(VIRTUAL_ENVIRONMENT_PATH)/bin/$(BELASTER_CLI_NAME)

## Helper for bash completer.
DEV_BASH_COMPLETER_HELPER_PATH=$(VIRTUAL_ENVIRONMENT_PATH)/bin/$(DEST_BASH_COMPLETER_HELPER_NAME)

## Belaster user library.
DEV_USER_LIB_PATH=$(VIRTUAL_ENVIRONMENT_PATH)/lib64/python$(PYTHON_VERSION)/site-packages/$(PROJECT_NAME)



# Installation.

DEST_LOCAL_EXECUTABLES=$${HOME}/.local/bin/

## Command-line belaster.
## The main tool.
DEST_EXE_BELASTER_PATH=$(DEST_LOCAL_EXECUTABLES)/$(BELASTER_CLI_NAME)

## Bash autocomplete script.
## Relies on a helper written in Python.
SRC_BASH_COMPLETER_PATH=exe/bash-completer
DEST_BASH_COMPLETER_PATH=/etc/bash_completion.d/_$(BELASTER_CLI_NAME)

## Bash autocomplete helper.
DEST_BASH_COMPLETER_HELPER_PATH=$(DEST_LOCAL_EXECUTABLES)/$(DEST_BASH_COMPLETER_HELPER_NAME)

## Belaster user library.
SRC_USER_LIB_PATH=lib

DEST_USER_LIB_PATH=/usr/lib/python3/dist-packages/$(PROJECT_NAME)


# That method creates symlinks when they do not exist.
# Note: the method does not verify whether an existing symlink has the correct target.
define symlink =
	if [ ! -h $(2) ]; then \
		ln -s $${PWD}/$(1) $${PWD}/$(2); \
	fi
endef



# Rules.

## Default recipe.
## Setup dev env if needed + run the tests: unit-tests and end-to-end.
.PHONY: all
all: test



## Install the executables and the library.
.PHONY: install
install: \
		$(DEST_USER_LIB_PATH) \
		$(DEST_EXE_BELASTER_PATH) \
		$(DEST_BASH_COMPLETER_PATH) \
		$(DEST_BASH_COMPLETER_HELPER_PATH)


$(DEST_USER_LIB_PATH): $(SRC_USER_LIB_PATH)
	sudo cp -R $(SRC_USER_LIB_PATH) $(DEST_USER_LIB_PATH)


$(DEST_EXE_BELASTER_PATH): $(SRC_BELASTER_CLI_PATH)
	cp $(SRC_BELASTER_CLI_PATH) $(DEST_EXE_BELASTER_PATH)
	chmod u+x $(DEST_EXE_BELASTER_PATH)


$(DEST_BASH_COMPLETER_PATH): $(SRC_BASH_COMPLETER_PATH)
	sudo cp $(SRC_BASH_COMPLETER_PATH) $(DEST_BASH_COMPLETER_PATH)


$(DEST_BASH_COMPLETER_HELPER_PATH): $(SRC_BASH_COMPLETER_HELPER_PATH)
	cp $(SRC_BASH_COMPLETER_HELPER_PATH) $(DEST_BASH_COMPLETER_HELPER_PATH)
	chmod u+x $(DEST_BASH_COMPLETER_HELPER_PATH)



## Setup the dev environment.
.PHONY: dev-env
dev-env: \
		$(DEV_USER_LIB_PATH) \
		$(DEV_BELASTER_CLI_PATH) \
		$(DEST_BASH_COMPLETER_PATH) \
		$(DEV_BASH_COMPLETER_HELPER_PATH)


### Create symlinks from dev env to executables and libraries in the local copy of the repository.
$(DEV_USER_LIB_PATH): $(VIRTUAL_ENVIRONMENT_PATH) $(SRC_USER_LIB_PATH)
	$(call symlink,$(SRC_USER_LIB_PATH),$(DEV_USER_LIB_PATH))


$(DEV_BELASTER_CLI_PATH): $(VIRTUAL_ENVIRONMENT_PATH) $(SRC_BELASTER_CLI_PATH)
	chmod u+x $(SRC_BELASTER_CLI_PATH)
	$(call symlink,$(SRC_BELASTER_CLI_PATH),$(DEV_BELASTER_CLI_PATH))


$(DEV_BASH_COMPLETER_HELPER_PATH): $(VIRTUAL_ENVIRONMENT_PATH) $(SRC_BASH_COMPLETER_HELPER_PATH)
	chmod u+x $(SRC_BASH_COMPLETER_HELPER_PATH)
	$(call symlink,$(SRC_BASH_COMPLETER_HELPER_PATH),$(DEV_BASH_COMPLETER_HELPER_PATH))


### Creation of the virtual environment.
$(VIRTUAL_ENVIRONMENT_PATH): $(PYENV_ENVIRONMENT_PATH)
	eval "$$(pyenv init -)" && \
	pyenv activate $(PYENV_ENVIRONMENT_NAME) && \
	python3 -m venv $(VIRTUAL_ENVIRONMENT_PATH) && \
	source $(VIRTUAL_ENVIRONMENT_PATH)/bin/activate && \
	python --version && \
	pip install pytest


### Creation of the belaster environment with the proper version of Python.
$(PYENV_ENVIRONMENT_PATH):
	eval "$$(pyenv init -)" && \
	pyenv virtualenv $(PYTHON_VERSION) $(PYENV_ENVIRONMENT_NAME) && \
	pyenv activate $(PYENV_ENVIRONMENT_NAME) && \
	python --version



## Run the tests.
## Assumes the dev env is setup.
## Adding the dependency to the dev env setup (ie target dev-env) would
## add noise since the target dev-env tries to recreate the symlinks whenever
## the source code changes.
.PHONY: test
test: dev-env
	source $(VIRTUAL_ENVIRONMENT_PATH)/bin/activate && \
	pytest



## Clean the dev environment.
.PHONY: clean-dev-env
clean-dev-env: clean-virtual-env clean-pyenv-virtualenv


.PHONY: clean-virtual-env
clean-virtual-env:
	rm -rf $(VIRTUAL_ENVIRONMENT_PATH)


.PHONY: clean-pyenv-virtualenv
clean-pyenv-virtualenv:
	pyenv virtualenv-delete --force $(PYENV_ENVIRONMENT_NAME)
