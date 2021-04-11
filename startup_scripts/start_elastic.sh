#!/bin/bash

ELASTIC_HOME=""
KIBANA_HOME=""

#Starting both
$ELASTIC_HOME/bin/elasticsearch &
$KIBANA_HOME/bin/kibana
