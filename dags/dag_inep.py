import pendulum
from inep.ingest_2019 import ingest as ingest_2019
from inep.ingest_2021 import ingest as ingest_2021
from inep.join_dfs import join_dfs
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator

dag =  DAG(dag_id="dag_ingest_inep",start_date=pendulum.today('UTC').add(days=-1), schedule='@once')
with dag:
    #Criação das tasks
    t_begin = EmptyOperator(task_id='Begin_Ingest_INEP')
    t_ingest = [
        PythonOperator(task_id='Ingest_2019',python_callable=ingest_2019),
        PythonOperator(task_id='Ingest_2021',python_callable=ingest_2021),
    ]
    t_join = PythonOperator(task_id='Join_DFs',python_callable=join_dfs)
    t_end = EmptyOperator(task_id='End_Ingest_INEP')
    #Criação do grafo
    t_begin >> t_ingest >> t_join >> t_end