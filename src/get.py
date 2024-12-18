import requests
from bs4 import BeautifulSoup

# HTMLの取得(GET)
req = requests.get("https://gakujo.shizuoka.ac.jp/lcu-web/SC_01002B00_00")
req.encoding = req.apparent_encoding  # 日本語の文字化け防止

# HTMLの解析
bsObj = BeautifulSoup(req.text, "html.parser")


items = bsObj.find_all("li") 
for item in items:
        print(item)
