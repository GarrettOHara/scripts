package main

import (
	"fmt"
	"strings"
	"reflect"
)

func main() {
	input := `{\n    \"AwsRoleArn\": \"arn:aws:iam::312498070417:role/terratest-p1sevw-mssql-db-reloads-source\",\n    \"AwsRoleArnSource\": \"arn:aws:iam::312498070417:role/terratest-p1sevw-mssql-db-reloads-source\",\n    \"AwsRoleArnTarget\": \"arn:aws:iam::312498070417:role/terratest-p1sevw-mssql-db-reloads-target\",\n    \"AwsTargetAccountId\": \"312498070417\",\n    \"Biweekly\": false,\n    \"DbPasswordSsmPath\": \"/terratest-p1sevw-mssql-stage/master_password\",\n    \"DbReloadStep\": \"IsBiweekly\",\n    \"EvenWeeks\": true,\n    \"Name\": \"mssql-terratest-p1sevw\",\n    \"Region\": \"us-west-1\",\n    \"ReloadType\": \"rds\",\n    \"RunPostReloadQueries\": true,\n    \"RunPreReloadQueries\": true,\n    \"S3PostReloadPath\": \"s3://terratest-p1sevw-db-reloads-queries20240417000307704300000001/terratest-p1sevw-mssql-stage/postload/\",\n    \"S3PreReloadPath\": \"s3://terratest-p1sevw-db-reloads-queries20240417000307704300000001/terratest-p1sevw-mssql-stage/preload/\",\n    \"SourceDbInstanceIdentifier\": \"terratest-p1sevw-mssql-prod\",\n    \"StatusCode\": 500,\n    \"TargetDbInstanceIdentifier\": \"terratest-p1sevw-mssql-stage\"\n}\n`

	// Replace '\n' and ' ' with empty strings
	output := strings.ReplaceAll(input, "\\n", "")
	output = strings.ReplaceAll(output, " ", "")
	output = strings.ReplaceAll(output, "\\", "")
	
	fmt.Println("Type of output:", reflect.TypeOf(output))
	fmt.Println(output)
}

