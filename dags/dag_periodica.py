import pendulum
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from datetime import timedelta

dag =  DAG(dag_id="nova_dag", start_date=pendulum.today('UTC').add(days=-1), schedule_interval=timedelta(seconds=30))
with dag:
    e1 = EmptyOperator(task_id='operacao_1')
    e2 = EmptyOperator(task_id='operacao_2')
    e3 = EmptyOperator(task_id='operacao_3')

    [e1, e2] >> e3
