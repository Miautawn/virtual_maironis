![maironis](https://user-images.githubusercontent.com/24988290/114064060-edb2b280-98a1-11eb-8669-e07566335aa3.png)
# VIRTUAL_MAIRONIS
This project aims to mimic the artistic capabilities of Jonas Mačiulis, aka Maironis - one of the greatest poets of Lithuania,  
by using Neural Networks.



### Example
**Input sentence:**  
"oi graži ta mūsų lietuva"  

**Generated:**  
"meiliai su augina prozos geros  
šarvuoti nepaliesiu šarvuoti tauta  
jaunoji grakšti ir bangos plačiausias  
jis kai ant meiliai pati savęs"

As we can see, it's almost giberish but it shows the wide application of Deep Learning.

## Infrastructure
This project was not really made to be an optimal solution to text generation problem, not for a long shot! It's more of a self-issued challange that includes various technologies to simulate data pipe-lining and scheduled workloads.

Tools used:
  * Kafka - to simulate streaming
  * PostgreSQL and ElasticSearch - for storing the data
  * Airflow - for organizing and scheduling various tasks
  * Tensorflow - for Neural Network construction

![aa](https://user-images.githubusercontent.com/24988290/114075758-91a25b00-98ae-11eb-817b-99f3fbb5b7e5.png)

I used Kafka to simulate data streaming of Maironis poems, which we simply 'grab' with our consumer and put the poems directly into PostgreSQL database. Then we use Airflow scheduled task to pull the poems from SQL DB, filter out the data and store it into ElasticSearch. Lastly, every 24h another scheduled task triggers to load the clean data into Tensorflow model which trains and outputs generated n words to 'generated_poem.txt' 


## How to use?
1.) Download the project  
2.) Install required tools: Kafka, PostgreSQL DB, Elasticsearch  
3.) Install all dependencies through Pipfile.lock  
```Shell
>> pipenv install --ignore-pipfile
```
4.) Configure `config.py` and `./Airflow_dags/airflow_config.py`  
5.) Startup all the tools manually or configure my scripts in /startup_scripts  
6.) Run the project with these steps:  
 * Run `start_stream.sh` in /startup_scripts - to start the kafka stream  
 * Start the `FILTER_DATA_DAG` and `LOAD_TO_TENSORFLOW_DAG` airflow DAGs  
 * See the result in `generated_poem.txt
