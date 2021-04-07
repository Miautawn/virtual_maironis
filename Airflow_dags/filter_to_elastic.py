from airflow import DAG
from airflow.operators.python import PythonOperator
import psycopg2 as db
from elasticsearch import Elasticsearch
from elasticsearch import helpers
from datetime import datetime, timedelta
import sys
import re
import csv
import airflow_config

#adding config to path
sys.path.append(airflow_config.CONFIG_DIR)
import config

connection_string = """
                    dbname='{}' host='{}'
                    user='{}' password='{}'
                    """.format(
                        config.SQL_DATABASE, config.SQL_HOST,
                        config.SQL_USER_NAME, config.SQL_USER_PASSWORD)

try:
    connection = db.connect(connection_string)
    elastic_connection = Elasticsearch({config.ELASTIC_HOST})
except Exception as e:
    print(e)
    exit(1)

cursor = connection.cursor()


default_args = {
    'owner' : 'admin',
    #enter your date (it shouldn't matter as the catchup is set to FALSE)
    'start_date' : datetime(2021,4,6),
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

def read_filtered_data():
    '''
    this fucntion will simply return the csv reader for the filtered_data.csv file
    '''
    csv_file = open(airflow_config.CONFIG_DIR+'/Airflow_dags/filtered_data.csv', 'r')
    m_reader = csv.reader(csv_file, delimiter=',')
    return m_reader


def filter_from_sql():
    '''
    this task will read the data from sql_database, filter it 
    and store it into a file in ./filtered_data.csv
    '''

    #read 10 poems at the time
    query = "SELECT * FROM {} LIMIT 10".format(config.SQL_TABLE)
    try:
        cursor.execute(query)
    except Exception as e:
        print("Something went wrong with reading data from the SQL database: ", e)
        exit(1)
    
    data = cursor.fetchall()

    if (len(data) != 0):
        csv_file = open(airflow_config.CONFIG_DIR+'/Airflow_dags/filtered_data.csv', 'w')
        m_writer = csv.writer(csv_file, delimiter=',')
        for poem in data:
            header, body, ID = poem

            #filtering the body
            body = body.lower()
            body = re.sub(r'[^a-ž\n ]', '', body)
            
            m_writer.writerow([ID, header, body])

def push_to_elastic():
    '''
    this task will simply read the filtered data file 
    and push the poems to elasticsearch
    '''

    #read the file
    m_reader = read_filtered_data()

    elastic_actions = []
    for row in m_reader:
        ID, header, body = row
        action = {'_index' : config.ELASTiC_INDEX,
                  'title' : header,
                  'body' : body
                 }
        elastic_actions.append(action)
    
    #put to elastic
    result = helpers.bulk(elastic_connection, elastic_actions)

def delete_from_sql():
    '''
    this task will delete the read poems from the SQL database
    '''

    #read the file
    m_reader = read_filtered_data()
    deletable_IDs = [int(row[0]) for row in m_reader]

    #deleting (ANY() is a psycopg2 substitute for IN)
    query = "DELETE FROM {} WHERE id = ANY(%s);".format(config.SQL_TABLE)
    try:
        cursor.execute(query, [deletable_IDs])
    except Exception as e:
        print("Could not delete the read poems from SQL database:", e)
        connection.rollback()
        exit(1)
    else:
        connection.commit()
    

    

#creating our DAG
with DAG('FILTER_DATA_DAG', schedule_interval=timedelta(minutes=5), 
        default_args=default_args, catchup=False, max_active_runs=1) as dag:

    filter_sql = PythonOperator(task_id='filter_from_SQL', python_callable = filter_from_sql)
    put_elastic = PythonOperator(task_id='put_to_elastic', python_callable = push_to_elastic)
    delete_sql = PythonOperator(task_id='delete_from_sql', python_callable  = delete_from_sql)

    filter_sql >> put_elastic >> delete_sql

