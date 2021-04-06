#!/bin/bash

ELASTIC_HOME="/home/miautawn/Programs/elasticsearch"
KIBANA_HOME="/home/miautawn/Programs/kibana"

#Starting both
$ELASTIC_HOME/bin/elasticsearch &
$KIBANA_HOME/bin/kibana
