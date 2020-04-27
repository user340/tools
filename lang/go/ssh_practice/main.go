package main

import (
	"fmt"

	"github.com/user340/tools/ssh/ssh"
)

func doSSHRemoteExec(command string) string {
	host := "localhost:22"
	user := "uki"
	key := "id_ed25519"

	client := ssh.SSHConnectTo(host, user, key)
	defer client.Close()

	session := ssh.CreateSessionFor(client)
	defer session.Close()

	result := ssh.RunCommandOnRemote(session, command)

	return result.String()
}

func main() {
	var commands [2]string = [2]string{"uname -a", "ls"}
	ch := make(chan string, 2)

	for i := 0; i < 2; i++ {
		go func(command string) {
			ch <- doSSHRemoteExec(command)
		}(commands[i])
		fmt.Println(<-ch)
	}
}
