# -*- coding: utf-8 -*-
# @Time : 2024/12/8 15:41
# @Author : 17507
# @File : test_login
# @Project : api-test
import time

import pytest
import allure
from common.readyaml import get_testcase_yaml
from common.sendrequests import SendRequest
from base.apiutil import RequestsBase

@allure.feature('登录接口')
class TestLogin:
    @allure.story('用户名和密码登录正常校验')
    @pytest.mark.parametrize('params',get_testcase_yaml('./testcase/login/login.yaml'))
    def test_case01(self,params):
        RequestsBase().specifcation_yaml(params)

    @allure.story('用户名和密码登录错误校验')
    @pytest.mark.parametrize('params', get_testcase_yaml('./testcase/login/login.yaml'))
    def test_case02(self, params):
        RequestsBase().specifcation_yaml(params)
