import time
import pendulum
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
import logging as log

dag =  DAG(dag_id="dag_teste", start_date=pendulum.today('UTC').add(days=-1), schedule='@once')
with dag:
    #Criação das tasks
    te1 = EmptyOperator(task_id='process_start')
    tp1 = PythonOperator(task_id='tp1', python_callable=lambda: log.info('Task 1'))
    tp2 = PythonOperator(task_id='tp2', python_callable=lambda: log.info('Task 2'))
    tp3 = PythonOperator(task_id='tp3', python_callable=lambda: log.info('Task 3'))
    tp4 = PythonOperator(task_id='tp4', python_callable=lambda: log.info('Task 4'))
    te2 = EmptyOperator(task_id='process_end')
    #Configuração do grafo das tasks
    te1 >> [tp1,tp2,tp3] >> tp4 >> te2