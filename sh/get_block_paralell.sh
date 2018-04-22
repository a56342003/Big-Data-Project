#!/bin/bash
#
# This script will get bitcoin block detail from given height
# by calling get_block.sh multiple times
#  



start_of_height=$1
end_of_height=$2
number_of_parallel=$3

interval=$(((${end_of_height}-${start_of_height}+1)/${number_of_parallel}))
echo ${interval}

number_of_parallel=$((${3}-1))

for i in $(seq 1 ${number_of_parallel})
do
        (echo "No.${i} start"
        echo "Height:${start_of_height}"
        sh ./get_block.sh ${start_of_height} $((${start_of_height}+${interval}-1)))&
        start_of_height=$((${start_of_height}+${interval}))

        if [ $((i%10)) == 0 ];then
                wait
        fi
done

number_of_last=$3

(echo "No.${number_of_last} start"
echo "Height:${start_of_height}"
sh ./get_block.sh ${start_of_height} ${end_of_height})&

wait

echo "done"
