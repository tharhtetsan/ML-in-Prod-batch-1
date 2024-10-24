from airflow.providers.google.cloud.sensors.gcs import GCSObjectUpdateSensor
from datetime import datetime
from airflow.operators.python import PythonOperator
from airflow import DAG
import os

DESTINATION_BUCKET_NAME = 'ths_ml_in_prod_batch_1'
FILE_NAME = "airflow_test/sample_vehicle_history.csv"

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.getcwd()+"/dags/service_account/service_account.json"

def _print_env():
    print(os.getenv('GOOGLE_APPLICATION_CREDENTIALS'))
    return os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

with DAG(
    dag_id='gcs_object_update_sensor_task',
    schedule=None,
    start_date=datetime(2024,8,12),
    tags=['gcp']
):
 
    check_exist_file = GCSObjectUpdateSensor(
            bucket=DESTINATION_BUCKET_NAME,
            object=FILE_NAME,
            task_id="gcs_object_update_sensor_task",
            poke_interval=60,  # Check every minute
            timeout=60 * 60,   # Timeout after 1 hour
    )

    task_a = PythonOperator(task_id ='task_a', python_callable=_print_env)
task_a >> check_exist_file