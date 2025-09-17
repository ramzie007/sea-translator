# Makefile for SEA-LION Translator

.PHONY: run test lint docker-build docker-run

run:
	python translate_sealion.py --target-language indonesian --output translated.txt

test:
	pytest tests/

format:
	black translate_sealion.py helpers.py tests/

lint:
	flake8 translate_sealion.py helpers.py tests/

docker-build:
	docker build -t sealion-translator .

docker-run:
	docker run --env-file .env -v $(PWD):/app sealion-translator
