from airflow.models import DAG
from airflow.decorators import task
from airflow.sensors.base import PokeReturnValue
from airflow.operators.empty import EmptyOperator
from pendulum import datetime, now

# Create Simple DAG
with DAG( dag_id= 'sensor_decorator', 
          schedule= '@daily',
          catchup= False,
          start_date= datetime(2024,3,1),
          max_active_runs= 1
        ) :
    # Start
    start= EmptyOperator(task_id= 'start')
    
    # Add Sensor    
    @task.sensor(task_id= 'check_datetime_python')
    def check_datetime_python_task() -> PokeReturnValue:
        # Check current > target
        condition_met = now() >= datetime(2024,8,21,14,0,tz= 'Asia/Bangkok')
        if condition_met :
            # Return Something
            operator_return_value = 'hello world'
        else: 
            # Return Value as None if condition doesn't met
            operator_return_value = None
        # Return Poke Value
        return PokeReturnValue(is_done=condition_met, 
                               xcom_value=operator_return_value)
    # Print Sensor's Value
    @task(task_id= 'print_value')
    def print_value_task(content) :
        print(content)
    check_datetime_python= check_datetime_python_task()
    print_value= print_value_task(check_datetime_python)
    
    # End
    end= EmptyOperator(task_id= 'end')
    # Set Dependencies Flow
    start >> check_datetime_python >> print_value >> end