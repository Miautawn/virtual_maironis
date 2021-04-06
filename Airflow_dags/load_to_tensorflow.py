from airflow import DAG
from airflow.operators.python import PythonOperator
from elasticsearch import Elasticsearch
from elasticsearch import helpers
from datetime import datetime, timedelta
import sys
import csv

CONFIG_DIR="/home/miautawn/virtual_maironis/"
sys.path.append(CONFIG_DIR)

import config

default_args = {
    'owner' : 'admin',
    #enter your date (it shouldn't matter as the catchup is set to FALSE)
    'start_date' : datetime(2021,4,6),
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

try:
    elastic_connection = Elasticsearch({config.ELASTIC_HOST})
except Exception as e:
    print(e)
    exit(1)


def read_from_elastic():
    '''
    this task will read all the data from elasticsearch
    and output it to a csv file the tensorflow to use
    '''

    #we will use scrolling, because Maironis was a busy poet :)
    result = elastic_connection.search(index = config.ELASTiC_INDEX, scroll = '50m', 
                                    size = 100, body = {"query":{"match_all":{}}})
    scroll_id = result['_scroll_id']
    scroll_size = result['hits']['total']['value']
    
    poems = [poem['_source']['body'] for poem in result['hits']['hits']]

    #start scrolling
    if scroll_size > 100:
        while scroll_size > 0:
            result = elastic_connection.scroll(scroll_id=scroll_id, scroll='50m')
            scroll_id = result['_scroll_id']
            scroll_size = len(result['hits']['hits'])
            for record in result['hits']['hits']:
                lox.append(record['_source']['body'])
    
    #Write to file
    with open(CONFIG_DIR+'/Airflow_dags/ready_data.txt', 'w') as file:
        for poem in poems:
            file.write(poem)

#This dag will run every 24 hours
with DAG('LOAD_TO_TENSORFLOW_DAG', schedule_interval=timedelta(hours=24),
            default_args = default_args, catchup=False, max_active_runs=1) as dag:

    read_elastic = PythonOperator(task_id='read_from_elastic', python_callable=read_from_elastic) 
