import os
import sys
#adding config directory to searchable module path
CONFIG_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(CONFIG_DIR)

import time
import random
import kafka_producer

file = open(CONFIG_DIR + '/maironis_fixed_poems.txt', 'r')
poems = file.read()
poems = poems.split('\n\n')

for poem in poems:
    #feed kafka
    kafka_producer.send_message(poem)

    #wait for 10-20 seconds to simulate streaming
    time.sleep(random.randint(10, 20))

    