#AutoBaiduMachine
-----

Update:2015-12-10 version:0.11  
AutoBaiduMachine 让机器自动从百度中学习到关键词的解释

##安装

python2.7测试通过

需要安装的python模块：

numpy:Python的一种开源的数值计算扩展,用于进行矩阵运算.  
jieba:Python中文分词包.  
networkx:用Python语言开发的图论与复杂网络建模工具.  
TextRank4ZH:结合jieba分词使用的textrank分析包,建议使用分支,对短语输出进行了优化https://github.com/qiqipipioioi/TextRank4ZH/blob/branch1/textrank4zh/, 原版本参见https://github.com/someus/TextRank4ZH.  
Levenshtein:单词相似度算法,用于计算两个字符串之间的Levenshtein距离.  
BeautifulSoup:是一个可以从HTML或XML文件中提取数据的Python库.


```
$ sudo pip install numpy
$ sudo pip install jieba
$ sudo pip install networkx
$ sudo pip install python-Levenshtein
$ sudo pip install beautifulsoup4
```

安装方法

```
$ sudo python setup.py install
```
##目录结构

```
├── AutoBaiduMachine      #!main
│   ├── AutoBaidu.py      #AutoBaidu类
│   ├── hanzi2pinyin.txt  #汉字转换为拼音的字典
│   ├── __init__.py       #初始化
│   ├── pinyin.txt        #拼音表
│   └── stopword.data     #停止词字典
├── LICENSE               #MIT开源许可证
├── MANIFEST.in 
├── README.md 
├── Changelog.txt
├── setup.py 
├── testlist.txt          #测试用关键词列表
└── test.py               #测试程序
```

##算法步骤

详细的算法解释请见AutoBaidu.py的AutoBaidu类的注释

###百度搜索返回的html分析

html分析可以拆分为三部分：

1.百度提供的联想关键词(StrongWord):有的情况下百度会提供一个联想关键词,该关键词可以作为返回的解释之一.  
2.百度红字标注的重点词(EmWord):重点词可能不止一个,只去出现频率最高的重点词.  
3.TextRank:利用TextRank算法对所有搜索标题句子分析得到的短语或者单词,该算法得到的是最重要的短语或单词.

###返回词组选优

经过第一步分析得到的词组,与输入的关键词进行关联,选择最优结果输出.这里有三级筛选条件:

1.如果输入关键词含有汉字,则直接用Levenshtein给出相关度最高的词.  
2.如果输入关键词不含有汉字,但含有汉语拼音,则将候选词组拼音化,选出相关度最高的词.  
3.如果不是以上两种情况,则选出长度最长的词.

##使用方法

为了适用于不同的爬虫模块,比如urllib2和scrapy,AutoBaiduMachine的AutoBaidu类以输入关键词,访问百度返回的html文本作为入参,输出str类型的最佳解释.

```
import AutoBaiduMachine
Baidu = AutoBaiduMachine.AutoBaidu()                 #实例化只需做一次,用于初始化字典
result = Baidu.MainBaidu(InputKeyword, ResponseBody)
```

##测试

`test.py`提供了使用的示例：
```
#!/usr/bin/python
#coding:utf-8
import AutoBaiduMachine
import urllib2
input = open('testlist.txt')                       #同目录下的搜索词列表
Baidu = AutoBaiduMachine.AutoBaidu()               #实例化
for i in input:
    i = i.strip()
    url = 'http://www.baidu.com/s?wd='+i
    body = urllib2.urlopen(url,timeout=5).read()   #urllib2访问返回的html
    result = Baidu.MainBaidu(i, body)              #得到结果
    outline = i+'\t'+result
    print outline
```

得到的结果样例,左侧是搜索关键词,右侧是解释：

```
WeFire  全民突击
QZone   qzone
腾讯新闻        腾讯
live4iphone     live4iphone
qqlive  腾讯视频播放器
爱奇艺视频      爱奇艺视频
bilianime       bilibili
netdisk;6.9.2;iPhone    iphone
优酷    优酷
cf      穿越火线
IPadQQ  版下载
网易新闻        网易新闻
Youku   优酷
YouKuHD 优酷hd
```

##附

这是本人第一个github上的开源项目,希望获得大家支持.  
其中获取候选词组以及选优的部分均有很大改进的空间.

有问题可以联系本人邮箱qiqipipioioi@qq.com
