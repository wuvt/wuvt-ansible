#!/bin/bash
DEBEMAIL="it@wuvt.vt.edu"
DEBFULLNAME="WUVT IT"
cd /opt/$1/src
tar cfz ../${1}-0.0.1.tar.gz *
dh_make -f  ../${1}-0.0.1.tar.gz

