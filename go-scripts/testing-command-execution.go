package main

import (
	"bytes"
	"fmt"
	"log"
	"math/rand"
	"os"
	"os/exec"
	"time"
)

func GetRandomSubset(values []string) []string {
	rand.Seed(time.Now().UnixNano()) // Initialize the random number generator with a seed based on the current time

	// Generate a random number between 1 and 3 (inclusive) to determine the subset size
	subsetSize := rand.Intn(3) + 1

	// Shuffle the input list of values
	shuffled := make([]string, len(values))
	copy(shuffled, values)
	rand.Shuffle(len(shuffled), func(i, j int) {
		shuffled[i], shuffled[j] = shuffled[j], shuffled[i]
	})

	// Return a subset of the shuffled values
	return shuffled[:subsetSize]
}

func Shell(command string) string {
	ShellToUse := "bash"
	var stdout bytes.Buffer
	var stderr bytes.Buffer
	cmd := exec.Command(ShellToUse, "-c", command)
	cmd.Stdout = &stdout
	cmd.Stderr = &stderr
	err := cmd.Run()
	if err != nil {
		log.Printf("ERROR: %s", err)
		fmt.Println(stderr.String())
	}
	return stdout.String()
}

func main() {
	region := "us-east-1"
	database_list := []string{"mssql", "mysql", "postgresql"}
	test_databases := GetRandomSubset(database_list)
	bastion_instance_name := "terratestdbreload-bastion"
	fmt.Println(test_databases)

	cmd := fmt.Sprintf("bash get-instance-id.sh %s", bastion_instance_name)
	bastion_instance_id := Shell(cmd)
	fmt.Println(bastion_instance_id)
	for _, db := range test_databases {

		switch db {
		case "mssql":
			bastion_command := fmt.Sprintf("sudo /home/ssm-user/mssql/set-mssql-data.sh %s", region)
			fmt.Println("BASTION COMMAND: ", bastion_command)

			tmp := fmt.Sprintf("bash send-bash-command.sh %s %s '%s' %s", "se-dev", region, bastion_command, bastion_instance_id)
			fmt.Println("Command: ", tmp)
			ssm_cmd_output := Shell(tmp)

			fmt.Println(ssm_cmd_output)
		case "mysql":
			bastion_command := fmt.Sprintf("sudo /home/ssm-user/mysql/set-mysql-data.sh %s", region)
			fmt.Println("BASTION COMMAND: ", bastion_command)

			tmp := fmt.Sprintf("bash send-bash-command.sh %s %s '%s' %s", "se-dev", region, bastion_command, bastion_instance_id)
			fmt.Println("Command: ", tmp)
			ssm_cmd_output := Shell(tmp)

			fmt.Println(ssm_cmd_output)
		case "postgresql":
			bastion_command := fmt.Sprintf("sudo /home/ssm-user/postgresql/set-postgresql-data.sh %s", region)
			fmt.Println("BASTION COMMAND: ", bastion_command)

			tmp := fmt.Sprintf("bash send-bash-command.sh %s %s '%s' %s", "se-dev", region, bastion_command, bastion_instance_id)
			fmt.Println("Command: ", tmp)
			ssm_cmd_output := Shell(tmp)

			fmt.Println(ssm_cmd_output)
		default:
			fmt.Println("ERROR: unexpected value")
		}
	}
	// just need to test above code
	os.Exit(0)

	cmd = fmt.Sprintf("aws stepfunctions list-state-machines --region %s --profile se-dev --query stateMachines[0].stateMachineArn --output text | tr -d '[:space:]'", region)
	step_function_arn := Shell(cmd)
	fmt.Println(step_function_arn)

	json_file := "file.json"
	cmd = fmt.Sprintf("bash remove_whitespace.sh %s", json_file)
	json_string := Shell(cmd)
	fmt.Println(json_string)

	cmd = fmt.Sprintf("aws stepfunctions start-execution --region %s --profile se-dev --state-machine-arn %s --input '%s'", region, step_function_arn, json_string)
	fmt.Println(cmd)
	step_function_execution := Shell(cmd)
	fmt.Print(step_function_execution)
}
