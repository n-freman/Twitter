FROM python:3.11

WORKDIR /code

RUN pip install poetry
COPY poetry.lock pyproject.toml /code/
RUN poetry config virtualenvs.create false
RUN poetry install --no-root

COPY . /code/
