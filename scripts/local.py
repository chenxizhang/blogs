# 从本地数据文件中读取数据

if __name__ == '__main__':
    import sys
    import os
    from bs4 import BeautifulSoup
    import lxml

    # 获取参数
    if len(sys.argv) < 2:
        print("请输入文件名")
        exit(1)

    file_name = sys.argv[1]
    if not os.path.exists(file_name):
        print("文件不存在")
        exit(1)

    # 读取数据
    soup = BeautifulSoup(open(file_name, mode="r", encoding="utf8"), 'lxml')
    items = [(item.title.string, item.guid.string, item.description.string)
             for item in soup.select('item')]

    print(len(items))
