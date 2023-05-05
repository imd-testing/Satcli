from datetime import datetime

from airflow import DAG
from airflow.decorators import task
from airflow.operators.latest_only import LatestOnlyOperator

with DAG(dag_id = "update_module", start_date = datetime(2023, 5, 5, hour = 16, minute = 10), schedule = '*/10 * * * *', catchup = False,) as dag:

    @task(task_id = "update_installed_module")
    def update_installed_module():
        import subprocess
        import sys
        
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", "/opt/steampowered", '--no-deps'])

    latest_only = LatestOnlyOperator(task_id="latest_only")
    update_installed_module_task = update_installed_module()

    latest_only >> update_installed_module_task
