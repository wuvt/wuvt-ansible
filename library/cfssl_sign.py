#!/usr/bin/python

import base64
import binascii
import hashlib
import hmac
import json
import requests
import urlparse

from ansible.module_utils.basic import AnsibleModule


# TODO
DOCUMENTATION = '''
---
module: cfssl_sign
short_description: Signs a CSR using the cfssl API.
description:
    - The M(cfssl_sign) module signs a certificate signing request (CSR) using the cfssl API.
options:
  endpoint:
    description:
      - URL to the remote cfssl server endpoint. Both http and https are supported.
    required: true
    default: null
  csr:
    description:
      - Path to a file containing the certificate signing request.
    required: true
    default: null
  dest:
    description:
      - Path to the file where the signed certificate will be written.
    required: true
    default: null
  auth_key:
    description:
      - Authentication key used to generate a token for authenticating against the cfssl endpoint. Currently, only standard authentication is supported (HMAC-SHA256).
    required: false
    default: null
  endpoint_ca:
    description:
      - Path to the CA certificate used for validating the remote cfssl server's certificate. If not provided, the default CA trust store will be used.
    required: false
    default: null
  label:
    description:
      - The label to provide to the cfssl endpoint. This is only necessary when using cfssl's multirootca server.
    required: false
    default: null
  profile:
    description:
      - The profile to provide to the cfssl endpoint.
    required: false
    default: null
author:
    - "mutantmonkey"
'''


def main():
    module = AnsibleModule(
        argument_spec=dict(
            endpoint=dict(required=True),
            csr=dict(required=True, type='path'),
            dest=dict(required=True, type='path'),
            auth_key=dict(default=None),
            endpoint_ca=dict(default=None, type='path'),
            label=dict(default=None),
            profile=dict(default=None),
        ),
        supports_check_mode=False
    )

    endpoint = module.params['endpoint']
    auth_key = module.params['auth_key']
    csr = module.params['csr']
    dest = module.params['dest']
    endpoint_ca = module.params['endpoint_ca']

    request = {
        'certificate_request': open(csr).read(),
    }

    for arg in ('label', 'profile'):
        if module.params[arg] is not None:
            request[arg] = module.params[arg]

    if endpoint_ca is not None:
        verify = endpoint_ca
    else:
        verify = True

    if auth_key is not None:
        h = hmac.new(binascii.unhexlify(auth_key), json.dumps(request),
                     hashlib.sha256)

        r = requests.post(
            urlparse.urljoin(endpoint, 'api/v1/cfssl/authsign'),
            data=json.dumps({
                'token': base64.b64encode(h.digest()),
                'request': base64.b64encode(json.dumps(request)),
            }),
            verify=verify,
        )
    else:
        r = requests.post(
            urlparse.urljoin(endpoint, 'api/v1/cfssl/sign'),
            data=json.dumps(request),
            verify=verify,
        )

    response = r.json()
    if response['success'] is True:
        with open(dest, 'w') as f:
            f.write(response['result']['certificate'].strip())
        module.exit_json(changed=True)
    else:
        module.fail_json(msg="Failed to sign certificate.",
                         errors=response['errors'])


if __name__ == '__main__':
    main()
