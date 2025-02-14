import csv
from conf.setting import DIR_PATH
import os
from common.recordlog import logs
def read_csv_data(file_name):
    '''
    获取csv数据
    :param file_name: csv文件名
    :return: csv数据
    '''
    try:
        with open(os.path.join(DIR_PATH,'data',file_name),'r',encoding='utf-8') as f:
            csv_reader = csv.reader(f)
            for value in csv_reader:
                print(value)
    except Exception as e:
        logs.error(e)


if __name__ == '__main__':
    print(read_csv_data)