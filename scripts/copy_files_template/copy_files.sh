

if [ $path ];
then
rsync -av -e ssh --exclude-from='exclude-files.txt' ../../../egeo_iot root@$path:~/
else
rsync -av -e ssh --exclude-from='exclude-files.txt' ../../../egeo_iot root@192.168.3.1:~/
fi

