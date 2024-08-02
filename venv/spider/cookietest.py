import requests
from requests.cookies import RequestsCookieJar

if __name__ == '__main__':
    url = "https://passport.cnblogs.com/user/signin"
    url2 = "https://www.cnblogs.com/yoyoketang/"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/114.0"}

    with requests.Session() as s:
        s.get(url2)

    s = requests.session()
    res = s.get(url, headers=headers, verify=False)
    #res = requests.get(url2)
    print(res.status_code)
    print(res.content)
    print(s.cookies)


    cookie_jar = requests.cookies.RequestsCookieJar()
    cookie_jar.set('.CNBlogsCookie',
                   '46FB88EE46D29877855D8D7D8C8FF7DA38E267FA02573F8A0981083F8CE8E04C178764E3459D272DDC48EA835D8031E953055C2DF4A655CAD030EC378C5193F408FFA4E7695A5C6F9F31920A6071CA7D6E69332032A2BF9B143761DF416549885F5C9B40')
    cookie_jar.set('.Cnblogs.AspNetCore.Cookies',
                   'CfDJ8Eg9kra6YURKsOjJwROiT4uYBu0OeEC2FDWHns7AgNxUUp0FZg_CunpiYBI32ZIWevXPdFojxcN013CSyQU3DV89Ssvodb16Xda38ii-Pg8Ry9wpbr1K0noBqqO9q5uvphAY4jQWhXmFeZyPmBSMrlT6-CPq46l8lVlgxcphcWNptkOxoCyYNhvL352ob0q4r9GDo2X1WA5QRNK3KvmA-Y0c61C627reCxPR27y-ZlpNE-keFzSIkN91NhtTfl99otHw3_hNFfKN8foGaHEHgh67R9MeeCgFNGUfR_YGQ3k_x1MsjJZSJcflydj27PdCV2QqMLdyRne7vDUrppi0ojnLFTe-greKM2onX4yNOJ9FobL-Wc7e5NpxsT59KFnPHy90_cIfhLEr65rhimqaw-PCnMteqX0vI1-bByHvltyR3m-hrDUPZFXtseEx_ujX9YulCd-dzJhNoiB-GmOPXbYQyOb1Bm4P3HiSyYJ3u92K7c_jbdcpOt9fPZAUSdVDwWQHwO_USLuabbO0i0f78KGcqPltWChTIeLZNva3A6_QEiRSGTQdZstQHXUEdfxrkiASA8s5BF511RI-algs8es')
    cookie_jar.set('AlwaysCreateItemsAsActive', 'True')
    cookie_jar.set('AdminCookieAlwaysExpandAdvanced', 'True')
    s.cookies.update(cookie_jar)

    print(s.cookies)

    print("*****************")
    print(res.content)
