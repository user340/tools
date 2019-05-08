# QEMU-KVM

## RHEL

1. `yum install bridge-utils`
1. `brctl addbr br0`
1. Edit /etc/qemu-kvm/bridge.conf
1. `chmod 640 /etc/qemu-kvm/bridge.conf`
1. `chown root.qemu /etc/qemu-kvm/bridge.conf`
1. `sysctl -w net.ipv4.ip_forward=1`
1. `brctl addif br0 enp2s0`
1. `ip link set up dev br0`
1. `firewall-cmd --permanent --direct --passthrough ipv4 -I FORWARD -i br0 -j ACCEPT`
1. `firewall-cmd --permanent --direct --passthrough ipv4 -I FORWARD -o br0 -j ACCEPT`
1. `firewall-cmd --reload`

