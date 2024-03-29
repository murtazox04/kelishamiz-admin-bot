FROM python:3.10-alpine

RUN pip install --upgrade pip

COPY ./poetry.lock ./pyproject.toml ./
RUN pip install poetry
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

COPY . /app

WORKDIR /app

CMD [ "poetry", "run", "uvicorn", "main:app", "--port=8080", "--reload" ]