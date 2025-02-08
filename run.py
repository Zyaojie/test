# -*- coding: utf-8 -*-
# @Time : 2024/12/8 15:49
# @Author : 17507
# @File : run
# @Project : api-test
import pytest
import os

if __name__ == '__main__':
    pytest.main()
    # os.system(r'allure serve ./report/temp')  # 使用原始字符串避免转义问题