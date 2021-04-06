from datetime import datetime

KAFKA_BROKERS = ['localhost:9092', 'localhost:9093', 'localhost:9094']
KAFKA_TOPIC = "virtual-maironis"
KAFKA_CONSUMER_GROUP_ID = "maironis-fans"


SQL_DATABASE = "virtual-maironis"
SQL_HOST = "localhost"
SQL_USER_NAME = "postgres"
SQL_USER_PASSWORD = "postgres"
SQL_TABLE = "poems"

ELASTIC_HOST = "127.0.0.1"
ELASTiC_INDEX = "maironis-poems"