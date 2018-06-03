# -*- coding: utf8 -*-

import time
from pyspark.sql import Row
from pyspark.sql import SparkSession

APP_NAME = 'dataCleanging'
BLOCK_FILE_ADDR = 'gs://nccu-bigdata/bigdata/*'
OUTPUT_PATH = 'gs://nccu-bigdata/output/'


def logging(message=''):
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),message)

    
def rearrangeRow(cols):
    row = cols[1][0]
    volume = cols[1][1][0]
    txNumber = cols[1][1][1]
    rowDict = row.asDict()
    rowDict['volume'] = volume
    rowDict['txNumber'] = txNumber
    return Row(**rowDict)

def txVolume(voutList):
    vol=0
    for vout in voutList:
        vol += vout[-1]        
    return vol

def cleanData(df):
    
    txvol = df.rdd\
            .map(lambda x: (x['height'], x['tx']))\
            .flatMapValues(lambda x:x)\
            .mapValues(lambda x:txVolume(x['vout']))\
            .reduceByKey(lambda x,y:x+y)

    txlen = df.rdd\
            .map(lambda x: (x['height'], x['tx']))\
            .flatMapValues(lambda x:x)\
            .mapValues(lambda x:len(x['vout']))\
            .reduceByKey(lambda x,y:x+y)

    txdetail = txvol.join(txlen)
    
    resultDF= df.drop('tx').rdd\
            .map(lambda x: (x['height'],x))\
            .join(txdetail)\
            .map(rearrangeRow)\
            .toDF()
            
    return resultDF
            
    

                
if __name__ == '__main__':
    
    # Build spark session
    spark = SparkSession.builder.appName(APP_NAME).getOrCreate()
    
    tic = time.time()
    # Read data
    logging('Reading data...')
    blockDF = spark.read.json(BLOCK_FILE_ADDR).cache()
    
    
    # Get trading volume
    logging('Computing trading volume...')
    resultDF = cleanData(blockDF)
    
    resultDF.write.csv(OUTPUT_PATH ,mode='append')
    toc = time.time()
    
    
    logging('Complete!')
    logging('Time consumed: {0:.2f}sec'.format(toc-tic))
    logging('Output path: {}'.format(OUTPUT_PATH))

    spark.stop()

