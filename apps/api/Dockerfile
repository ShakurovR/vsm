# syntax = docker/dockerfile:experimental
FROM python:3.11
WORKDIR /app
COPY ./req.txt /app/req.txt
RUN --mount=type=cache,target=/root/.cache/pip pip install -r /app/req.txt
COPY ./ /app
EXPOSE 9000

CMD ["python", "/app/main.py"]