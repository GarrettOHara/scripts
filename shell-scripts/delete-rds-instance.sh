#! /bin/zsh

echo "Please pass in arguments as <PROFILE> <REGION> <INSTANCE_NAME>"

aws rds delete-db-instance \
	--profile $1 \
	--region $2 \
	--db-instance-identifier $3 \
	--skip-final-snapshot
