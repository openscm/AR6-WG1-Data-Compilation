.DEFAULT_GOAL := help

CONDA_ENV_YML=environment.yml


ifndef CONDA_PREFIX
$(error Conda environment not active. Activate your conda environment before using this Makefile.)
else
ifeq ($(CONDA_DEFAULT_ENV),base)
$(error Do not install to conda base environment. Activate a different conda environment and rerun make. A new environment can be created with e.g. `conda create --name ar6-wg1-data-compilation`.))
endif
VENV_DIR=$(CONDA_PREFIX)
endif


PYTHON=$(VENV_DIR)/bin/python


define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT


.PHONY: help
help:  ## show help messages for all targets
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

.PHONY: format
format: black isort ## auto-format the code

.PHONY: black
black: $(VENV_DIR)  ## apply black formatter
	$(VENV_DIR)/bin/black --exclude _version.py setup.py src tests

.PHONY: isort
isort: $(VENV_DIR)  ## format the code
	$(VENV_DIR)/bin/isort src tests setup.py

.PHONY: setup
setup: conda-environment  ## setup environment for running


.PHONY: conda-environment
conda-environment:  $(VENV_DIR)  ## make conda environment


$(VENV_DIR): $(CONDA_ENV_YML)
	$(CONDA_EXE) env update --name $(CONDA_DEFAULT_ENV) -f $(CONDA_ENV_YML)
	$(VENV_DIR)/bin/pip install -e .
	touch $(VENV_DIR)
