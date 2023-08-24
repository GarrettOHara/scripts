#!/bin/bash
if [ $# -eq 0 ]; then
  echo "Error: JSON file name not provided."
  echo "Usage: bash mysql-connecter.sh <RDS Hostanme> <RDS Master Password"
  exit 1
fi

MYSQL_PROD_HOST="$1"
MYSQL_PROD_PASS="$2"

mysql -h $MYSQL_PROD_HOST \
    -u admin \
    -p$MYSQL_PROD_PASS

