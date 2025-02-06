import time

import pytest
import allure
from common.readyaml import get_testcase_yaml
from common.sendrequests import SendRequest
from base.apiutil import RequestsBase

@allure.feature('商品列表')
class TestProd:
    @allure.story('获取商品列表')
    @pytest.mark.parametrize('params',get_testcase_yaml('./testcase/prodductManager/getProdctList.yaml'))
    def test_get_product_list(self,params):
        RequestsBase().specifcation_yaml(params)
