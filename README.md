# SEA-LION Translator

A Python tool to translate English text (e.g., Project Gutenberg books) into Southeast Asian languages using the SEA-LION API.

## Features
- Translates to Indonesian, Filipino, Tamil, Thai, or Vietnamese
- Typer CLI app with rich progress output
- Loads API key from `.env` (python-dotenv)
- Parallel translation for speed
- Bilingual output option (English + translation)
- Sentence chunking for better translation
- Docker support
- Makefile for common tasks
- Pytest tests

## Requirements
- Python 3.11
- See `requirements.txt` and `dev-requirements.txt`

## Setup
Clone the repository:
```sh
git clone https://github.com/ramzie007/sea-lion-translator.git
cd sea-lion-translator
```
Install dependencies:
```sh
pip install -r requirements.txt
pip install -r dev-requirements.txt
```
Set environment variables:
- `SEA_LION_API_KEY`: API key for SEA-LION translation
- You can use a `.env` file or export them in your shell.

## Usage
Run the main script:
```sh
python translate_sealion.py --target-language thai --output translated.txt
```
See all options:
```sh
python translate_sealion.py --help
```

## Docker
You can run this app in a Docker container:

Build the Docker image:
```sh
docker build -t sealion-translator .
```
Run the container (mount your current directory and set your API key):
```sh
docker run --env-file .env -v "$PWD":/app sealion-translator --target-language thai --output /app/translated.txt
```
This will write the output file to your current directory.

## Development
Use the provided Makefile for common tasks:
```sh
make install   # Install dependencies
make lint      # Lint code with flake8
make format    # Format code with black
make test      # Run tests
make all       # Run all
```

## Testing & CI
- Formatting and linting are enforced via Black and Flake8
- GitHub Actions CI runs on every push and PR

## License
MIT