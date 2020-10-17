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

# Database-related env vars: will need to be set on Heroku
ENV MONGO_URI changeme
ENV BAR_CHART_COLLECTION changeme
ENV NATIONAL_DATA_COLLECTION changeme
ENV REGIONAL_DATA_COLLECTION changeme
ENV PROVINCIAL_DATA_COLLECTION changeme
ENV LATEST_REGIONAL_DATA_COLLECTION changeme
ENV LATEST_PROVINCIAL_DATA_COLLECTION changeme

# Run the app.  CMD is required to run on Heroku
CMD gunicorn --bind 0.0.0.0:$PORT wsgi:app
