# -*- coding: utf-8 -*-
# @Time : 2024/12/8 15:41
# @Author : 17507
# @File : test_login
# @Project : api-test
import time

import pytest


@pytest.fixture(scope="",params="",autouse=False,ids="",name="")
def fixture_test():
    '''前后置处理'''
    print('这是处理前后置的方法')

class TestLogin:

    def test_case01(self):
        print('我第二个执行')

    @pytest.mark.skip(reason='跳过')

    def test_case02(self):
        print('我第三个执行')


    def test_case03(self):
        print('我第一个执行')
