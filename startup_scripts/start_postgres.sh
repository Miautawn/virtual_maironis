#!/bin/bash

#Starts the postgres database together with omnidb server

OMNIDB_HOME="/home/miautawn/Programs/omnidb"

sudo service postgresql start
$OMNIDB_HOME/omnidb-server
