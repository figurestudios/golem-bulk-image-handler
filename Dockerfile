FROM alpine:latest
RUN apk add python3-dev py3-pip zlib-dev jpeg-dev gcc musl-dev g++
RUN pip install --upgrade pip
RUN pip install Pillow
RUN pip install py7zr
VOLUME /golem/input
WORKDIR /golem/work