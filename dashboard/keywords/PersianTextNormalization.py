#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
##########################################################


##########################################################
# Persian Text Normalization
# Mohammad Mahdavi
# moh.mahdavi.l@gmail.com
# July 2016
# Homaplus Corporation
# homaplus.com
# All Rights Reserved
# Do not Change, Alter, or Remove this Licence
##########################################################


##########################################################
import os
import re
import pickle
import json
import operator
import itertools
from itertools import count

#from pycallgraph.output.output import Output

import ParameterConfiguration as PC
import DataFileIteration
import TextTokenization
import io
##########################################################


##########################################################
class PersianTextNormalization:
    """
    This class implements a sophisticated text normalization system for Persian.
    """

    def __init__(self):
        """
        This constructor loads model.
        """
        formal_term_transformation_backup_path = os.path.join(PC.MODEL_FOLDER, "FormalPersianTextNormalizationModel.dictionary")
        if os.path.exists(formal_term_transformation_backup_path):
            self.formal_term_transformation = pickle.load(open(formal_term_transformation_backup_path, "rb"))
        else:
            print "Formal Persian Text Normalization Model is not Found!"
        informal_term_transformation_backup_path = os.path.join(PC.MODEL_FOLDER, "InformalPersianTextNormalizationModel.dictionary")
        if os.path.exists(informal_term_transformation_backup_path):
            self.informal_term_transformation = pickle.load(open(informal_term_transformation_backup_path, "rb"))
        else:
            print "Informal Persian Text Normalization Model is not Found!"
        self.tt = TextTokenization.TextTokenization()

    def characterNormalizer(self, text, learning=False):
        """
        This method is a character normalizer for Persian.
        """
        # Remove Useless Characters
        text = re.sub("[ًٌٍَُِّْٰٖٓٔـۖۚٴ]+".decode("utf-8"), "", text, flags=re.UNICODE)
        text = re.sub(u"[\u200b\u200d\u202b\u202c\u202e\u202d\ufeff\ufe0f]+", "", text, flags=re.UNICODE)
        # Unify Different Half Distance, Space, and New Line Characters
        text = re.sub(u"[\u200c\u00ac\u200f\u200e\u202a\u009d\u2029\u0086\u0097\u0090\u0093\u0098\u009e\u206f\u206d]+|(&zwnj;)+", "\xE2\x80\x8C".decode("utf-8"), text, flags=re.UNICODE)
        text = re.sub(u"[ \u00a0\u200a\u2009\u2005\u2003\u202f\u2028\t\f\v]+|(&nbsp;)+", " ", text, flags=re.UNICODE)
        text = re.sub("[\r\n]+", "\n", text, flags=re.UNICODE)
        text = text.strip("\n \xE2\x80\x8C".decode("utf-8"))
        # Unify Different Symbols
        # text = re.sub("[Δ□■¥●▪•♦◄٭❤✔♥✅★♡❄⚡⭐✩]".decode("utf-8"), "•".decode("utf-8"), text, flags=re.UNICODE)
        text = re.sub("[″˝”“]".decode("utf-8"), '"'.decode("utf-8"), text, flags=re.UNICODE)
        text = re.sub("[‘٬ˈ`’]".decode("utf-8"), "'".decode("utf-8"), text, flags=re.UNICODE)
        text = re.sub("[­−–—‐]".decode("utf-8"), "-".decode("utf-8"), text, flags=re.UNICODE)
        text = re.sub("[❗]".decode("utf-8"), "!".decode("utf-8"), text, flags=re.UNICODE)
        text = re.sub("[·]".decode("utf-8"), ".".decode("utf-8"), text, flags=re.UNICODE)
        text = re.sub("[˛]".decode("utf-8"), "،".decode("utf-8"), text, flags=re.UNICODE)
        text = re.sub("[：]".decode("utf-8"), ":".decode("utf-8"), text, flags=re.UNICODE)
        text = re.sub("[》﴿]".decode("utf-8"), "»".decode("utf-8"), text, flags=re.UNICODE)
        text = re.sub("[《﴾]".decode("utf-8"), "«".decode("utf-8"), text, flags=re.UNICODE)
        text = re.sub("[›]".decode("utf-8"), ">".decode("utf-8"), text, flags=re.UNICODE)
        text = re.sub("[‹]".decode("utf-8"), "<".decode("utf-8"), text, flags=re.UNICODE)
        text = re.sub("[）]".decode("utf-8"), ")".decode("utf-8"), text, flags=re.UNICODE)
        text = re.sub("[（]".decode("utf-8"), "(".decode("utf-8"), text, flags=re.UNICODE)
        text = re.sub(" ?[.]{3,}".decode("utf-8"), "…".decode("utf-8"), text, flags=re.UNICODE)
        text = re.sub("[٪]".decode("utf-8"), "%".decode("utf-8"), text, flags=re.UNICODE)
        # Unify Alphabet Characters
        text = re.sub("[ﺍﺎٱ]".decode("utf-8"), "ا".decode("utf-8"), text, flags=re.UNICODE)
        text = re.sub("[ٱﺁ]".decode("utf-8"), "آ".decode("utf-8"), text, flags=re.UNICODE)
        text = re.sub("[ﺏﺐﺒﺑ]".decode("utf-8"), "ب".decode("utf-8"), text, flags=re.UNICODE)
        text = re.sub("[ﭙﭘﭗ]".decode("utf-8"), "پ".decode("utf-8"), text, flags=re.UNICODE)
        text = re.sub("[ﺕﺗﺖﺘ]".decode("utf-8"), "ت".decode("utf-8"), text, flags=re.UNICODE)
        text = re.sub("[ﺚﺛﺜ]".decode("utf-8"), "ث".decode("utf-8"), text, flags=re.UNICODE)
        text = re.sub("[ﺞﺠﺟﺝ]".decode("utf-8"), "ج".decode("utf-8"), text, flags=re.UNICODE)
        text = re.sub("[ﭻﭽﭼ]".decode("utf-8"), "چ".decode("utf-8"), text, flags=re.UNICODE)
        text = re.sub("[ﺤﺣﺢ]".decode("utf-8"), "ح".decode("utf-8"), text, flags=re.UNICODE)
        text = re.sub("[ﺨﺧﺦ]".decode("utf-8"), "خ".decode("utf-8"), text, flags=re.UNICODE)
        text = re.sub("[ﺩﺪ]".decode("utf-8"), "د".decode("utf-8"), text, flags=re.UNICODE)
        text = re.sub("[ﺬﺫ]".decode("utf-8"), "ذ".decode("utf-8"), text, flags=re.UNICODE)
        text = re.sub("[ﺭﺮ]".decode("utf-8"), "ر".decode("utf-8"), text, flags=re.UNICODE)
        text = re.sub("[ﺰﺯ]".decode("utf-8"), "ز".decode("utf-8"), text, flags=re.UNICODE)
        text = re.sub("[ﮊ]".decode("utf-8"), "ژ".decode("utf-8"), text, flags=re.UNICODE)
        text = re.sub("[ﺲﺱﺴﺳ]".decode("utf-8"), "س".decode("utf-8"), text, flags=re.UNICODE)
        text = re.sub("[ﺵﺶﺸﺷ]".decode("utf-8"), "ش".decode("utf-8"), text, flags=re.UNICODE)
        text = re.sub("[ﺺﺼﺻ]".decode("utf-8"), "ص".decode("utf-8"), text, flags=re.UNICODE)
        text = re.sub("[ﺿﻀﺽ]".decode("utf-8"), "ض".decode("utf-8"), text, flags=re.UNICODE)
        text = re.sub("[ﻂﻄﻃ]".decode("utf-8"), "ط".decode("utf-8"), text, flags=re.UNICODE)
        text = re.sub("[ﻈﻇ]".decode("utf-8"), "ظ".decode("utf-8"), text, flags=re.UNICODE)
        text = re.sub("[ﻊﻌﻋﻉ]".decode("utf-8"), "ع".decode("utf-8"), text, flags=re.UNICODE)
        text = re.sub("[ﻎﻐﻏﻍ]".decode("utf-8"), "غ".decode("utf-8"), text, flags=re.UNICODE)
        text = re.sub("[ﻑﻒﻔﻓ]".decode("utf-8"), "ف".decode("utf-8"), text, flags=re.UNICODE)
        text = re.sub("[ﻕﻖﻘﻗ]".decode("utf-8"), "ق".decode("utf-8"), text, flags=re.UNICODE)
        text = re.sub("[ﻜﻛﮎﮏﮑﮐكڪﻚګ]".decode("utf-8"), "ک".decode("utf-8"), text, flags=re.UNICODE)
        text = re.sub("[ﮓﮒﮕﮔ]".decode("utf-8"), "گ".decode("utf-8"), text, flags=re.UNICODE)
        text = re.sub("[ﻝﻞﻠﻟ]".decode("utf-8"), "ل".decode("utf-8"), text, flags=re.UNICODE)
        text = re.sub("[ﻡﻢﻤﻣ]".decode("utf-8"), "م".decode("utf-8"), text, flags=re.UNICODE)
        text = re.sub("[ﻦﻥﻨﻧ]".decode("utf-8"), "ن".decode("utf-8"), text, flags=re.UNICODE)
        text = re.sub("[ۆﻭﻮۊ]".decode("utf-8"), "و".decode("utf-8"), text, flags=re.UNICODE)
        text = re.sub("[ەھﻬﻩﻫﻪﮤۀةہ]".decode("utf-8"), "ه".decode("utf-8"), text, flags=re.UNICODE)
        text = re.sub("[ﻱﻲﻯﻴﻰﻳﯼﯽﯾﯿيىےێې]".decode("utf-8"), "ی".decode("utf-8"), text, flags=re.UNICODE)
        text = re.sub("ﻻ|ﻼ".decode("utf-8"), "لا".decode("utf-8"), text, flags=re.UNICODE)
        # Unify and Remove Hamzeh Characters
        text = re.sub("[ﺌﺋ]".decode("utf-8"), "ئ".decode("utf-8"), text, flags=re.UNICODE)
        text = re.sub("[ء]".decode("utf-8"), "".decode("utf-8"), text, flags=re.UNICODE)
        text = re.sub("[إأ]".decode("utf-8"), "ا".decode("utf-8"), text, flags=re.UNICODE)
        text = re.sub("[ؤ]".decode("utf-8"), "و".decode("utf-8"), text, flags=re.UNICODE)
        for x, y in PC.PTN_HAMZEH_REPLACE_LIST:
            text = re.sub(x, y, text, flags=re.UNICODE)
        # Convert Numbers to English
        text = re.sub("[۰٠]".decode("utf-8"), "0".decode("utf-8"), text, flags=re.UNICODE)
        text = re.sub("[۱١]".decode("utf-8"), "1".decode("utf-8"), text, flags=re.UNICODE)
        text = re.sub("[۲٢]".decode("utf-8"), "2".decode("utf-8"), text, flags=re.UNICODE)
        text = re.sub("[۳٣]".decode("utf-8"), "3".decode("utf-8"), text, flags=re.UNICODE)
        text = re.sub("[۴٤]".decode("utf-8"), "4".decode("utf-8"), text, flags=re.UNICODE)
        text = re.sub("[۵٥]".decode("utf-8"), "5".decode("utf-8"), text, flags=re.UNICODE)
        text = re.sub("[۶٦]".decode("utf-8"), "6".decode("utf-8"), text, flags=re.UNICODE)
        text = re.sub("[۷٧]".decode("utf-8"), "7".decode("utf-8"), text, flags=re.UNICODE)
        text = re.sub("[۸٨]".decode("utf-8"), "8".decode("utf-8"), text, flags=re.UNICODE)
        text = re.sub("[۹٩]".decode("utf-8"), "9".decode("utf-8"), text, flags=re.UNICODE)
        # Remove Extra Half Distance Characters
        text = re.sub("([^{}])\xE2\x80\x8C".decode("utf-8").format(PC.PERSIAN_ALPHABET_JOINABLE), "\g<1>", text, flags=re.UNICODE)
        text = re.sub("\xE2\x80\x8C([^{}])".decode("utf-8").format(PC.PERSIAN_ALPHABET_FULL), "\g<1>", text, flags=re.UNICODE)
        # Remove Yeh Character
        text = re.sub("ه[ \xE2\x80\x8C]ی([^{}]|$)".decode("utf-8").format(PC.PERSIAN_ALPHABET_FULL), "ه\g<1>".decode("utf-8"), text, flags=re.UNICODE)
        # Replace . with Half Distance in Persian Abbreviations
        text = re.sub("(^|[^{0}])([{0}]{{1,2}})([.])([{0}]{{1,2}})([.])([{0}]{{1,2}})([.])([{0}]{{1,2}})([^{0}]|$)".decode("utf-8").format(PC.PERSIAN_ALPHABET_FULL), "\g<1>\g<2>\xE2\x80\x8C\g<4>\xE2\x80\x8C\g<6>\xE2\x80\x8C\g<8>\g<9>".decode("utf-8"), text, flags=re.UNICODE)
        text = re.sub("(^|[^{0}])([{0}]{{1,2}})([.])([{0}]{{1,2}})([.])([{0}]{{1,2}})([^{0}]|$)".decode("utf-8").format(PC.PERSIAN_ALPHABET_FULL), "\g<1>\g<2>\xE2\x80\x8C\g<4>\xE2\x80\x8C\g<6>\g<7>".decode("utf-8"), text, flags=re.UNICODE)
        text = re.sub("(^|[^{0}])([{0}]{{1,2}})([.])([{0}]{{1,2}})([^{0}]|$)".decode("utf-8").format(PC.PERSIAN_ALPHABET_FULL), "\g<1>\g<2>\xE2\x80\x8C\g<4>\g<5>".decode("utf-8"), text, flags=re.UNICODE)
        # Remove In Parentheses Spaces
        text = re.sub("([(«<{{[]) ([{}])".decode("utf-8").format(PC.PERSIAN_ALPHABET_FULL), "\g<1>\g<2>", text, flags=re.UNICODE)
        text = re.sub("([{}]) ([)»>}}\]])".decode("utf-8").format(PC.PERSIAN_ALPHABET_FULL), "\g<1>\g<2>", text, flags=re.UNICODE)     
        # Set Space Before Persian and English, Number or Some Punctuations Characters
        text = re.sub("([{}])([a-zA-Z\d(«<{{[])".decode("utf-8").format(PC.PERSIAN_ALPHABET_FULL), "\g<1> \g<2>", text, flags=re.UNICODE)
        text = re.sub("([a-zA-Z\d)»>}}\].،:؛!؟…])([{}])".decode("utf-8").format(PC.PERSIAN_ALPHABET_FULL), "\g<1> \g<2>", text, flags=re.UNICODE)
        # Remove Space Between Persian and Some Punctuations Characters
        text = re.sub("([{}]) ([.،:؛!؟…])".decode("utf-8").format(PC.PERSIAN_ALPHABET_FULL), "\g<1>\g<2>".decode("utf-8"), text, flags=re.UNICODE)
        # Remove Repetitive Characters
        if not learning:
            text = re.sub("([{}])\\1{{2,}}".decode("utf-8").format(PC.PERSIAN_ALPHABET_FULL), "\g<1>\g<1>", text, flags=re.UNICODE)
        return text

    def makeModel(self):
        """
        This method makes the Persian text normalization models.
        """
        for language_style in ["Formal", "Informal"]:
            unnormalized_term_vocabulary_backup_path = os.path.join(PC.MODEL_FOLDER, language_style + "UnnormalisedTermVocabulary.dictionary")
            if not os.path.exists(unnormalized_term_vocabulary_backup_path):
                print "Processing {} Data...".format(language_style)
                unnormalized_term_vocabulary = {}
                if language_style == "Formal":
                    dfi = DataFileIteration.DataFileIteration(root_path=PC.FORMAL_CORPUS_DATA_FOLDER, file_type="json")
                elif language_style == "Informal":
                    dfi = DataFileIteration.DataFileIteration(root_path=PC.INFORMAL_CORPUS_DATA_FOLDER, file_type="json")
                data = dfi.getNextData()
                while data:
                    data_string = data["string"]
                    document_dictionary = json.loads(data_string)
                    document_content = ""
                    if language_style == "Formal":
                        document_content += "\n".join(document_dictionary["category_list"])
                        document_content += "\n".join(document_dictionary["tag_list"])
                        document_content += document_dictionary["title"]
                        document_content += document_dictionary["abstract"]
                        document_content += document_dictionary["text"]
                    elif language_style == "Informal":
                        if "text" in document_dictionary:
                            document_content += document_dictionary["text"]
                        if "commentText" in document_dictionary:
                            document_content += "\n" + document_dictionary["commentText"]
                    document_content = self.characterNormalizer(document_content, learning=True)
                    for term in self.tt.getTermList(document_content, n=PC.PTN_N_GRAM, t=["PERSIAN"]):
                        if term not in unnormalized_term_vocabulary:
                            unnormalized_term_vocabulary[term] = 0
                        unnormalized_term_vocabulary[term] += 1
                    data = dfi.getNextData()
                pickle.dump(unnormalized_term_vocabulary, open(unnormalized_term_vocabulary_backup_path, "wb"))
            unnormalized_term_vocabulary = pickle.load(open(unnormalized_term_vocabulary_backup_path, "rb"))
            term_transformation = {}
            print "Learning {} Persian Text Normalization Model...".format(language_style)
            for term in unnormalized_term_vocabulary:
                if term.count(" ") == 0:
                    # Normalization of ی and ئ
                    if "ئ".decode("utf-8") in term:
                        index_list = [i for i, x in enumerate(list(term)) if x == "ئ".decode("utf-8")]
                        character_list = "یئ".decode("utf-8")
                        permutation_list = itertools.product(character_list, repeat=len(index_list))
                        term_type_dictionary = {}
                        for permutation in permutation_list:
                            new_term = list(term)
                            for i, character in enumerate(permutation):
                                new_term[index_list[i]] = character
                            new_term = "".join(new_term)
                            if new_term in unnormalized_term_vocabulary:
                                term_type_dictionary[new_term] = unnormalized_term_vocabulary[new_term]
                        true_term = max(term_type_dictionary.items(), key=operator.itemgetter(1))[0]
                        if unnormalized_term_vocabulary[true_term] >= PC.PTN_TERM_MIN_SUPPORT:
                            for term_type in term_type_dictionary:
                                if term_type != true_term and term_type not in PC.PTN_HAMZEH_BLACK_LIST:
                                    term_transformation[term_type] = true_term
                    # Normalization of آ and ا
                    # This Part Needs a Black List
                    # if "آ".decode("utf-8") in term:
                    #     index_list = [i for i, x in enumerate(list(term)) if x == "آ".decode("utf-8")]
                    #     character_list = "آا".decode("utf-8")
                    #     permutation_list = itertools.product(character_list, repeat=len(index_list))
                    #     term_type_dictionary = {}
                    #     for permutation in permutation_list:
                    #         new_term = list(term)
                    #         for i, character in enumerate(permutation):
                    #             new_term[index_list[i]] = character
                    #         new_term = "".join(new_term)
                    #         if new_term in unnormalized_term_vocabulary:
                    #             term_type_dictionary[new_term] = unnormalized_term_vocabulary[new_term]
                    #     true_term = max(term_type_dictionary.items(), key=operator.itemgetter(1))[0]
                    #     if unnormalized_term_vocabulary[true_term] >= PC.TERM_MIN_SUPPORT:
                    #         for term_type in term_type_dictionary:
                    #             if term_type != true_term and term_type not in PC.ALEF_BLACK_LIST:
                    #                 term_transformation[term_type] = true_term
                    # Normalization of Repetitive Characters
                    match = re.finditer("([اآبپتثجچحخدذرزژسشصضطظعغفقکگلمنوهیئ\xE2\x80\x8C])\\1{2,}".decode("utf-8"), term, flags=re.UNICODE)
                    span_list = [x.span() for x in match]
                    if span_list:
                        permutation_list = [x for x in itertools.product("12", repeat=len(span_list))]
                        new_term_dictionary = {}
                        for permutation in permutation_list:
                            new_term = ""
                            s = 0
                            for i, c in enumerate(permutation):
                                character = term[span_list[i][0]]
                                new_term += term[s:span_list[i][0]] + int(c) * character
                                s = span_list[i][1]
                            new_term += term[s:]
                            new_term_dictionary[new_term] = 0
                            if new_term in unnormalized_term_vocabulary:
                                new_term_dictionary[new_term] = unnormalized_term_vocabulary[new_term]
                        best_new_term = max(new_term_dictionary.items(), key=operator.itemgetter(1))[0]
                        support = new_term_dictionary[best_new_term]
                        confidence = float(new_term_dictionary[best_new_term]) / (sum(new_term_dictionary.values()) + 1)
                        if confidence >= PC.PTN_TERM_MIN_CONFIDENCE and support >= PC.PTN_TERM_MIN_SUPPORT:
                            for x in new_term_dictionary:
                                if x != best_new_term:
                                    term_transformation[x] = best_new_term
                else:
                    # Deciding on Different Terms Types
                    space_list = re.findall("([اآبپتثجچحخدذرزژسشصضطظعغفقکگلمنوهیئ]+) ([اآبپتثجچحخدذرزژسشصضطظعغفقکگلمنوهیئ]+)".decode("utf-8"), term, flags=re.UNICODE)
                    for x, y in space_list:
                        term_type_1 = x + " " + y
                        term_type_2 = self.characterNormalizer(x + "\xE2\x80\x8C".decode("utf-8") + y)
                        term_type_3 = x + y
                        v_1 = 0
                        if term_type_1 in unnormalized_term_vocabulary:
                            v_1 = unnormalized_term_vocabulary[term_type_1]
                        v_2 = 0
                        if term_type_2 in unnormalized_term_vocabulary:
                            v_2 = unnormalized_term_vocabulary[term_type_2]
                        v_3 = 0
                        if term_type_3 in unnormalized_term_vocabulary:
                            v_3 = unnormalized_term_vocabulary[term_type_3]
                        confidence_1_on_2 = v_1 / float(v_1 + v_2 + 1)
                        if confidence_1_on_2 >= PC.PTN_TERM_MIN_CONFIDENCE:
                            if v_1 >= PC.PTN_TERM_MIN_SUPPORT and v_2 > 0:
                                term_transformation[term_type_2] = term_type_1
                        else:
                            if v_2 >= PC.PTN_TERM_MIN_SUPPORT and v_1 > 0:
                                term_transformation[term_type_1] = term_type_2
                        confidence_2_on_3 = v_2 / float(v_2 + v_3 + 1)
                        if confidence_2_on_3 >= PC.PTN_TERM_MIN_CONFIDENCE:
                            if v_2 >= PC.PTN_TERM_MIN_SUPPORT and v_3 > 0:
                                term_transformation[term_type_3] = term_type_2
                        confidence_3_on_2 = v_3 / float(v_2 + v_3 + 1)
                        if confidence_3_on_2 >= PC.PTN_TERM_MIN_CONFIDENCE:
                            if v_3 >= PC.PTN_TERM_MIN_SUPPORT and v_2 > 0:
                                term_transformation[term_type_2] = term_type_3
            for term in term_transformation:
                new_term = term_transformation[term]
                while new_term in term_transformation:
                    new_term = term_transformation[new_term]
                term_transformation[term] = new_term
            if language_style == "Informal":
                formal_term_transformation_backup_path = os.path.join(PC.MODEL_FOLDER, "FormalPersianTextNormalizationModel.dictionary")
                formal_term_transformation = pickle.load(open(formal_term_transformation_backup_path, "rb"))
                for term in term_transformation:
                    new_term = term_transformation[term]
                    if new_term in formal_term_transformation:
                        new_term = formal_term_transformation[new_term]
                    if term in formal_term_transformation:
                        new_term = formal_term_transformation[term]
                    term_transformation[term] = new_term
            term_transformation_backup_path = os.path.join(PC.MODEL_FOLDER, language_style + "PersianTextNormalizationModel.dictionary")
            pickle.dump(term_transformation, open(term_transformation_backup_path, "wb"))

    def useFormalModel(self, text):
        """
        This method uses the formal Persian text normalization model.
        """
        text = self.characterNormalizer(text)
        for term in self.tt.getTermList(text, n=1, t=["PERSIAN"]):
            if term in self.formal_term_transformation:
                text = text.replace(term, self.formal_term_transformation[term])
        for term in self.tt.getTermList(text, n=2, t=["PERSIAN"]):
            if term.count(" ") > 0:
                space_list = re.findall("[اآبپتثجچحخدذرزژسشصضطظعغفقکگلمنوهیئ]+ [اآبپتثجچحخدذرزژسشصضطظعغفقکگلمنوهیئ]+".decode("utf-8"), term, flags=re.UNICODE)
                for x in space_list:
                    if x in self.formal_term_transformation:
                        text = text.replace(x, self.formal_term_transformation[x])
        return text

    def useInformalModel(self, text):
        """
        This method uses the informal Persian text normalization model.
        """
        text = self.characterNormalizer(text)
        for term in self.tt.getTermList(text, n=1, t=["PERSIAN"]):
            if term in self.informal_term_transformation:
                text = text.replace(term, self.informal_term_transformation[term])
        for term in self.tt.getTermList(text, n=2, t=["PERSIAN"]):
            if term.count(" ") > 0:
                space_list = re.findall("[اآبپتثجچحخدذرزژسشصضطظعغفقکگلمنوهیئ]+ [اآبپتثجچحخدذرزژسشصضطظعغفقکگلمنوهیئ]+".decode("utf-8"), term, flags=re.UNICODE)
                for x in space_list:
                    if x in self.informal_term_transformation:
                        text = text.replace(x, self.informal_term_transformation[x])
        return text
