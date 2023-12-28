# Define PROJECT_DIR variable to get the directory of the Makefile
this := $(word $(words $(MAKEFILE_LIST)),$(MAKEFILE_LIST))
PROJECT_DIR := $(dir $(this))

# Target to display help message
help:
	@echo "Make targets:"
	@echo "============="
	@awk '/^[a-zA-Z_-]+:.*?## / {split($$0, N, ":.*?## "); printf "%-20s %s\n", N[1], N[2]}' $(MAKEFILE_LIST) | sort


install: ## Install Python dependencies needed for the tests
	@echo "Installing Python packages..."
	pip install -r src/requirements.txt



load-test: ## Run the load testing script
	@echo "Running load tests on the Kubernetes application..."
	python src/load_test.py


resilience-test: ## Run the resilience testing script
	@echo "Running resilience tests on the Kubernetes application..."
	python src/resilience_test.py


clean: ## Clean up .pyc files and __pycache__ directories
	@echo "Cleaning up Python bytecode..."
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -exec rm -rf {} +