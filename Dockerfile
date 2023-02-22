FROM python:3.9.10-alpine3.15 as build-image

COPY requirements.txt setup.py README.md /srv/app/

RUN apk add --update --no-cache git \
    && pip install --upgrade pip \
    && pip install -r /srv/app/requirements.txt

COPY src /srv/app/src
RUN pip install /srv/app/

ENTRYPOINT [ "e2c", "-vvv" ]
