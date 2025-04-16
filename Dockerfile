FROM python:3.13
COPY requirements.txt /
RUN pip install -r requirements.txt

COPY src/app_collector_local.py /src/
WORKDIR /src

USER otel_collector

CMD ["python", "app_collector_local.py"]