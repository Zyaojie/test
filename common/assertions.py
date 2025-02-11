import operator
import os.path
import allure
import jsonpath

from common.recordlog import logs


class Assertions:
    """
    接口断言模式封装，支持
    1、字符串包含
    2、结果相等断言
    3、结果不相等断言
    4、断言接口返回值里面的任意一个值
    5、数据库断言
    """

    def contanins_assert(self, value, response, status_code):
        """
        第一种模式：字符串包含断言，断言预期结果的字符串是否包含在接口的实际返回结果当中
        :param value:预期结果，yaml文件当中validation关键字下的结果
        :param response:接口实际返回结果，需要json格式
        :param status_code:接口实际返回状态码
        """
        # 断言状态表示，0代表成功，其他代表失败
        flag = 0
        for assert_key, assert_value in value.items():
            print(assert_key, assert_value)
            if assert_key == 'status_code':
                if assert_value != status_code:
                    flag += 1
                    allure.attach(f'预期结果：{assert_value}\n实际结果为：{status_code}', '响应代码断言结果：失败',
                                  allure.attachment_type.TEXT)
                    logs.error('contanins断言失败，接口返回码【%s】不等于【%s】' % (status_code, assert_value))
            else:
                resp_list = jsonpath.jsonpath(response, '$..%s' % assert_key)
                if isinstance(resp_list[0], str):
                    resp_list = ''.join(resp_list)
                if resp_list:
                    if assert_value in resp_list:
                        logs.info('字符串包含断言成功：预期结果为：【%s】，实际结果为：【%s】' % (assert_value, resp_list))
                    else:
                        flag += 1
                        logs.error('响应文本断言失败：预期结果为：【%s】，实际结果为：【%s】' % (assert_value, resp_list))
                        allure.attach(f'预期结果：{assert_value}\n实际结果为：{status_code}', '响应文本断言结果：失败',
                                      allure.attachment_type.TEXT)
        return flag

    def equal_assert(self,value,response):
        """相等模式
        :param value: 预期结果,也就是yaml文件里面的validation关键字下的参数，必须为dict类型
        :param response: 接口的实际返回结果，必须为dict类型
        :return: flag标识，o0表示测试通过，非0表示不通过
        """
        flag = 0
        res_lst = []
        if isinstance(value,dict) and isinstance(response,dict):
            #处理实际结果的数据结构，保留与预期结果的数据结构一致
            for res in response:
                if list(value.keys())[0] !=res:
                    res_lst.append(res)
            for rl in res_lst:
                del response[rl]

            #通过判断实际结果的字典和预期结果的字典
            eq_assert = operator.eq(response,value)
            if eq_assert:
                logs.info('相等断言成功：接口的实际结果为：%s,等于预期结果为：%s' % (response,str(value)))
            else:
                flag = flag+1
                logs.info('相等断言失败：接口的预期结果为：%s，不等于接口的实际返回值：%s' % (str(value),response,))
        else:
            raise TypeError('相等断言失败--类型错误，预期结果和接口的实际响应结果必须为字典类型！')
        return flag

    def not_equal_assert(self,value,response):
        """不相等模式
        :param value: 预期结果,也就是yaml文件里面的validation关键字下的参数，必须为dict类型
        :param response: 接口的实际返回结果，必须为dict类型
        :return: flag标识，o0表示测试通过，非0表示不通过
        """
        flag = 0
        res_lst = []
        if isinstance(value,dict) and isinstance(response,dict):
            #处理实际结果的数据结构，保留与预期结果的数据结构一致
            for res in response:
                if list(value.keys())[0] !=res:
                    res_lst.append(res)
            for rl in res_lst:
                del response[rl]

            #通过判断实际结果的字典和预期结果的字典
            eq_assert = operator.ne(response,value)
            if eq_assert:
                logs.info(f'不相等断言成功：接口的实际结果为：{response},等于预期结果为：{str(value)}')
            else:
                flag = flag+1
                logs.info('不相等断言失败：接口的预期结果为：%s，不等于接口的实际返回值：%s' % (str(value),response,))
        else:
            raise TypeError('相等断言失败--类型错误，预期结果和接口的实际响应结果必须为字典类型！')
        return flag


    def assert_result(self, expected, response, status_code):
        '''
        断言模式,通过all_flag标记
        :param expected: 预期结果
        :param response: 接口实际返回值,需要josn格式
        :param status_code: 接口实际返回状态码
        '''
        all_fiag = 0
        # 代表成功，其他代表失败
        try:
            for yq in expected:
                for key, value in yq.items():
                    if key == 'contains':
                        flag = self.contanins_assert(value, response, status_code)
                        all_fiag = all_fiag + flag
                    elif key == 'eq':
                        flag = self.equal_assert(value,response)
                        all_fiag = all_fiag + flag
                    elif key == 'ne':
                        flag = self.not_equal_assert(value,response)
                        all_fiag = all_fiag + flag

            assert all_fiag == 0
            logs.info('测试成功!')
        except Exception as e:
            logs.error('测试失败')
            logs.error(f'异常信息：{e}')
            assert all_fiag == 0


if __name__ == '__main__':
    from common.readyaml import get_testcase_yaml

    data = get_testcase_yaml(os.path.join(os.path.dirname(os.path.dirname(__file__)), r'testcase\Login', 'login.yaml'))[
        0]
    value = data['testCase'][0]['validation']
    response = {
        "error_code": None,
        "msg": "登录成功",
        "msg_code": 200,
        "orgId": "6140913758128971280",
        "token": "2DACDDf6E72a9CafA1e5B6FEe1dC3",
        "userId": "9540154955574567022"
    }

    ass = Assertions()
    for i in value:
        for k, v in i.items():
            ass.equal_assert(v, response)
