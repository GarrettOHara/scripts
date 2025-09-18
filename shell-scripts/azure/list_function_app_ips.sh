#!/bin/zsh

RESOURCE_GROUP='arti-prod-west-us-2-rg'
APP_NAME='arti-ai-prod-function-app'

az functionapp show --resource-group $RESOURCE_GROUP --name $APP_NAME --query outboundIpAddresses --output tsv
az functionapp show --resource-group $RESOURCE_GROUP --name $APP_NAME --query possibleOutboundIpAddresses --output tsv
