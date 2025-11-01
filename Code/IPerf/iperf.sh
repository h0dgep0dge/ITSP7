#!/bin/bash


ip netns add client
ip link set enp11s0 netns client
ip -n client link set lo up
ip -n client link set enp11s0 up
ip -n client addr add 192.168.20.10/24 dev enp11s0
ip -n client route add default via 192.168.20.1

ip netns add server
ip link set enp12s0 netns server
ip -n server link set lo up
ip -n server link set enp12s0 up
ip -n server addr add 4.4.4.4/32 dev enp12s0
ip -n server route add 3.3.3.3/32 dev enp12s0
ip -n server route add default via 3.3.3.3
ip netns exec server iperf3 -D -s
