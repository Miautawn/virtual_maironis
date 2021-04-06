#!/bin/bash

#Start both webserver and scheduler
airflow webserver &
airflow scheduler
