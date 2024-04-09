package main

import (
	"fmt"
	"io/ioutil"
	"net/http"
)

func main() {
	// Make a GET request to example.com
	response, err := http.Get("http://example.com")
	if err != nil {
		fmt.Println("Error:", err)
		return
	}
	defer response.Body.Close()

	// Read the response body
	body, err := ioutil.ReadAll(response.Body)
	if err != nil {
		fmt.Println("Error reading response:", err)
		return
	}

	// Store the response as a string
	responseString := string(body)

	// Print the response status code
	fmt.Println("Response Code:", response.StatusCode)

	// Print or further process the response
	fmt.Println("Response:", responseString)
}

