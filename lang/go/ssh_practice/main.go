package main

import (
	"fmt"

	"github.com/user340/tools/ssh/ssh"
)

func main() {
	host := "localhost:22"
	user := "uki"
	key := "id_ed25519"

	client := ssh.SSHConnectTo(host, user, key)
	defer client.Close()

	session := ssh.CreateSessionFor(client)
	defer session.Close()

	result := ssh.RunCommandOnRemote(session, "uname -a")
	fmt.Print(result.String())
}
