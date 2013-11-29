#!/bin/sh
cd /usr/local/src
svn co http://darkice.googlecode.com/svn/darkice/trunk darkice-read-only
cd darkice-read-only
./autogen.sh
./configure --with-faac-prefix=/usr/local
make
make install
