package main

import (
	"os"
	"testing"
)

const configPath string = "./config.yml"

var conf ConfigData

func TestMain(m *testing.M) {
	// Setup
	conf = loadConfig(configPath)

	code := m.Run()

	// Tear Down
	os.Exit(code)
}
