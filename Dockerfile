#Grab the latest alpine image
FROM alpine:latest

# Install python and pip
RUN apk add --no-cache --update python3 py3-pip bash
ADD ./requirements.txt /tmp/requirements.txt

# Install dependencies
RUN pip3 install --upgrade pip \
    && pip3 install --no-cache-dir -q -r /tmp/requirements.txt

# Add our code
ADD . /opt/app/
WORKDIR /opt/app

# This is only for testing purposes as $PORT is automatically set by Heroku
#ENV PORT 5000

# Environment variables that need to be set locally
# to retrieve the bar-chart races from mongoDB
#ENV COLLECTION_NAME changeme
#ENV MONGO_URI changeme

# Run the app.  CMD is required to run on Heroku
CMD gunicorn --bind 0.0.0.0:$PORT wsgi:app
