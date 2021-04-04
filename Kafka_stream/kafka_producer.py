from kafka import KafkaProducer
import json
import config
import kafka_utilities

LOG_SENDER = "PRODUCER"

#creating kafka producer
try:
    producer = KafkaProducer(bootstrap_servers = config.KAFKA_BROKERS)
except Exception as e:
    message = "ERROR: Something went wrong with initializing the producer: {}".format(e)
    print(message)
    kafka_utilities.log(message, LOG_SENDER)
    exit(1)

#success callback
def on_message_success(record_metadata):
    message_result = "SUCCESS : message delivered on topic '{}' in partition {} at offset {}".format(
        record_metadata.topic, record_metadata.partition, record_metadata.offset)
    print(message_result)
    kafka_utilities.log(message_result, LOG_SENDER)

#failure callback
def on_message_error(exception):
    error_result = "ERROR: {}".format(exception)
    print(error_result)
    kafka_utilities.log(error_result, LOG_SENDER)

#send logs
def send_message(data):
    message = json.dumps(data)
    producer.send(config.KAFKA_TOPIC, value = message.encode('utf-8')).add_callback(
        on_message_success).add_errback(on_message_error)



