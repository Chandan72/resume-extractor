# Makefile for Resume Data Extractor

.PHONY: help install test clean run lint format

help:
	@echo "Available commands:"
	@echo "  install    - Install dependencies"
	@echo "  test       - Run tests"
	@echo "  clean      - Clean up generated files"
	@echo "  run        - Run the extractor"
	@echo "  lint       - Run linting"
	@echo "  format     - Format code"

install:
	python -m pip install --upgrade pip
	pip install -r requirements.txt

test:
	python -m pytest tests/ -v

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -f *.log

run:
	python main.py

lint:
	pylint src/ tests/

format:
	black src/ tests/ main.py
	isort src/ tests/ main.py

dev-install:
	pip install -e .[dev]

build:
	python setup.py sdist bdist_wheel