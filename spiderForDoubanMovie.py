# coding=utf-8

import csv
from time import sleep
from urllib import request
from pyquery import PyQuery
#  from bs4 import BeautifulSoup
from collections import deque

def spider():
    url = 'http://movie.douban.com/subject/10549480/'
    website = deque()
    visited = set()
    website.append(url)
    with open("movie.csv", "at") as f:
        fieldnames = ("name", "director", "actor", "genres", "releaseDate",
                    "average", "vote")
        output = csv.writer(f, delimiter="\t")
        output.writerow(fieldnames)
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
        try:
            director = find("a[rel='v:directedBy']")
        except:
            director = ''
        try:
            starring = find("a[rel='v:starring']")
        except:
            continue
        try:
            genres = find("span[property='v:genre']")
        except:
            continue
        try:
            releaseDate = find("span[property='v:initialReleaseDate']")
        except:
            releaseDate = ' '
        try:
            average = find("strong[property='v:average']")
        except:
            average = ' '
        try:
            vote = find("span[property='v:votes']")
        except:
            vote = ' '
        """
        summary = soup.find(property="v:summary").get_text()
        result = name + ' ' + '|' + 'director:' + director + ' ' + 'actor:' + starring + ' ' + genres\
                + ' '+ releaseDate + ' ' + average + ' ' + vote + ' ' + '\n' + '\n'
        with open('movie.txt', 'at') as f:
            f.write(result)
            """
        with open("movie.csv", "at") as f:
            output = csv.writer(f, delimiter="\t")
            output.writerow([name, director, starring, genres, releaseDate,
                            average, vote])
        visited |= {url}
        """
        soup = BeautifulSoup(html)
        link = str(soup.find_all("dd"))
        linkhtml = BeautifulSoup(link)
        for linkre in linkhtml.find_all('a'):
            if linkre.get('href') not in visited:
                website.append(linkre.get('href'))
        """
        for linkre in res("dd"):
            link = PyQuery(linkre).find('a').attr('href')
            print(link)
            if link not in visited:
                website.append(link)
        sleep(1)
        
if __name__ == '__main__':
    spider()