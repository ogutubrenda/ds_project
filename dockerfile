FROM python:3.9-slim

WORKDIR /app
COPY . /app

RUN pip install flask

CMD ["python", "load_balancer.py"]
