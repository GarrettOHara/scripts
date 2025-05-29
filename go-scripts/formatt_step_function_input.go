// package main
// 
// import (
// 	"fmt"
// 	"strings"
// 	"reflect"
// )
// 
// func main() {
// 	input := `{\n    \"AwsRoleArn\": \"arn:aws:iam::312498070417:role/terratest-p1sevw-mssql-db-reloads-source\",\n    \"AwsRoleArnSource\": \"arn:aws:iam::312498070417:role/terratest-p1sevw-mssql-db-reloads-source\",\n    \"AwsRoleArnTarget\": \"arn:aws:iam::312498070417:role/terratest-p1sevw-mssql-db-reloads-target\",\n    \"AwsTargetAccountId\": \"312498070417\",\n    \"Biweekly\": false,\n    \"DbPasswordSsmPath\": \"/terratest-p1sevw-mssql-stage/master_password\",\n    \"DbReloadStep\": \"IsBiweekly\",\n    \"EvenWeeks\": true,\n    \"Name\": \"mssql-terratest-p1sevw\",\n    \"Region\": \"us-west-1\",\n    \"ReloadType\": \"rds\",\n    \"RunPostReloadQueries\": true,\n    \"RunPreReloadQueries\": true,\n    \"S3PostReloadPath\": \"s3://terratest-p1sevw-db-reloads-queries20240417000307704300000001/terratest-p1sevw-mssql-stage/postload/\",\n    \"S3PreReloadPath\": \"s3://terratest-p1sevw-db-reloads-queries20240417000307704300000001/terratest-p1sevw-mssql-stage/preload/\",\n    \"SourceDbInstanceIdentifier\": \"terratest-p1sevw-mssql-prod\",\n    \"StatusCode\": 500,\n    \"TargetDbInstanceIdentifier\": \"terratest-p1sevw-mssql-stage\"\n}\n`
// 
// 	// Replace '\n' and ' ' with empty strings
// 	output := strings.ReplaceAll(input, "\\n", "")
// 	output = strings.ReplaceAll(output, " ", "")
// 	output = strings.ReplaceAll(output, "\\", "")
// 	
// 	fmt.Println("Type of output:", reflect.TypeOf(output))
// 	fmt.Println(output)
// }
package main
import (
	"encoding/json"
	"fmt"
	"strings"
)

func formatStepFunctionInput(input string) (string, error) {
	// Remove backslashes and escaped newlines
 	input = strings.ReplaceAll(input, "\\n", "")
 	input = strings.ReplaceAll(input, " ", "")
 	input = strings.ReplaceAll(input, "\\", "")
	// Remove new lines
	input = strings.ReplaceAll(input, "\n", "")
	// Marshal the input string to format it as JSON
	var formattedJSON map[string]interface{}
	err := json.Unmarshal([]byte(input), &formattedJSON)
	if err != nil {
		return "", err
	}
	// Marshal it back to a JSON string
	output, err := json.Marshal(formattedJSON)
	if err != nil {
		return "", err
	}
	fmt.Println("Formatted step function input:")
	fmt.Println(string(output))

	return string(output), nil
}

func main() {

	input := `{\n    \"AwsRoleArn\": \"arn:aws:iam::312498070417:role/terratest-p1sevw-mssql-db-reloads-source\",\n    \"AwsRoleArnSource\": \"arn:aws:iam::312498070417:role/terratest-p1sevw-mssql-db-reloads-source\",\n    \"AwsRoleArnTarget\": \"arn:aws:iam::312498070417:role/terratest-p1sevw-mssql-db-reloads-target\",\n    \"AwsTargetAccountId\": \"312498070417\",\n    \"Biweekly\": false,\n    \"DbPasswordSsmPath\": \"/terratest-p1sevw-mssql-stage/master_password\",\n    \"DbReloadStep\": \"IsBiweekly\",\n    \"EvenWeeks\": true,\n    \"Name\": \"mssql-terratest-p1sevw\",\n    \"Region\": \"us-west-1\",\n    \"ReloadType\": \"rds\",\n    \"RunPostReloadQueries\": true,\n    \"RunPreReloadQueries\": true,\n    \"S3PostReloadPath\": \"s3://terratest-p1sevw-db-reloads-queries20240417000307704300000001/terratest-p1sevw-mssql-stage/postload/\",\n    \"S3PreReloadPath\": \"s3://terratest-p1sevw-db-reloads-queries20240417000307704300000001/terratest-p1sevw-mssql-stage/preload/\",\n    \"SourceDbInstanceIdentifier\": \"terratest-p1sevw-mssql-prod\",\n    \"StatusCode\": 500,\n    \"TargetDbInstanceIdentifier\": \"terratest-p1sevw-mssql-stage\"\n}\n`

	_, err := formatStepFunctionInput(input)
	if err != nil {
		fmt.Println("Error:", err)
		return
	}
}
