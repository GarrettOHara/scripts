#!/bin/bash

curl -v -X POST --location 'https://commissioner.sportngin.com/gordon/api/deploys' \
	-H 'Authorization: Bearer <TOKEN>' \
	-H 'Content-Type: application/json' \
	-d '{
        "app_name": "user_service",
        "environment": "staging",
        "force_deploy": "false",
        "deploy_plan_options":{
          "delay": "false",
          "pod_replacement": "false",
          "deploy": "false",
          "rolling_restart": "false",
          "post_reload": "false"
        }
      }'

