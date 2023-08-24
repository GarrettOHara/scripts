#!/bin/bash

echo "\nUsage: ./connect-postgresql.sh HOST DATABASE USER PASSWORD\n"

export POSTGRESQL_HOST=$1
export PGDATABASE=$2
export PGUSER=$3
export PGPASSWORD=$4

psql -h $POSTGRESQL_PROD_HOST \
	-d $PGDATABASE\
	-U $PGUSER
