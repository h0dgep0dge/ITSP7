#!/bin/bash
# Sets up veth

ip netns add monitor

ip link add type veth
ip link add type veth

ip link set veth1 netns monitor
ip link set veth2 netns monitor

ip -n monitor link set veth1 up
ip -n monitor link set veth2 up

ip -n monitor addr add 2.2.2.2/32 dev veth1
ip -n monitor route add 1.1.1.1/32 dev veth1

ip -n monitor addr add 3.3.3.3/32 dev veth2
ip -n monitor route add 4.4.4.4/32 dev veth2

ip -n monitor route add 48.0.0.0/16 via 4.4.4.4
ip -n monitor route add 16.0.0.0/16 via 1.1.1.1
ip netns exec monitor sysctl -w net.ipv6.conf.all.forwarding=1


ip link set veth0 up
ip link set veth3 up

cd /opt/v3.06
#exec /bin/bash
./t-rex-64 --cfg /etc/bridged_trex_cfg.yaml -i
