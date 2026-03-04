#!/bin/zsh
az vm create \
  --resource-group "arti-prod-east-us-2-rg" \
  --name "test-vm-east" \
  --image "Ubuntu2204" \
  --size "Standard_B1s" \
  --vnet-name "arti-prod-east-us-2-vnet" \
  --subnet "vm-subnet" \
  --admin-username "azureuser" \
  --generate-ssh-keys \
  --public-ip-sku "Standard" \
  --tags "Environment=Test" "Purpose=NetworkConnectivityTest" "SafeToDelete=Yes" "Owner=$(whoami)" "CreatedDate=$(date +%Y-%m-%d)"
