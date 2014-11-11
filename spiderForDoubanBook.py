# coding=utf-8

from time import sleep
from urllib import request
from pyquery import PyQuery
# from bs4 import BeautifulSoup
from collections import deque

def spider():
    url = 'http://book.douban.com/subject/4242172/'
    website = deque()
    visited = set()
    website.append(url)
    find = lambda s: PyQuery(res(s)).text()
    while website:
        url = website.popleft()
        if url in visited:
            continue
        else:
            try:
                print(url)
                urlopen = request.urlopen(url, timeout = 2)
                html = urlopen.read().decode('utf-8')
            except:
                visited |= {url}
                continue
        res = PyQuery(html)
        name = find("span[property='v:itemreviewed']")
        info = find("div[id='info']")
        try:
            average = find("strong[property='v:average']")
        except:
            average = ' '
        try:
            vote = find("span[property='v:votes']")
        except:
            vote = ' '
        result = name + ' ' + info + ' ' + average + ' ' + vote + '\n' + '\n'
        with open('book.txt', 'at') as f:
            f.write(result)
        visited |= {url}
        """
        soup = BeautifulSoup(html)
        link = str(soup.find_all("dd"))
        linkhtml = BeautifulSoup(link)
        for linkre in linkhtml.find_all('a'):
            if 'http://read' not in linkre.get('href') and linkre.get('href') not in visited:
                website.append(linkre.get('href'))
        """
        for linkre in res("dd"):
            link = PyQuery(linkre).find('a').attr('href')
            print(link)
            if 'http://read' not in link and link not in visited:
                website.append(link)
        sleep(1)
        
if __name__ == '__main__':
    spider()