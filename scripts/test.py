import shutil

import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md


def htmlToMarkdown(html):
    # 下载并替换图片地址
    soup = BeautifulSoup(html, 'html.parser')
    for img in soup.find_all('img'):
        try:
            r = requests.get(img['src'], stream=True)
            if(r.status_code == 200):
                path = '/images/8870829-' + img['src'].split('/')[-1]
                with open("."+path, 'wb') as f:
                    shutil.copyfileobj(r.raw, f)
                img['src'] = "."+path
            else:
                print("图片下载失败:{}".format(img['src']))
        except:
            continue

    return md(str(soup))


body = open(file="body.txt", mode="r", encoding="utf-8").read()
open(file="body.md", mode="w", encoding="utf-8").write(htmlToMarkdown(body))
