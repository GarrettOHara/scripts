package main

import (
	"bytes"
	"os/exec"
)

func Shellout(command string) (string, string, error) {
	ShellToUse := "bash"
	var stdout bytes.Buffer
	var stderr bytes.Buffer
	cmd := exec.Command(ShellToUse, "-c", command)
	cmd.Stdout = &stdout
	cmd.Stderr = &stderr
	err := cmd.Run()
	return stdout.String(), stderr.String(), err
}

// func main() {
// 	region := "us-east-1"
// 	cmd := fmt.Sprintf("aws stepfunctions list-state-machines --region %s --profile se-dev --query stateMachines[0].stateMachineArn --output text | tr -d '[:space:]'", region)
// 	step_function_arn, errout, err := Shellout(cmd)
// 	if err != nil {
// 		log.Printf("error: %v\n", err)
// 		fmt.Println(errout)
// 	}
// 	fmt.Println("%q\n", step_function_arn)

// 	json_file := "file.json"
// 	cmd = fmt.Sprintf("bash remove_whitespace.sh %s", json_file)
// 	json_string, errout, err := Shellout(cmd)
// 	if err != nil {
// 		log.Printf("error: %v\n", err)
// 		fmt.Println(errout)
// 	}
// 	fmt.Println(json_string)

// 	cmd = fmt.Sprintf("aws stepfunctions start-execution --region %s --profile se-dev --state-machine-arn %s --input '%s'", region, step_function_arn, json_string)
// 	fmt.Println(cmd)
// 	step_function_execution, errout, err := Shellout(cmd)
// 	if err != nil {
// 		log.Printf("error: %v\n", err)
// 		fmt.Println(errout)
// 	}
// 	fmt.Print(step_function_execution)
// }
