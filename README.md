# wuvt-ansible

This is a repository of Ansible playbooks for hosts on WUVT's network. Currently everything assumes that networking is manually setup (internal interface on eth0, external on eth1 if applicable, and a bridged interface for the VM servers).

For files that contain secrets, you should encrypt them using Ansible Vault and also add them to .gitignore to ensure they are not stored in the repo (which is intentionally public). For a list of files that are missing from this repository that you may need, refer to .gitignore.

To execute a playbook on all machines, run 
```sh
ansible-playbook main.yml -i inventory --limit=workstations -K
```

(replacing "workstations" with the hosts group you would like to deploy on)

For more info, `man ansible-playbook` or see https://ansible.com/

Several things have not yet been added to Ansible, including the mail server.

### Client-side config required

In your client's config file, be sure to change the `remote_tmp` parameter
if you are working with an NFS mount using root squash.

```
remote_tmp  = /tmp/$USER-ansible/tmp
```

This is usually found in /etc/ansible/ansible.cfg.

### Troubleshooting

You may need to set the environment variable `ANSIBLE_SCP_IF_SSH=y` if you are
using an SSH proxy.

See ansible issue #13401 as to why.
