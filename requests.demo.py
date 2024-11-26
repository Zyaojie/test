import requests
url = 'http://127.0.0.1:8787//dar/user/login'

header = {'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'}

data = {
    'user_name': 'test01',
    'passwd': 'admin123'
}

#-------------------------post-----------------
res = requests.post(url=url,data=data)

print(res.text)

#------------------------get--------------------------------

url_2 = 'http://127.0.0.1:8787//coupApply/cms/goodsList'
header_2 = {'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'}
jsondata ={
"msgType": "getHandsetListOfCust",
"page":1,
"size":20
}

res2 = requests.get(url=url_2,params=jsondata,headers=header_2)
print(res2.text)
print(1111)