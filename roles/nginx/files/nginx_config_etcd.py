#!/usr/bin/python3

import os.path
import requests
import subprocess
try:
    import urllib.parse as urlparse
except:
    import urlparse

ETCD_URL = 'http://127.0.0.1:2379'
ROUTES_DIR = '/traefik/backends'
NGINX_CONFIG_FILE = '/etc/nginx/conf.d/etcd_upstreams.conf'


def generate_config(etcd_url, routes_dir):
    r = requests.get('{0}/v2/keys{1}/?recursive=true'.format(
        etcd_url, routes_dir))
    data = r.json()
    output = ""

    upstreams = {}

    if 'node' in data and 'nodes' in data['node']:
        for route in data['node']['nodes']:
            sanitized_route = route['key'].rsplit('/', 1)[1]
            sanitized_route = sanitized_route.split('.', 1)[0]
            urls = []

            if 'nodes' in route:
                for subkey in route['nodes']:
                    if 'nodes' in subkey and \
                            os.path.basename(subkey['key']) == 'servers':
                        for server in subkey['nodes']:
                            if 'nodes' in server:
                                for subkey2 in server['nodes']:
                                    if os.path.basename(subkey2['key']) == \
                                            'url':
                                        urls.append(subkey2['value'])

            upstreams[sanitized_route] = sorted(urls)

    for upstream, urls in sorted(upstreams.items()):
        output += "upstream {} {{\n".format(upstream)
        output += "    ip_hash;\n"

        for url in urls:
            u = urlparse.urlparse(url)
            output += "    server {};\n".format(u.netloc)

        output += "}\n"

    return output


if __name__ == '__main__':
    config = generate_config(ETCD_URL, ROUTES_DIR)
    with open(NGINX_CONFIG_FILE, 'w') as f:
        f.write(config)
        subprocess.call(['systemctl', 'reload', 'nginx.service'])

    while True:
        r = requests.get('{0}/v2/keys{1}?wait=true&recursive=true'.format(
            ETCD_URL, ROUTES_DIR))

        old_config = config
        config = generate_config(ETCD_URL, ROUTES_DIR)
        if config != old_config:
            with open(NGINX_CONFIG_FILE, 'w') as f:
                f.write(config)
                subprocess.call(['systemctl', 'reload', 'nginx.service'])
