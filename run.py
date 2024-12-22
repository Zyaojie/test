# -*- coding: utf-8 -*-
# @Time : 2024/12/8 15:49
# @Author : 17507
# @File : run
# @Project : api-test
import pytest
import os
if __name__ == '__main__':
    pytest.main()
    os.system(f'allure serve ./report/temp')