# -*- coding: utf-8 -*-
# @Time : 2024/12/8 17:47
# @Author : 17507
# @File : test_addUser
# @Project : api-test
import time

import pytest


class TestAddUser:

    def test_case01(self):
        print('新增用户')


    def test_case02(self):
        print('删除用户 ')


    @pytest.mark.skip(reason='跳过')
    def test_case03(self):
        print('修改用户')
