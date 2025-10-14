#!/bin/bash
# Sets up veth

ip netns add monitor
ip -n monitor link add br0 type bridge

ip link add type veth
ip link add type veth

ip link set veth1 netns monitor
ip link set veth2 netns monitor

ip -n monitor link set veth1 master br0
ip -n monitor link set veth2 master br0
ip -n monitor link set veth1 up
ip -n monitor link set veth2 up
ip -n monitor link set br0 up

ip link set veth0 up
ip link set veth3 up


cd /opt/v3.06
./t-rex-64 -i -c 4
