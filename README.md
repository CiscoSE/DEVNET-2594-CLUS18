# DEVNET-2594-CLUS18
Example code for my (Tim Miller) CLUS Orlando 2018 DEVNET-2594 
session : "Leveraging NX-APIs for Customized Operational Analytics"

# Directory Layout
- n9kv : files related to the Vagrant box for the Nexus 9000v.
  This includes the Python scripts required to set up the iCAM
  functionality.

- vxlan : Ansible playbook to configure the DEVNET Sandbox
  "Open NXOS with VIRL"

- nxapi_cli : 4 different demo script scenarios with progressive
  functionality of metric generation, collection, and visualization

# How to use this repository
Some of the demo scripts are running locally on your laptop
against a NXOSv image (deployed as a Vagrant box).  These demos
are "step-01", "step-02", and "step-03" in the "nxapi_cli" directory.
For those demos, you'll need to follow the [n9kv instructions](n9kv/README.md)
to provision the Vagrant box prior to running the demos.

Other demo scripts ("step-04") are designed to run against the
DEVNET Sandbox environment.  To use these demo scripts, you'll need
to first reserve a DEVNET Sandbox environment at https://devnetsandbox.cisco.com/.
Once the sandbox is provisioned, you'll need to VPN into the sandbox
environment and follow the instructions in the [vxlan instructions](vxlan/README.md) 
file.

Each directory has a README.md file with instructions on how to use
the content in each directory.

# Versions
- Ansible : 2.5.4

- Python : 3.6.5

- NX-OS 9000v (local laptop) : 7.0(3)I7(3)

- NX-OS 9000v (DEVNET Sandbox "Open NX-OS with Nexus 9Kv") : 7.0(3)I6(1)

