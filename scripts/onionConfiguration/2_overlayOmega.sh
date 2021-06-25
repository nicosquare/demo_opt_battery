#!/bin/ash

# Formatting SD
# umount /tmp/mounts/SD-P1
# umount /tmp/mounts/mmcblk0p1

opkg update # Actualiza paquetes de Onion Omega
umount /mnt/mmcblk0p1 # Desmonta sdcard
echo y | mkfs.ext4 /dev/mmcblk0p1

#Mounting the External Storage Device
echo Mounting SD
mount /dev/mmcblk0p1 /mnt/
tar -C /overlay -cvf - . | tar -C /mnt/ -xf -
umount /mnt/

#Automatically Mount /overlay on Startup
echo block detect routine
block detect > /etc/config/fstab

#Change fstab file parameters
echo Change fstab file parameter
sed -i -e 's!/mnt/mmcblk0p1!/overlay!;/enabled/s/0/1/' /etc/config/fstab
echo rebooting, please check if the onion reboot correctly
reboot

