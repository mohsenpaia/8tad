#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import gensim
import os


class QE:
    """
      This class implements a query expansion system for Persian.
    """

    def __init__(self):
        """
        This constructor loads model.
        """
        # self.W2Vmodel = gensim.models.Word2Vec.load('Model/WordEmbeddingModel.model')
        dir = os.path.dirname(__file__)
        self.W2Vmodel_1 = gensim.models.Word2Vec.load(str(dir) + r'/Model2/model.w2v')
        print
        "Model2 Loaded"
        # self.W2Vmodel = gensim.models.KeyedVectors.load('Model/WordEmbeddingModel.model')
        # self.W2Vmodel_1 = gensim.models.KeyedVectors.load('Model/model.w2v')
        # self.normalizer = PerNor.PersianTextNormalization()

    def useModel(self, query="", number_of_related_word=5):
        if type(query) == str:
            query = query.decode('utf-8')
        # query_normal = self.normalizer.useFormalModel(query)
        query_normal = query
        # query_spl = query_normal.encode('utf-8').split()
        query_spl = list(set(query_normal.split()))
        positive_word = []
        for word in query_spl:
            if word in self.W2Vmodel.wv.vocab:
                positive_word.append(word)
        try:
            related_words = self.W2Vmodel.most_similar(positive=positive_word, negative=''.split(),
                                                       topn=number_of_related_word)  # ,negative='امریکا آمریکا'.split()
        except:
            print
            u"عبارت '" + query + u"' در لغتنامه وجور ندارد."
            return query
        # query_expanded = [i for i in query_spl]
        query_expanded = []
        query_expanded.extend(i[0] for i in related_words)
        for i in query_expanded: print i
        return (' ').join(query_expanded)

    def useModel_1(self, query="", number_of_related_word=5):
        query_normal = query
        # query_normal = 'asdasdasdas dream💜 💜purpell'
        # print query_normal
        # query_spl = query_normal.encode('utf-8').split()
        query_spl = list(set(query_normal.split()))
        positive_word = []
        for word in query_spl:
            if word in self.W2Vmodel_1.wv.vocab:
                positive_word.append(word)
            # else:
            #     print word
        # print 'ssdasdasdasd'
        # print positive_word
        # print 'sdadasdasd'
        if len(positive_word) == 0:
            return []
        try:
            related_words = self.W2Vmodel_1.most_similar(positive=positive_word, negative=''.split(),
                                                         topn=number_of_related_word)  # ,negative='امریکا آمریکا'.split()

        except:
            # print query_normal + " not found in dictionary!"
            return query_normal
        # print '------------'
        # for i in positive_word:
        #     print i
        # query_expanded = [i for i in query_spl]
        query_expanded = []

        query_expanded.extend(i[0] for i in related_words)
        # print '------------'
        # for i in query_expanded:
        #     print i

        return query_expanded
