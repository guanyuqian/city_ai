import datetime
import os
import time
from concurrent.futures import ProcessPoolExecutor
from math import ceil
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


# 读取和转换当天各个数段的进出情况
def read_translate_train_data(data_path):
    result_table = pd.DataFrame([], columns=['stationID', 'startTime', 'status_0', 'status_1'])
    train_ori_data = pd.read_csv(data_path, usecols=['stationID', 'time', 'status'])

    # 分开进出情况
    train_ori_data[['status']] = train_ori_data[['status']].astype('str')
    train_ori_data = pd.get_dummies(train_ori_data, columns=['status'])

    # station分组处理
    group_station = train_ori_data.groupby('stationID', as_index=False)
    for stationId, group in group_station:
        # 对于每个station分开不同时间段的time
        time_table = group.groupby(group['time'].map(lambda x: x[:15] + '0'))['status_0', 'status_1'].sum()
        time_table['stationID'] = stationId
        time_table['startTime'] = time_table.index
        time_table = time_table.reset_index(drop=True)
        result_table = pd.concat([result_table, time_table])

    # 改变特征顺序和名字
    # result_table.columns = ['stationID', 'outNums', 'inNums', 'startTime']
    # result_table = result_table[['stationID', 'startTime', 'inNums', 'outNums']]
    # print(result_table)
    return result_table


if __name__ == '__main__':
    print(read_translate_train_data('data/Metro_testA/testA_record_2019-01-28.csv'))
    pd.set_option('display.width', None)
