from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.models import Variable

from datetime import datetime

def _ml_task(ariflow_parameter):
    print(ariflow_parameter)


with DAG("airflow_variable", start_date=datetime(2024,8,1),
        schedule_interval='@daily', catchup=False) as dag:
        for _parameter in Variable.get('ML_MODEL_PARA',deserialize_json=True)["param"]:
            PythonOperator(
                task_id =f"ml_task_{_parameter}",
                python_callable=_ml_task,
                op_kwargs = {
                    'ariflow_parameter': _parameter
                }
            )
