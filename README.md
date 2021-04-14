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
 * See the result in `generated_poem.txt`

## About the model  
The model itself is nothing special and small in comparison as not to go crazy in training times.    
It consists of 5 layers:  
 * Embedding layer - for vectorizing our tokenized sentences  
 * 2 Bidirectional LSTM with a Dropout in between - this is of course used because text generation   
  works better with sequence models  
 * 1 Dense hidden layer   
 * 1 Output Dense layer with neurons which output the most likely word.

### How does it generate the rhymes
We take each sentence of the corpus (consisting of poems), tokenize it and then split it for each word  
to make pairs of predicting data and 'labels':    

Let's take a sentence "kur bega sesupe kur nemunas teka"  
Our sliced input will be:  
- kur [bega]  
- kur bega [sesupe]  
- kur bega sesupe [kur]  
- kur bega sesupe kur [nemunas]  
- kur bega sesupe kur nemunas [teka]  

These input will be our training data and [words] will be our labels.  
Then we simply pad these sequnces and let the embedding do its magic.
