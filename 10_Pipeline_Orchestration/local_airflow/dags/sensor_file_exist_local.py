from airflow.decorators import dag, task
from airflow.sensors.filesystem import FileSensor
from datetime import datetime

@dag(
    dag_id= 'sensor_files_exist_local',
    schedule='@daily',
    start_date=datetime(2023, 1, 1),
    tags=['sensor'],
    catchup=False
)
def first_dag():

    wait_for_files = FileSensor.partial(
        task_id='wait_for_files',
        fs_conn_id='fs_default',
    ).expand(
        filepath=['data_1.csv', 'data_2.csv', 'data_3.csv']
    )

    @task
    def process_file():
        print("I processed the file!")

    wait_for_files >> process_file()

first_dag()