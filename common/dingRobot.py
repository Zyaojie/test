import time
import hmac
import hashlib
import base64
import urllib.parse

import requests


def generate_sign():
    """
    签名计算
    ：return：
    """
    timestamp = str(round(time.time() * 1000))
    # 钉钉机器人生成的秘钥
    secret = 'SEC3a87602a6637fcca2add2d7d58046baf4ce42e320ecff02c7fbde56202b7c172'
    secret_enc = secret.encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))

    return timestamp, sign


def send_dingding_msg(content, at_all=True):
    """
    向钉钉群机器人推送结果
    :param content: 发送的内容
    :param at_all: 是否@所有人，默认为True
    :return:
    """
    timestamp_sign = generate_sign()
    # 首先需要拿到钉钉机器人的webhook地址+timestamp+sign
    url = f'https://oapi.dingtalk.com/robot/send?access_token=015c89e63762e7a5ab17c79def2d56b4f98f949a8979fa1c47a09cfdc7b87fda&timestamp={timestamp_sign[0]}&sign={timestamp_sign[1]}'
    headers = {'Content-Type': 'application/json;charset=utf-8'}
    req_data = {
        'msgtype': 'text',
        'text': {
            'content': content
        },
        'at': {
            'isAtAll': at_all
        }
    }
    res = requests.post(url, json=req_data, headers=headers)
    return res.text

if __name__ == '__main__':
    content = """
    各位好，本次电商项目的测试报告执行结果如下：
    测试用例共：100
    通过：100
    点击查看测试报告
    """
    send_dingding_msg(content)
