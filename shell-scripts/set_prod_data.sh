#!/bin/bash

MYSQL_PROD_HOST=$(./find-rds-endpoint.sh $1 $2 terratestdbreloadmysqlprod)
MYSQL_PROD_PASS=$(./get-parameter.sh $1 $2 /terratestdbreloadmysqlprod/master_password)

MYSQL_STAGE_HOST=$(./find-rds-endpoint.sh $1 $2 terratestdbreloadmysqlstage)
MYSQL_STAGE_PASS=$(get-parameter.sh $1 $2 /terratestdbreloadmysqlstage/master_password)

MSSQL_PROD_HOST=$(./find-rds-endpoint.sh $1 $2 terratestdbreloadmssqlprod)
MSSQL_PROD_PASS=$(./get-parameter.sh $1 $2 /terratestdbreloadmssqlprod/master_password)

MSSQL_STAGE_HOST=$(./find-rds-endpoint.sh $1 $2 terratestdbreloadmssqlstage)
MSSQL_STAGE_PASS=$(./get-parameter.sh $1 $2 /terratestdbreloadmssqlstage/master_password)

POSTGRES_PROD_HOST=$(./find-rds-endpoint.sh $1 $2 terratestdbreloadpostgresprod)
POSTGRES_PROD_PASS=$(./get-parameter.sh $1 $2 /terratestdbreloadpostgresprod/master_password)

POSTGRES_STAGE_HOST=$(./find-rds-endpoint.sh $1 $2 terratestdbrealoadpostgresstage)
POSTGRES_STAGE_PASS=$(./get-parameter.sh $1 $2 /terratestdbreloadpostgresstage/master_password)

./mysql.sh
./mssql.sh
./postgresql.sh

