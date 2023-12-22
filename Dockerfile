# Grab the latest alpine image
FROM python:3.10

# maintainer stuff
LABEL maintainer='fabriziomiano@gmail.com'

# Copy the project code into the container
WORKDIR /covidashit
COPY . .

# Upgrade pip to the latest version
RUN pip install --upgrade pip && \
	pip install -r requirements.txt

# Run Application
CMD gunicorn --bind 0.0.0.0:$PORT wsgi:app
