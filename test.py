#!/usr/bin/python
#coding:utf-8
import AutoBaiduMachine
import urllib2
input = open('testlist.txt')
Baidu = AutoBaiduMachine.AutoBaidu()
for i in input:
    i = i.strip()
    key = i
    if ';' in i:
        m = i.find(';',2)
        i = i[0:m]
    url = 'http://www.baidu.com/s?wd='+i
    try:
        body = urllib2.urlopen(url,timeout=5).read()
        result = Baidu.MainBaidu(i, body)
        outline = key+'\t'+result+'\n'
    except:
        outline = key+'\t\n'
    print outline
