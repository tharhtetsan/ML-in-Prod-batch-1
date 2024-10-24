from airflow import DAG
from datetime import datetime
from datetime import timedelta
import time 
from airflow.operators.python import PythonOperator




def print_a():
    time.sleep(3)
    print("hello from task a")

def print_b():
    time.sleep(1)
    print("hello from task b")


with DAG("v8_airflow_schedule_2", start_date=datetime(2024,9,11), 
        description="This is a about scheduler", tags=["scheduler"],
        schedule=timedelta(minutes=2),catchup=False ):

    task_a = PythonOperator(task_id="task_a", python_callable=print_a)
    task_b = PythonOperator(task_id="task_b", python_callable=print_b)

task_a >> task_b
  