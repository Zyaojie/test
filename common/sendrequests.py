import json  # 导入json模块，用于处理接口请求/响应的序列化和美化
# 为什么：HTTP接口常用json格式传递数据，美化输出便于日志和调试

import requests  # 导入requests库，用于HTTP请求
# 为什么：requests是Python最常用的第三方HTTP库，语法简洁，支持Session等高级用法

from common.recordlog import logs  # 导入自定义日志对象
# 为什么：所有接口请求、异常等都要有日志记录，方便排查问题

from requests import utils  # 导入requests.utils，处理cookie等
# 为什么：utils.dict_from_cookiejar可方便将cookiejar对象转为字典，便于后续处理

from common.readyaml import ReadyamlData  # 导入自定义的yaml处理类
# 为什么：用于将接口返回的cookie等数据写入yaml文件，便于后续用例参数化/依赖

import pytest  # 导入pytest，用于用例失败时主动中止并标记失败
# 为什么：异常情况下直接fail可终止测试，出错用例不再继续影响后续用例

import allure  # 导入allure，用于生成测试报告和附加日志
# 为什么：自动化测试需要生成可读性强的报告，allure支持报告图形化和日志附件

class SendRequest(object):  # 定义请求发送类
    '''
    封装接口的请求
    # 为什么：统一管理所有接口请求逻辑，便于扩展、维护、日志集中处理
    '''

    def __init__(self):
        self.read = ReadyamlData()  # 实例化yaml处理对象
        # 为什么：便于后续自动将cookie等写入yaml，支持自动参数提取/依赖

    def send_request(self,**kwargs):  # 通用请求方法，接收所有请求参数
        cookie = {}  # 初始化cookie字典
        session = requests.session()  # 创建会话对象，支持自动管理cookie等
        # 为什么：session复用连接，支持自动管理cookie，适合接口自动化场景
        result = None  # 预置返回结果变量
        try:
            result = session.request(**kwargs)  # 发送HTTP请求，所有参数透传
            # 为什么：支持GET/POST/PUT/DELETE等所有方法，参数灵活
            set_cookies = requests.utils.dict_from_cookiejar(result.cookies)  # 提取响应cookie
            # 为什么：部分接口需要依赖cookie，统一提取方便写入yaml或后续用例复用
            if set_cookies:
                cookie['Cookie'] = set_cookies  # 存入cookie字典
                self.read.write_yaml_data(set_cookies)  # 写入yaml文件
                # 为什么：自动化测试中需要跨用例复用cookie，写入yaml便于后续读取
                logs.info(f'cookie:{cookie}')  # 记录cookie日志
            formatted_response = json.dumps(result.json(), indent=4, ensure_ascii=False)  # 美化接口响应
            # 为什么：接口响应格式化便于日志查阅和问题定位
            logs.info(f'接口实际返回信息：\n{formatted_response}')  # 打印接口响应
        except requests.exceptions.ConnectionError:
            logs.error('接口连接服务器异常！！！')
            # 为什么：网络连接异常要重点提示，便于第一时间排查环境问题
            pytest.fail('接口请求异常，可能是request的连接数过多或者请求速度过快导致系统报错')
            # 为什么：请求异常要直接fail，防止后续用例继续执行带来误判
        except requests.exceptions.HTTPError:
            logs.error('http异常')
            pytest.fail('http请求异常')
            # 为什么：http错误（如4xx/5xx）直接fail并记录日志，便于快速定位
        except requests.exceptions.RequestException as e:
            logs.error(e)
            pytest.fail('请求异常，请检查系统或数据是否正常')
            # 为什么：其它requests异常统一处理，避免遗漏特殊报错

        return result  # 返回接口请求结果
        # 为什么：上层用例需要获取响应对象做断言、提取数据等处理

    def run_main(self, name, url, case_name, header, method, cookies=None, file=None, **kwargs):
        '''
        接口请求主函数
        :param name: 接口名称
        :param url: 请求地址
        :param case_name: 用例名称
        :param header: 请求头
        :param method: 请求方法
        :param cookies: 请求cookies
        :param file: 上传文件
        :param kwargs: 其余请求参数（如data、json、params等）
        :return: 响应对象
        '''
        try:
            # 收集报告日志信息
            logs.info(f'接口名称：{name}')
            logs.info(f'接口请求地址：{url}')
            logs.info(f'请求方法：{method}')
            logs.info(f'测试用例名称：{case_name}')
            logs.info(f'请求头：{header}')
            logs.info(f'Cookies：{cookies}')
            # 处理请求参数
            req_params = json.dumps(kwargs, ensure_ascii=False)  # 请求参数转字符串
            # 为什么：日志和allure报告展示更美观，参数有中文时确保不乱码
            if 'data' in kwargs.keys():
                logs.info(f'请求参数:{kwargs}')
                allure.attach(req_params, f'请求参数：{req_params}', allure.attachment_type.TEXT)
                # 为什么：不同参数类型分别日志打印并附加到allure报告，便于调试
            elif 'json' in kwargs.keys():
                logs.info(f'请求参数:{kwargs}')
                allure.attach(req_params, f'请求参数：{req_params}', allure.attachment_type.TEXT)
            elif 'params' in kwargs.keys():
                logs.info(f'请求参数:{kwargs}')
                allure.attach(req_params, f'请求参数：{req_params}', allure.attachment_type.TEXT)

        except Exception as e:
            logs.error(e)
            # 为什么：参数处理或日志记录出错要有异常捕捉，不影响主流程

        response = self.send_request(
            method=method,
            url=url,
            headers=header,
            cookies=cookies,
            files=file,
            verify=False,  # 关闭SSL证书校验（适合测试环境）
            **kwargs  # 透传其余所有参数
        )
        # 为什么：所有请求参数统一出口，便于后续加钩子或特殊逻辑

        return response  # 返回响应对象，便于用例断言、数据提取

if __name__ == '__main__':  # 主程序入口
    url = 'http://127.0.0.1:8787//dar/user/login'  # 本地测试用例接口
    data = {
        'user_name': 'test01',
        'passwd': 'admin123'
    }
    method = 'post'
    header = None
    send = SendRequest()  # 实例化请求对象
    res = send.run_main(url=url, data=data, header=header, method=method)  # 发起请求
    print(res)
    # 为什么：本地手动运行时可快速验证接口请求逻辑是否正确