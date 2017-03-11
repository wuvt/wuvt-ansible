#!/bin/sh
basedir="/etc/letsencrypt/live/stream.wuvt.vt.edu"

install -o icecast -g icecast -m 600 $basedir/fullchain.pem /etc/icecast_tls.pem
cat $basedir/privkey.pem >> /etc/icecast_tls.pem

service icecast restart
service darkice restart
