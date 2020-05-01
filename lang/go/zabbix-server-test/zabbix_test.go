package main

import (
	"log"
	"testing"
	"time"

	"github.com/cavaliercoder/go-zabbix"
)

const HostName string = "NetBSD Zabbix"
const HostID string = "10084"

type ZabbixTest struct {
	server   string
	user     string
	password string
	api      string
	session  *zabbix.Session
}

func (z *ZabbixTest) startSession() *zabbix.Session {
	session, err := zabbix.NewSession(z.api, z.user, z.password)
	if err != nil {
		log.Fatal(err)
	}

	return session
}

func (z *ZabbixTest) getHosts(params zabbix.HostGetParams) []zabbix.Host {
	hosts, err := z.session.GetHosts(params)
	if err != nil {
		log.Fatal(err)
	}

	return hosts
}

func (z *ZabbixTest) getItems(params zabbix.ItemGetParams) []zabbix.Item {
	items, err := z.session.GetItems(params)
	if err != nil {
		log.Fatal(err)
	}

	return items
}

func NewTest() *ZabbixTest {
	z := new(ZabbixTest)
	z.server = conf.Server
	z.user = conf.User
	z.password = conf.Password
	z.api = "http://" + conf.Server + "/zabbix/api_jsonrpc.php"
	z.session = z.startSession()

	return z
}

func TestHosts(t *testing.T) {
	var params zabbix.HostGetParams
	params.Filter = map[string]interface{}{"host": HostName}

	host := z.getHosts(params)[0]

	if host.DisplayName != HostName {
		t.Fatalf("Display name is %v but expected %v", host.DisplayName, HostName)
	}
	if host.HostID != HostID {
		t.Fatalf("Host ID is %v but expected %v", host.HostID, HostID)
	}
}

func TestPingLastClock(t *testing.T) {
	expectedItem := "Agent ping"
	now := int(time.Now().Unix()) // Epoch

	var params zabbix.ItemGetParams
	params.Host = HostName
	params.Filter = map[string]interface{}{"name": expectedItem}

	item := z.getItems(params)[0]
	if item.ItemName != expectedItem {
		t.Fatalf("\"%v\" is not \"%v\"", item.ItemName, expectedItem)
	}

	if now-item.LastClock > 60 {
		t.Fatalf("\"%v\" over 60 seconds from now", item.ItemName)
	} else if item.LastValue != "1" {
		t.Fatalf("Last value is \"%v\", ping was failed", item.LastValue)
	}
}
