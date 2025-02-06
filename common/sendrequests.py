import json

import requests
from common.recordlog import logs
from requests import utils
from common.read import ReadyamlData
import pytest
import allure
class SendRequest(object):

    '''
    封装接口的请求
    '''

    def __init__(self):
        self.read = ReadyamlData()

    def send_request(self,**kwargs):
        cookie = {}
        session = requests.session()
        result = None
        try:
            result = session.request(**kwargs)
            set_cookies = requests.utils.dict_from_cookiejar(result.cookies)
            if set_cookies:
                cookie['Cookie'] = set_cookies
                self.read.write_yaml_data(set_cookies)
                logs.info(f'cookie:{cookie}')
            # formatted_response = json.dumps(result.json(), indent=4, ensure_ascii=False)
            logs.info(f'接口实际返回信息：{result}')
        except requests.exceptions.ConnectionError:
            logs.error('接口连接服务器异常！！！')
            pytest.fail('接口请求异常，可能是request的连接数过多或者请求速度过快导致系统报错')
        except requests.exceptions.HTTPError:
            logs.error('http异常')
            pytest.fail('http请求异常')
        except requests.exceptions.RequestException as e:
            logs.error(e)
            pytest.fail('请求异常，请检查系统或数据是否正常')

        return result

    def run_main(self, name,url, case_name, header, method,cookies=None,file=None,**kwargs):
        '''
        接口请求主函数
        :param url:请求地址
        :param data: 请求参数
        :param header: 请求头
        :param method: 请求方法
        :return:
        '''
        try:
        #收集报告日志信息
            logs.info(f'接口名称：{name}')
            logs.info(f'接口请求地址：{url}')
            logs.info(f'请求方法：{method}')
            logs.info(f'测试用例名称：{case_name}')
            logs.info(f'请求头：{header}')
            logs.info(f'Cookies：{cookies}')
            #处理请求参数
            req_params = json.dumps(kwargs,ensure_ascii=False)
            if 'data' in kwargs.keys():
                logs.info(f'请求参数:{kwargs}')
                allure.attach(req_params, f'请求参数：{req_params}', allure.attachment_type.TEXT)
            elif 'json' in kwargs.keys():
                logs.info(f'请求参数:{kwargs}')
                allure.attach(req_params, f'请求参数：{req_params}', allure.attachment_type.TEXT)
            elif 'params' in kwargs.keys():
                logs.info(f'请求参数:{kwargs}')
                allure.attach(req_params, f'请求参数：{req_params}', allure.attachment_type.TEXT)

        except Exception as e:
            logs.error(e)

        response = self.send_request(method = method,url = url,headers=header,cookies=cookies,files=file,verify=False,
                                     **kwargs)

        return response

if __name__ == '__main__':
    url = 'http://127.0.0.1:8787//dar/user/login'
    data = {
        'user_name': 'test01',
        'passwd': 'admin123'
    }
    method = 'post'
    header = None
    send = SendRequest()
    res = send.run_main(url=url, data=data, header=header, method=method)
    print(res)
