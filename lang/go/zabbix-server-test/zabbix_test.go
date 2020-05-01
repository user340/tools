package main

import (
	"log"
	"testing"

	"github.com/cavaliercoder/go-zabbix"
)

const ZabbixAPI string = "/zabbix/api_jsonrpc.php"
const HostName string = "NetBSD Zabbix"

func startSession() *zabbix.Session {
	frontend := "http://" + conf.Server + ZabbixAPI

	session, err := zabbix.NewSession(frontend, conf.User, conf.Pass)
	if err != nil {
		log.Fatal(err)
	}

	return session
}

func TestHosts(t *testing.T) {
	var params zabbix.HostGetParams
	params.Filter = map[string]interface{}{"host": HostName}

	session := startSession()

	hosts, err := session.GetHosts(params)
	if err != nil {
		log.Fatal(err)
	}

	if len(hosts) != 1 {
		t.Fatalf("Return array is not 1 length")
	}

	for _, host := range hosts {
		if host.DisplayName != HostName {
			t.Fatalf("Display name is not %v", HostName)
		}
	}
}
