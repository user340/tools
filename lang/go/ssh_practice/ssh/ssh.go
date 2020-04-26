package ssh

import (
	"bytes"
	"fmt"
	"io/ioutil"
	"log"
	"os"
	"syscall"

	"golang.org/x/crypto/ssh"
	"golang.org/x/crypto/ssh/terminal"
)

func findPrivateKey(privatekey string) []byte {
	key, err := ioutil.ReadFile(os.Getenv("HOME") + "/.ssh/" + privatekey)
	if err != nil {
		log.Fatalf("Unable to read private key: %v", err)
	}

	return key
}

func readPassphraseFromStdin() []byte {
	fmt.Print("Enter passphrase: ")

	passphrase, err := terminal.ReadPassword(syscall.Stdin)
	if err != nil {
		log.Fatalf("Unable to read passphrase from STDIN: %v", err)
	}

	fmt.Println()
	return passphrase
}

func parsePrivateKeyWithPassphraseFromKeyboard(key []byte) ssh.Signer {
	passphrase := readPassphraseFromStdin()

	signer, err := ssh.ParsePrivateKeyWithPassphrase(key, passphrase)
	if err != nil {
		log.Fatalf("Unable to parse private key with passphrase: %v", err)
	}

	return signer
}

func parsePrivateKey(key []byte) ssh.Signer {
	signer, err := ssh.ParsePrivateKey(key)
	if err != nil {
		return parsePrivateKeyWithPassphraseFromKeyboard(key)
	}

	return signer
}

func loadConfig(signer ssh.Signer, user string) *ssh.ClientConfig {
	config := &ssh.ClientConfig{
		User: user,
		Auth: []ssh.AuthMethod{
			ssh.PublicKeys(signer),
		},
		HostKeyCallback: ssh.InsecureIgnoreHostKey(),
	}

	return config
}

func connectTo(host string, config *ssh.ClientConfig) *ssh.Client {
	client, err := ssh.Dial("tcp", host, config)
	if err != nil {
		log.Fatalf("Unable to connect: %v", err)
	}

	return client
}

// SSHConnectTo return *ssh.Client
func SSHConnectTo(host string, user string, privatekey string) *ssh.Client {
	key := parsePrivateKey(findPrivateKey(privatekey))
	return connectTo(host, loadConfig(key, user))
}

// CreateSessionFor return *ssh.Session
func CreateSessionFor(client *ssh.Client) *ssh.Session {
	session, err := client.NewSession()
	if err != nil {
		log.Fatalf("Failed to create session: %v", err)
	}

	return session
}

// RunCommandOnRemote returns bytes.Buffer which contains STDOUT on remote
func RunCommandOnRemote(session *ssh.Session, command string) bytes.Buffer {
	var buf bytes.Buffer
	session.Stdout = &buf
	if err := session.Run(command); err != nil {
		log.Fatalf("Failed to run: %v", err)
	}

	return buf
}
