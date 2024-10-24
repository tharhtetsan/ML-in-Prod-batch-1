from airflow import DAG
from datetime import datetime
from airflow.operators.python import PythonOperator

def print_a():
    print("hello from task aaa")

def print_b():
    print("hello from task bbb")


with DAG("helloworld", start_date=datetime(2024,8,12), 
        description="This is a hello world pipeline", tags=["hello"],
        schedule='@daily',catchup=False ):

    task_a = PythonOperator(task_id="task_a", python_callable=print_a)
    task_b = PythonOperator(task_id="task_b", python_callable=print_b)
    
task_a >> task_b