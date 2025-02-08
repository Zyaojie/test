import pytest
from common.recordlog import logs
from common.readyaml import ReadyamlData

read = ReadyamlData()
@pytest.fixture(scope='session',autouse=True)
def clear_extract_data():
    read.clear_yaml_data()


@pytest.fixture(scope="class",autouse=True)
def fixture_test():
    '''前后置处理'''
    logs.info('————————————————接口测试开始————————————————')
    yield
    logs.info('————————————————接口测试结束————————————————')
