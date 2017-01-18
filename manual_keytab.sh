#!/bin/sh
# This script shows how to manually add a host to the domain and fetch a keytab
# using the ipa tools. This is useful if you need to add a host to the domain
# that is running an OS that does not ship the ipa tools.

host=sasago.wuvt.vt.edu
public_ipv4=192.168.0.157
user=$(whoami)
ipa_server=zolitude.wuvt.vt.edu

ipa host-add $host --ip-address=$public_ipv4
ipa host-allow-create-keytab $host --users=$user
ipa-getkeytab -s $ipa_server -k $host.keytab -p host/$host
