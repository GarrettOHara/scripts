#!/bin/zsh

export TOKEN=$1

curl -X POST https://slack.com/api/users.getPresence \
	--data "token=$TOKEN&user=U03G58C3563"
echo ""

