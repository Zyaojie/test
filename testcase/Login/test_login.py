# -*- coding: utf-8 -*-
# @Time : 2024/12/8 15:41
# @Author : 17507
# @File : test_login
# @Project : api-test
import time

import pytest

from common.readyaml import get_testcase_yaml
from common.sendrequests import SendRequest


class TestLogin:


    @pytest.mark.parametrize('params',get_testcase_yaml('./testcase/login/login.yaml'))
    def test_case01(self,params):
        url = params['baseInfo']['url']
        new_url = 'http://127.0.0.1:8787' + url

        method = params['baseInfo']['method']
        headers = params['baseInfo']['header']

        data = params['testCase'][0]['data']

        send = SendRequest()

        res = send.run_main(url=new_url,data=data,header=None,method=method)
        print('接口实际返回值：',res)
        assert res['msg'] == '登录成功'

    @pytest.mark.parametrize('params', get_testcase_yaml('./testcase/login/login.yaml'))
    def test_case02(self, params):
        url = params['baseInfo']['url']
        new_url = 'http://127.0.0.1:8787' + url

        method = params['baseInfo']['method']
        headers = params['baseInfo']['header']

        data = {'user_name':'test01','passwd':'123'}

        send = SendRequest()

        res = send.run_main(url=new_url, data=data, header=None, method=method)
        print('接口实际返回值：', res)
        assert res['msg'] == '登录成功'

    @pytest.mark.parametrize('params', get_testcase_yaml('./testcase/login/login.yaml'))
    def test_case03(self, params):
        url = params['baseInfo']['url']
        new_url = 'http://127.0.0.1:8787' + url

        method = params['baseInfo']['method']
        headers = params['baseInfo']['header']

        data = {'user_name':'test03','passwd':'admin123'}

        send = SendRequest()

        res = send.run_main(url=new_url, data=data, header=None, method=method)
        print('接口实际返回值：', res)
        assert res['msg'] == '登录失败,用户名或密码错误'