package main

import (
	"fmt"

	"github.com/cavaliercoder/go-zabbix"
)

func startSession(url string, user string, password string) *zabbix.Session {
	session, err := zabbix.NewSession("http://"+url+"/zabbix/api_jsonrpc.php", user, password)
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

func showAllHosts(session *zabbix.Session) {
	var params zabbix.HostGetParams

	hosts, err := session.GetHosts(params)
	if err != nil {
		panic(err)
	}

	for _, host := range hosts {
		fmt.Printf("%v\n", host.DisplayName)
	}
}

func main() {
	session := startSession("192.168.1.100", "Admin", "zabbix")

	showAPIVersion(session)
	showAllHosts(session)
}
