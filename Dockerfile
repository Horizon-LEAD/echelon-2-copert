FROM python:3.9.10-alpine3.15 as build-image

WORKDIR /app

COPY requirements.txt setup.py README.md ./
COPY src src
RUN pip install --upgrade pip \
    && pip install -r requirements.txt \
    && pip install .

ENTRYPOINT [ "e2c", "-vvv" ]
