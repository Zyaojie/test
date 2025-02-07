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

    def write_yaml_data(self,value):
        '''写入数据到yaml文件
        ：param value: （dict）写入的数据
        ：return：
        '''
        file = None
        file_path = FILE_PATA['extract']
        if not os.path.exists(file_path):
            os.system(file_path)
        try:
            # file =  open(file_path,'a（a=追加读写，w=清空读写）',encoding='utf-8')    使用此方法打开文件后需要在最后添加关闭文件的操作
                # finally:
                #     file.close()
            with open(file_path, 'a', encoding='utf-8') as file:    #使用此方法打开文件不需要进行关闭文件的操作

                if isinstance(value,dict):
                    write_data = yaml.dump(value,allow_unicode=True,sort_keys=False)
                    file.write(write_data)
                else:
                    print('写入到【extract】的数据必须为字典类型！！！')
        except  Exception as e:
            print(e)

    def get_extract_yaml(self,node_name):
        '''
        读取接口提取的变量值
        :param node_name:yaml中的key值
        :return:
        '''
        if os.path.exists('../extract.yaml'):
            pass
        else:
            print('extract.yaml不存在')
            file = open('../extract.yaml', 'w')
            file.close()
            print('extract.yaml创建成功')


        with open('../extract.yaml', 'r', encoding='utf-8') as rf:
            extract_data = yaml.safe_load(rf)
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