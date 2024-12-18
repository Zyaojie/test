# -*- coding: utf-8 -*-
# @Time : 2024/12/8 15:41
# @Author : 17507
# @File : test_login
# @Project : api-test
import time

import pytest




class TestLogin:


    @pytest.mark.parametrize('params',('小张','小王','小李'))
    def test_case01(self,params):
        print('用例1')
        print('获取到的参数为：',params)


    # def test_case02(self):
    #     print('用例2')
    #
    #
    # def test_case03(self):
    #     print('用例3')

