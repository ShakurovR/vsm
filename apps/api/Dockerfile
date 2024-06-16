# syntax = docker/dockerfile:experimental
#FROM python:3.11
FROM nvidia/cuda:12.0.0-cudnn8-devel-ubuntu22.04

ENV PIP_ROOT_USER_ACTION=ignore
ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && apt-get install python3-pip git libpq-dev -y

WORKDIR /app
COPY ./req.txt /app/req.txt
RUN --mount=type=cache,target=/root/.cache/pip pip install -r /app/req.txt
COPY ./ /app
EXPOSE 9000

CMD ["python3", "/app/main.py"]
