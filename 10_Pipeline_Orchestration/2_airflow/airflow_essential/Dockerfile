FROM apache/airflow:2.10.2-python3.12

USER root

COPY requirements.txt .

RUN apt-get update

USER airflow

RUN pip install -r requirements.txt