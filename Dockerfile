#Grab the latest alpine image
FROM python:3.8

# Add requirements and install dependencies
ADD ./requirements.txt /tmp/requirements.txt
RUN pip3 install --upgrade pip && \
    pip3 install --no-cache-dir -q -r /tmp/requirements.txt

# Add our code
ADD . /opt/app/
WORKDIR /opt/app

# These are only for dev purpose as $PORT is automatically set by Heroku
#ENV PORT 5000
#ENV MONGO_URI changeme
#ENV NATIONAL_DATA_COLLECTION changeme
#ENV REGIONAL_DATA_COLLECTION changeme
#ENV PROVINCIAL_DATA_COLLECTION changeme
#ENV NATIONAL_TRENDS_COLLECTION changeme
#ENV REGIONAL_TRENDS_COLLECTION changeme
#ENV PROVINCIAL_TRENDS_COLLECTION changeme
#ENV REGIONAL_BREAKDOWN_COLLECTION changeme
#ENV PROVINCIAL_BREAKDOWN_COLLECTION changeme
#ENV NATIONAL_SERIES_COLLECTION changeme
#ENV REGIONAL_SERIES_COLLECTION changeme
#ENV PROVINCIAL_SERIES_COLLECTION changeme
#ENV GH_WEBHOOK_SECRET changeme
#ENV SECRET_KEY changeme

# Run the app.  CMD is required to run on Heroku
# crate the collections on DB before running the gunicorn server
CMD python3 -m flask create-collections && \
    gunicorn --bind 0.0.0.0:$PORT wsgi:app
