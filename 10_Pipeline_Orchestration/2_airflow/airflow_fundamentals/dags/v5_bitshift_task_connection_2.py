from airflow import DAG
from datetime import datetime
from airflow.operators.python import PythonOperator

def print_a():
    print("hello from task a")

def print_b():
    print("hello from task b")

def print_c():
    print("hello from task c")

def print_d():
    print("hello from task d")

def print_e():
    print("hello from task e")



with DAG("v5_bitshift_task_connection_2", start_date=datetime(2024,8,12), 
        description="This is a hello world pipeline", tags=["hello"],
        schedule='@daily',catchup=False ):

    task_a = PythonOperator(task_id="task_a", python_callable=print_a)
    task_b = PythonOperator(task_id="task_b", python_callable=print_b)
    task_c = PythonOperator(task_id="task_c", python_callable=print_c)
    task_d = PythonOperator(task_id="task_d", python_callable=print_d)
    task_e = PythonOperator(task_id="task_e", python_callable=print_e)


task_a >> [task_b,task_c] >> task_d
task_a >> [task_b,task_c] >> task_e

