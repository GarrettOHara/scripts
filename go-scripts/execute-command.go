package main

//import (
//	"bytes"
////	"crypto/tls"
//	"fmt"
//	"io/ioutil"
//	"log"
//	"os/exec"
////	"strings"
////	"testing"
////	"time"
//)
//
//// source: https://stackoverflow.com/questions/6182369/exec-a-shell-command-in-go
//func Shellout(command string) (string, string, error) {
//	ShellToUse := "bash"
//	var stdout bytes.Buffer
//	var stderr bytes.Buffer
//	cmd := exec.Command(ShellToUse, "-c", command)
//	cmd.Stdout = &stdout
//	cmd.Stderr = &stderr
//	err := cmd.Run()
//	return stdout.String(), stderr.String(), err
//}
//
//func main() {
//	region := "us-east-1"
//	cmd := fmt.Sprintf("aws stepfunctions list-state-machines --region %s --profile se-dev --query stateMachines[0].stateMachineArn --output text", region)
//	out, errout, err := Shellout(cmd)
//	if err != nil {
//		log.Printf("error: %v\n", err)
//		fmt.Println(errout)
//	}
//	fmt.Print(out)
//
//	json_file, err := iotuil.ReadFile("file.txt")
//    if err != nil {
//        log.Fatalf("unable to read file: %v", err)
//    }
//    fmt.Println(string(json_file))
//
//	cmd := fmt.Sprintf("aws stepfunctions start-execution --region %s --profile se-dev --input %s --query stateMachines[0].stateMachineArn --output text", region, json_file)
//	out, errout, err := Shellout(cmd)
//	if err != nil {
//		log.Printf("error: %v\n", err)
//		fmt.Println(errout)
//	}
//	fmt.Print(out)
//}
