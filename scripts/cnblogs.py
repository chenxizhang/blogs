import shutil
import sys
import xmlrpc.client as xmlrpclib
from itertools import groupby

import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md

serviceUrl, appkey = 'http://rpc.cnblogs.com/metaweblog/chenxizhang', 'chenxizhang'


def htmlToMarkdown(html):
    # 下载并替换图片地址
    soup = BeautifulSoup(html, 'html.parser')
    for img in soup.find_all('img'):
        try:
            r = requests.get(img['src'], stream=True)
            if(r.status_code == 200):
                path = '/images/' + img['src'].split('/')[-1]
                with open("../src"+path, 'wb') as f:
                    shutil.copyfileobj(r.raw, f)
                img['src'] = ".."+path
        except:
            pass

    return md(str(soup))


def groupPosts(posts):
    # 排序处理
    posts = sorted(posts, key=lambda x: x['dateCreated'].strftime(
        '%Y-%m'), reverse=True)
    return groupby(iterable=posts, key=lambda x: x['dateCreated'].strftime('%Y-%m'))


if __name__ == '__main__':
    usr, passwd = len(sys.argv) == 3 and sys.argv[1:] or (None, None)
    if(usr is None or passwd is None):
        print("请输入用户名和密码")
        exit()

    server = xmlrpclib.ServerProxy(serviceUrl, use_datetime=True)
    blogInfo = server.blogger.getUsersBlogs(appkey, usr, passwd)

    # 打印博客信息
    blogid = blogInfo[0]['blogid']

    # 获取所有的文章
    posts = server.metaWeblog.getRecentPosts(blogid, usr, passwd, 10)

    with open(file='../src/SUMMARY.md', mode='w', encoding='utf-8') as f:
        f.write('# SUMMARY'+'\n\n\n')

        for group in groupPosts(posts):
            month = group[0]
            f.write('### ' + month + '\n')
            for post in group[1]:
                f.write('* [{}]({})\n'.format(post['title'],
                        "./blogs/{}-{}.md".format(month, post['postid'])))

                open(file='../src/blogs/{}-{}.md'.format(month, post['postid']), mode='w', encoding='utf-8').write("# {} \n> 原文发表于 {}, 地址: {} \n\n\n{}".format(
                    post["title"], post["dateCreated"].strftime("%Y-%m-%d"), post["link"], htmlToMarkdown(str(post["description"]))))
