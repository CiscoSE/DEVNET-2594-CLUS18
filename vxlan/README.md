# Ansible playbook for VXLAN fabrics
Ansible VXLAN playbooks borrowed heavily from Matt Tarkington GitHub repo: 
https://github.com/mtarking/cisco-programmable-fabric

Adapted heavily to support my personal lab gear and DEVNET Sandbox.

# Usage
ansible-playbook -i hosts.sandbox.yml vxlan.yml

# Repo Notes
"Hosts" with the nx-osv9000 based names refer to DEVNET Sandbox switches.

Developed and tested with Ansible 2.4. Ansible 2.5 introduced new, preferred
methods for connections (network_cli). So, if you are using radically newer
versions of Ansible, this set of plays may need some adaptation.

