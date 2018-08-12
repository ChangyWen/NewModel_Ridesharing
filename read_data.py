import csv
import pandas as pd
import numpy as np
from datetime import datetime

def read_riders(file_name) -> list:
    '''
    :param file_name:
    :return:
    '''
    inputfile = open(file_name, 'rb')
    data = pd.read_csv(inputfile, usecols=['tpep_pickup_datetime','tpep_dropoff_datetime','PULocationID', \
                                           'DOLocationID'], iterator= True)
    loop = True
    chunkSize = 10000
    chunks = []
    i = 0
    while loop:
        try:
            chunk = data.get_chunk(chunkSize)
            chunks.append(chunk)
            i += 1
            if i > 5:
                loop = False
        except StopIteration:
            loop = False
    data = pd.concat(chunks, ignore_index = True)
    # print(type(data))
    data = np.array(data)
    data = data.tolist()
    # print(type(data))
    # print(len(data))
    for i in range(len(data)):
        for j in range(2):
            data[i][j] = datetime.strptime(data[i][j], '%Y-%m-%d %H:%M:%S')

    return data

