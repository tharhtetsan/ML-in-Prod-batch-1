from prefect import task, flow,Flow


@task
def extract(path):
    with open(path, "r") as file:
        text = file.readline().strip()
    data=  text.split(",")
    return data

def multi_tran(num):
    return num*num

@task
def transform(data):
    tran_data = [multi_tran(  int(i))+1 for i in data]
    return tran_data

@task
def load_text(data,path):
    import csv
    with open(path, "w") as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(data)

@flow()
def my_main_flow():
    data = extract(path="test.txt")
    tran_data = transform(data=data)
    load_text(tran_data,path="tran_data.csv")




from prefect.deployments import Deployment
from prefect.orion.schemas.schedules import IntervalSchedule

from datetime import timedelta

deployment_dev = Deployment.build_from_flow(
    flow=my_main_flow,
    name="model_training_dev",
    schedule = IntervalSchedule(interval=timedelta(minutes=3)),
    work_queue_name = "dev",

)

deployment_dev.apply()


deployment_prod = Deployment.build_from_flow(
    flow=my_main_flow,
    name="model_training-prod",
    schedule=IntervalSchedule(interval=timedelta(minutes=5)),
    work_queue_name="prod"
)

deployment_prod.apply()