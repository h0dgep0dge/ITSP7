#!/bin/bash
# Sets up veth

ip netns add router

ip link add type veth # veth0 <-> veth1
ip link add type veth # veth2 <-> veth3

ip link set veth1 netns router
ip link set veth2 netns router

ip -n router link set veth1 up
ip -n router link set veth2 up

ip -n router addr add 2.2.2.2/32 dev veth1
ip -n router route add 1.1.1.1/32 dev veth1

ip -n router addr add 3.3.3.3/32 dev veth2
ip -n router route add 4.4.4.4/32 dev veth2

ip -n router route add 48.0.0.0/16 via 4.4.4.4
ip -n router route add 16.0.0.0/16 via 1.1.1.1
ip netns exec router sysctl -w net.ipv4.ip_forward=1


ip link set veth0 up
ip link set veth3 up

cd /opt/v3.06
#exec /bin/bash
./t-rex-64 --cfg /etc/routed_trex_cfg.yaml -i
