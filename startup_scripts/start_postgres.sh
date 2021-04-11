#!/bin/bash

#Starts the postgres database together with omnidb server

OMNIDB_HOME=""

sudo service postgresql start
$OMNIDB_HOME/omnidb-server
