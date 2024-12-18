#!/bin/bash          

for DIR in `ls ~/pCloudDrive/Photos/faglar`; do
    LOCATION=`echo ${DIR} | sed -E s/-[0-9]{6}$//`
    DATE=`echo ${DIR} | grep -o -E [0-9]{6}$`

    for FILE in `ls ~/pCloudDrive/Photos/faglar/${DIR}`; do
	echo ${LOCATION}\;${DATE}\;${FILE}
    done

done
