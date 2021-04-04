from datetime import datetime
import os

LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs') 

def log(log_message, sender):
    timestamp = datetime.today()
    log_name = os.path.join(LOG_DIR, str(timestamp.date()) + '.log')
    with open(log_name, 'a') as f:
        f.write("{}|{}: {}\n".format(sender, timestamp.time(), log_message))