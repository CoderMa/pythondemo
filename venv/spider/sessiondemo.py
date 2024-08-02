import requests

headers = {
    "content-type": "application/x-www-form-urlencoded;charset=UTF-8",
    "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1.6) ",
}

# 设置一个会话session对象s
s = requests.session()
res = s.get('https://www.baidu.com/s?wd=python', headers=headers)
# 打印请求头和cookies
print(res.request.headers)
print(res.cookies)

# 利用s再访问一次
res = s.get('https://www.baidu.com/s?wd=python', headers=headers)

# 请求头已保持首次请求后产生的cookie
print(res.request.headers)
print(res.cookies)
