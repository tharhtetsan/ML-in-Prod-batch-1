from airflow import DAG
from airflow.sensors.python import PythonSensor
from airflow.operators.python import PythonOperator
from datetime import datetime

def print_a():
    print("hello from task aa")

def _condition():
    return False

with DAG(
    dag_id="sensor",
    start_date=datetime(2023, 8, 12),
    schedule="@daily",
    catchup=False,
):
    waiting_for_condition = PythonSensor(
        task_id="waiting_for_condition",
        python_callable=_condition,
        poke_interval=60,
        timeout=60 * 2
    )
    task_a = PythonOperator(task_id ='task_a', python_callable=print_a)

"""
The Sensor checks  _condition to be true every 60 seconds by default (poke_interval). 
Since _condition always returns False, the Sensor will continue checking every 60 seconds 
until it times out after 120 seconds (2 * 60  ) by default(7 days = 7 * 24 * 60 * 60). When the Sensor times out, it is marked failed.
"""

task_a
