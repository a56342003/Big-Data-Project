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
for i in $(seq $1 $2)
do
	bitcoin-cli getblock $(bitcoin-cli getblockhash "$i") | jq -c '.tx' | sed -e 's/[\[\"]//g' -e 's/\]//g' >> "${file1}"
	echo $i	
done



cat ${file1} | tr "\n" "," > ${file2}


number_of_tx=$(grep -o "," ${file2} | wc -l)


# get raw transaction detail from blockchain
for i in $(seq 1 $number_of_tx)
do
	bitcoin-cli decoderawtransaction $(bitcoin-cli getrawtransaction $(cat ${file2} | cut -d',' -f $i)) >> "bitcoin_transaction_$1_$2"

done

rm ${file1}
rm ${file2}

