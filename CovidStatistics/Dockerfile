# syntax=docker/dockerfile:1
FROM python:3.8
ENV PYTHONUNBUFFERED=1
WORKDIR /code
ADD . /code
COPY requirements.txt /code/requirements.txt
RUN pip install -r requirements.txt
COPY . /code/
ENTRYPOINT ["sh", "/code/run.sh"]
