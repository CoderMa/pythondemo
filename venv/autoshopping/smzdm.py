import requests
from bs4 import BeautifulSoup

# 账号和密码
username = '18019101737'
password = 'mjlei!@0051'

# 会话对象
session = requests.Session()

# 登录的URL
login_url = 'https://zhiyou.smzdm.com/user/login/ajax_check'

# 登录的表单数据
login_data = {
    'username': username,
    'password': password,
    'rememberme': '1'
}

# 发送登录请求
response = session.post(login_url, data=login_data)
if response.status_code == 200 and response.json().get('error_code') == 0:
    print("登录成功")

    # 签到的URL
    checkin_url = 'https://zhiyou.smzdm.com/user/checkin/jsonp_checkin'

    # 发送签到请求
    checkin_response = session.get(checkin_url)
    if checkin_response.status_code == 200:
        checkin_result = checkin_response.json()
        if checkin_result.get('error_code') == 0:
            print("签到成功:", checkin_result.get('data'))
        else:
            print("签到失败:", checkin_result.get('error_msg'))
    else:
        print("签到请求失败")
else:
    print("登录失败或用户名/密码错误")

# 关闭会话
session.close()
