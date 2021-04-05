import os
import sys
#adding config directory to searchable module path
CONFIG_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(CONFIG_DIR)

import postgresql_DB
from kafka import KafkaConsumer
from kafka import TopicPartition
import kafka_utilities
import json
import time
import config

LOG_SENDER = "CONSUMER"

#initializing the consumer
try:
    consumer = KafkaConsumer(group_id = config.KAFKA_CONSUMER_GROUP_ID, 
        bootstrap_servers=config.KAFKA_BROKERS)
except Exception as e:
    message = "ERROR: Something went wrong with initializing the consumer: {}".format(e)
    print(message)
    kafka_utilities.log(message, LOG_SENDER)
    exit(1)
else:
    kafka_utilities.log("Succesfully initalized the consumer", LOG_SENDER)

#assign partitions mannually in order to read only the latest logs (it's all about the freshest rhymes :) )
available_partitions = consumer.partitions_for_topic(config.KAFKA_TOPIC)
consumer.assign([ TopicPartition(config.KAFKA_TOPIC, partition_id) for partition_id in available_partitions])
consumer.seek_to_end()


for message in consumer:
    
    #store a message in SQL db
    postgresql_DB.put_record(json.loads(message.value.decode('utf-8')))

    log_message = "SUCCESS : message read on topic '{}' in partition {} at offset {}".format(
        message.topic, message.partition, message.offset)
    print(log_message)
    kafka_utilities.log(log_message, LOG_SENDER)




