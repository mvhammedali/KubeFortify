# Define PROJECT_DIR variable to get the directory of the Makefile
this := $(word $(words $(MAKEFILE_LIST)),$(MAKEFILE_LIST))
PROJECT_DIR := $(dir $(this))

# Target to display help message
help:
	@echo "Make targets:"
	@echo "============="
	@awk '/^[a-zA-Z_-]+:.*?## / {split($$0, N, ":.*?## "); printf "%-20s %s\n", N[1], N[2]}' $(MAKEFILE_LIST) | sort


# Install Python dependencies needed for the tests
install:
	@echo "Installing Python packages..."
	pip install -r src/requirements.txt


# Run the load testing script
load-test:
	@echo "Running load tests on the Kubernetes application..."
	python src/load_test.py

# Run the resilience testing script
resilience-test:
	@echo "Running resilience tests on the Kubernetes application..."
	python src/resilience_test.py

# Clean up .pyc files and __pycache__ directories
clean:
	@echo "Cleaning up Python bytecode..."
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -exec rm -rf {} +