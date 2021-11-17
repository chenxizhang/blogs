import sys
import os
import shutil
from itertools import groupby

import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md

# 从本地数据文件中读取数据


def getNumbers(link):
    t = link.split('/')
    return {"year": t[5], "month": t[6], "day": t[7], "id": t[8].split('.')[0]}


def getPost(item):
    n = getNumbers(item.guid.string)
    return {
        "title": item.title.string,
        "link": item.guid.string,
        "body": item.description.string,
        "id": n["id"],
        "month": n["year"] + "-" + n["month"],
        "pubdate": "{}-{}-{}".format(n["year"], n["month"], n["day"])
    }


def htmlToMarkdown(html, id):
    # 下载并替换图片地址
    soup = BeautifulSoup(html, 'html.parser')
    for img in soup.find_all('img'):
        try:
            r = requests.get(img['src'], stream=True)
            if(r.status_code == 200):
                path = '/images/'+id+"-" + img['src'].split('/')[-1]
                with open("../docs"+path, 'wb') as f:
                    shutil.copyfileobj(r.raw, f)
                img['src'] = "."+path
            else:
                print("图片下载失败:{}".format(img['src']))
        except Exception as e:
            print("图片下载报错:{},{}".format(img['src'], e))
    return md(str(soup))


if __name__ == '__main__':

    # 获取参数
    if len(sys.argv) < 2:
        print("请输入文件名")
        exit(1)

    file_name = sys.argv[1]
    if not os.path.exists(file_name):
        print("文件不存在")
        exit(1)

    # 读取数据
    soup = BeautifulSoup(
        open(file_name, mode="r", encoding="utf8"), 'html.parser')

    items = groupby(sorted([getPost(item) for item in soup.find_all(
        'item')][:20], key=lambda x: x['month'], reverse=True), lambda x: x['month'])

    with open("../docs/SUMMARY.md", mode="a", encoding="utf8") as f:
        for g in items:
            f.write("\n\n\n### {}\n".format(g[0]))
            for post in g[1]:
                file_path = "{}-{}.md".format(post["month"], post["id"])
                f.write("* [{}]({})\n".format(post["title"], file_path))
                open(file='../docs/{}'.format(file_path), mode='w', encoding='utf-8').write("# {} \n> 原文发表于 {}, 地址: {} \n\n\n{}".format(
                    post["title"], post["pubdate"], post["link"], htmlToMarkdown(post["body"], post["id"])))
