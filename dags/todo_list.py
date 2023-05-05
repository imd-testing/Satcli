from datetime import datetime

from airflow import DAG
from airflow.decorators import task
from airflow.operators.latest_only import LatestOnlyOperator

with DAG(dag_id = "todo_list", start_date = datetime(2023, 5, 5, hour = 16, minute = 10), schedule = '10 * * * *', catchup = False,) as dag:

    @task(task_id = "add_to_todo_list")
    def add_to_todo_list():
        import steampowered

        steampowered.add_to_todolist()

    latest_only = LatestOnlyOperator(task_id="latest_only")
    add_to_todo_list_task = add_to_todo_list()
    
    latest_only >> add_to_todo_list_task
