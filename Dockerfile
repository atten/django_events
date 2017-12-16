FROM python:3.6.3-stretch

RUN apt-get update && apt-get --assume-yes upgrade && pip3 install wheel


ENV BUILD_DEPS \
    build-essential \
    libpq-dev

ENV RUN_DEPS \
    libpq5 \
    git-core 

RUN apt-get install --no-install-recommends --assume-yes ${BUILD_DEPS} ${RUN_DEPS}

WORKDIR /application/django_events
ADD requirements.txt /application/django_events
ADD requirements /application/django_events/requirements

RUN pip install --no-cache-dir -r requirements.txt --src /usr/local/src

# ====================== REMOVE ======================
RUN apt-get remove --purge --assume-yes $BUILD_DEPS

# move it on the top of Dockerfile when it'll be ready
ENV UNWANTED_PACKAGES \
    python2.7 \
    python2.7-minimal \
    python3.5 \
    python3.5-minimal

RUN apt-get remove --purge --assume-yes $UNWANTED_PACKAGES
RUN apt-get autoremove --assume-yes
RUN apt-get autoclean && apt-get clean

# ====================================================

ADD . /application/django_events

# create static && media to prevent root owning of the static volume
# https://github.com/docker/compose/issues/3270#issuecomment-206214034
RUN mkdir /application/log \
  && mkdir /application/run \
  && mkdir /application/django_events/static \
  && mkdir /application/django_events/media \
  && adduser --uid 1000 --home /application --disabled-password --gecos "" django_events \
  && chown -hR django_events: /application


USER django_events

ENV DOCKERIZED=1
ENV PYTHONUNBUFFERED=1

EXPOSE 8000
ENTRYPOINT ["python", "manage.py"]
CMD ["runuwsgi"]
