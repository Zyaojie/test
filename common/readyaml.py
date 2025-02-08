# -*- coding: utf-8 -*-
# @Time : 2024/12/1 12:56
# @Author : 17507
# @File : readyaml
# @Project : api-test
import os

import yaml
from conf.setting import FILE_PATA

def get_testcase_yaml(file):
    '''
    获取yaml文件的数据
    :param file: yaml文件的路径
    :return:
    '''

    try:
        with open(file, 'r' ,encoding='utf-8') as f:
            yaml_data = yaml.safe_load(f)
            return yaml_data
    except Exception as e:
        print(f'读取yaml文件出错：{str(e)}')

class ReadyamlData:
    '''读取yaml数据，以及写入数据到yaml文件'''
    def __init__(self, yaml_fine=None):
        if yaml_fine is not  None:
            self.yaml_fine = yaml_fine
        else:
            self.yaml_fine = 'login.yaml'

    def write_yaml_data(self, value):
        '''写入数据到yaml文件
        ：param value: （dict）写入的数据
        ：return：
        '''
        file_path = 'D:/api-test/extract.yaml'  # 使用统一路径
        print(f"写入文件的路径：{file_path}")  # 打印文件路径，确认是否正确

        # 确保文件夹存在
        folder_path = os.path.dirname(file_path)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)  # 创建文件夹

        try:
            # 先读取文件内容
            with open(file_path, 'r', encoding='utf-8') as file:
                content = yaml.safe_load(file)

            # 如果内容是字典，更新其中的键值对
            if isinstance(content, dict) and isinstance(value, dict):
                content.update(value)
            else:
                content = value  # 如果不是字典，直接覆盖原有内容

            # 写入修改后的内容
            with open(file_path, 'w', encoding='utf-8') as file:
                write_data = yaml.dump(content, allow_unicode=True, sort_keys=False)
                file.write(write_data)
                print(f"写入的数据：{write_data}")  # 打印写入的数据，帮助调试

        except Exception as e:
            print(e)

    def get_extract_yaml(self, node_name):
        '''
        读取接口提取的变量值
        :param node_name: yaml中的key值
        :return:
        '''
        # 检查文件路径是否正确
        file_path = '../extract.yaml'
        if not os.path.exists(file_path):
            print(f"extract.yaml 不存在，正在创建：{file_path}")
            with open(file_path, 'w', encoding='utf-8') as file:
                file.close()
            print('extract.yaml 创建成功')

        # 读取 YAML 文件
        with open(file_path, 'r', encoding='utf-8') as rf:
            extract_data = yaml.safe_load(rf)

        print(f"读取到的 extract.yaml 内容：{extract_data}")  # 输出文件内容，帮助调试

        # 检查 key 是否存在
        if node_name not in extract_data:
            print(f"警告：extract.yaml 中没有找到 {node_name} 这个键")
            return []  # 返回空列表或默认值

        return extract_data[node_name]


if __name__ == '__main__':
    res = get_testcase_yaml('../testcase/Login/login.yaml')[0]
    url = res['baseInfo']['url']
    new_url = 'http://127.0.0.1:8787//'+url
    method = res['baseInfo']['method']
    header = res['baseInfo']['header']
    data = res['testCase'][0]['data']
    from sendrequests import SendRequest
    send = SendRequest()
    send = send.post(url=new_url,data=data,header=header)
    # print(send)

    # token = send.get('token')
    #
    # write_data = {}
    # write_data['Token'] = token

    read = ReadyamlData()
    # read.write_yaml_data(write_data)

    re = read.get_extract_yaml('token')
    print(re)


    #pyrhon常用的数据类型：str(字符串) list（列表） dict（字典） set（集合） tuple（元祖）
    #json序列化和反序列化
    #json序列化，就是将python的字典类型转换成字符串
    #json反序列化，就是将python的字符串转换成字典