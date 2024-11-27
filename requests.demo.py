import requests
from requests import utils



url = 'http://127.0.0.1:8787//dar/user/login'

header = {'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'}

data = {
    'user_name': 'test01',
    'passwd': 'admin123'
}

#1、-------------------------post-----------------
# res = requests.post(url=url,data=data)
#
# print(res.text)

#2、------------------------get--------------------------------

url_2 = 'http://127.0.0.1:8787//coupApply/cms/goodsList'
header_2 = {'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'}
jsondata ={
"msgType": "getHandsetListOfCust",
"page":1,
"size":20
}

# res2 = requests.get(url=url_2,params=jsondata,headers=header_2)
# print(res2.text)





#3、------------------------requests.session()创建会话管理--------------------------------
session = requests.session()

# res3 = session.request(method='get',url=url_2,params=jsondata,headers=header_2)
#
# print(res3.json())

#4、cookie
#获取接口的cookie
result = session.request(method='post',url=url, data=data)

get_cookie = requests.utils.dict_from_cookiejar(result.cookies)
print(get_cookie)
