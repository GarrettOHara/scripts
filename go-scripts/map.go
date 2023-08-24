package main

import "fmt"

func main() {
    // Create a map
    myMap := map[string]int{
        "apple":  1,
        "banana": 2,
        "orange": 3,
    }

    // Iterate over the map and print keys and values
    for key := range myMap {
        fmt.Printf("Key: %s\n", key)
    }
}

