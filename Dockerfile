#Grab the latest alpine image
FROM ubuntu:18.04

# Install python and pip
RUN apt-get update && apt-get upgrade -y \
    && apt-get install -y python3-pip ffmpeg systemd dbus
ADD ./requirements.txt /tmp/requirements.txt

# Install dependencies
RUN pip3 install --upgrade pip \
    && pip3 install --no-cache-dir -q -r /tmp/requirements.txt

# Add our code
ADD . /opt/app/
WORKDIR /opt/app


# Set Europe/Rome Timezone
RUN ln -snf /usr/share/zoneinfo/Europe/Rome /etc/localtime && echo Europe/Rome > /etc/timezone
RUN apt-get install -y tzdata && dpkg-reconfigure -f noninteractive tzdata

# Run the image as a non-root user
RUN useradd -m myuser
USER myuser

# Run the app.  CMD is required to run on Heroku
# This is only for testing purposes: $PORT is set by Heroku
# This is only for testing purposes: "EXPOSE" is NOT supported by Heroku
#EXPOSE 5000
#ENV PORT 5000

CMD gunicorn --workers=3 --bind 0.0.0.0:$PORT wsgi:app
