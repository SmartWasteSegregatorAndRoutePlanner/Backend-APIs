# DESCRIPTION:	  Deploys Backend-APIs repo in Container
# AUTHOR:		  Dhrumil Mistry <contact@dmdhrumilmistry.tech>
# COMMENTS:
#	This file describes how to deploy Backend-APIs
#	in a container with all dependencies installed.
# USAGE:
#	# Download googlephish Dockerfile
#	wget [link]
#
#	# Build image
#	docker build -t swsrp-backend-api .
#
#   # run docker container
#	docker run -d -p 8000:8000 swsrp-backend-api
#

# choose baseimage
FROM python:3.10

# set initial Working Directory
WORKDIR /

# create project directory and set as workding directory
ENV PROJ_DIR="/Backend-APIs"
RUN [ -d ${PROJ_DIR} ] || mkdir -p ${PROJ_DIR}
WORKDIR ${PROJ_DIR}

# copy project files
COPY . .

# add current directory to python path
ENV PYTHONPATH=${PYTHONPATH}:${PWD}

# install requirements
RUN python -m pip install gunicorn
RUN python -m pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-root --only main

# check for errors in application
RUN python manage.py check

# migrate database
RUN python manage.py makemigrations
RUN python manage.py migrate

# collect static images
# RUN python manage.py collectstatic

# get build arguments (credentials)
ARG dj_email=admin@localhost
ARG dj_username=admin
ARG dj_password=admin
ARG dj_allowed_host=*

# create superuser
ENV DJANGO_SUPERUSER_EMAIL=${dj_email}
ENV DJANGO_SUPERUSER_USERNAME=${dj_username}
ENV DJANGO_SUPERUSER_PASSWORD=${dj_password}
ENV ALLOWED_HOSTS=${dj_allowed_host}
RUN python manage.py createsuperuser --noinput

# expose ports
EXPOSE 8000

# start application
CMD [ "gunicorn", "backend_api.wsgi", "-b", "0.0.0.0:8000" ]