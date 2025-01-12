import json

from common.readyaml import ReadyamlData,get_testcase_yaml
from common.debugtalk import Debugtaik
from conf.operationConfig import OperationConfig
import allure
class RequestsBase(object):

    def __init__(self):
        self.read = ReadyamlData()
        self.conf = OperationConfig()


    def replace_load(self,data):
        '''yaml文件替换解析{}格式的数据'''
        str_data = data
        if not isinstance(data,str):
            str_data = json.dumps(data,ensure_ascii=False)

        for i in range(str_data.count('${')):

            if '${' in str_data and '}' in str_data:
                #index检测字符串是否子字符串，并找到字符串的索引位置
                start_index = str_data.index('$')
                end_index = str_data.index('}',start_index)
                ref_all_params = str_data[start_index:end_index+1]
                print(ref_all_params)
                #取出函数名
                func_name = ref_all_params[2:ref_all_params.index('(')]
                print(func_name)
                #取出函数中的参数值
                funcs_params = ref_all_params[ref_all_params.index('(')+1:ref_all_params.index(')')]
                print(funcs_params)

                #传入替换的参数获取对应的值
                extract_data = getattr(Debugtaik(),func_name)(*funcs_params.split(',') if funcs_params else '')
                print(extract_data)

        if data and isinstance(data,dict):
            data = json.loads(str_data)
        else:
            data = str_data

        return data

    def specification_yaml(self, base_info, test_case):
        """
        接口请求处理基本方法
        :param base_info: yaml文件里面的baseInfo
        :param test_case: yaml文件里面的testCase
        :return:
        """
        params_type = ['data', 'json', 'params']
        cookie = None
        try:
            base_url = self.conf.get_envi('host')
            url_host = self.conf.get_section_for_data('api_envi', 'host')
            api_name = base_info['api_name']
            allure.attach(api_name, f'接口名称：{api_name}', allure.attachment_type.TEXT)
            url = url_host + base_info['url']
            allure.attach(api_name, f'接口地址：{url}', allure.attachment_type.TEXT)
            method = base_info['method']
            allure.attach(api_name, f'请求方法：{method}', allure.attachment_type.TEXT)
            header = self.replace_load(base_info['header'])
            allure.attach(api_name, f'请求头：{header}', allure.attachment_type.TEXT)
            # 处理cookie
            cookie = None
            if base_info.get('cookies') is not None:
                cookie = eval(self.replace_load(base_info['cookies']))
            case_name = test_case.pop('case_name')
            allure.attach(api_name, f'测试用例名称：{case_name}', allure.attachment_type.TEXT)
            # 处理断言
            val = self.replace_load(test_case.get('validation'))
            test_case['validation'] = val
            validation = eval(test_case.pop('validation'))
            # 处理参数提取
            extract = test_case.pop('extract', None)
            extract_list = test_case.pop('extract_list', None)
            # 处理接口的请求参数
            for key, value in test_case.items():
                if key in params_type:
                    test_case[key] = self.replace_load(value)

            # 处理文件上传接口
            file, files = test_case.pop('files', None), None
            if file is not None:
                for fk, fv in file.items():
                    allure.attach(json.dumps(file), '导入文件')
                    files = {fk: open(fv, mode='rb')}

            res = self.run.run_main(name=api_name, url=url, case_name=case_name, header=header, method=method,
                                    file=files, cookies=cookie, **test_case)
            status_code = res.status_code
            allure.attach(self.allure_attach_response(res.json()), '接口响应信息', allure.attachment_type.TEXT)

            try:
                res_json = json.loads(res.text)  # 把json格式转换成字典字典
                if extract is not None:
                    self.extract_data(extract, res.text)
                if extract_list is not None:
                    self.extract_data_list(extract_list, res.text)
                # 处理断言
                self.asserts.assert_result(validation, res_json, status_code)
            except JSONDecodeError as js:
                logs.error('系统异常或接口未请求！')
                raise js
            except Exception as e:
                logs.error(e)
                raise e

        except Exception as e:
            raise e

    @classmethod
    def allure_attach_response(cls, response):
        if isinstance(response, dict):
            allure_response = json.dumps(response, ensure_ascii=False, indent=4)
        else:
            allure_response = response
        return allure_response



    def specifcation_yaml(self,case_info):
        """
        规范yaml接口测试数据的写法
        :param case_info:list类型，调试取case_info[0]
        :return:
        """
        base_url = self.conf.get_envi('host')



if __name__ == '__main__':
    req = RequestsBase()
    data = get_testcase_yaml('../testcase/Login/login.yaml')[0]
    # req.replace_load(data)
    print(req.specifcation_yaml(data))