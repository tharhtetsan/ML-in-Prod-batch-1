from airflow.decorators import dag, task
from datetime import datetime, timedelta
from airflow.utils.dates import days_ago
import time

default_args ={
    'owner' : 'tharhtet',
    'retries': 1,
    'retry_delay': timedelta(minutes=2)
}



@dag(
    dag_id='dag_ddecorators_and_task_flow',
    default_args=default_args,
    description='This is the example of using : dag_decorators, task_flow, timedelta, days_ago',
    start_date=days_ago(0),# would start 2 days ago at 00:15
    max_active_runs=1,
    schedule_interval=timedelta(days=1)
)
def dag_ddecorators_and_task_flow():
    @task
    def _give_a_name():
        name = 'Thar Htet'
        time.sleep(30)
        return name

    @task
    def _give_a_value():
        value = 89
        return value
    
    @task
    def print_method(name, value):
        str_out = "Elden Lord Name : {}, Level : {}".format(name,value)
        print(str_out)
        return str_out
    
    _name = _give_a_name()
    _value = _give_a_value()
    result = print_method(_name,_value)

dag_ddecorators_and_task_flow_obj = dag_ddecorators_and_task_flow()