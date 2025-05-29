#!/bin/zsh

REGION=$1
FUNCTION_NAME=$2

for i in {1..25}; do
	echo "Deleting $FUNCTION_NAME version $i"
	aws lambda --region $REGION delete-function --function-name $FUNCTION_NAME:$i
done
