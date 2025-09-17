# Makefile for SEA-LION Translator

.PHONY: run install test lint

install:
	pip install -r requirements.txt
	pip install -r dev-requirements.txt

run:
	python translate_sealion.py --target-language indonesian --output translated.txt

test:
	pytest tests/

format:
	black translate_sealion.py helpers.py

lint:
	flake8 translate_sealion.py helpers.py