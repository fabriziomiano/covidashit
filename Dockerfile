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

# This is only for testing purposes: "EXPOSE" is NOT supported by Heroku
#EXPOSE 5000

# This is only for testing purposes: $PORT is set by Heroku
#ENV PORT 5000

# Run the app.  CMD is required to run on Heroku
CMD gunicorn --bind 0.0.0.0:$PORT wsgi:app
