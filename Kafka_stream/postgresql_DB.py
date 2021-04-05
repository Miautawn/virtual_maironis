import os
import sys
#adding config directory to searchable module path
CONFIG_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(CONFIG_DIR)

import psycopg2 as db
import config
import kafka_utilities



LOG_SENDER = "SQL_DATABASE"
connection_string = """
                    dbname='{}' host='{}'
                    user='{}' password='{}'
                    """.format(
                        config.SQL_DATABASE, config.SQL_HOST,
                        config.SQL_USER_NAME, config.SQL_USER_PASSWORD)

try:
    connection = db.connect(connection_string)
except Exception as e:
    message = "Something went wrong\nwhen connecting to the {} DB: {}".format(config.SQL_DATABASE, e)
    print(message)
    kafka_utilities.log(message, LOG_SENDER)
    exit(1)
else:
    message = "Successfully connected to the {} DB!".format(config.SQL_DATABASE)
    print(message)
    kafka_utilities.log(message, LOG_SENDER)

cursor = connection.cursor()

#put a message in DB
def put_record(message):

    #get title and the body of a poem
    rows = message.splitlines()
    title, body = rows[0], '\n'.join(rows[1:])

    try:
        query = "INSERT INTO {} VALUES ('{}', '{}')".format(config.SQL_TABLE, title, body)
        cursor.execute(query)
    except Exception as e:
        print("ALLAG", e)
        connection.rollback()
    else:
        connection.commit()


