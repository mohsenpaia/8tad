#!/usr/bin/python
# -*- coding: utf-8 -*-

import io
import re
import glob
import os
import string
import codecs
import PersianTextNormalization as PerNor
import operator
from bs4 import BeautifulSoup
from nltk import ngrams



class TagExtraction:
    def __init__(self):
        self.Pe = PerNor.PersianTextNormalization()

    def HTML_ExtractContent(self, HTML):
        HTML = HTML.replace('\r\n', ' ')
        HTML = HTML.replace('\n', ' ')
        HTML = HTML.replace('\r', ' ')
        HTML = HTML.replace('\t', ' ')
        HTML = re.sub(
            r"(<!--.*?-->)|(<ul.*?</ul>)|(<head.*?</head>)|(<a.*?</a>)|(<li.*?</li>)|(<h\d.*?</h\d>)|(<footer.*?</footer>)|(<script.*?</script>)|(<header>.*?</header>)|(<ul.*?</ul>)|(<h\d.*?</h\d>)".decode(
                'utf-8'), ' ', HTML, flags=re.UNICODE)
        HTML = re.sub(r"([a-zA-Z0-9])|(=|\"|-|>|<|/|:|;|_|\!|'|\(|\)|\*|،|,)|(&|\$|\+|\.|#)".decode('utf-8'), ' ', HTML,
                      flags=re.UNICODE)
        HTML = re.sub(r"( )( )+|(\t+)".decode('utf-8'), ' ', HTML, flags=re.UNICODE)
        HTML = HTML.replace('،', ' ').replace('%', ' ').replace('}', ' ').replace('|', ' ').replace('{', ' ').replace('[',
                                                                                                                      ' ').replace(
            ']', ' ')
        HTML = re.sub(r"( )( )+|(\t+)".decode('utf-8'), ' ', HTML, flags=re.UNICODE)
        return HTML
    def HTML_ExtractContent_ListHTML(self):
        Output = io.open(r"D:\Python\HTML2Content\Output_HTMLs2Content.txt", 'w', encoding="utf-8")
        with io.open(r"C:\Users\Goorj\Downloads\Telegram Desktop\r (2).txt", 'rb') as input:
            HTML = input.readline()
            while HTML:
                Content = HTML_ExtractContent(HTML)
                Output.write(Content.decode('utf-8') + '\n')
                HTML = input.readline()
        Output.close()
    def HTML_CleanText(self, HTML_Normal):
        HTML_FarsiCharacter = HTML_Normal.replace(u'\n', u' ').replace(u'<', u' ').replace(u'>', u' ').replace(u'\r', u' ')
        HTML_FarsiCharacter = re.sub(
            r"([a-zA-Z])|(=|\"|-|>|<|/|:|;|_|\!|'|\(|\)|\*|،|,)|(&|\$|\+|\.|#)".decode('utf-8'), ' ', HTML_FarsiCharacter,
            flags=re.UNICODE)
        HTML_FarsiCharacter = re.sub(r"( )( )+|(\t+)".decode('utf-8'), ' ', HTML_FarsiCharacter, flags=re.UNICODE)
        HTML_FarsiCharacter = HTML_FarsiCharacter.replace(u'،', u' ').replace(u'%', u' ').replace(u'}', u' ').replace(u'|',
                                                                                                                      u' ').replace(
            u'{', u' ').replace(u'[', u' ').replace(u']', u' ')
        HTML_FarsiCharacter = re.sub(r"( )( )+|(\t+)".decode('utf-8'), ' ', HTML_FarsiCharacter, flags=re.UNICODE)
        return HTML_FarsiCharacter
    def HTML_KeywordsExtractionByNewsTags(self, HTML, StopWords,Blacklists,BigramTags,TrigramTags,QuadgramTags):
        #StopWords, Blacklists, BigramTags, TrigramTags, QuadgramTags = Load_Files()
        Pe = PerNor.PersianTextNormalization()
        HTML_Normal = Normalization(HTML, Pe)
        soup = BeautifulSoup(HTML, 'html.parser')
        Titles = soup.find_all('title')
        H1s = soup.find_all('h1')
        H2s = soup.find_all('h2')
        Metas = soup.find_all('meta', {'content' : True})
        Bs = soup.find_all('b')
        Title,H1,H2,Meta,B = '','','','',''
        for i in Titles:
            Title += i.get_text() + ' ';
        Title = Title.strip()
        for i in H1s:
            H1 += i.get_text() + ' ';
        H1 = H1.strip()
        for i in H2s:
            H2 += i.get_text() + ' ';
        H2 = H2.strip()
        for i in Metas:
            Meta += i.get('content') + ' ';
        Meta = Meta.strip()
        for i in Bs:
            B += i.get_text() + ' ';
        B = B.strip()

        Title = HTML_CleanText(Title)
        H1 = HTML_CleanText(H1)
        H2 = HTML_CleanText(H2)
        Meta = HTML_CleanText(Meta)
        B = HTML_CleanText(B)
        BiHTMLT, TriHTMLT, QuadHTMLT = Extract_BiTriQuadGramFromRowText(Title,BigramTags,TrigramTags,QuadgramTags)
        BiHTMLH1, TriHTMLH1, QuadHTMLH1 = Extract_BiTriQuadGramFromRowText(H1, BigramTags, TrigramTags, QuadgramTags)
        BiHTMLH2, TriHTMLH2, QuadHTMLH2 = Extract_BiTriQuadGramFromRowText(H2, BigramTags, TrigramTags, QuadgramTags)
        BiHTMLMeta, TriHTMLMeta, QuadHTMLMeta = Extract_BiTriQuadGramFromRowText(Meta, BigramTags, TrigramTags, QuadgramTags)
        BiHTMLB, TriHTMLB, QuadHTMLB = Extract_BiTriQuadGramFromRowText(B, BigramTags, TrigramTags, QuadgramTags)


        # for k, v in BiHTML.items():
        #     if k not in BigramTags:
        #         del BiHTML[k]
        # for k, v in TriHTML.items():
        #     if k not in TrigramTags:
        #         del TriHTML[k]
        # for k, v in QuadHTML.items():
        #     if k not in QuadgramTags:
        #         del QuadHTML[k]
        NgramsT = HTML_SortNgrams(BiHTMLT, TriHTMLT, QuadHTMLT, StopWords, Blacklists,3)
        NgramsH1 = HTML_SortNgrams(BiHTMLH1, TriHTMLH1, QuadHTMLH1, StopWords, Blacklists,2)
        NgramsH2 = HTML_SortNgrams(BiHTMLH2, TriHTMLH2, QuadHTMLH2, StopWords, Blacklists,1.5)
        NgramsM = HTML_SortNgrams(BiHTMLMeta, TriHTMLMeta, QuadHTMLMeta, StopWords, Blacklists,3)
        NgramsB = HTML_SortNgrams(BiHTMLB, TriHTMLB, QuadHTMLB, StopWords, Blacklists,1.5)

        Ngrams = {}
        for i in NgramsT:
            if i[0] not in Ngrams:
                Ngrams[i[0]] = i[1]
        for i in NgramsH1:
            if i[0] not in Ngrams:
                Ngrams[i[0]] = i[1]
        for i in NgramsH2:
            if i[0] not in Ngrams:
                Ngrams[i[0]] = i[1]
        for i in NgramsM:
            if i[0] not in Ngrams:
                Ngrams[i[0]] = i[1]
        for i in NgramsB:
            if i[0] not in Ngrams:
                Ngrams[i[0]] = i[1]
        sorted_Ngrams = sorted(Ngrams.items(), key=operator.itemgetter(1), reverse=True)

        NgramsList = []
        for i in sorted_Ngrams:
            NgramsList.append(i[0])
        return NgramsList
    def HTML_WeightNgrams(self, HTML,word):
        #HTML = u'<sdasdasdas asdasdas> <title>اخبار محلی dadasad adasd </title> <title>بز</title>'
        #word = u'اخبار محلی'
        #word = u'بز'

        W_title,W_meta,W_h1,W_h2,W_b = 3,3,2,1.5,1.5
        temp = re.findall(u"(<title.*?{0}.*?</title)|(<meta.*?{0}.*?</meta)".format(word), HTML.decode('utf-8'), flags=re.UNICODE)
        if len(temp) > 0:
            return 3
        temp = re.findall(u"(<h1.*?{0}.*?</h1)".format(word), HTML.decode('utf-8'), flags=re.UNICODE)
        if len(temp) > 0:
            return 2
        temp = re.findall(u"(<h2.*?{0}.*?</h2)|(<b.*?{0}.*?</b>)".format(word), HTML.decode('utf-8'), flags=re.UNICODE)
        if len(temp) > 0:
            return 1.5
        return 1
    def HTML_KeywordsExtractionByNewsTagsBatch(self):
        inputTags = io.open(r"D:\Python\NER\AutomaticKeyphraseExtractionModel.dictionary", 'r', encoding='utf-8')
        StopWord = io.open(r"D:\Python\HTML2Content\stopwords_Keywords.txt", 'r', encoding='utf-8')
        Blacklist = io.open(r"D:\Python\HTML2Content\BlackList.txt", 'r', encoding='utf-8')

        StopWords = {}
        line = StopWord.readline()
        while line:
            line = line.replace('\n', '')
            if line not in StopWords:
                StopWords[line] = ''
            line = StopWord.readline()
        Blacklists = {}
        line = Blacklist.readline()
        while line:
            line = line.replace('\n', '')
            if line not in Blacklists:
                Blacklists[line] = ''
            line = Blacklist.readline()

        # line = inputTags.readline().decode('unicode-escape')
        ListOfTags = {}
        counter = 0
        BigramTags = {}
        TrigramTags = {}
        QuadgramTags = {}
        line = inputTags.readline().decode('unicode-escape')
        while line != u'':
            line = line.replace('\n', '')
            spl = line.split()
            if len(spl) == 1 or len(spl) > 4:
                line = inputTags.readline().decode('unicode-escape')
                continue
            if len(spl) == 4:
                if line not in QuadgramTags:
                    QuadgramTags[line] = ''
            elif len(spl) == 3:
                if line not in TrigramTags:
                    TrigramTags[line] = ''
            elif len(spl) == 2:
                if line not in BigramTags and spl[0] not in StopWords and spl[1] not in StopWords:
                    BigramTags[line] = ''
            else:
                sdsada = 0
            line = inputTags.readline().decode('unicode-escape')
            counter += 1
        Output = io.open(r"D:\Python\HTML2Content\KeywordsExtractionByNewsTags_Result.txt", 'w', encoding='utf-8')
        with io.open("D:\Python\HTML2Content\HTMLs.txt", 'rb') as input:
            HTML = input.readline()
            while HTML:
                HTML_FarsiCharacter = re.sub(
                    r"([a-zA-Z])|(=|\"|-|>|<|/|:|;|_|\!|'|\(|\)|\*|،|,)|(&|\$|\+|\.|#)".decode('utf-8'), ' ', HTML,
                    flags=re.UNICODE)
                HTML_FarsiCharacter = re.sub(r"( )( )+|(\t+)".decode('utf-8'), ' ', HTML_FarsiCharacter, flags=re.UNICODE)
                HTML_FarsiCharacter = HTML_FarsiCharacter.replace('،', ' ').replace('%', ' ').replace('}', ' ').replace('|',
                                                                                                                        ' ').replace(
                    '{', ' ').replace('[', ' ').replace(']', ' ')
                HTML_FarsiCharacter = re.sub(r"( )( )+|(\t+)".decode('utf-8'), ' ', HTML_FarsiCharacter, flags=re.UNICODE)
                BiHTML,TriHTML,QuadHTML = Extract_BiTriQuadGramFromRowText(HTML_FarsiCharacter)
                for k,v in BiHTML.items():
                    if k not in BigramTags:
                        del BiHTML[k]

                for k,v in TriHTML.items():
                    if k not in TrigramTags:
                        del TriHTML[k]
                for k,v in QuadHTML.items():
                    if k not in QuadgramTags:
                        del QuadHTML[k]
                BiHTML, TriHTML, QuadHTML, Ngrams = HTML_SortNgrams(BiHTML, TriHTML, QuadHTML, StopWords, Blacklists)
                Output.write(u'--------------------------------------------------------------------------------\n')
                Output.write('News:\t' + HTML_FarsiCharacter.decode('utf-8'))
                for i in Ngrams:
                    Output.write(i[0] + '\t')
                # Output.write(u'\nQuadgrams:\n')
                # for i in QuadHTML:
                #     Output.write(i[0] + '\t')
                # Output.write(u'\nTrigrams:\n')
                # for i in TriHTML:
                #     Output.write(i[0] + '\t')
                # Output.write(u'\nBigrams:\n')
                # for i in BiHTML:
                #     Output.write(i[0] + '\t')
                Output.write(u'\n')
                HTML = input.readline()
        Output.close()





    def HTML_KeywordsExtractionByNewsTagsV2(self,HTML, StopWords,Blacklists,BigramTags,TrigramTags,QuadgramTags, min = 1, max = 10):
        #StopWords, Blacklists, BigramTags, TrigramTags, QuadgramTags = Load_Files()

        HTML_Normal = self.Normalization(HTML, self.Pe)
        # print 'HTML_Normal : {}'.format(HTML_Normal)

        soup = BeautifulSoup(HTML, 'html.parser')
        Titles = soup.find_all('title')
        H1s = soup.find_all('h1')
        H2s = soup.find_all('h2')
        Metas = soup.find_all('meta', {'content' : True})
        Bs = soup.find_all('b')
        Title,H1,H2,Meta,B = '','','','',''
        for i in Titles:
            Title += i.get_text() + ' ';
        Title = Title.strip()
        for i in H1s:
            H1 += i.get_text() + ' ';
        H1 = H1.strip()
        for i in H2s:
            H2 += i.get_text() + ' ';
        H2 = H2.strip()
        for i in Metas:
            Meta += i.get('content') + ' ';
        Meta = Meta.strip()
        for i in Bs:
            B += i.get_text() + ' ';
        B = B.strip()

        Title = self.HTML_CleanText(Title)
        H1 = self.HTML_CleanText(H1)
        H2 = self.HTML_CleanText(H2)
        Meta = self.HTML_CleanText(Meta)
        B = self.HTML_CleanText(B)
        # print 'title : {}'.format(Title)
        # print 'H1 : {}'.format(H1)
        # print 'H2 : {}'.format(H2)
        # print 'Meta : {}'.format(Meta)
        # print 'B : {}'.format(B)
        BiHTMLT, TriHTMLT, QuadHTMLT = self.Extract_BiTriQuadGramFromRowText(Title,BigramTags,TrigramTags,QuadgramTags)
        BiHTMLH1, TriHTMLH1, QuadHTMLH1 = self.Extract_BiTriQuadGramFromRowText(H1, BigramTags, TrigramTags, QuadgramTags)
        BiHTMLH2, TriHTMLH2, QuadHTMLH2 = self.Extract_BiTriQuadGramFromRowText(H2, BigramTags, TrigramTags, QuadgramTags)
        BiHTMLMeta, TriHTMLMeta, QuadHTMLMeta = self.Extract_BiTriQuadGramFromRowText(Meta, BigramTags, TrigramTags, QuadgramTags)
        BiHTMLB, TriHTMLB, QuadHTMLB = self.Extract_BiTriQuadGramFromRowText(B, BigramTags, TrigramTags, QuadgramTags)


        # for k, v in BiHTML.items():
        #     if k not in BigramTags:
        #         del BiHTML[k]
        # for k, v in TriHTML.items():
        #     if k not in TrigramTags:
        #         del TriHTML[k]
        # for k, v in QuadHTML.items():
        #     if k not in QuadgramTags:
        #         del QuadHTML[k]
        NgramsT = self.HTML_SortNgrams(BiHTMLT, TriHTMLT, QuadHTMLT, StopWords, Blacklists,3,HTML)
        NgramsH1 = self.HTML_SortNgrams(BiHTMLH1, TriHTMLH1, QuadHTMLH1, StopWords, Blacklists,2,HTML)
        NgramsH2 = self.HTML_SortNgrams(BiHTMLH2, TriHTMLH2, QuadHTMLH2, StopWords, Blacklists,1.5,HTML)
        NgramsM = self.HTML_SortNgrams(BiHTMLMeta, TriHTMLMeta, QuadHTMLMeta, StopWords, Blacklists,3,HTML)
        NgramsB = self.HTML_SortNgrams(BiHTMLB, TriHTMLB, QuadHTMLB, StopWords, Blacklists,1.5,HTML)

        Ngrams = {}
        for i in NgramsT:
            if i[0] not in Ngrams:
                Ngrams[i[0]] = i[1]
        for i in NgramsH1:
            if i[0] not in Ngrams:
                Ngrams[i[0]] = i[1]
        for i in NgramsH2:
            if i[0] not in Ngrams:
                Ngrams[i[0]] = i[1]
        for i in NgramsM:
            if i[0] not in Ngrams:
                Ngrams[i[0]] = i[1]
        for i in NgramsB:
            if i[0] not in Ngrams:
                Ngrams[i[0]] = i[1]
        # print 'len ngrams : {}'.format(len(Ngrams))
        # print Ngrams
        if len(Ngrams) == 0:
            return []
        sorted_Ngrams = sorted(Ngrams.items(), key=operator.itemgetter(1), reverse=True)
        length = len(sorted_Ngrams)
        # print 'len ngrams : {}'.format(len(sorted_Ngrams))
        # print min
        # print length

        if length <= min:
            return [i[0] for i in sorted_Ngrams]
        if length > max:
            sorted_Ngrams = sorted_Ngrams[:max]

        NgramsList = [i[0] for i in sorted_Ngrams[:min]]
        # score_sum = sorted_Ngrams[0][1]
        pscore = sorted_Ngrams[min-1][1]
        for i in sorted_Ngrams[min:]:
            if float(pscore)/float(i[1]) > 2:
                break
            NgramsList.append(i[0])
            pscore = i[1]
        # sorted_Ngrams_normalize = [(i[0],float(i[1])/float(score_sum)) for i in sorted_Ngrams[:min(num,len(NgramsList))]]

        return NgramsList
    def HTML_SortNgrams(self,BiHTML,TriHTML,QuadHTML,StopWords,Blacklists,weight, HTML):
        BagOfWords = {}
        for words in BiHTML:
            spl = words.split()
            for word in spl:
                if word not in StopWords:
                    if word not in BagOfWords:
                        BagOfWords[word] = HTML.count(word.encode('utf-8'))
                    else:
                        BagOfWords[word] = BagOfWords[word] + 1
        for words in TriHTML:
            spl = words.split()
            for word in spl:
                if word not in StopWords:
                    if word not in BagOfWords:
                        BagOfWords[word] =  HTML.count(word.encode('utf-8'))
                    else:
                        BagOfWords[word] = BagOfWords[word] + 1
        for words in QuadHTML:
            spl = words.split()
            for word in spl:
                if word not in StopWords:
                    if word not in BagOfWords:
                        BagOfWords[word] = HTML.count(word.encode('utf-8'))
                    else:
                        BagOfWords[word] = BagOfWords[word] + 1
        #--------------------score Ngrmas
        Stop = .5
        for words in BiHTML:
            spl = words.split()
            for word in spl:
                if word in StopWords:
                    BiHTML[words] += Stop
                else:
                    BiHTML[words] +=  BagOfWords[word]
        for words in TriHTML:
            spl = words.split()
            for word in spl:
                if word in StopWords:
                    TriHTML[words] += Stop
                else:
                    TriHTML[words] += BagOfWords[word]
        for words in QuadHTML:
            spl = words.split()
            for word in spl:
                if word in StopWords:
                    QuadHTML[words] += Stop
                else:
                    QuadHTML[words] += BagOfWords[word]
        Ngrams = BiHTML.copy()
        Ngrams.update(TriHTML)
        Ngrams.update(QuadHTML)
        for k, v in Ngrams.items():
            for k1 in Blacklists:
                if k1 in k:
                    del Ngrams[k]

        for k, v in Ngrams.items():
            Ngrams[k] *= weight
        sorted_Ngrams = sorted(Ngrams.items(), key=operator.itemgetter(1), reverse=True)
        return sorted_Ngrams

    # --------Misc------------
    def Load_Files(self):
        # --------Load Files-------------
        dir = os.path.dirname(__file__)
        inputTags = io.open(str(dir) + r'/AutomaticKeyphraseExtractionModel.dictionary', 'r', encoding='utf-8')
        StopWord = io.open(str(dir) + r'/stopwords_Keywords.txt', 'r', encoding='utf-8')
        Blacklist = io.open(str(dir) + r'/BlackList.txt', 'r', encoding='utf-8')
        StopWords = {}
        line = StopWord.readline()
        while line:
            line = line.replace('\n', '')
            if line not in StopWords:
                StopWords[line] = ''
            line = StopWord.readline()
        Blacklists = {}
        line = Blacklist.readline()
        while line:
            line = line.replace('\n', '')
            if line not in Blacklists:
                Blacklists[line] = ''
            line = Blacklist.readline()
        # line = inputTags.readline().decode('unicode-escape')
        ListOfTags = {}
        counter = 0
        BigramTags = {}
        TrigramTags = {}
        QuadgramTags = {}
        line = inputTags.readline().decode('unicode-escape')
        while line != u'':
            line = line.replace('\n', '')
            spl = line.split()
            if len(spl) == 1 or len(spl) > 4:
                line = inputTags.readline().decode('unicode-escape')
                continue
            if len(spl) == 4:
                if line not in QuadgramTags:
                    QuadgramTags[line] = ''
            elif len(spl) == 3:
                if line not in TrigramTags:
                    TrigramTags[line] = ''
            elif len(spl) == 2:
                if line not in BigramTags and spl[0] not in StopWords and spl[1] not in StopWords:
                    BigramTags[line] = ''
            line = inputTags.readline().decode('unicode-escape')
            counter += 1
        return StopWords,Blacklists,BigramTags,TrigramTags,QuadgramTags
    def Normalization(self,InputString, Pe):
        OutputString = Pe.useFormalModel(InputString.decode('utf-8'))
        return OutputString
    def Extract_BiTriQuadGramFromTags(self,Tags):
        fdsfsd = 0
    def Extract_BiTriQuadGramFromRowText(self,HTML, BigramTags,TrigramTags,QuadgramTags):
        Bigram = {}
        Trigram = {}
        Quadgram = {}
        QuadgramCount = 0
        TrigramCount = 0
        BigramCount = 0
        #Pe = PerNor.PersianTextNormalization()
        #HTML_Normal = Normalization(HTML, Pe)
        Ngrams = {}
        # token = '<Hi How are you? i am fine and you \n dasdaasd aasdas\n dasdasdasdas X>\n>'
        HTML_Normal = HTML.replace('\n', ' ').replace('<', ' ').replace('>', ' ').replace('\r', ' ').split()
        c = 0
        while c < len(HTML_Normal) - 3:
            temp = HTML_Normal[c] + ' ' + HTML_Normal[c + 1] + ' ' + HTML_Normal[c + 2] + ' ' + HTML_Normal[c + 3]
            if temp not in Quadgram and temp in QuadgramTags:
                Quadgram[temp] = 0
                QuadgramCount += 1
            temp = HTML_Normal[c] + ' ' + HTML_Normal[c + 1] + ' ' + HTML_Normal[c + 2]
            if temp not in Trigram and temp in TrigramTags:
                Trigram[temp] = 0
                TrigramCount += 1
            temp = HTML_Normal[c] + ' ' + HTML_Normal[c + 1]
            if temp not in Bigram and temp in BigramTags:
                Bigram[temp] = 0
                BigramCount += 1
            c += 1
        c -= 1
        if len(HTML_Normal)>2:
            temp = HTML_Normal[c] + ' ' + HTML_Normal[c + 1] + ' ' + HTML_Normal[c + 2]
            if temp not in Trigram and temp in TrigramTags:
                Trigram[temp] = 0
                TrigramCount += 1
        if len(HTML_Normal) > 1:
            temp = HTML_Normal[c] + ' ' + HTML_Normal[c + 1]
            if temp not in Bigram and temp in BigramTags:
                Bigram[temp] = 0
                BigramCount += 1
            c += 1
            temp = HTML_Normal[c] + ' ' + HTML_Normal[c + 1]
            if temp not in Bigram and temp in BigramTags:
                Bigram[temp] = 0
                BigramCount += 1
        #print 'Bigram:' + str(BigramCount)
        #print 'Trigram:' + str(TrigramCount)
        #print 'Quadgram:' + str(QuadgramCount)
        return Bigram, Trigram, Quadgram