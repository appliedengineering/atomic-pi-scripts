#!/bin/bash
echo "---------------------------------------SETUP SCRIPT--------------------------------------------"

echo "[START] network configure"
service hostapd stop
service hostapd start
service hostapd status

service isc-dhcp-server stop
service isc-dhcp-server start
service isc-dhcp-server status
echo "[END] network configure"

echo "[START] pin configure"
# give perms
chmod -R 777 /sys/class/gpio/

# setup pins
echo 332 > /sys/class/gpio/export

chmod -R 777 /sys/class/gpio/gpio332
echo "[END] pin configure"

read -p "Would you like to start network scripts? (yes/no)" continue && [[ $continue == [yY][eE][sS] ]] || exit 0 

echo "[START] network scripts"

cd /usr/local/bin/atomic-pi-scripts
cd Telementry
sudo -u ae-groundstation python3 ForwardingDevice.py

echo "[END] network scripts"

echo "-------------------------------------END SETUP SCRIPT------------------------------------------"

