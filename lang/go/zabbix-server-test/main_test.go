package main

import (
	"os"
	"testing"
)

const configPath string = "./config.yml"

var conf ConfigData
var z *ZabbixTest

func TestMain(m *testing.M) {
	// Setup
	conf = loadConfig(configPath)
	z = NewTest()

	code := m.Run()

	// Tear Down
	os.Exit(code)
}
