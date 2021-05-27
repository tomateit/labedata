FROM python:3.8.3-slim

WORKDIR /code

ENV POETRY_VERSION="1.1.4"

RUN pip install poetry==$POETRY_VERSION

RUN poetry config virtualenvs.create false

COPY poetry.lock pyproject.toml /code/  

RUN poetry install --no-interaction --no-ansi

COPY . /code

#Run the container
ENV FLASK_APP=wsgi.py
RUN flask init-db
CMD [ "flask", "run" ]