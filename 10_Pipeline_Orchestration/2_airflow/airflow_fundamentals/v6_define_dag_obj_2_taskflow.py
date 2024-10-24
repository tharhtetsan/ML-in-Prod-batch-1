from airflow.decorators import dag,task
from datetime import datetime


@dag("v6_define_dag_obj_2_taskflow", start_date=datetime(2024,8,12), 
        description="This is a hello world pipeline", tags=["hello"],
        schedule='@daily',catchup=False)

def parent_task():
    @task
    def print_a():
        print("hello from task a")
        return 9999

    @task
    def print_b(temp):
        print("hello from task b")
        print(temp)
    
    temp = print_a()
    print_b(temp)


parent_task()