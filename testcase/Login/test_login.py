# -*- coding: utf-8 -*-
# @Time : 2024/12/8 15:41
# @Author : 17507
# @File : test_login
# @Project : api-test
import time

import pytest


@pytest.fixture(scope="function",autouse=True ,params=['北京', '广州','深圳'],ids=['BJ','GZ','SZ'],name='test3')
def fixture_test(request):
    '''前后置处理'''
    # print('————————————————接口测试开始————————————————')
    # yield
    # print('————————————————接口测试结束————————————————')
    return request.param

class TestLogin:

    def test_case01(self):
        print('用例1')


    def test_case02(self):
        print('用例2')


    def test_case03(self,test3):
        print('用例3')
        print('获取前置操作的参数：',test3)
