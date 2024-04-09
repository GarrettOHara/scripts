#!/bin/zsh

echo "USAGE: ./script <PROFILE> <REGION> <INSTANCE_ID_A> <INSTANCE_ID_B> ..."

PROFILE=$1
REGION=$2

for n in $(seq 3 $#); do

	aws ec2 create-tags \
		--profile $PROFILE \
		--region $REGION \
		--resources $3 \
		--tags Key="backup",Value="true"
	shift

done

echo "Finished applying tags to instances."
