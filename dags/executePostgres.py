from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

# Define default arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False, # if True, the task instance will run only if the previous task instance has succeeded
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(seconds=5), # retry tasks after 5 seconds 
}

# Define the DAG
dag = DAG(
    'deploy_project_postgres',
    default_args=default_args,
    description='Deploy project using Airflow',
    schedule_interval='30 9 * * *', 
    start_date=datetime(2024, 3, 26),  
    catchup=False
)

def print_message(message):
    print(message)

# Task to print "Task 1 Executed" when executed
task1 = BashOperator(
    task_id='task_1_insertFile',
    bash_command='python /opt/airflow/dags/postgres/postgres.py',
    dag=dag
)

# Task to print "Task 2 Executed" when executed
task2 = BashOperator(
    task_id='task_2_insertFromTable',
    bash_command='python /opt/airflow/dags/postgres/pgToClickhouse.py',
    dag=dag
)


# Define task dependencies
task1 >> task2
