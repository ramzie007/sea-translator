# Dockerfile for SEA-LION Translator
FROM python:3.11-slim

WORKDIR /app

COPY translate_sealion.py ./
COPY helpers.py ./
COPY requirements.txt ./
COPY .env.example ./.env

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "translate_sealion.py", "--help"]
ENTRYPOINT ["python", "translate_sealion.py"]