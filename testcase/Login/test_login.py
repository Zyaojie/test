# -*- coding: utf-8 -*-
# @Time : 2024/12/8 15:41
# @Author : 17507
# @File : test_login
# @Project : api-test
import time

import pytest


class TestLogin:
    @pytest.mark.run(order=2)
    def test_case01(self):
        print('我第二个执行')

    @pytest.mark.run(order=3)
    def test_case02(self):
        print('我第三个执行')
        assert 1 > 2

    @pytest.mark.run(order=1)
    def test_case03(self):
        print('我第一个执行')
