# -*- coding: utf-8 -*-
# @Time : 2024/12/1 16:47
# @Author : 17507
# @File : debugtalk
# @Project : api-test
from readyaml import ReadyamlData

class Debugtaik:

    def __init__(self):
       self.read = ReadyamlData()

    def get_extract_data(self, node_name, randoms=None):
        '''
        获取extract.yaml中的数据
        :param node_name: 获取extract.yaml中的key值
        :param random: 随机读取extract.yaml中的数据
        :return:
        '''

        data = self.read.get_extract_yaml(node_name)
        print(data)
        if randoms is not None:
            data = int(randoms)
            data_value = {
                0 : randoms.choice(data)
            }

    def md5_params(self,params):
        print('实现md5加密')



if __name__ == '__main__':
    debug = Debugtaik()
    print(debug.get_extract_data('token'))


