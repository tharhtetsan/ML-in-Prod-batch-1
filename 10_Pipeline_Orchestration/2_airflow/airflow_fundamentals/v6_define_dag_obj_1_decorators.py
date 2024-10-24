from airflow.decorators import dag,task
from datetime import datetime


@dag("v6_define_dag_obj_1_decorators", start_date=datetime(2024,8,12), 
        description="This is a hello world pipeline", tags=["hello"],
        schedule='@daily',catchup=False)
@task
def print_a():
    print("hello from task a")

@task
def print_b():
    print("hello from task b")

print_a()
print_b()