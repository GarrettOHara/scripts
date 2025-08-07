#!/bin/zsh

ENV_NAME="ai-arti-proxy-prod-env"
RG_NAME="arti-prod-west-us-2-rg"
EMAIL="your@email.com"

while true; do
	STATUS=$(az containerapp env show \
		--name "$ENV_NAME" \
		--resource-group "$RG_NAME" \
		--query "properties.provisioningState" -o tsv)

	echo "[$(date +"%T")] Status: $STATUS"

	if [[ "$STATUS" == "Succeeded" ]]; then
		echo "Container App Env is now Running" | mail -s "Azure Env Ready" "$EMAIL"
		break
	fi
	sleep 60
done
