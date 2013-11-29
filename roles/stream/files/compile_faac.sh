#!/bin/sh
cd /usr/local/src
rm faac-1.28.tar.gz
wget http://downloads.sourceforge.net/faac/faac-1.28.tar.gz
tar zxvf faac-1.28.tar.gz
cd /usr/local/src/faac-1.28
sed '126d' /usr/local/src/faac-1.28/common/mp4v2/mpeg4ip.h
./configure
make
make install
