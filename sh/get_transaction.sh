#!/bin/bash
# 
# This script will get bitcoin txid from given height of blocks
# Using bitcoin-cli
# 
# History:
#    First release by CTsai 2018/03/30

file1="file1_$1_$2"
file2="file2_$1_$2"

# get txid from blockchain
echo "==============Part1:${1} to ${2} start=============="


for i in $(seq $1 $2)
do
	bitcoin-cli getblock $(bitcoin-cli getblockhash "$i") | jq -c '.tx' | sed -e 's/[\[\"]//g' -e 's/\]//g' >> "${file1}"
done


echo "==============Part1:${1} to ${2} done=============="




cat ${file1} | tr "," "\n" > ${file2}

number_of_tx=$(wc -l ${file2})
echo "Height${1} to ${2}, number of tx: ${number_of_tx}"




echo "==============Part2:${1} to ${2} start=============="


while read line
do 
	bitcoin-cli decoderawtransaction $(bitcoin-cli getrawtransaction $(echo $line)) >> "bitcoin_transaction_$1_$2"
done < ${file2}


echo "==============Part2:${1} to ${2} done=============="

rm ${file1}
rm ${file2}
 
