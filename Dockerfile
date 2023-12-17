# Grab the latest alpine image
FROM python:3.10

# maintainer stuff
LABEL maintainer='fabriziomiano@gmail.com'

# Upgrade pip to the latest version
RUN pip install --upgrade pip poetry

# Install dependencies using poetry.lock file
COPY ./pyproject.toml ./poetry.lock /app/
WORKDIR /app

RUN poetry install --no-root

# Copy the project code into the container
COPY . .

# Start the application
CMD python3 -m flask createdb && gunicorn --bind 0.0.0.0:$PORT wsgi:app
