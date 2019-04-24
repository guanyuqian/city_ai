"""Summary of class here.
   特征工程
"""

# 线性回归

import pandas as pd

import os
import const


# 拼接所有完成数据
def combind_all_post_data(read_path, save_path):
    # 获取当前路径
    cwd = os.getcwd()
    # 修改当前工作目录
    os.chdir(read_path)
    # 将该文件夹下的所有文件名存入列表
    csv_name_list = os.listdir()
    csv_name_list = [x for x in csv_name_list if os.path.splitext(x)[1] == ".csv"]
    # 读取第一个CSV文件并包含表头，用于后续的csv文件拼接
    df = pd.read_csv(csv_name_list[0])
    # 读取第一个CSV文件并保存
    df.to_csv(cwd + '\\' + save_path, encoding="utf_8", index=False)
    # 循环遍历列表中各个CSV文件名，并完成文件拼接
    for f in csv_name_list:
        df = pd.read_csv(f)
        df.to_csv(cwd + '\\' + save_path, encoding="utf_8", index=False, header=False, mode='a+')
    print("merge over")

# 时间特征分离选取
def time_selection(processed_merge_data_path=None, feature_data_path=None,df=None):
    if df is None:
        df = pd.read_csv(processed_merge_data_path)
    df['startTime'] = pd.to_datetime(df['startTime'])
    df['day'] = df['startTime'].map(lambda x: x.day)
    #df['hour'] = df['startTime'].map(lambda x: x.hour)
    # 分钟数
    df['time'] = df['startTime'].map(lambda x: x.minute+x.hour*60)
    df = df[['stationID', 'day', 'time', 'inNums_pre', 'outNums_pre', 'inNums', 'outNums']]
    if feature_data_path==None:
        df.to_csv(feature_data_path, encoding="utf_8", index=False)
    print("time_selection over")
    return df



if __name__ == '__main__':
    # combind_all_post_data(read_path=const.PROCESSED_DATA_PATH, save_path=const.PROCESSED_MERGE_DATA_FILE_PATH)
    time_selection(const.PROCESSED_MERGE_DATA_FILE_PATH, const.FEATURE_DATA_FILE_PATH,None)
