from datetime import datetime

from airflow import DAG
from airflow.decorators import task
from airflow.operators.latest_only import LatestOnlyOperator

with DAG(dag_id = "queue", start_date = datetime(2023, 5, 5, hour = 19, minute = 00), schedule = '*/5 * * * *', catchup = False,) as dag:

    @task(task_id = "update_installed_module")
    def update_installed_module():
        import subprocess
        import sys
        
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", "/opt/steampowered", '--no-deps'])

    @task(task_id = "run_queue")
    def run_queue():
        import steampowered

        steampowered.run_queue()

    latest_only = LatestOnlyOperator(task_id="latest_only")
    update_installed_module_task = update_installed_module()
    run_queue_task = run_queue()

    latest_only >> update_installed_module_task >> run_queue_task
