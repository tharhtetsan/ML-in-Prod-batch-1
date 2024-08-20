from airflow import DAG
from airflow.providers.google.cloud.sensors.gcs import GCSObjectsWithPrefixExistenceSensor
from datetime import datetime


DESTINATION_BUCKET_NAME = 'ths_ml_in_prod_batch_1'
FILE_NAME = "airflow_test/"


default_args = {
    'start_date': datetime(2023, 1, 1),
}

with DAG(
    'gcs_object_update_sensor_dag',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False,
) as dag:

    check_exist_file = GCSObjectsWithPrefixExistenceSensor(
        bucket='ths_ml_in_prod_batch_1',  # No 'gs://'
        prefix='airflow_test/',  # Prefix should not contain wildcards
        task_id='gcs_object_prefix_exist_sensor_task',
        poke_interval=60,
        timeout=60 * 6,
    )
