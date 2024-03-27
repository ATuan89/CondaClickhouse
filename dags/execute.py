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
    'deploy_project_clickhouse',
    default_args=default_args,
    description='Deploy Java JAR using Airflow',
    schedule_interval='30 9 * * *',  # Set schedule interval to run every 10 minutes
    start_date=datetime(2024, 3, 26),  # Set the start date
    catchup=False
)

# Define a function to print a message
def print_message(message):
    print(message)

# Task to print "Task 1 Executed" when executed
task1 = BashOperator(
    task_id='task_1_insertFile',
    bash_command='python /opt/airflow/dags/handle/insertFile.py',
    dag=dag
)

# Task to print "Task 2 Executed" when executed
task2 = BashOperator(
    task_id='task_2_insertFromTable',
    bash_command='python /opt/airflow/dags/handle/insertFromTable.py',
    dag=dag
)

# Task to print "Task 3 Executed" when executed
task3 = BashOperator(
    task_id='task_3_query1',
    bash_command='python /opt/airflow/dags/handle/query1.py',
    dag=dag
)

# Task to call the print_message function with a custom message
task4 = BashOperator(
    task_id='task_4_query2',
    bash_command='python /opt/airflow/dags/handle/query2.py',
    dag=dag
)

# Define task dependencies
task1 >> task2  # task1 should run before task2 and task3
task2 >> [task3,task4]  # task2 should run before task4
