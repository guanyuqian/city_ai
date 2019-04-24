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
const.PROCESSED_TRAIN_DATA_FILE_PATH = const.PROCESSED_DATA_PATH + 'train_data.csv'
const.PREDICT_RESULT_FILE_PATH = const.DATA_PATH + 'result.csv'
