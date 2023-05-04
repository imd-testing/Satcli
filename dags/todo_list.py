from datetime import datetime

from airflow import DAG
from airflow.decorators import task

# A DAG represents a workflow, a collection of tasks
with DAG(dag_id = "todo_list", start_date = datetime(2023, 4, 21), schedule = None) as dag:

    # Tasks are represented as operators
    # hello = BashOperator(task_id="todo_list", bash_command="echo hello")

    @task()
    def airflow():
        print("airflow")

    # Set dependencies between tasks
    #hello >> airflow()

    @task.virtualenv(
        task_id = "virtualenv_python",
        system_site_packages = False
    )
    def callable_virtualenv():
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
        
        from steampowered import test_function

        test_function()

    virtualenv_task = callable_virtualenv()

    virtualenv_task >> airflow()
