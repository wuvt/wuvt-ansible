#!/bin/bash
DEBEMAIL="it@wuvt.vt.edu"
DEBFULLNAME="WUVT IT"
cd /opt/PiFmRds/src
dpkg-buildpackage -us -uc
