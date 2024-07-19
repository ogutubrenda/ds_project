FROM python:3.8-slim

WORKDIR /app

COPY load_balancer.py consistent_hash.py /app/

RUN pip install flask docker

CMD [ "python", "./app.py", "&", "python", "./load_balancer.py" ]
