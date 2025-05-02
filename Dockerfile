FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src ./src/

WORKDIR /app/src

ENV IP_ADDR=localhost

CMD ["python", "main.py"]