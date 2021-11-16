import lxml
from bs4 import BeautifulSoup


def getNumbers(link):
    print(link)
    t = link.split('/')
    if(len(t) == 9):
        return "{}-{},{}".format(t[5], t[6], t[8].split('.')[0])
    else:
        return ''


soup = BeautifulSoup(open('2011.xml', mode="r", encoding="utf8"), 'lxml')
items = soup.select('item')


out = [getNumbers(x.guid.string) for x in items]
with open(file="ids.txt", mode="a", encoding="utf8") as f:
    f.write("\n".join(out))
