from airflow.decorators import dag, task
from airflow.sensors.filesystem import FileSensor
from datetime import datetime
import os

@dag(dag_id="v10_sensor_local_file_exist",schedule="@daily",
     start_date=datetime(2024,9,10),tags=['sensors'],catchup=False)
def check_folder():
    
    wait_for_files = FileSensor.partial(
        task_id="wait_for_files",
        fs_conn_id = "fs_default",
    ).expand(
        filepath = ["data_1.csv","data_2.csv","data_3.csv"]
    )

    @task
    def process_file():
        path = os.getcwd()+"/include"
        print("process_file : ",os.listdir(path))



    wait_for_files >> process_file()

check_folder()