from airflow import DAG
from airflow.operators.python import PythonOperator
import pendulum
import requests

def _transform(ti):
   
   resp = requests.get('https://swapi.dev/api/people/1').json()
   print(resp)
   my_character = {}
   my_character["height"] = int(resp["height"]) - 20
   my_character["mass"] = int(resp["mass"]) - 50
   my_character["hair_color"] = "black" if resp["hair_color"] == "blond" else "blond"
   my_character["eye_color"] = "hazel" if resp["eye_color"] == "blue" else "blue"
   my_character["gender"] = "female" if resp["gender"] == "male" else "female"
   ti.xcom_push("character_info", my_character)


def _load(ti):
   print(ti.xcom_pull(key = 'character_info',task_ids = '_transform'))


with DAG('xcoms_demo1',schedule = None,start_date = pendulum.datetime(2024,8,18),
   catchup = False):

   t1 = PythonOperator(task_id = '_transform',python_callable = _transform)
   t2 = PythonOperator(task_id = 'load', python_callable = _load)


t1 >> t2