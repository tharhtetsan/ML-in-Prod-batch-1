from airflow import DAG
from datetime import datetime
from airflow.models import Variable
from airflow.sensors.python import PythonSensor


def _condition():
    api_token = Variable.get("API_TOKEN")
    if api_token == "123456":
        return True
    return False



with DAG(dag_id="v10_sensor_PythonSensor", schedule="@daily",
        start_date=datetime(2024,9,10), catchup=False,tags=["sensors","variable"]):
        wait_for_condition = PythonSensor(
            task_id = "wait_for_condition",
            python_callable = _condition,
            poke_interval=60,
            timeout = 24 * 60* 60
        )
        