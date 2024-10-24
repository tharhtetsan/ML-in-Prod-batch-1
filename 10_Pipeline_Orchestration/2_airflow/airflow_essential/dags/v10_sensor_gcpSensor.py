from airflow.providers.google.cloud.sensors.gcs import GCSObjectUpdateSensor,GCSObjectExistenceSensor,GCSObjectsWithPrefixExistenceSensor

from datetime import datetime
from airflow.operators.python import PythonOperator
from airflow import DAG
import os

DESTINATION_BUCKET_NAME = 'mlflow_ths_server'
FILE_NAME = "airflow_test/winequality-white.csv"

#/opt/airflow/dags/service_account/service_account.json
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.getcwd()+"/dags/service_account/service_account.json"



#https://airflow.apache.org/docs/apache-airflow-providers-google/stable/_api/airflow/providers/google/cloud/sensors/gcs/index.html#airflow.providers.google.cloud.sensors.gcs.GCSObjectsWithPrefixExistenceSensor


def _print_env():
    print(os.getenv('GOOGLE_APPLICATION_CREDENTIALS'))
    return os.getenv('GOOGLE_APPLICATION_CREDENTIALS')


def file_changes():
    print(".....New Machine Learning model is released......")

    return "File Changes"

with DAG(
    dag_id='gcs_object_update_sensor_task',
    schedule=None,
    start_date=datetime(2024,8,12),
    tags=['gcp']
):
 
    check_update_file = GCSObjectUpdateSensor(
            bucket=DESTINATION_BUCKET_NAME,
            object=FILE_NAME,
            task_id="gcs_object_update_sensor_task",
            poke_interval=60,  # Check every minute
            timeout=60 * 60,   # Timeout after 1 hour
    )


    check_exist_file = GCSObjectExistenceSensor(
            bucket=DESTINATION_BUCKET_NAME,
            object="airflow_test/",
            task_id="gcs_object_exist_sensor_task",
            poke_interval=60,  # Check every minute
            timeout=60 * 60,   # Timeout after 1 hour
    )


    check_update_folder = GCSObjectsWithPrefixExistenceSensor(
                bucket=DESTINATION_BUCKET_NAME,
                prefix="airflow_test/winequality-white",
                task_id="gcs_object_update_folder_sensor_task",
                poke_interval=60,  # Check every minute
                timeout=60 * 60,   # Timeout after 1 hour
        )
    
    

    task_a = PythonOperator(task_id ='task_a', python_callable=_print_env)

    task_b = PythonOperator(task_id ='task_b', python_callable=file_changes)

check_update_file
task_a >> check_update_folder >> task_b
task_a >> check_exist_file >> task_b