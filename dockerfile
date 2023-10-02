# Use an official Python runtime as the base image
FROM python:3.11-alpine

# Set the working directory in the container
WORKDIR /app

# Set environment variables
# - Prevents Python from writing pyc files to disc
# - Prevents Python from buffering stdout and stderr
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /app/requirements.txt

# Install system dependencies (you can add any other system dependencies you might have)
RUN set -eux \
    && apk add --no-cache --virtual .build-deps build-base \
        openssl-dev gcc python3-dev libpq-dev \
    && pip install --upgrade pip setuptools wheel \
    && pip install -r /app/requirements.txt \
    && rm -rf /root/.cache/pip

# Copy the current directory contents into the container
COPY . /app

# Define the default command to run when starting the container
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--log-config", "logging-config.yml", "--reload"]
