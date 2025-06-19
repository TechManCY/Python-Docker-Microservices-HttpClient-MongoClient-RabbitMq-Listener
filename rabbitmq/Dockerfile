FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /rabbitmq

# Copy the current directory contents into the container at /app
COPY . /rabbitmq

RUN pip install pika

CMD ["python", "consumer.py"]