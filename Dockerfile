FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src ./src/

WORKDIR /app/src

ENV IP_ADDR=localhost

RUN python setup.py build_ext --inplace

CMD ["python", "main.py"]