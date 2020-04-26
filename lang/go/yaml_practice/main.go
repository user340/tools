package main

import (
	"fmt"
	"io/ioutil"
	"log"

	"github.com/go-yaml/yaml"
)

func main() {
	configPath := "./example.yml"
	buf, err := ioutil.ReadFile(configPath)
	if err != nil {
		log.Fatalf("Unable to read config: %v", err)
	}

	m := make(map[interface{}]interface{})

	err = yaml.Unmarshal(buf, &m)
	if err != nil {
		log.Fatalf("Unable to parse YAML data: %v", err)
	}

	fmt.Printf("%v\n", m)
	fmt.Printf("    %v\n", m["user"])
	fmt.Printf("    %v\n", m["port"])
	fmt.Printf("    %v\n", m["privateKey"])
}
