.ONESHELL:		# ← very important – all lines in one shell

.DEFAULT_GOAL := help

VENV      ?= .venv
PYTHON    ?= $(VENV)/bin/python
PIP       ?= $(VENV)/bin/pip
PYTEST    ?= $(VENV)/bin/pytest

.PHONY: help
help:           ## Show this help message
	@echo "Usage: make <target>"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

# Install Python, PIP, & LaTeX requirements
# pip install pip-upgrade-all

# Generate a list of installed packages and upgrade them at once
.PHONY: upgrade-all-safe
upgrade-all-safe: ## Upgrades all Python packages with PIP
	. .venv/bin/activate
	pip-upgrade-all

# Build Poomsae Pro Database
.PHONY: poomsaepro-build
poomsaepro-build: ## Builds Poomsae Pro database
	. $(VENV)/bin/activate
	python PoomsaeProConnector/PoomsaeProConnection.py
	@echo "Running all .py files in PoomsaeProConnector/DataCorrection/ ..." 
	@for f in PoomsaeProConnector/DataCorrection/*.py; do \
		[ -f "$$f" ] || continue; \
		echo "────────────────────────────────────────"; \
		echo "→ $$(basename "$$f")"; \
		echo "────────────────────────────────────────"; \
		python "$$f" || echo "(exited with $$?)"; \
		echo ""; \
	done
	@echo "────────────────────────────────────────"
	@echo "Done."
		@echo "Running all .py files in PoomsaeProConnector/Custom/ ..."
	@for f in PoomsaeProConnector/Custom/*.py; do \
		[ -f "$$f" ] || continue; \
		echo "────────────────────────────────────────"; \
		echo "→ $$(basename "$$f")"; \
		echo "────────────────────────────────────────"; \
		python "$$f" || echo "(exited with $$?)"; \
		echo ""; \
	done
	@echo "────────────────────────────────────────"
	@echo "Done."
	python PoomsaeProConnector/PoomsaeProRefereeCreation.py

# Import Referee Data
.PHONY: referee-import
referee-import: ## Imports Referee data into database from Excel files
	. .venv/bin/activate
	python PoomsaeProConnector/PoomsaeProRefereeImport.py

.PHONY: poomsaepro-build-all
poomsaepro-build-all: poomsaepro-build referee-import ## Builds PoomsaePro Database and Imports referee data


# Runs the Referee Analysis Dashboard
.PHONY: dashboard
dashboard: ## Runs Referee Analysis Dashboard
	. .venv/bin/activate
	python -m RefereeAnalysis.dashboard

# Single Elimination Consistency
.PHONY: single-elmin
single-elmin: ## Runs Single Elimination Consistency
	. .venv/bin/activate
	python SingleEliminationConsistency.py

# Chung Sequential Advantage
.PHONY: chung-adv
chung-adv: ## Runs Chung Sequential Advantage
	. .venv/bin/activate
	python -m ChungSequentialAdvantage.dashboard

#python ChungSequentialAdvantage.py

.PHONY: chung-adv-pair
chung-adv-pair: ## Runs Chung Sequential Advantage
	. .venv/bin/activate
	python ChungSequentialAdvantage-PairTeam.py

# LaTeX build all Assignment & Eval Sheets
.PHONY: build-forms
build-forms: ## Build all LaTeX forms (TBD)