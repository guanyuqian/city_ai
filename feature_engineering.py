"""Summary of class here.
   特征工程
"""

# 线性回归
import datetime as dt
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
# 训练集交叉验证，得到平均值
from sklearn.model_selection import KFold

import const


# 时间特征分离选取
def time_selection():
    data_path = const.PROCESSED_TRAIN_DATA_FILE_PATH
    df = pd.read_csv(data_path)
    df['startTime'] = pd.to_datetime(df['startTime'])
    df['day'] = df['startTime'].map(lambda x: x.day)
    df['hour'] = df['startTime'].map(lambda x: x.hour)
    df['minute'] = df['startTime'].map(lambda x: x.minute)
    df = df[['stationID', 'day', 'hour', 'minute', 'inNums_pre', 'outNums_pre', 'inNums', 'outNums']]
    df.to_csv(const.PROCESSED_TRAIN_DATA_FILE_PATH, encoding="utf_8", index=False)


if __name__ == '__main__':
    # time_selection()
    data_path = const.PROCESSED_TRAIN_DATA_FILE_PATH
    data_train = pd.read_csv(data_path)
    predictors = ['stationID', 'day', 'hour', 'minute', 'inNums_pre', 'outNums_pre']
    # 初始化现行回归算法
    alg = LinearRegression()
    # 样本平均分成3份，3折交叉验证
    # kf = KFold(data_train.shape[0],n_folds=3,random_state=1)
    kf = KFold(n_splits=3, shuffle=False, random_state=1)

    predictions = []
    for train, test in kf.split(data_train):
        # The predictors we're using to train the algorithm.  Note how we only take then rows in the train folds.
        train_predictors = (data_train[predictors].iloc[train, :])
        # The target we're using to train the algorithm.
        train_target = data_train[['inNums', 'outNums']].iloc[train]
        # Training the algorithm using the predictors and target.
        alg.fit(train_predictors, train_target)
        # We can now make predictions on the test fold
        test_predictions = alg.predict(data_train[predictors].iloc[test, :])
        predictions.append(test_predictions)

    # The predictions are in three aeparate numpy arrays.	Concatenate them into one.
    # We concatenate them on axis 0,as they only have one axis.
    predictions = np.concatenate(predictions, axis=0)

    # Map predictions to outcomes(only possible outcomes are 1 and 0)
    predictions = pd.DataFrame(predictions, columns=['inNums', 'outNums'])
    result_cvs = pd.merge(pd.DataFrame(predictions, columns=['inNums', 'outNums']), data_train[['inNums', 'outNums']],
                          left_index=True, right_index=True,
                          how='outer', suffixes=('_pre', ''))
    result_cvs['inNums_res'] = (predictions['inNums'] - data_train['inNums']).map(lambda x: x ** 2)
    result_cvs['outNums_res'] = (predictions['outNums'] - data_train['outNums']).map(lambda x: x ** 2)
    result_cvs.to_csv(const.PREDICT_RESULT_FILE_PATH, encoding="utf_8", index=False)
    accuracy = result_cvs[['inNums_res', 'outNums_res']]
    print("准确率为: ", accuracy)
