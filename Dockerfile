FROM python:3.9.10-alpine3.15 as build-image

RUN apk add --update --no-cache git

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /app

RUN pip install --upgrade pip
COPY requirements.txt setup.py README.md ./
COPY src src
RUN pip install -r requirements.txt
RUN pip install .

##############################################################################

FROM python:3.9.10-alpine3.15 as run-image
ENV PYTHONUNBUFFERED 1
ENV TZ=UTC

COPY --from=build-image /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

ENTRYPOINT [ "e2c", "-vvv" ]
