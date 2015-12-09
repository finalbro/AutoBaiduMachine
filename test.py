#!/usr/bin/python
#coding:utf-8
import AutoBaiduMachine
import urllib2
input = open('testlist.txt')
Baidu = AutoBaiduMachine.AutoBaidu()
for i in input:
    i = i.strip()
    url = 'http://www.baidu.com/s?wd='+i
    body = urllib2.urlopen(url,timeout=5).read()
    result = Baidu.MainBaidu(i, body)
    outline = i+'\t'+result
    print outline
