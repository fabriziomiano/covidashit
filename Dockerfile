#Grab the latest alpine image
FROM python:3.8

# Add requirements and install dependencies
ADD ./requirements.txt /tmp/requirements.txt
RUN pip3 install --upgrade pip && \
    pip3 install --no-cache-dir -q -r /tmp/requirements.txt

# Add our code
ADD . /opt/app/
WORKDIR /opt/app

# Uncomment for development purposes only as $PORT is automatically set by Heroku
ENV PORT 5000

# Run the app.  CMD is required to run on Heroku
# crate the collections on DB before running the gunicorn server
CMD python3 -m flask create-collections && \
    gunicorn --bind 0.0.0.0:$PORT wsgi:app
