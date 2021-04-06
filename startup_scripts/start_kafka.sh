#!/bin/bash

#Home for root kafka folder
KAFKA_HOME="/home/miautawn/Programs/Kafka/"

#Should print the kafka messages? 0 - No, 1 - yes
VERBOSE=0
if [ "$1" == "0" ]; then VERBOSE=0; else VERBOSE=1; fi

#Starting the zookeeper nodes
echo "Starting the zookeeper nodes..."
#Do this for every zookeeper node you have
if [ $VERBOSE -eq 0 ]
    then
        $KAFKA_HOME"kafka_1/bin/zookeeper-server-start.sh" $KAFKA_HOME"kafka_1/config/zookeeper.properties" &>/dev/null &
        $KAFKA_HOME"kafka_2/bin/zookeeper-server-start.sh" $KAFKA_HOME"kafka_2/config/zookeeper.properties" &>/dev/null &
        $KAFKA_HOME"kafka_3/bin/zookeeper-server-start.sh" $KAFKA_HOME"kafka_3/config/zookeeper.properties" &>/dev/null &

    else
        $KAFKA_HOME"kafka_1/bin/zookeeper-server-start.sh" $KAFKA_HOME"kafka_1/config/zookeeper.properties" &
        $KAFKA_HOME"kafka_2/bin/zookeeper-server-start.sh" $KAFKA_HOME"kafka_2/config/zookeeper.properties" &
        $KAFKA_HOME"kafka_3/bin/zookeeper-server-start.sh" $KAFKA_HOME"kafka_3/config/zookeeper.properties" &
fi

#wait for some time
sleep 5
#Starting the kafka nodes
echo "starting the kafka nodes..."
#Do this for every kafka node you have
if [ $VERBOSE -eq 0 ]
    then
        $KAFKA_HOME"kafka_1/bin/kafka-server-start.sh" $KAFKA_HOME"kafka_1/config/server.properties" &>/dev/null &
        $KAFKA_HOME"kafka_2/bin/kafka-server-start.sh" $KAFKA_HOME"kafka_2/config/server.properties" &>/dev/null &
        $KAFKA_HOME"kafka_3/bin/kafka-server-start.sh" $KAFKA_HOME"kafka_3/config/server.properties" &>/dev/null &

    else
        $KAFKA_HOME"kafka_1/bin/kafka-server-start.sh" $KAFKA_HOME"kafka_1/config/server.properties" &
        $KAFKA_HOME"kafka_2/bin/kafka-server-start.sh" $KAFKA_HOME"kafka_2/config/server.properties" &
        $KAFKA_HOME"kafka_3/bin/kafka-server-start.sh" $KAFKA_HOME"kafka_3/config/server.properties" &
fi