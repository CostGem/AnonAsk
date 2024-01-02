# base image with python
FROM python:3.11.4

ENV IS_DOCKER=docker

RUN chmod 755 .

RUN pip install "poetry==1.6.1"

COPY poetry.lock pyproject.toml /code/

WORKDIR /app
COPY poetry.lock pyproject.toml /app/

RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

RUN poetry
COY . /app

CMD ["python", "/app/src/main.py"]
