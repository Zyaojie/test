import pytest
from common.recordlog import logs
@pytest.fixture(scope="class",autouse=True)
def fixture_test():
    '''前后置处理'''
    logs.info('————————————————接口测试开始————————————————')
    yield
    logs.info('————————————————接口测试结束————————————————')