##########################################################


##########################################################

def main():


    persian_text_normalization = PersianTextNormalization()
    # persian_text_normalization.makeModel()
    text = """برای پیش بینی بازی ها به سایت ما مراجعه کنید!""".decode("utf-8")
    #text = """من سیب زمینی ها را خوردم.""".decode("utf-8")
    # persian_text_normalization.characterNormalizer(text)
    #persian_text_normalization.useFormalModel(text)
    print(persian_text_normalization.useFormalModel(text))
    # persian_text_normalization.useInformalModel(text)
def main_getfile():
    persian_text_normalization = PersianTextNormalization()

    Foreignname = io.open(r"D:\Python\NER\Data\Corpus\RawCorpus\LargeNewsCorpus[Ali].txt", 'r', encoding='utf-8')
    listForeignname = Foreignname.readline()
    OutForeignname = io.open(r"D:\Python\NER\Data\Corpus\RawCorpus\LargeNewsCorpus[Ali].txt_Normal_P7.txt", 'wb')
    counter = 1
    part = 7
    while counter < 6231315:
        try:
            listForeignname = Foreignname.readline()
        except:
            listForeignname = Foreignname.readline()
        counter += 1
    counter = 1
    while listForeignname:
        try:
            if len(listForeignname) > 1:
                OutForeignname.write(persian_text_normalization.useFormalModel(listForeignname).encode('utf-8') + "\r\n")
                listForeignname = Foreignname.readline()
                counter += 1
                if counter > 1000000:
                    OutForeignname.close()
                    part += 1
                    OutForeignname = io.open(
                        r"D:\Python\NER\Data\Corpus\RawCorpus\LargeNewsCorpus[Ali].txt_Normal_P" + str(part) + ".txt", 'wb')
                    counter = 0
            else:
                listForeignname = Foreignname.readline()
                counter += 1
        except:
            print "This is an error message!"

    OutForeignname.close()
    '''
    Fname = io.open(r"D:\Python\NER\Data\Person\first names.txt", 'r',encoding='utf-8')
    listFname = Fname.readlines()
    OutFname = io.open(r"D:\Python\NER\Data\Person\first names_Normal.txt", 'wb')
    for text in listFname:
        OutFname.write(persian_text_normalization.useFormalModel(text).encode('utf-8')+"\r\n")
    OutFname.close()

    Lname = io.open(r"D:\Python\NER\Data\Person\last names.txt", 'r',encoding='utf-8')
    listLname = Lname.readlines()
    OutLname = io.open(r"D:\Python\NER\Data\Person\last names_Normal.txt", 'wb')
    for text in listLname:
        OutLname.write(persian_text_normalization.useFormalModel(text).encode('utf-8')+"\r\n")
    OutLname.close()

    Aname = io.open(r"D:\Python\NER\Data\Person\Affiliation.txt", 'r',encoding='utf-8')
    listAname = Aname.readlines()
    OutAname = io.open(r"D:\Python\NER\Data\Person\Affiliation_Normal.txt", 'wb')
    for text in listAname:
        OutAname.write(persian_text_normalization.useFormalModel(text).encode('utf-8')+"\r\n")
    OutAname.close()

    F3name = io.open(r"D:\Python\NER\Data\Person\first names_3tike.txt", 'r',encoding='utf-8')
    listF3name =F3name.readlines()
    OutF3name = io.open(r"D:\Python\NER\Data\Person\first names_3tike_Normal.txt", 'wb')
    for text in listF3name:
        OutF3name.write(persian_text_normalization.useFormalModel(text).encode('utf-8')+"\r\n")
    OutF3name.close()

    Oname = io.open(r"D:\Python\NER\Data\Organization\Clean\Clean_Merge_Organization.txt",'r',encoding='utf-8')
    listOname =Oname.readlines()
    OutOname = io.open(r"D:\Python\NER\Data\Organization\Clean\Clean_Merge_Organization_Normal.txt", 'wb')
    for text in listOname:
        OutOname.write(persian_text_normalization.useFormalModel(text).encode('utf-8')+"\r\n")
    OutOname.close()

    Pname = io.open(r"D:\Python\NER\Data\Place\Clean_Place_merge.txt", 'r',encoding='utf-8')
    listPname =Pname.readlines()
    OutPname = io.open(r"D:\Python\NER\Data\Place\Clean_Place_merge_Normal.txt", 'wb')
    for text in listPname:
        OutPname.write(persian_text_normalization.useFormalModel(text).encode('utf-8')+"\r\n")
    OutPname.close()
    '''
    print "End!!!"

##########################################################

##########################################################
if __name__ == "__main__":
    main_getfile()
##########################################################
