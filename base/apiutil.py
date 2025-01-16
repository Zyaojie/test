import json
from common.readyaml import ReadyamlData, get_testcase_yaml
from common.debugtalk import Debugtaik
from conf.operationConfig import OperationConfig
import allure
from common.sendrequests import SendRequest
from common.recordlog import logs
from conf.setting import FILE_PATA

class RequestsBase(object):

    def __init__(self):
        self.read = ReadyamlData()
        self.conf = OperationConfig()
        self.send = SendRequest()

    def replace_load(self, data):
        '''yaml文件替换解析{}格式的数据'''
        str_data = data
        if not isinstance(data, str):
            str_data = json.dumps(data, ensure_ascii=False)

        for i in range(str_data.count('${')):

            if '${' in str_data and '}' in str_data:
                # index检测字符串是否子字符串，并找到字符串的索引位置
                start_index = str_data.index('$')
                end_index = str_data.index('}', start_index)
                ref_all_params = str_data[start_index:end_index + 1]
                # 取出函数名
                func_name = ref_all_params[2:ref_all_params.index('(')]
                # 取出函数中的参数值
                funcs_params = ref_all_params[ref_all_params.index('(') + 1:ref_all_params.index(')')]
                # 传入替换的参数获取对应的值
                extract_data = getattr(Debugtaik(), func_name)(*funcs_params.split(',') if funcs_params else '')

        if data and isinstance(data, dict):
            data = json.loads(str_data)
        else:
            data = str_data

        return data

    def specifcation_yaml(self, case_info):
        """
        规范yaml接口测试数据的写法
        :param case_info:list类型，调试取case_info[0]
        :return:
        """
        params_type = ['params', 'data', 'json']
        base_url = self.conf.get_envi('host')
        url = base_url + case_info['baseInfo']['url']
        api_name = case_info['baseInfo']['api_name']
        method = case_info['baseInfo']['method']
        header = case_info['baseInfo']['header']
        cookie = self.replace_load(case_info['baseInfo']['cookies'])

        for tc in case_info['testCase']:
            case_name = tc.pop('case_name')
            validation = tc.pop('validation')
            extract = tc.pop('extract', None)
            extract_list = tc.pop('extract_list', None)
            for key, value in tc.items():
                if key in params_type:
                    tc[key] = self.replace_load(value)
            res = self.send.run_main(name=api_name, url=url, case_name=case_name, header=header, method=method,
                                     cookies=cookie, file=None,
                                     **tc)
            print(res.text)


if __name__ == '__main__':
    req = RequestsBase()
    data = get_testcase_yaml('../testcase/Login/login.yaml')[0]
    # req.replace_load(data)
    print(req.specifcation_yaml(data))
