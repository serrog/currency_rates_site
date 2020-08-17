# pull official base image
FROM python:3.8.3

# Update system and install packages.
RUN apt-get update -y && apt-get install -y --no-install-recommends \
    python-psycopg2

# set work directory
WORKDIR /usr/src/currency_rates

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY requirements.txt ./
RUN pip install -r requirements.txt

# copy project
COPY . .