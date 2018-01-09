import sys
import os
import re
import json
import wget
import urllib.request
from bs4 import BeautifulSoup

def Tudou(url):
    vidid = re.search(r'(?:\/v\/)(.*)(\.html)', url, re.I).group(1)
    url = 'http://video.tudou.com/v/' + vidid + '.html'
    fnameappend = '.info.json'
    jsonenc = json.JSONEncoder()
    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page, 'html.parser')
    title = soup.find('span', attrs={'id': 'subtitle'})['title']

    dict = {'vidid': vidid, \
            'origurl': url, \
            'title': title, \
            'description': None, \
            'uploader': None, \
            'channel': None, \
            'uploaded': None}

    uploader = soup.find('a', attrs={'class': 'td-play__userinfo__name'})
    dict['uploader'] = uploader.text.strip()
    dict['channel'] = 'http:' + uploader['href']
    dict['description'] = soup.find('div', attrs={'class': 'td-play__videoinfo__details-box__desc'}).text.strip()
    dict['uploaded'] = soup.find('meta', attrs={'name': 'publishedtime'})['content']

    print('Title: ' + dict['title'])
    print('Uploader: ' + dict['uploader'])
    print('Channel link: ' + dict['channel'])
    print('Description: ' + dict['description'])
    print('Upload date: ' + dict['uploaded'])
    print('Original url: ' + dict['origurl'])

    filename=title.translate(str.maketrans("*/\\<>:\"|","--------")).strip()+"-" + vidid + fnameappend
    print(filename)
    print(dict)
    f = open(filename, 'w')
    f.write(jsonenc.encode({dict['vidid']: dict}))
    f.close()

    vidname = title.translate(str.maketrans("*/\\<>:\"|","--------")).strip()+"-" + vidid

    return vidname
