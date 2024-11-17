FROM python:3.11.4

ENV IS_DOCKER=true

RUN chmod 755 .

RUN pip install "poetry==1.6.1"

COPY poetry.lock pyproject.toml /code/

WORKDIR /app
COPY poetry.lock pyproject.toml /app/

RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

RUN poetry
COPY . /app

CMD ["python", "app.py"]
