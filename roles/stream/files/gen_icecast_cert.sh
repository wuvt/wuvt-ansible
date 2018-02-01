#!/bin/sh
basedir="/etc/letsencrypt/live/stream.wuvt.vt.edu"

install -o icecast2 -g icecast -m 600 $basedir/fullchain.pem /etc/icecast2/icecast_tls.pem
cat $basedir/privkey.pem >> /etc/icecast2/icecast_tls.pem

service icecast restart
