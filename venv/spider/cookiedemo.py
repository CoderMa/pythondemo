from typing import Dict

import requests

get_url = "https://postman-echo.com/get"
# key为Cookie，值为使用;拼接的 cookie_name=cookie_value 字符串
headers = {"Cookie": "cka=111a;ckb=111b"}

res = requests.get(url=get_url, headers=headers)

print(res.json().get("headers").get("cookie"))
print(res.request.headers.get("Cookie"))

# 注意：同时通过headers，cookies 参数传递Cookie时，只有headers传递的Cookie有效。

# cookies 以字典形式提供，cookies 值以字典形式提供，key为cookie_name，value为cookie_value
cookies = {"cka": "222a", "ckb": "222b"}

res = requests.get(url=get_url, cookies=cookies)

print(res.json().get("headers").get("cookie"))
print(res.request.headers.get("Cookie"))

"""
通过Session会话使用
通过Session会话管理Cookie，同一会话的多个请求可共享Cookie；
在Session中添加Cookie又有多种方式
"""

# 方式0：自动设置
# 在会话过程中，如果有接口响应头中有 set-cookie，则将自动添加到会话的Cookie中
session = requests.session()
print("会话初始cookie：", dict(session.cookies))

get_url = "https://postman-echo.com/get"
res = session.get(url=get_url)

print("响应头中set-cookie：", res.headers.get("set-cookie"))
print("会话现有cookie：", dict(session.cookies))

# 方式1：通过key设置
# 直接通过key设置cookie，但不支持设置cookie的 path、domain 等值
session = requests.session()
print("会话初始cookie：", dict(session.cookies))

# 直接通过key设置cookie，但不支持设置cookie的 path、domain 等值
session.cookies["cka"] = "111a"
session.cookies["ckb"] = "111b"

get_url = "https://postman-echo.com/get"
res = session.get(url=get_url)

print("本次请求使用的cookie：", res.request.headers.get("Cookie"))
print("会话现有cookie：", dict(session.cookies))

# 方式2：通过set 方法设置
# 通过set方法设置cookie，且支持设置path、domain等值
session = requests.session()
print("会话初始cookie：", dict(session.cookies))

# 通过set方法设置cookie，且支持设置path、domain等值
session.cookies.set("ck2", "222", path="/", domain="postman-echo.com")

get_url = "https://postman-echo.com/get"
res = session.get(url=get_url)

print("本次请求使用的cookie：", res.request.headers.get("Cookie"))
print("会话现有cookie：", session.cookies)

# 方式3：通过 add_dict_to_cookiejar 方法设置
# 通过 requests.utils 工具包里的 add_dict_to_cookiejar 方法设置cookie，但不支持设置 path、domain 等值
session = requests.session()
print("会话初始cookie：", dict(session.cookies))

# 通过 requests.utils 工具包里的 add_dict_to_cookiejar 方法设置cookie，但不支持设置 path、domain 等值
cookie_dict: Dict[str, str] = {"ck3a": "333a", "ck3b": "333b"}
requests.utils.add_dict_to_cookiejar(session.cookies, cookie_dict=cookie_dict)

get_url = "https://postman-echo.com/get"
res = session.get(url=get_url)

print("本次请求使用的cookie：", res.request.headers.get("Cookie"))
print("会话现有cookie：", dict(session.cookies))

# 通过 RequestsCookieJar() 对象设置
# 创建一个空 RequestsCookieJar()对象，然后使用对象的set方法赋值，然后update更新到当前会话cookie，支持设置 path、domain等值
session = requests.session()
print("会话初始cookie：", dict(session.cookies))

# 创建一个空 RequestsCookieJar()对象，然后使用对象的set方法赋值，然后update更新到当前会话cookie，支持设置 path、domain等值
ckj = requests.sessions.RequestsCookieJar()
ckj.set('ck4a', '444a', path='/', domain='postman-echo.com')
session.cookies.update(ckj)

get_url = "https://postman-echo.com/get"
res = session.get(url=get_url)

print("本次请求使用的cookie：", res.request.headers.get("Cookie"))
print("会话现有cookie：", dict(session.cookies))

# 方式5：通过 cookiejar_from_dict 方法设置#
# 通过 requests.utils 工具包里的 cookiejar_from_dict 方法将字典格式的cookie转换为cookiejar对象，然后update更新到当前会话，不支持设置 path、domain 等值
session = requests.session()
print("会话初始cookie：", dict(session.cookies))

# 通过 requests.utils 工具包里的 cookiejar_from_dict 方法将字典格式的cookie转换为cookiejar对象，然后update更新到当前会话，不支持设置 path、domain 等值
cookie_dict = {"ck5a": "555a", "ck5b": "555b"}
ckj5 = requests.utils.cookiejar_from_dict(cookie_dict=cookie_dict)
session.cookies.update(ckj5)

get_url = "https://postman-echo.com/get"
res = session.get(url=get_url)

print("本次请求使用的cookie：", res.request.headers.get("Cookie"))
print("会话现有cookie：", dict(session.cookies))
