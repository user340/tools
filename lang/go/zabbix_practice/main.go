package main

import (
	"fmt"

	"github.com/cavaliercoder/go-zabbix"
)

func startSession(url string, user string, password string) *zabbix.Session {
	frontend := "http://" + url + "/zabbix/api_jsonrpc.php"
	session, err := zabbix.NewSession(frontend, user, password)
	if err != nil {
		panic(err)
	}

	return session
}
func showAPIVersion(session *zabbix.Session) {
	version, err := session.GetVersion()
	if err != nil {
		panic(err)
	}

	fmt.Printf("Connected to Zabbix API %v\n", version)
}

func getAllHostsFrom(session *zabbix.Session) []zabbix.Host {
	var params zabbix.HostGetParams
	hosts, err := session.GetHosts(params)
	if err != nil {
		panic(err)
	}

	return hosts
}

func showAllHosts(session *zabbix.Session) {
	hosts := getAllHostsFrom(session)

	for _, host := range hosts {
		fmt.Printf("%v\n", host.DisplayName)
	}
}

func getItemsFrom(session *zabbix.Session, host string) []zabbix.Item {
	var params zabbix.ItemGetParams
	params.Host = host
	items, err := session.GetItems(params)
	if err != nil {
		panic(err)
	}

	return items
}

func showItems(session *zabbix.Session, host string) {
	items := getItemsFrom(session, host)

	for _, item := range items {
		fmt.Printf("%v -- %v at %v\n", item.ItemName, item.LastValue, item.LastClock)
	}
}

func main() {
	session := startSession("192.168.1.100", "Admin", "zabbix")

	showAPIVersion(session)
	showAllHosts(session)
	showItems(session, "NetBSD Zabbix")
}
