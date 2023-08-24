package main

import (
	"fmt"
	"strconv"
	"strings"
)

func main() {
	formattedString := "%!s(float64=1200.50)%"

	// Extract the numeric part by splitting the string and removing non-numeric characters
	//numericPart := strings.Trim(strings.TrimPrefix(strings.TrimSuffix(formattedString, ")%"), "%!s(float64="), "=")
	
	trimmed := strings.Trim(formattedString, "%!s=

	// Convert the numeric part to a float64
	floatValue, err := strconv.ParseFloat(numericPart, 64)
	if err != nil {
		fmt.Println("Error:", err)
		return
	}

	// Convert the float64 to an integer
	intValue := int(floatValue)

	fmt.Println("Integer value:", intValue)
}

