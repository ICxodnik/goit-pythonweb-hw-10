# Вибираємо базовий образ
FROM python:3.13-slim

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml poetry.lock README.md ./

RUN poetry config virtualenvs.create false && poetry install --only=main --no-interaction --no-ansi

COPY . .

ENV PYTHONPATH=/app

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
