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

# Expose is NOT supported by Heroku
#EXPOSE 5000

# Set Europe/Rome Timezone
ENV TZ=Europe/Rome
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get install -y tzdata && dpkg-reconfigure -f noninteractive tzdata

# Run the image as a non-root user
RUN useradd -m myuser
USER myuser

# Run the app.  CMD is required to run on Heroku
# $PORT is set by Heroku
#ENV PORT 5000
CMD gunicorn --bind 0.0.0.0:$PORT wsgi:app
