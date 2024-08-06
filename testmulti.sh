#!/usr/bin/env bash
#
sudo sysctl -w net.ipv4.icmp_echo_ignore_broadcasts=0
sudo ip addr add 224.10.10.10/24 dev eth0 autojoin
sudo ip addr add 239.192.1.100/24 dev eth0 autojoin
sudo ip -f inet maddr show dev eth0
sudo ping -I eth0 224.10.10.10



