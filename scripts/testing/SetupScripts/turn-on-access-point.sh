#!/bin/bash
echo "----------------------------CONFIGURING ACCESS POINT NETWORK-----------------------"

echo "[START] edit netplan files"

cat access-wifi-netplan.yaml > /etc/netplan/00-installer-config-wifi.yaml

echo "[FINISH] edit netplan files"

