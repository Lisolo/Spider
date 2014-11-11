# coding=utf-8

import re
import csv
from time import sleep
from pyquery import PyQuery
from gzip import decompress
from collections import deque
from urllib import request, parse
from http.cookiejar import CookieJar

def ungzip(data):
    try:       
        print('Extracting.....')
        data = decompress(data)
        print('Done!')
    except:
        print('Without compression')
    return data
 
def getXSRF(data):
    cer = re.compile('name="_xsrf" value="(.*)"', flags = 0)
    strlist = cer.findall(data)
    return strlist[0]
 
def getOpener(head):
    # deal with the Cookies
    cj = CookieJar()
    pro = request.HTTPCookieProcessor(cj)
    opener = request.build_opener(pro)
    header = []
    for key, value in head.items():
        elem = (key, value)
        header.append(elem)
    opener.addheaders = header
    return opener
 
header = {
    'Connection': 'Keep-Alive',
    'Accept': 'text/html, application/xhtml+xml, */*',
    'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Accept-Encoding': 'gzip, deflate',
    'Host': 'www.zhihu.com',
    'DNT': '1'
}

def spider():
    host = 'http://www.zhihu.com/'
    website = deque()
    visited = set()
    website.append(host)
    number = 1
    with open("zhihu.csv", "at") as f:
        fieldnames = ("name", "tag", "questionNumber")
        output = csv.writer(f, delimiter="\t")
        output.writerow(fieldnames)
    find = lambda s: PyQuery(res(s)).text()
    while website:
        url = website.popleft()
        if number == 1:
            url = parse.urljoin(host, url) 
            url += 'login'
            print(url)
            opener = getOpener(header)
            op = opener.open(url)
            data = op.read()
            data = ungzip(data)     
            _xsrf = getXSRF(data.decode()) 
            id = 'Your email'
            password = 'Your password'
            postDict = {
                    '_xsrf':_xsrf,
                    'email': id,
                    'password': password,
                    'rememberme': 'y'
            }
            postData = parse.urlencode(postDict).encode()
            op = opener.open(url, postData)
            data = op.read()
            data = ungzip(data)
            html = data.decode('utf-8')
            number -= 1
        else:
            if url in visited:
                continue
            else:
                url = parse.urljoin(host, url) 
                print(url)
                op = opener.open(url)
                data = op.read()
                data = ungzip(data)
                html = data.decode('utf-8')
        res = PyQuery(html)
        name = find("h2[class='zm-item-title zm-editable-content']")
        try:
            tag = find("a[class='zm-item-tag']")
        except:
            continue
        try:
            questionNumber = find("h3[id='zh-question-answer-num']")
        except:
            director = ''
        result = name + ' ' + tag + ' ' + questionNumber + ' ' + '\n' + '\n'
        with open('zhihu.csv', 'at') as f:
            output = csv.writer(f, delimiter="\t")
            output.writerow([name, tag, questionNumber])
        visited |= {url}
        for linkre in res("a[class='question_link']"):
            link = PyQuery(linkre).attr('href')
            print(link)
            if link not in visited:
                website.append(link)
        sleep(1)
        
if __name__ == '__main__':
    spider()