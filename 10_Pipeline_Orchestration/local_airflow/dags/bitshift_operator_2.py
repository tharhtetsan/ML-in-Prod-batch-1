from airflow import DAG
from datetime import datetime
from airflow.operators.python import PythonOperator
from airflow.utils.helpers import chain



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


with DAG("bitshift_operator_2", start_date=datetime(2024,1,1),
        description="bitshift_operator_2 ", tags=["hello_world"],
        schedule='@daily', catchup=False):
        

    task_a = PythonOperator(task_id ='task_a', python_callable=print_a)
    task_b = PythonOperator(task_id ='task_b', python_callable=print_b)
    task_c = PythonOperator(task_id ='task_c', python_callable=print_c)
    task_d = PythonOperator(task_id ='task_d', python_callable=print_d)
    task_e = PythonOperator(task_id ='task_e', python_callable=print_d)

chain(task_a,[task_b,task_c],[task_e,task_d])
