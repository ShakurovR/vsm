# syntax = docker/dockerfile:experimental
FROM  nvidia/cuda:11.7.1-devel-ubuntu22.04
ENV PIP_ROOT_USER_ACTION=ignore
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && apt-get install ffmpeg libpq-dev -y
RUN apt-get install software-properties-common wget -y
RUN add-apt-repository ppa:deadsnakes/ppa -y
RUN apt-get update
RUN apt-get install python3.10 python3.10-venv python3.10-dev sqlite3 libsqlite3-dev -y
RUN python3.10 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install wheel
WORKDIR /app
COPY ./uploader.txt /app/req.txt
RUN pip install pysqlite3-binary
RUN --mount=type=cache,target=/root/.cache/pip pip install -r /app/req.txt
COPY ./ /app
ENV PYTHONUNBUFFERED=1
CMD ["celery", "-A", "uploader", "worker", "--loglevel=info", "-Q", "uploader"]
# "--pool=solo", "--heartbeat-interval=3600"]
