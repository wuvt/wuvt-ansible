#!/bin/sh
python uwsgiconfig.py --build centos
python uwsgiconfig.py --plugin plugins/python centos python
python uwsgiconfig.py --plugin plugins/gevent centos gevent
install -m0755 uwsgi /usr/bin/uwsgi
install -D -m0755 gevent_plugin.so /usr/lib64/uwsgi/
install -D -m0755 python_plugin.so /usr/lib64/uwsgi/

uwsgi --build-plugin https://github.com/unbit/uwsgi-sse-offload
install -D -m0755 sse_offload_plugin.so /usr/lib64/uwsgi/
