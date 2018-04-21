#!/bin/bash
#
# This script will get block from bitcoin blockchain

start=$1
end=$2
echo '' > bitcoin_block_${start}_${end}
for i in $(seq ${start} ${end})
do
	bitcoin-cli getblock $(bitcoin-cli getblockhash ${i}) 2 | jq -c '.' >> bitcoin_block_${start}_${end}
done
