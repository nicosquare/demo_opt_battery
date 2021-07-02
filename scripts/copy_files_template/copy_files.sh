#!/bin/bash

echo Pasando datos
if [ $1 ]; then
echo Path con datos
rsync -arv -e ssh --exclude-from='exclude-files.txt' ../../scripts ../../web-server root@$1:~/egeo_iot/
else
rsync -arv -e ssh --exclude-from='exclude-files.txt' ../../scripts ../../web-server root@192.168.3.1:~/egeo_iot/
fi
