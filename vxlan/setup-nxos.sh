#!/bin/sh

echo "At each password prompt, enter the password for each of the switches:"

for host in $(awk -F: '/ansible_host/ { print $2;}' hosts.sandbox.yml); do 
     echo
     echo "*** CONFIGURING ${host} ***"
     echo
     printf "configure terminal\n
             feature nxapi\n
             nxapi http port 80\n
             feature icam\n
             boot nxos bootflash:nxos.9.2.1.bin\n
             end\n
             copy running-config startup-config\n
             exit\n" | ssh cisco@${host}
done
