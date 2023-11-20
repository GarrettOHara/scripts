#!/bin/zsh

SERVER_NAME=$1
echo | openssl s_client -servername $SERVER_NAME -connect $SERVER_NAME:443 2>/dev/null | openssl x509 -noout -dates
