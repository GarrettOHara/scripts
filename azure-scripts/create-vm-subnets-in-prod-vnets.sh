#!/bin/zsh

# West US 2
az network vnet subnet create \
  --resource-group "arti-prod-west-us-2-rg" \
  --vnet-name "arti-prod-west-us-2-vnet" \
  --name "vm-subnet" \
  --address-prefixes "10.120.250.0/24"

# East US 2  
az network vnet subnet create \
  --resource-group "arti-prod-east-us-2-rg" \
  --vnet-name "arti-prod-east-us-2-vnet" \
  --name "vm-subnet" \
  --address-prefixes "10.122.250.0/24"
