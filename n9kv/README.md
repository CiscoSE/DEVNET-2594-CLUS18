# Nexus 9000v Vagrant Box
Download *nxosv-final.7.0.3.I7.3.box* from cisco.com to this directory

    vagrant box add base nxosv-final.7.0.3.I7.3.box
    vagrant up

# Configure the NXOSv image for NXAPI and boot variable

    printf "conf t\nfeature nxapi\nend" | vagrant ssh
    printf "conf t\nboot nxos bootflash:nxos.7.0.3.I7.3.bin\nend" | vagrant ssh
    printf "conf t\ncopy run start\nexit" | vagrant ssh

# Cautions
Please note that you will get an error about SSH when the box 
startup completes.  This is normal.


