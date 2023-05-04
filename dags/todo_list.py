from datetime import datetime

from airflow import DAG
from airflow.decorators import task

with DAG(dag_id = "todo_list", start_date = datetime(2023, 4, 21), schedule = None) as dag:

    @task.virtualenv(
        task_id = "add_to_todo_list",
        system_site_packages = False
    )
    def add_to_todo_list_container():
        """
        We need to manually move our sources so we can build our project in the container, as PIP is made by peoples too stupid
        to understand the very concept of configurable build PATH.
        """

        import subprocess
        import sys
        import shutil
        import tempfile
        
        with tempfile.TemporaryDirectory() as dest:
            target = f"{dest}/src"
            
            shutil.copytree("/opt/src", target)
            subprocess.check_call([sys.executable, "-m", "pip", "install", target])
        
        from steampowered import add_to_todolist

        add_to_todolist()

    add_to_todo_list_task = add_to_todo_list_container()

