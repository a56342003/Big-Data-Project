# -*- coding: utf8 -*-

import time
from pyspark.sql import SparkSession

APP_NAME = 'project'
TX_FILE_ADDR = '/mnt/data/fedorabackup/project/SparkMidterm/tx/bitcoin_transaction_9*.json'
BLOCK_FILE_ADDR = '/mnt/data/fedorabackup/project/SparkMidterm/block/bitcoin_block_90001_100000.json'



def logging(message=''):
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),message)


def txVolume(txDF):
    '''
    txDF   : bitcoin transaction DataFrame
    return : RDD that contains list of (txid, txVolume) 
    '''
    # DataFrame to rdd
    # Take id and vout
    # Flaten subtransaction
    # Take tranding value in subtransaction
    # Sum up by transaction id
    
    return txDF.rdd\
               .map(lambda x: (x['txid'],x['vout']))\
               .flatMapValues(lambda subtx:subtx)\
               .map(lambda subtx:(subtx[0],subtx[1]['value']))\
               .reduceByKey(lambda x,y: x+y)

def blockVolume(blockDF, txDF):
    '''
    blockDF: bitcoin block DataFrame
    txDF   : bitcoin transaction DataFrame
    return : RDD that contains list of (height, TradingVolume) 
    '''
    
    tx_out = txVolume(txDF)
    
    # DataFrame to RDD
    # Take height and txid
    # Flatten txid
    # Swap txid and height
    # Join tx trading volume
    # Map only trading volume to height
    # Sum up by height
    
    return blockDF.rdd\
                  .map(lambda x: (x['height'],x['tx']))\
                  .flatMapValues(lambda x:x)\
                  .map(lambda x: (x[1],x[0]))\
                  .join(tx_out)\
                  .map(lambda x: x[1])\
                  .reduceByKey(lambda x,y: x+y)

                
if __name__ == '__main__':
    
    # Build spark session
    spark = SparkSession.builder.appName(APP_NAME).getOrCreate()
    
    # Read data
    logging('Reading data...')
    txDF = spark.read.json(TX_FILE_ADDR).cache()
    txDF.registerTempTable('txDF')
    
    block_file_addr = '/mnt/data/fedorabackup/project/SparkMidterm/block/bitcoin_block_90001_100000.json'
    blockDF = spark.read.json(BLOCK_FILE_ADDR).cache()
    blockDF.registerTempTable('blockDF')
    
    
    # Get trading volume
    logging('Computing trading volume...')
    trading_volume = blockVolume(blockDF, txDF)
    logging()
    print(trading_volume.collect()[0:10])
    logging('Complete!')