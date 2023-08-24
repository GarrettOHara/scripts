// source: https://stackoverflow.com/questions/6182369/exec-a-shell-command-in-go
func Shellout(command string) string {
	ShellToUse := "bash"

	var stdout bytes.Buffer
	var stderr bytes.Buffer

	// Create a new command with the specified shell and command to execute.
	cmd := exec.Command(ShellToUse, "-c", command)

	// Capture stdOut and stdErr
	cmd.Stdout = &stdout
	cmd.Stderr = &stderr

	// Execute the command and capture any error that occurs.
	error := cmd.Run()
	if error != nil {
		log.Printf("ERROR: %s", error)
		fmt.Println(stderr.String())
	}
	// Return the captured standard output as a string.
	return stdout.String()
}
