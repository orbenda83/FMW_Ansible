# Ansible playbooks for Oracle products  

1. Download latest epel-release rpm from  
> http://download-ib01.fedoraproject.org/pub/epel/7/x86_64/  
2. Install epel-release rpm:  
```bash
# rpm -Uvh epel-release*rpm
```
3. Install ansible rpm package:  
```bash
# yum install ansible
```

# To run the ansible playbook:
```bash
cd /software/ansible
# ansible-playbook <playbook location, i.e: playbooks/main.yml> --limit <ansible group from inventory, i.e. db-dev>  [-vv | for verbose]

# For example:
ansible-playbook playbooks/main.yml --limit db-dev -vv
```
