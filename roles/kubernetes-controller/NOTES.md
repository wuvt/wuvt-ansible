The service accounts in the kube-system namespace are not separated by role.
Instead, the system services either use certificate-based authentication, the
default kube-system service account, or no authentication at all.

## Certificate-based authentication
    * `kube-proxy` on workers

## Default kube-system service account
    * `system:dns`
    * `system:logging`
    * `system:monitoring`

## No authentication (local access only)
    * `system:controller_manager`
    * `system:scheduler`
    * `kube-proxy` on controller
