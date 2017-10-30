#!/bin/bash

NAME="bigday"                                                              # Name of the application
DJANGODIR=/home/ec2-user/wedding/django-wedding-website                 # Django project directory
SOCKFILE=/home/ec2-user/wedding/django-wedding-website/gunicorn.sock      # we will communicte using this unix socket
USER=ec2-user                                                                # the user to run as
GROUP=ec2-user                                                             # the group to run as
NUM_WORKERS=3                                                             # how many worker processes should Gunicorn spawn
DJANGO_SETTINGS_MODULE=bigday.settings                                     # which settings file should Django use
DJANGO_WSGI_MODULE=bigday.wsgi                                             # WSGI module name

echo "Starting $NAME as `whoami`"

# Activate the virtual environment
cd $DJANGODIR

# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec gunicorn ${DJANGO_WSGI_MODULE}:application \
  --name $NAME \
  --workers $NUM_WORKERS \
  --bind=unix:$SOCKFILE \
  --user=$USER --group=$GROUP \
  --log-level=debug \
  --log-file=-
