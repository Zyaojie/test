# -*- coding: utf-8 -*-
# @Time : 2024/12/1 16:47
# @Author : 17507
# @File : debugtalk
# @Project : api-test
from readyaml import ReadyamlData
import random

class Debugtaik:
    def __init__(self):
       self.read = ReadyamlData()

    def get_extract_order_data(self,data,randoms):
        if randoms not in [0,-1,-2]:
            return data[randoms - 1]


    def get_extract_data(self, node_name, randoms=None):
        '''
        获取extract.yaml中的数据
        :param node_name: 获取extract.yaml中的key值
        :param random: 随机读取extract.yaml中的数据
        :return:
        '''

        data = self.read.get_extract_yaml(node_name)
        if randoms is not None:
            irandoms = int(randoms)
            data_value = {
                randoms: self.get_extract_order_data(data,randoms),
                0 : random.choice(data),#随机读取
                -1: ', '.join(data),#读取全部
                -2: ', '.join(data).split(',')#将读取出来的数据转换为列表
            }
            data = data_value[randoms]
        return data


    def md5_params(self,params):
        print('实现md5加密')



if __name__ == '__main__':
    debug = Debugtaik()
    print(debug.get_extract_data('product_id',1))


