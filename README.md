## wuvt-ansible
This is a repository of ansible playbooks for hosts on WUVT's network. Currently everything assumes that networking is manually setup (internal interface on eth0, external on eth1 if applicable, and a bridged interface for the VM servers).

Add files containing passwords to .gitignore before staging so they are not stored in the repo.

To execute a playbook on all machines, run 

    "ansible-playbook main.yml -i hosts.cfg --limit=workstations -K"

(replacing "workstations" with the hosts group you would like to deploy on)

For more info, man ansible-playbook or see http://ansible.cc

Note that RHEL systems prior to RHEL6 require bootstrapping, as they come with 
python <= 2.4, which lacks python-simplejson. The bootstrap.sh script will run 
this on all machines in the "rhel5" category.

Several things have not yet been added to ansible, including the mail server

### Client-side config required

In your client's config file, be sure to change the `remote_tmp` parameter
if you are working with an NFS mount using root squash.

```
remote_tmp  = /tmp/$USER-ansible/tmp
```

This is usually found in /etc/ansible/ansible.cfg.

### Troubleshooting

You may need to set the environment variable ANSIBLE_SCP_IF_SSH=y if you are
using an SSH proxy.

See ansible issue #13401 as to why.


