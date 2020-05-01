package main

import (
	"io/ioutil"
	"log"

	"github.com/go-yaml/yaml"
)

// ConfigData used to contain data which read from YAML
type ConfigData struct {
	Server   string
	User     string
	Password string
}

func readConfig(path string) []byte {
	buf, err := ioutil.ReadFile(path)
	if err != nil {
		log.Fatal(err)
	}

	return buf
}

func parseYamlConfig(buf []byte) ConfigData {
	conf := ConfigData{}
	err := yaml.Unmarshal(buf, &conf)
	if err != nil {
		log.Fatal(err)
	}

	return conf
}

func loadConfig(path string) ConfigData {
	return parseYamlConfig(readConfig(path))
}
