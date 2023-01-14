# syntax=docker/dockerfile:1

# Which environment you use?
FROM python:3.9

# Set work directory
WORKDIR /app

# set environment variables
ENV PYTHONUNBUFFERED 1
ENV DOCKER true

COPY requirements.txt /app
RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir -r requirements.txt

# copy project
COPY . /app

ENTRYPOINT ["python3"]
CMD ["app.py"]