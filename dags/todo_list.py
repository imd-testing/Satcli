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
        task_id="virtualenv_python", requirements=["colorama==0.4.0"], system_site_packages=False
    )
    def callable_virtualenv():
        """
        Example function that will be performed in a virtual environment.

        Importing at the module level ensures that it will not attempt to import the
        library before it is installed.
        """
        from time import sleep

        from colorama import Back, Fore, Style

        print(Fore.RED + "some red text")
        print(Back.GREEN + "and with a green background")
        print(Style.DIM + "and in dim text")
        print(Style.RESET_ALL)
        for _ in range(4):
            print(Style.DIM + "Please wait...", flush=True)
            sleep(1)
        print("Finished")

    virtualenv_task = callable_virtualenv()

    virtualenv_task >> airflow()
