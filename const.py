# coding:utf-8

class _const:
    class ConstError(TypeError):
        pass

    class ConstCaseError(ConstError):
        pass

    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise self.ConstError("can't change const %s" % name)
        if not name.isupper():
            raise self.ConstCaseError('const name "%s" is not all uppercase' % name)
        self.__dict__[name] = value


import sys

sys.modules[__name__] = _const()

import const

const.DATA_PATH = 'data/'
const.PROCESSED_DATA_PATH = const.DATA_PATH + 'Processed_data/'
const.MERGE_DATA_FILE_NAME = 'merge_data.csv'
const.FEATURE_DATA_FILE_PATH = const.DATA_PATH + 'feature_data.csv'
const.PROCESSED_MERGE_DATA_FILE_PATH = const.DATA_PATH + const.MERGE_DATA_FILE_NAME

const.PREDICT_RESULT_FILE_PATH = const.DATA_PATH + 'result.csv'
const.TEST_A_PATH = const.DATA_PATH + 'Metro_testA/'
const.TEST_A_PROCESSED_FILE_PATH = const.TEST_A_PATH + 'merge_testA.csv'
const.RESULT_TEST_A_FILE_PATH = const.TEST_A_PATH + 'result_testA.csv'
