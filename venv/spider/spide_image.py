import os
import requests
import pyhttpx
from bs4 import BeautifulSoup

if __name__ == '__main__':
    url = "https://699pic.com/sousuo-218808-13-1-0-0-0.html"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
    }
    session = pyhttpx.HttpSession()
    res = session.get(url=url, headers=headers)

    # res = requests.get(url, headers=headers)
    result = res.content
    soup = BeautifulSoup(result, "html.parser")
    # 找出所有的image标签
    images = soup.find_all(class_="img-visibility")

    current_dir = os.getcwd()

    for image in images:
        try:
            jpg_url = image["src"]  # //img95.699pic.com/photo/40172/8292.jpg_wh300.jpg
            title = image["title"]
            alt = image["alt"]
            print(jpg_url)
            print(title)
            saved_path = os.path.join(current_dir, 'images', alt + ".jpg")
            with open(saved_path, 'wb') as f:
                f.write(session.get(url="https:"+jpg_url, headers=headers).content)

        except Exception as e:
            print(e)
