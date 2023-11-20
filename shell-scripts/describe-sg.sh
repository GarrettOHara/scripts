#!/bin/bash

aws ec2 describe-security-groups \
	--profile "se-staging" \
	--region "us-east-1" \
    --filters "Name=ip-permission.protocol,Values=-1" \
    --query "SecurityGroups[?IpPermissions[?IpProtocol == 'tcp' &&
      contains(IpRanges[].CidrIp,'10.0.0.0/16') &&
      contains(IpRanges[].CidrIp,'10.57.0.0/16') &&
      contains(IpRanges[].CidrIp,'100.121.0.0/16') &&
      contains(IpRanges[].CidrIp,'172.25.0.0/22')]].GroupId"
