#!/bin/sh
for i in $(seq 1 2); do
	fleetctl stop wuvt-site-prod-discovery@$i.service
	sleep 2
	fleetctl stop wuvt-site-prod@$i.service
	sleep 2
	fleetctl start wuvt-site-prod@$i.service
	sleep 2
	fleetctl start wuvt-site-prod-discovery@$i.service
	sleep 10
done
