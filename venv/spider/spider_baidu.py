import requests
import sys
from bs4 import BeautifulSoup as bs
import re
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/57.0.2987.133 Safari/537.36',
}


def main(keyword):
    file_name = "{}.txt".format(keyword)
    # 创建空文件
    f = open(file_name, 'w', encoding="utf-8")
    f.close()
    for pn in range(0, 20, 10):
        params = {"wd": keyword, "pn": pn, }
        r = requests.get(url='http://www.baidu.com/s', params=params, headers=headers)
        soup = bs(r.content, "html.parser")
        urls = soup.find_all(name='a', attrs={'href': re.compile(('.'))})
        # 抓取百度搜索结果中的a标签，其中href是包含了百度的跳转地址
        for i in urls:
            if 'www.baidu.com/link?url=' in i['href']:
                # 抓取跳转后的页面
                a = requests.get(url=i['href'], headers=headers)
                time.sleep(1)
                soup1 = bs(a.content, "html.parser")
                title = soup1.title.string
                with open(keyword + '.txt', 'r', encoding="utf-8") as f:
                    if a.url not in f.read():
                        f = open(keyword + '.txt', 'a', encoding="utf-8")
                        f.write(title + '\n')
                        f.write(a.url + '\n')
                        f.close()


if __name__ == '__main__':
    """
    if len(sys.argv) != 2:
        print('no keyword')
        print('Please enter keyword')
        sys.exit(-1)
    else:
        main(sys.argv[1])
        print("下载完成。")
    """
    keyword = "django"
    main(keyword)
