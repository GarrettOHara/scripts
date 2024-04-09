package main

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestAssertion(t *testing.T) {
	testBoolean := false

	// Use assert.True for asserting true conditions
	assert.True(t, testBoolean)

	// Alternatively, use assert.False for asserting false conditions
	// assert.False(t, testBoolean)
}
