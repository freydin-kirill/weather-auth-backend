FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN python -m pip install --no-cache-dir poetry==2.1.2 \
    && poetry config virtualenvs.create false \
    && poetry install --without dev --no-interaction --no-ansi \
    && rm -rf $(poetry config cache-dir)/{cache,artifacts}

COPY . .

CMD ["python", "-m", "src.weather.weather_saver.consumer"]
