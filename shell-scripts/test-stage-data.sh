#!/bin/bash

MYSQL_STAGE_HOST=$(./find-rds-endpoint.sh $1 $2 terratestdbreloadmysqlstage)
MYSQL_STAGE_PASS=$(get-parameter.sh $1 $2 /terratestdbreloadmysqlstage/master_password)

MSSQL_STAGE_HOST=$(./find-rds-endpoint.sh $1 $2 terratestdbreloadmssqlstage)
MSSQL_STAGE_PASS=$(./get-parameter.sh $1 $2 /terratestdbreloadmssqlstage/master_password)

POSTGRES_STAGE_HOST=$(./find-rds-endpoint.sh $1 $2 terratestdbrealoadpostgresstage)
POSTGRES_STAGE_PASS=$(./get-parameter.sh $1 $2 /terratestdbreloadpostgresstage/master_password)

./stage-mysql.sh
./stage-mssql.sh
./stage-postgresql.sh
