IMGLIST=`cat url_list_CB1300_b.lst`

for i in ${IMGLIST}
do
 wget $i
 sleep 1
done
