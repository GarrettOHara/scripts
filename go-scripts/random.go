package main

import (
	"fmt"
	"math/rand"
	"time"
)

func GetRandomSubset(values []string) []string {
	// Initialize the random number generator with a seed based on the current time
	// rand.Seed(time.Now().UnixNano())

	seed := time.Now().UnixNano()
	r := rand.New(rand.NewSource(seed))

	// Generate a random number between 1 and 3 (inclusive) to determine the subset size
	subsetSize := r.Intn(len(values)) + 1

	// Shuffle the input list of values
	shuffled := make([]string, len(values))
	copy(shuffled, values)
	rand.Shuffle(len(shuffled), func(i, j int) {
		shuffled[i], shuffled[j] = shuffled[j], shuffled[i]
	})

	// Return a subset of the shuffled values
	return shuffled[:subsetSize]
}

func main() {
	original := []string{"apple", "banana", "cherry"}

	subset := GetRandomSubset(original)
	fmt.Println(subset)
}
