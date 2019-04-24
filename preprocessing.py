"""Summary of class here.
   将train数据统计处理
"""


import os
import time
import pandas as pd
import datetime as dt
import os.path


# 读取和转换当天各个数段的进出情况
import const


def read_translate_train_data(data_path):
    print(time.strftime('%Y%m%d%H%M%S') + ": read_translate_train_data " + data_path + " Begin")
    result_table = pd.DataFrame([], columns=['stationID', 'startTime', 'endTime', 'inNums', 'outNums'])
    train_ori_data = pd.read_csv(data_path, usecols=['stationID', 'time', 'status'])

    # 分开进出情况
    train_ori_data[['status']] = train_ori_data[['status']].astype('str')
    train_ori_data = pd.get_dummies(train_ori_data, columns=['status'])
    train_ori_data = train_ori_data.rename(columns={'status_0': 'outNums', 'status_1': 'inNums'})
    train_ori_data['time'] = pd.to_datetime(train_ori_data['time'])

    all_time_df = pd.DataFrame([], columns=['startTime'])
    begin = train_ori_data['time'][0].replace(hour=0, minute=0, second=0)
    end = train_ori_data['time'][0].replace(hour=23, minute=50, second=0)
    d = begin
    delta = dt.timedelta(minutes=10)
    while d <= end:
        all_time_df.loc[all_time_df.shape[0] + 1] = {'startTime': d}
        d += delta
    # print(train_ori_data.info())
    # station分组处理
    group_station = train_ori_data.groupby('stationID', as_index=False)

    for stationId, group in group_station:
        # 对于每个station分开不同时间段的time 这里 '0:00' 需要添加吗？显示问题
        time_table = group.groupby(group['time'].map(
            lambda x: x - dt.timedelta(minutes=x.minute % 10, seconds=x.second)))['outNums', 'inNums'].sum()

        # 添加每人的时间，结束时间
        time_table['startTime'] = time_table.index
        # time_table = time_table.reset_index(drop=True)
        time_table = time_table.merge(all_time_df, how='right')
        time_table = time_table.fillna(0)
        time_table['stationID'] = stationId
        time_table['endTime'] = time_table['startTime'].map(lambda x: x + dt.timedelta(minutes=10))

        result_table = pd.concat([result_table, time_table], sort=False)

    # result_table.columns = ['endTime', 'startTime', 'stationID', 'outNums', 'inNums']
    # result_table = result_table[['stationID', 'startTime', 'inNums', 'outNums']]
    # print(result_table)
    print(time.strftime('%Y%m%d%H%M%S') + ": translate_train_data " + data_path + " End")
    return result_table.sort_values(by=['stationID', 'startTime']).reset_index(drop=True)


# 结合昨天和今天的特征
def combind_pre_and_now(yes_table, today_table):
    return pd.merge(today_table, yes_table, left_index=True, right_index=True, how='outer', suffixes=('', '_pre'))[
        ['stationID', 'startTime', 'endTime', 'inNums_pre', 'outNums_pre', 'inNums', 'outNums']]


# 拼接所有完成数据
def combind_all_post_data(read_path, save_path, save_name='train_data.csv'):
    # 获取当前路径
    cwd = os.getcwd()
    # 修改当前工作目录
    os.chdir(read_path)
    # 将该文件夹下的所有文件名存入列表
    csv_name_list = os.listdir()
    csv_name_list=[x for x in csv_name_list if os.path.splitext(x)[1] == ".csv"]
    # 读取第一个CSV文件并包含表头，用于后续的csv文件拼接
    df = pd.read_csv(csv_name_list[0])
    # 读取第一个CSV文件并保存
    df.to_csv(cwd + '\\' + save_path + '\\' + save_name, encoding="utf_8", index=False)



    # 循环遍历列表中各个CSV文件名，并完成文件拼接

    for f in csv_name_list:
        df = pd.read_csv(f)
        df.to_csv(cwd + '\\' + save_path + '\\' + save_name, encoding="utf_8", index=False, header=False, mode='a+')


def pre_processing_train_data(file_path_list):
    last = ''
    for i in range(len(file_path_list)):
        file_name = os.path.basename(file_path_list[i])
        now = read_translate_train_data(file_path_list[i])
        if i != 0:
            combind_pre_and_now(last, now).to_csv("data/Processed_data/" + file_name, index=False)
            print(time.strftime('%Y%m%d%H%M%S') + ": write to data/Processed_data/ " + file_name)

        last = now


if __name__ == '__main__':

    combind_all_post_data(read_path=const.PROCESSED_DATA_PATH , save_path=const.PROCESSED_DATA_PATH , save_name='train_data.csv')
    file_path_list = ['data/Metro_train/record_2019-01-01.csv', 'data/Metro_train/record_2019-01-02.csv',
                      'data/Metro_train/record_2019-01-03.csv', 'data/Metro_train/record_2019-01-04.csv',
                      'data/Metro_train/record_2019-01-05.csv', 'data/Metro_train/record_2019-01-06.csv',
                      'data/Metro_train/record_2019-01-07.csv', 'data/Metro_train/record_2019-01-08.csv',
                      'data/Metro_train/record_2019-01-09.csv', 'data/Metro_train/record_2019-01-10.csv',
                      'data/Metro_train/record_2019-01-11.csv', 'data/Metro_train/record_2019-01-12.csv',
                      'data/Metro_train/record_2019-01-13.csv', 'data/Metro_train/record_2019-01-14.csv',
                      'data/Metro_train/record_2019-01-15.csv', 'data/Metro_train/record_2019-01-16.csv',
                      'data/Metro_train/record_2019-01-17.csv', 'data/Metro_train/record_2019-01-18.csv',
                      'data/Metro_train/record_2019-01-19.csv', 'data/Metro_train/record_2019-01-20.csv',
                      'data/Metro_train/record_2019-01-21.csv', 'data/Metro_train/record_2019-01-22.csv',
                      'data/Metro_train/record_2019-01-23.csv', 'data/Metro_train/record_2019-01-24.csv',
                      'data/Metro_train/record_2019-01-25.csv']
    pre_processing_train_data(file_path_list)
