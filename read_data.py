import os
import time
import pandas as pd

class DataReader():
    def __init__(self):
        self.root_path = './datalab'
        self.train_path = os.path.join(self.root_path, 'Metro_train')
        self.testA_path = os.path.join(self.root_path, 'Metro_trainA')
        self.testB_path = os.path.join(self.root_path, 'Metro_trainB')
        self.testC_path = os.path.join(self.root_path, 'Metro_trainC')

    # 获取某一路径下的所有文件名
    def get_file_names(self, path):
        file_names = []

        for file in os.listdir(path):
            file_path = os.path.join(path, file)   
            file_names.append(file_path) 
        return file_names

    # 给定一个时间的字符串，求出其所在时间片

    # 统计某一个天各站点各时刻的进出人数
    def compute_num(self, file_name):
        file = pd.read_csv(file_name)

        # [暂时]删除多余的列
        file = file.drop(['payType'], axis=1)
        file = file.drop(['deviceID'], axis=1)
        file = file.drop(['userID'], axis=1)
        file = file.drop(['lineID'], axis=1)

        #时间格式整理
        time_zero = time.mktime(time.strptime(file['time'][0].split()[0] + ' 00:00:00', '%Y-%m-%d %H:%M:%S'))
        new_times = []
        for old_time in file['time']:
             new_times.append(int((time.mktime(time.strptime(old_time, '%Y-%m-%d %H:%M:%S')) - time_zero)/600))
        del file['time']
        file.loc[:, 'time'] = pd.Series(new_times)

        print(file.head(10))

data = DataReader()
file_names = data.get_file_names(data.train_path)
data.compute_num(file_names[0])

# print(time.mktime(time.strptime('2018-9-30 11:32:23', '%Y-%m-%d %H:%M:%S')) - time.mktime(time.strptime('2018-9-30 11:00:00', '%Y-%m-%d %H:%M:%S')))



