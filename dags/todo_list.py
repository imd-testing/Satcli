from datetime import datetime

from airflow import DAG
from airflow.decorators import task

with DAG(dag_id = "todo_list", start_date = datetime(2023, 4, 21), schedule = None) as dag:

    @task(task_id = "update_installed_module")
    def update_installed_module():
        import subprocess
        import sys
        
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", "/opt/steampowered", '--no-deps'])

    @task(task_id = "add_to_todo_list")
    def add_to_todo_list_container():
        import steampowered

        steampowered.add_to_todolist()

    update_installed_module_task = update_installed_module()
    add_to_todo_list_task = add_to_todo_list_container()
    
    update_installed_module_task >> add_to_todo_list_task


