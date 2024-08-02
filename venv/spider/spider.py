import requests
import time
from lxml import etree
from multiprocessing.dummy import Pool

# cook = {"Cookie": ""}
# url = 'http://weibo.cn/u/1890493665'
# html = requests.get(url)
#
# print(html.content)


if __name__ == '__main__':
    urls = ["http://codema.freevar.com/survey/survey.html", "http://codema.freevar.com/cityskyline/index.html", "http://mjl.freevar.com/register/register.html", "http://codema.freevar.com/survey/survey.html", "http://codema.freevar.com/photogallery/index.html", "http://codema.freevar.com/nutritionlabel/index.html", "http://codema.freevar.com/rose/bingdwen.html", "http://codema.freevar.com/balancesheet/index.html", "http://codema.freevar.com/rose/heart.html", "http://codema.freevar.com/picassopainting/index.html", "http://mjl.freevar.com/piano/index.html", "http://codema.freevar.com/accessibilityquiz/index.html", "http://codema.freevar.com/jsdocument/index.html", "http://codema.freevar.com/magazine/index.html", "http://codema.freevar.com/ferriswheel/index.html", "http://mjl.freevar.com/trombone/index.html", "http://codema.freevar.com/penguin/index.html", "http://codema.freevar.com/personalportfolio/index.html"]

    while True:
        for url in urls:
            res = requests.get(url)
            res.encoding = "utf-8"
            print(res.text)

        time.sleep(864000)
