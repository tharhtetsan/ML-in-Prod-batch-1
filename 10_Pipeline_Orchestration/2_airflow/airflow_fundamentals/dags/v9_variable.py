from airflow.decorators import dag, task
from datetime import datetime
from airflow.models import Variable

@dag(
    dag_id="v9_variable",
    start_date=datetime(2024,9,10),
    schedule_interval='@daily', catchup=False)
def run_variable():
    
    @task
    def _osGetENV():
        import os
        os_env = os.getenv("AIRFLOW_VAR_OS_ENVNAME")
        print("os_env : ",os_env)

    @task
    def _get_dotENV_params():
        dot_env = Variable.get("OS_ENVNAME")
        print("dot_env : ",dot_env)


    @task
    def _get_tokenAndPassowrd():
        api_token = Variable.get("API_TOKEN")
        sql_password = Variable.get("SQL_PASSWORD")

        print("api_token : ",int(api_token)+1)
        print("sql_password : ",sql_password)

        if sql_password == "12345678":
            print("Correct sql_password ")

    @task
    def _added_params():
        _params = Variable.get('ML_MODEL_PARA',deserialize_json=True)["param"]
        for _cur in _params:
            print("_cur : ",_cur)




    _osGetENV()
    _get_dotENV_params()
    _added_params()
    _get_tokenAndPassowrd()


run_variable()