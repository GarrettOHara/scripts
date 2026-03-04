#!/bin/bash

# Get West VM private IP
az vm show -d --resource-group "arti-prod-west-us-2-rg" --name "test-vm-west" --query "privateIps" -o tsv

# Get East VM private IP  
az vm show -d --resource-group "arti-prod-east-us-2-rg" --name "test-vm-east" --query "privateIps" -o tsv
