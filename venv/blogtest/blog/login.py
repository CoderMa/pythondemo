import re
import requests
# 禁用安全请求警告
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class Blog():
    def __init__(self, s):
        # s = requests.session() # 全局参数
        self.s = s

    def login(self):
        """登录接口"""

        url = "https://passport.cnblogs.com/user/signin"

        header = {  # "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0",
            # "Accept": "application/json, text/javascript, */*; q=0.01",

            # "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",

            # "Accept-Encoding": "gzip, deflate, br",

            # "Content-Type": "application/json; charset=utf-8",

            # "VerificationToken": "xxx 已省略",

            "Cookie": "xxx 已省略",

            "X-Requested-With": "XMLHttpRequest",  # "Connection":"keep-alive",
            # "Content-Length":"385"

        }

        json_data = {"input1": "账号",

                     "input2": "密码",

                     "remember": False}

        res = self.s.post(url, headers=header, json=json_data, verify=False)

        result1 = res.content  # 字节输出

        print(result1)

        return res.json()

    def save(self, title, body):
        """保存草稿箱：

        参数 1：title # 标题

        参数 2：body # 中文"""

        url2 = "https://i.cnblogs.com/EditPosts.aspx?opt=1"

        d = {" VIEWSTATE": "",

             " VIEWSTATEGENERATOR": "FE27D343",

             "Editor$Edit$txbTitle": title,

             "Editor$Edit$EditorBody": "<p>%s</p>" % body,

             "Editor$Edit$Advanced$ckbPublished": "on",

             "Editor$Edit$Advanced$chkDisplayHomePage": "on",

             "Editor$Edit$Advanced$chkComments": "on",

             "Editor$Edit$Advanced$chkMainSyndication": "on",

             "Editor$Edit$lkbDraft": "存为草稿",

             }

        r2 = self.s.post(url2, data=d, verify=False)  # 保存草稿箱

        print(r2.url)
        return r2.url


    def get_postid(self, r2_url):
        """正则表达式提取"""

        postid = re.findall(r"postid=(.+?)&", r2_url)
        print(postid)  # 这里是 list []

        #  提取为字符串
        print(postid[0])

        return postid[0]


    def del_tie(self, postid):
        """删除帖子"""

        del_json = {"postId": postid}

        del_url = "https://i.cnblogs.com/post/delete"

        r3 = self.s.post(del_url, json=del_json, verify=False)
        print(r3.json()["isSuccess"])
        return r3.json()


if __name__ == '__main__':
    s = requests.session()
    Blog(s).login()
