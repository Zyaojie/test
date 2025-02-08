# -*- coding: utf-8 -*-
# @Time : 2024/12/1 16:47
# @Author : 17507
# @File : debugtalk
# @Project : api-test
from common.readyaml import ReadyamlData
import random


class Debugtaik:
    def __init__(self):
        self.read = ReadyamlData()

    def get_extract_order_data(self, data, randoms):
        if randoms not in [0, -1, -2]:
            return data[randoms - 1]

    def get_extract_data(self, node_name, randoms=None):
        '''
        获取extract.yaml中的数据
        :param node_name: 获取extract.yaml中的key值
        :param random: 随机读取extract.yaml中的数据
        :return:
        '''
        # 获取 extract.yaml 内容
        data = self.read.get_extract_yaml(node_name)

        # 输出调试信息，确认数据读取问题
        print(type(f"读取到的 data：{data}"))

        # 如果数据为空，则返回默认值
        if not data:
            print(f"警告：无法提取到 {node_name} 的数据，返回默认值")
            return []  # 返回空列表或其他默认值

        # 如果有随机参数，则随机选择数据
        if randoms is not None:
            randoms = int(randoms)
            data_value = {
                randoms: self.get_extract_order_data(data, randoms),
                0: random.choice(data),  # 随机读取
                -1: ', '.join(data),  # 读取全部
                -2: ', '.join(data).split(',')  # 将读取出来的数据转换为列表
            }
            data = data_value[randoms]

        return data

    def md5_params(self, params):
        return 'ABCDEFG123456' + str(params)


if __name__ == '__main__':
    debug = Debugtaik()
    print(debug.get_extract_data('product_id', -1))
