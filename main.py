# 训练集交叉验证，得到平均值
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

import const
from feature_engineering import time_selection

if __name__ == '__main__':
    data_path = const.FEATURE_DATA_FILE_PATH
    data = pd.read_csv(data_path)
    feature_cols = ['stationID', 'day', 'time', 'inNums_pre', 'outNums_pre']
    label_cols = ['inNums', 'outNums']
    X = data[feature_cols]
    y = data[label_cols]
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1, train_size=0.7)
    # 生成scikit-learn的线性回归对象
    clf = LinearRegression(n_jobs=-1)
    # 开始训练
    clf.fit(X_train, y_train)
    # 用测试数据评估准确性
    accuracy = clf.score(X_test, y_test)
    print(accuracy)

    # 进行预测
    # forecast_set = clf.predict(X_lately)
    predict_data = time_selection(
        df=pd.read_csv(r'C:\Users\the_s\PycharmProjects\city_ai\data\Processed_data\record_2019-01-25.csv'))
    X_lately = predict_data[feature_cols]
    y_lately = predict_data[label_cols]
    forecast_set =  pd.DataFrame(clf.predict(X_lately))
    pd.merge(predict_data, forecast_set, left_index=True, right_index=True, how='outer').to_csv(const.RESULT_TEST_A_FILE_PATH)
    accuracy = clf.score(X_lately, y_lately)
    print(accuracy)
