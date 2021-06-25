#!/bin/ash

# Creating swap file
echo Create swap file
dd if=/dev/zero of=/overlay/swap.page bs=1M count=512
mkswap /overlay/swap.page
free

#Automatically Mount the SD using Block + Fstab
echo Automatically Mount the SD using Block + Fstab
block detect > /etc/config/fstab
uci show fstab
uci set fstab.@mount[0].enabled='1'
uci commit fstab
/etc/init.d/fstab enable
block mount


#Change rc.local
sed -i '/exit/d' /etc/rc.local
echo Changing rc.local
echo "### activate the swap file on an external SD" >> /etc/rc.local
echo 'SWAP_FILE="/mnt/mmcblk0p1/swap.page"' >> /etc/rc.local
echo 'if [ -e "$SWAP_FILE" ]; then' >> /etc/rc.local
echo -e '\tswapon $SWAP_FILE' >> /etc/rc.local
echo 'fi' >> /etc/rc.local
echo -e '\nexit 0' >> /etc/rc.local
reboot

