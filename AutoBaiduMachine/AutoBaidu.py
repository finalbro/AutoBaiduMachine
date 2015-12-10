#!/usr/bin/python
#coding:utf-8
import jieba.analyse
from bs4 import BeautifulSoup
from textrank4zh import TextRank4Keyword, TextRank4Sentence
import Levenshtein
import sys
import re
import os
reload(sys)
sys.setdefaultencoding('utf-8')

class AutoBaidu():

    def __init__(self):
#       初始化停止词,以及汉语对应拼音的字典
        path = os.path.split(os.path.realpath(__file__))[0]
        self.tr4w = TextRank4Keyword(stop_words_file= path+'/stopword.data')
        self.Hanzi2PinyinDict = {}
        for line in open(path+'/hanzi2pinyin.txt'):
            line = line.strip()
            hanzi, pinyin = line.split('\t')
            UnicodeHanzi = hanzi.decode('utf-8')
            self.Hanzi2PinyinDict[UnicodeHanzi] = unicode(pinyin)
        self.PinyinDict = set()
        for line in open(path+'/pinyin.txt'):
            line = line.strip()
            self.PinyinDict.add(line)

    def FindStrongWord(self,a):
#       找到百度自动跳转的关键词
        strongs = []
        for tag in a:
            strongs.extend(tag.find_all('strong'))
        strong_words = []
        for p in strongs:
            try:
                p1 = p.get_text()
                if p1 != None and p1 != '':
                    strong_words.append(p1)
            except:
                continue
        try:
            strong_word = max(map(lambda x: (strong_words.count(x), x), strong_words))[1]
        except:
            strong_word = ''
        return strong_word

    def FindEmWord(self,a):
#       找到百度匹配的重点词
        ems = []
        for tag in a:
            ems.extend(tag.find_all('em'))
        em_words = []
        for q in ems:
            try:
                q1 = q.get_text()
                if q1 != None and q1 != '':
                    em_words.append(q1)
            except:
                continue
        try:
            em_word =  max(map(lambda x: (em_words.count(x), x), em_words))[1]
        except:
            em_word = ''
        return em_word

    def TextRankPhrasesAndKeyword(self, soup):
#       用TextRank算法找出重要的短语以及最重要的关键词
        h3 = soup.find_all('h3',class_="t")
        word = ''
        for tag in h3:
            try:
                word = word+'\n'+tag.get_text()
            except:
                continue
        try:
            word = word.encode('utf-8')
        except:
            word = ''
        self.tr4w.train(text=word, speech_tag_filter=False, lower=True, window=2)
        keywords = self.tr4w.get_keywords(10, word_min_len=1)
        keyphrases = self.tr4w.get_keyphrases(keywords_num=10, min_occur_num= 2)
        KeyphrasesKeyword = []
        KeyphrasesKeyword.extend(keyphrases)
        KeyphrasesKeyword.extend(keywords[0:2])
        return KeyphrasesKeyword

    def is_chinese(self, uchars):
#       判断一个字符串中是否含有中文
        for uchar in uchars:
            if uchar >= u'\u4e00' and uchar <=u'\u9fa5':
                return True
        return False

    def is_pinyin(self, chars):
#       判断一个字符串是否含有拼音
        ShengmuSet = {'b','p','m','f','d','t','n','l','g','k','h','j','q','x','zh','ch','sh','r','z','c','s'}
        re1 = re.compile('(zh|ch|sh|b|p|m|f|d|t|n|l|g|k|h|j|q|x|r|z|c|s)')
        SplitResults = re1.split(chars)
        PrePinyinList = []
        LastSplitResult = ''
        for SplitResult in SplitResults:
            if SplitResult not in ShengmuSet:
                LastSplitResult += SplitResult
            else:
                if LastSplitResult:
                    PrePinyinList.append(LastSplitResult)
                LastSplitResult = SplitResult
        if LastSplitResult != SplitResult: PrePinyinList.append(LastSplitResult)
        PinyinCount = 0
        for PrePinyin in PrePinyinList:
            if PrePinyin in self.PinyinDict:
                PinyinCount += 1
        if PinyinCount >= 2:
            return True
        else:return False

    def Trans2Pinyin(self, uchar):
#       把短语中的汉子转换为拼音
        Pinyin = ''
        for word in uchar:
            if word in self.Hanzi2PinyinDict:
                Pinyin += self.Hanzi2PinyinDict[word]
            else: Pinyin += word
        return Pinyin

    def length_count(self, uchar):
#       计算字符串长度,中文算2个
        length = 0
        for i in uchar:
            if self.is_chinese(i):
                length += 2
            else:length += 1
        return length       

    def MatchBestResults(self, keyword, PreResults):
#       从预备的结果里找到最佳匹配
        uPreResults = [PreResult.decode('utf-8').lower() for PreResult in PreResults]
        ukeyword = keyword.decode('utf-8').lower()
        if self.is_chinese(ukeyword):
            Results = map(lambda x: (Levenshtein.ratio(ukeyword,x), x), uPreResults)
            return max(Results)[1].encode('utf-8')
        elif self.is_pinyin(ukeyword):
            uPrePinyin = map(self.Trans2Pinyin, uPreResults)
            Results = map(lambda x: (Levenshtein.ratio(ukeyword,x), x), uPrePinyin)
            MaxResult = max(Results)[1]
            i = uPrePinyin.index(MaxResult)
            return uPreResults[i].encode('utf-8')
        else:
            Results = map(lambda x: (self.length_count(x), x), uPreResults)
            MaxCount = max(Results)[0]
            BestResult = [result[1] for result in Results if result[0] == MaxCount][0]
            return BestResult


    def MainBaidu(self, keyword, ResponseBody):
#       主程序,访问百度后返回的htmlbody以及访问的关键词作为输入,输出最佳匹配短语或关键词
        soup = BeautifulSoup(ResponseBody,'lxml')
        a = soup.find_all('a')
        StrongWord = self.FindStrongWord(a)
        EmWord = self.FindEmWord(a)
        KeyphrasesKeyword = self.TextRankPhrasesAndKeyword(soup)
        PreResults = []
        PreResults.extend(KeyphrasesKeyword)
        PreResults.append(StrongWord)
        PreResults.append(EmWord)
        PreSet = set(PreResults)
        try:
            PreSet.remove('')
        except:
            pass
        PreList = list(PreSet)
        PreList.sort(key = PreResults.index)
        if PreList == []:
            return ''
        else:
            Result = self.MatchBestResults(keyword, PreList)
            return Result
