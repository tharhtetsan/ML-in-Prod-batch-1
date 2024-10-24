from airflow import DAG
from datetime import datetime
from airflow.operators.python import PythonOperator
import requests 

def _tranform(ti):
    xcom_data = requests.get('https://swapi.dev/api/people/1').json()
    ti.xcom_push("t_number", xcom_data)
    
def _load(ti):
    print(ti.xcom_pull(key='t_number',task_ids='_tranform'))


with DAG("v7_xcom_sample", start_date = datetime(2024,9,1), catchup = False):
    t1 = PythonOperator(task_id = "_tranform",python_callable=_tranform)
    t2 = PythonOperator(task_id = "_load",python_callable=_load)


t1 >> t2