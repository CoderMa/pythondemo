import requests
from bs4 import BeautifulSoup

if __name__ == '__main__':
    r = requests.get("http://www.cnblogs.com/yoyoketang/")
    blog = r.content

    soup = BeautifulSoup(blog, "html.parser")
     
    # 获取所有的class属性为dayTitle, 返回Tag类
    times = soup.find_all(class_='dayTitle')
    titles = soup.find_all(class_="postTitle")
    descs = soup.find_all(class_="postCon")

    """
    for i in times:
        a = i
        print(i.a.string)

  
    for i in titles:
        #c = i.a.string
        c = i.text
        d = i.a.contents[1].text
        print(c)
        print(d)

    
    for i in descs:
        c = i.div.contents[0]
        print(c)
    """


    for i, j, k in zip(times, titles, descs):
        print(i.a.string)
        # print(j.a.string)
        title = str(j.text).replace('\n', '').strip()
        # print(str(j.text).strip())
        print(title)
        print(k.div.contents[0])
        print("")
