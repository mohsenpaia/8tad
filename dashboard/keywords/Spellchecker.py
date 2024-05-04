#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
##########################################################
import datetime
import TextTokenization as TT
import io
import os
import re
import json
import PersianTextNormalization as PTN


class SpellChecker:
    """

    """

    def __init__(self):
        """

        """
        # import textacy.datasets
        # cw = textacy.datasets.CapitolWords()
        #
        # records = cw.records(speaker_name={'Hillary Clinton', 'Barack Obama'})
        # text_stream, metadata_stream = textacy.fileio.split_record_fields(records, 'text')
        # corpus = textacy.Corpus('en', texts=text_stream, metadatas=metadata_stream)
        # corpus
        # self.stop_words = PC.AKE_TAG_STOPWORDS
        self.persian_text_normalizer = PTN.PersianTextNormalization()
        self.text_tokenizer = TT.TextTokenization()
        self.dictionary_formal = {}
        self.dictionary_informal = {}
        self.weight_of_errors = {}
        #
        # self.weight_of_errors['insertion'] = 1
        # self.weight_of_errors['deletion'] = 1
        # self.weight_of_errors['transposition'] = 1
        # self.weight_of_errors['substitution'] = 1
        self.weight_of_errors['merge'] = 1
        self.weight_of_errors['split'] = 1
        self.weight_of_errors['halfspace'] = 1
        self.weight_of_errors['halfspace_all'] = 1
        # self.weight_of_errors['insertion'] = 1-0.197
        # self.weight_of_errors['deletion'] = 1-0.152
        # self.weight_of_errors['transposition'] = 1-0.102
        # self.weight_of_errors['substitution'] = 1-0.548
        # self.weight_of_errors['merge'] = 1-0.4
        # self.weight_of_errors['split'] = 1-0.6
        # self.weight_of_errors['halfspace'] = 1-0.9
        # self.weight_of_errors['halfspace_all'] = self.weight_of_errors['halfspace']
        self.weight_of_errors['self'] = 1 - .1

        self.pre_post = {u"POST": [
            u"هایتون", u"هایمان", u"هایشان", u"هایتان", u"هایشون", u"هاییم", u"هایم", u"هایت"
            , u"هایش", u"آگین", u"ترین", u"گانه", u"گانی", u"واری", u"های", u"آسا", u"گین", u"اده"
            , u"انه", u"ایک", u"ینه", u"بار", u"باز", u"بان", u"دان", u"دیس", u"زار", u"سار", u"سان"
            , u"سرا", u"سیر", u"کار", u"کده", u"گار", u"گاه", u"گرد", u"گون", u"لاخ", u"مان", u"مند"
            , u"ناک", u"نده", u"وار", u"ها", u"ان"
            , u"ات", u"ون", u"ور", u"ار", u"اک", u"ال", u"ین", u"بد", u"تر", u"گر", u"ند", u"ور"]
            , u"PRE": [u"اندر", u"پارا", u"پیرا", u"نمی", u"ابر", u"ابی", u"ارد", u"باز", u"بیش",
                       u"پاد", u"پرا", u"پسا", u"پیش", u"ترا", u"ریز", u"فرا", u"فرو", u"می",
                       u"اف", u"با", u"بر", u"بس", u"بی", u"پت", u"پس", u"پی", u"پر", u"تک",
                       u"در", u"دژ", u"دش", u"سر", u"اش", u"اس", u"فر", u"نا", u"وا", u"ور",
                       u"هن", u"ان", u"هم", u"هو", u"خو"]
        }
        self.charachter_weight = {}
        # self.charachter_weight[u'insertion'] = {}
        # self.charachter_weight[u'deletion'] = {}
        # self.charachter_weight[u'transposition'] = {}
        # self.charachter_weight[u'substitution'] = {}
        self.charachter_weight[u'merge'] = {}
        self.charachter_weight[u'split'] = {}
        self.charachter_weight[u'halfspace'] = {}
        self.charachter_weight[u'halfspace_all'] = {}
        # with io.open(os.path.join("Data","Weight","Sub.txt"),"r", encoding='utf-8') as file:
        #     weight = file.readlines()
        #     alph = weight[0].strip().split('\t')
        #     del weight[0]
        #     for index, w in enumerate(weight):
        #         weights = w.strip().split('\t')
        #         for i,we in enumerate(weights):
        #             self.charachter_weight[u'substitution'][(alph[index],alph[i])] = float(we)
        # with io.open(os.path.join("Data","Weight","Ins.txt"), "r", encoding='utf-8') as file:
        #     weight = file.readlines()
        #     alph = weight[0].strip().split('\t')
        #     del weight[0]
        #     for index, we in enumerate(weight[0].strip().split('\t')):
        #         self.charachter_weight[u'insertion'][alph[index]] = float(we)
        # with io.open(os.path.join("Data","Weight","Del.txt"), "r", encoding='utf-8') as file:
        #     weight = file.readlines()
        #     alph = weight[0].strip().split('\t')
        #     del weight[0]
        #     for index, w in enumerate(weight):
        #         weights = w.strip().split('\t')
        #         for i, we in enumerate(weights):
        #             self.charachter_weight[u'deletion'][(alph[index], alph[i])] = float(we)
        # with io.open(os.path.join("Data","Weight","Tran.txt"), "r", encoding='utf-8') as file:
        #     weight = file.readlines()
        #     alph = weight[0].strip().split('\t')
        #     del weight[0]
        #     for index, w in enumerate(weight):
        #         weights = w.strip().split('\t')
        #         for i, we in enumerate(weights):
        #             self.charachter_weight[u'transposition'][(alph[index], alph[i])] = float(we)
        self.PERSIAN_ALPHABET_FULL = list("""اآبپتثجچحخدذرزژسشصضطظعغفقکگلمنوهیئ""".decode("utf-8"))
        # word2vec_path = os.path.join("Model","model.w2v")
        # if os.path.isfile(word2vec_path):
        #     try:
        #         self.W2V = gensim.models.Word2Vec.load(word2vec_path)
        #
        #     except:
        #         print "W2V format is corrupted!"
        # else:
        #     print "W2V model is not Found!"
        Dictionary_formal_path = os.path.join(os.path.dirname(__file__), "Data", "Dictionary", "Dictionary.Formal - Copy.json")
        # Dictionary_formal_path = r"Data\Dictionary\Dictionary.Formal.json"
        Dictionary_informal_path = os.path.join(os.path.dirname(__file__), "Data", "Dictionary", "Dictionary.Informal.json")
        # Dictionary_PMI_path = os.path.join("Data","Dictionary","Dictionary_PMI.json")
        # LM_path = r"Data\LM\LM_LargeNewsCorpus[All].arpa"
        # LM_path = os.path.join("Data","LM","LM_LargeNewsCorpus[All]_P1_2.arpa1111111111111111111")
        # LM_path = r"Data\LM\LM_ALL_digikala_merveV2+_mergeV3-_newsp1_newsp2.arpa"

        # LM_path = r"Data\LM\LM_LargeNewsCorpus[All]_P1.arpa"
        # if os.path.isfile(Dictionary_PMI_path):
        #     try:
        #         self.PMI = json.loads(io.open(Dictionary_PMI_path, 'r',encoding='utf-8').read(), encoding='utf-8')
        #
        #     except:
        #         print "PMI dictionary is not JSON!"
        # else:
        #     print "PMI dictionary is not found!"
        if os.path.isfile(Dictionary_formal_path):
            try:
                self.dictionary_formal = json.loads(io.open(Dictionary_formal_path, 'r', encoding='utf-8').read(),
                                                    encoding='utf-8')

            except:
                print
                "Fromal dictionary is not JSON!"
        else:
            print
            "Fromal dictionary is not found!"
        if os.path.isfile(Dictionary_informal_path):
            try:
                self.dictionary_informal = json.loads(io.open(Dictionary_informal_path, 'r', encoding='utf-8').read(),
                                                      encoding='utf-8')
            except:
                print
                "Infromal dictionary is not JSON!"
        else:
            print
            "Informal dictionary is not found!"

        # if os.path.isfile(LM_path):
        #     try:
        #         self.LM = LM.LM(LM_path)
        #     except:
        #         print "Language model file is not ARPA!"
        # else:
        #     print "Language model is not found!"

        self.clean_dictionary(u"formal")
        self.clean_dictionary(u"informal")
        self.remove_less_than_N_from_dictionary(50, u"formal")
        self.remove_less_than_N_from_dictionary(50, u"informal")
        self.remove_formal_from_informal()

    def remove_less_than_N_from_dictionary(self, minN, informal_formal):
        if informal_formal == u"formal":
            for term in self.dictionary_formal.keys():
                if self.dictionary_formal[term] < minN:
                    del self.dictionary_formal[term]
        else:
            for term in self.dictionary_informal.keys():
                if self.dictionary_informal[term] < minN:
                    del self.dictionary_informal[term]

    def clean_dictionary(self, informal_formal):
        if informal_formal == u'formal':
            for term in self.dictionary_formal.keys():
                if re.findall(r"[a-zA-Z0-9]", term):
                    del self.dictionary_formal[term]
                    continue
                if len(term) == 1 and term != u'و':
                    del self.dictionary_formal[term]
                    continue
        elif informal_formal == u'informal':
            for term in self.dictionary_informal.keys():
                if len(term) == 1 and term != u'و':
                    del self.dictionary_informal[term]
                    continue
                if re.findall(r"[a-zA-Z0-9]", term):
                    del self.dictionary_informal[term]
                    continue
                    # with io.open(r"Data\Dictionary.Formal_V2.json", 'w', encoding='utf-8') as dic:
                    #     dic.write(json.dumps(self.dictionary_formal, encoding='utf-8').decode('utf-8'))

    def merge_words(self, index, word_tokens):
        output = []
        if index < len(word_tokens) - 1:
            candidate = word_tokens[index] + word_tokens[index + 1]
            if candidate in self.dictionary_formal:
                output.append((candidate, 1))
        if index > 0:
            candidate = word_tokens[index - 1] + word_tokens[index]
            if candidate in self.dictionary_formal:
                output.append((candidate, -1))
        return output

    def halfspace_merge_split(self, index, word_tokens):
        output = []
        if index < len(word_tokens) - 1:
            candidate = word_tokens[index] + u"‌" + word_tokens[index + 1]
            if candidate in self.dictionary_formal:
                output.append((candidate, 1))
        if index > 0:
            candidate = word_tokens[index - 1] + u"‌" + word_tokens[index]
            if candidate in self.dictionary_formal:
                output.append((candidate, -1))
        token = word_tokens[index]
        for index_char in range(1, len(token)):
            candidate = token[:index_char] + u"‌" + token[index_char:]
            if candidate in self.dictionary_formal:
                output.append((candidate, 0))
                candidate = token[:index_char] + u" " + token[index_char:]
                output.append((candidate, 0))
        return output

    def split_words(self, index, word_tokens):
        output = []
        if len(word_tokens[index]) < 5:
            return output
        token = word_tokens[index]
        for index_char in range(1, len(token)):
            candidate = token[:index_char] + " " + token[index_char:]
            if token[:index_char] in self.dictionary_formal and token[index_char:] in self.dictionary_formal \
                    and len(token[:index_char]) > 2 and len(token[index_char:]) > 2:
                output.append(candidate)
        return output

    def remove_formal_from_informal(self):
        removed_words = 0
        for word_formal in self.dictionary_formal:
            if word_formal in self.dictionary_informal:
                del self.dictionary_informal[word_formal]
                removed_words += 1
        print
        removed_words

    def prefix_postfix_with_next_previous_words(self, index, word_tokens):
        output = []
        if index < len(word_tokens) - 1 and word_tokens[index + 1] in self.pre_post[u"POST"]:
            candidate = word_tokens[index] + word_tokens[index + 1]
            # if candidate in self.dictionary_formal:
            output.append((candidate, 1))
            candidate = word_tokens[index] + u"‌" + word_tokens[index + 1]
            # if candidate in self.dictionary_formal:
            output.append((candidate, 1))
        if index > 0 and word_tokens[index - 1] in self.pre_post[u"PRE"]:
            candidate = word_tokens[index - 1] + word_tokens[index]
            # if candidate in self.dictionary_formal:
            output.append((candidate, -1))
            candidate = word_tokens[index - 1] + u"‌" + word_tokens[index]
            # if candidate in self.dictionary_formal:
            output.append((candidate, -1))
        return output

    def prefix_postfix(self, index, word_tokens):
        output = []
        for pre in self.pre_post[u"PRE"]:
            if word_tokens[index].startswith(pre) and word_tokens[index][len(pre):] in self.dictionary_formal:
                candidate = pre + u" " + word_tokens[index][len(pre):]
                output.append((candidate, 0))
                break
        for post in self.pre_post[u"POST"]:
            if word_tokens[index].endswith(post) and word_tokens[index][:-len(post)] in self.dictionary_formal:
                candidate = word_tokens[index][:-len(post)] + u" " + post
                output.append((candidate, 0))
                break
        return output

    def insertion(self, index, word_tokens):
        output = []
        token = word_tokens[index]
        token_org = token
        for index_char, char in enumerate(token):
            for alphabet in self.PERSIAN_ALPHABET_FULL:
                candidate = token[:index_char] + alphabet + token[index_char:]
                if candidate in self.dictionary_formal:
                    output.append((candidate, alphabet))
        for alphabet in self.PERSIAN_ALPHABET_FULL:
            candidate = token + alphabet
            if candidate in self.dictionary_formal:
                output.append((candidate, alphabet))
        return output

    def deletion(self, index, word_tokens):
        output = []
        token = word_tokens[index]
        token_org = token
        for index_char, char in enumerate(token):
            token_org = list(token)

            del token_org[index_char]
            candidate = ('').join(token_org)
            if candidate in self.dictionary_formal:
                if index_char == 0:
                    output.append((candidate, token[index_char], token[index_char + 1], ''))
                elif index_char == len(token) - 1:
                    output.append((candidate, token[index_char], token[index_char - 1], ''))
                else:
                    output.append((candidate, token[index_char], token[index_char - 1], token[index_char + 1]))

        return output

    def transposition(self, index, word_tokens):
        output = []
        token = word_tokens[index]
        token_org = token
        for index_char, char in enumerate(token[:-1]):
            token_org = list(token)
            token_org[index_char] = token_org[index_char + 1]
            token_org[index_char + 1] = list(token)[index_char]
            candidate = ('').join(token_org)
            if candidate in self.dictionary_formal:
                output.append((candidate, token[index_char], token[index_char + 1]))
        return output

    def substitution(self, index, word_tokens):
        output = []
        token = word_tokens[index]
        token_org = list(token)
        for index_char, char in enumerate(token):
            for alphabet in self.PERSIAN_ALPHABET_FULL:
                token_org = list(token)
                token_org[index_char] = alphabet
                candidate = ('').join(token_org)
                if candidate in self.dictionary_formal:
                    output.append((candidate, token[index_char], alphabet))
        return output

    # def useModel(self,text):
    #     # text = 'پرسپ ولیس'
    #     if type(text) == str:
    #         text = text.decode('utf-8')
    #     text_normal =  self.persian_text_normalizer.useFormalModel(text)
    #     text_normal =  self.persian_text_normalizer.useInformalModel(text_normal)
    #     # text_normal = re.sub(u"([" + PC.PERSIAN_ALPHABET_FULL + u"])(" + PC.PUNCTUATION + u"+)([" + PC.PERSIAN_ALPHABET_FULL + u"])","\g<1> \g<2> \g<3>".decode("utf-8"), text, flags=re.UNICODE)
    #     text_normal = self.persian_text_normalizer.characterNormalizer(text_normal)
    #     text_tokens = self.text_tokenizer.getTokenList(text_normal)
    #     word_tokens = []
    #     errors = []
    #     # errors2 = []
    #     for i in text_tokens:
    #         word_tokens.append(i[0])
    #     index = 0
    #     output = []
    #     length = len(text_tokens)
    #     index_error = 0
    #     while index < length:
    #
    #         candidates = {}
    #         candidates[u"halfspace"] = []
    #         candidates[u"merge"] = []
    #         candidates[u"split"] = []
    #         candidates[u"spell"] = []
    #         candidates[u"halfspace"] = self.halfspace_merge_split(index, word_tokens)
    #         if len(candidates[u"halfspace"]) == 0:
    #             if word_tokens[index] not in self.dictionary_formal:# and word_tokens[index] not in self.dictionary_informal:
    #                 candidates[u"merge"] = self.merge_words(index, word_tokens)
    #                 if len(candidates[u"merge"]) == 0:
    #                     candidates[u"split"] = self.split_words(index, word_tokens)
    #                     if len(candidates[u"split"]) == 0:
    #                         index += 1 # kandid sahih tolid nakard
    #                     else: # khataye split
    #                         word_tokens[index] = candidates[u"split"][0].split()[0]
    #                         word_tokens.insert(index + 1,candidates[u"split"][0].split()[1])
    #                         index += 2
    #                 else: # khataye merge
    #                     word_tokens[index] = candidates[u"merge"][0][0]
    #                     del word_tokens[index + candidates[u"merge"][0][1]]
    #                     index += 1
    #
    #             else: # loghat dorost
    #                 index += 1
    #         else: #khataye HF
    #             word_tokens[index] = candidates[u"halfspace"][0][0]
    #             if candidates[u"halfspace"][0][1] != 0:
    #                 del word_tokens[index + candidates[u"halfspace"][0][1]]
    #                 index += 1
    #                 if candidates[u"halfspace"][0][1] == -1:
    #                     index -= 1
    #             else:
    #                 index += 1
    #
    #             # for kind_of_error in candidates:
    #             #     for candidate in candidates[kind_of_error]:
    #             #         merge_sen = self.candidate_sentence(candidate,word_tokens[:], index, kind_of_error)
    #         # else:
    #         #     output.append(word_tokens[index])#لغت صحیح
    #         #
    #         # index +=1
    #     # output = (' ').join(output)
    #     # for i,j in enumerate(errors):
    #     #     if j[1][0][2] == u"self":
    #     #         del errors[i]
    #         length = len(word_tokens)
    #     return ' '.join(word_tokens)
    def useModel(self, text):
        # text = 'من این خنک کننده آبی رو بر روی کیس گلادیاتور گرین ( که با هم سازگاری کامل دارند) نصب کردم . کیس گلادیاتور بزرگ است (full tower) بنابراین به هواکشی نیاز دارد تا از پس مکیدن هوای حجیم داخل کیس برآید.باید بگم این خنک کننده بسیار عالی اینکار را انجام میدهد .هنگامی که دست خود را بر روی سقف کیس قرار میدهیم به وضوح باد سرد را که از میان سه هواکش نیرومند خارج میشود ،احساس میکنیم.با آنکه قطعات سخت افزاری بسیار قدرتمندی دارم اما تاکنون باد گرم از کیس خارج نشده و این نشان از قدرت فوق العاده این محصول دارد .نسبت به خنک کننده بادی مزیت فراوان دارد . بیگمان اگر میخواستم پردازنده خود را با خنک کننده بادی سرد کنم نیاز به خنک کننده ای غول پیکر بود که هم جای بسیاری از درون کیس را اشغال میکرد و هم به خاطر وزنش به پردازنده آسیب میزد.اما از کوچکی و سبکی water block (قطعه متصل به پردازنده) شگفت زده خواهید شد.در کیس های حرفه ای این محصول را به جای هرگونه خنک کننده بادی ،   بسیار سفارش میکنم .'
        # text = 'موها موهای موهایش موهایمان ابرمو'
        if type(text) == str:
            text = text.decode('utf-8')
        PUNCTUATION = """[~!@#$%^&*()-_=+{}\|;:'",<.>/?÷٪×،ـ»«؛؟…↓↑→←™®°∞٫،]""".decode("utf-8")
        for punc in PUNCTUATION:
            text = text.replace(punc, u" ")
        list_errors = []
        RESULTS = set(text.strip().split())
        text_normal = self.persian_text_normalizer.useFormalModel(text)
        for t in text_normal.strip().split():
            RESULTS.add(t)
        text_normal = self.persian_text_normalizer.useInformalModel(text_normal)
        for t in text_normal.strip().split():
            RESULTS.add(t)
        text_normal = self.persian_text_normalizer.characterNormalizer(text_normal)
        for t in text_normal.strip().split():
            RESULTS.add(t)
        # text_tokens = self.text_tokenizer.getTokenList(text_normal)
        text_tokens = self.text_tokenizer.getTokenList(text)
        word_tokens = []
        for i in text_tokens:
            word_tokens.append(i[0])
            if i[0][-1] == u'ی' and (i[0][:-1] in self.dictionary_formal or i[0][:-1] in self.dictionary_informal):
                RESULTS.add(i[0][:-1])
            RESULTS.add(i[0])
        index = 0
        length = len(text_tokens)
        while index < length:
            candidates = {}
            candidates[u"halfspace"] = []
            candidates[u"pre_post"] = []
            candidates[u"merge"] = []
            candidates[u"split"] = []
            candidates[u"halfspace"] = self.halfspace_merge_split(index, word_tokens)
            candidates[u"merge"] = self.merge_words(index, word_tokens)
            candidates[u"split"] = self.split_words(index, word_tokens)
            candidates[u"pre_post_next"] = self.prefix_postfix_with_next_previous_words(index, word_tokens)
            candidates[u"pre_post"] = self.prefix_postfix(index, word_tokens)
            if len(candidates[u"pre_post"]) > 0:
                for i in candidates[u"pre_post"]:
                    for w in i[0].split():
                        RESULTS.add(w)
                        list_errors.append(w)
            if len(candidates[u"pre_post_next"]) > 0:
                for i in candidates[u"pre_post_next"]:
                    RESULTS.add(i[0])
                    list_errors.append(i[0])
            if len(candidates[u"halfspace"]) > 0:
                for i in candidates[u"halfspace"]:
                    RESULTS.add(i[0])
                    list_errors.append(i[0])

            if len(candidates[u"split"]) > 0:
                for i in candidates[u"split"]:
                    for w in i.split():
                        RESULTS.add(w)
                        list_errors.append(w)

            if len(candidates[u"merge"]) > 0:
                for i in candidates[u"merge"]:
                    RESULTS.add(i[0])
                    list_errors.append(i[0])

            index += 1
            length = len(word_tokens)
        index = 0
        while index < length:
            candidates = {}
            candidates[u"insert"] = []
            candidates[u"delete"] = []
            candidates[u"sub"] = []
            candidates[u"transposition"] = []
            if word_tokens[index] not in self.dictionary_formal:
                candidates[u"insert"] = self.insertion(index, word_tokens)
                candidates[u"delete"] = self.deletion(index, word_tokens)
                candidates[u"sub"] = self.substitution(index, word_tokens)
                candidates[u"transposition"] = self.transposition(index, word_tokens)
                if len(candidates[u"insert"]) > 0:
                    for i in candidates[u"insert"]:
                        RESULTS.add(i[0])
                        list_errors.append(i[0])

                if len(candidates[u"delete"]) > 0:
                    for i in candidates[u"delete"]:
                        RESULTS.add(i[0])
                        list_errors.append(i[0])

                if len(candidates[u"sub"]) > 0:
                    for i in candidates[u"sub"]:
                        RESULTS.add(i[0])
                        list_errors.append(i[0])

                if len(candidates[u"transposition"]) > 0:
                    for i in candidates[u"transposition"]:
                        RESULTS.add(i[0])
                        list_errors.append(i[0])

            index += 1
            length = len(word_tokens)
        list_errors = list(set(list_errors))
        temp = []
        for i in RESULTS:
            if u"‌" in i:
                temp.append(i.replace(u"‌", u" "))
                temp.append(i.replace(u"‌", u""))
        for i in temp:
            for j in i.split():
                RESULTS.add(j)
        # if len(RESULTS) - len(text.split()) > 20:
        #     dsd = 0

        return ' '.join(RESULTS)


if __name__ == "__main__":

    spellchecker = SpellChecker()
    result = spellchecker.useModel("حسابی")
    print result

    # output = io.open(r"log.txt", 'w', encoding='utf-8')
    # start_time = datetime.datetime.now()
    # counter = 1
    # with io.open(r"test1", 'r', encoding='utf-8') as testset:
    #     for line in testset:
    #         print
    #         counter
    #         counter += 1
    #         result = spellchecker.useModel(line.strip())
    #         output.write(u'{}\n{}\n-------------------------------------\n'.format(line.strip(), result.strip()))
    # output.close()
    # # text = 'پرسپ ولیسی ها به مدرسهرفتند دکتر'
    # # result = spellchecker.useModel(text)
    # end_time = datetime.datetime.now()
    # cost_time = (end_time - start_time)
    #
    # # print result
    # print
    # cost_time
    # pass


    # spellchecker = SpellChecker()
    # ss = PTN.PersianTextNormalization()
    # testset = io.open(r"Data\temp_testset_space.txt", 'r', encoding='utf-8').readlines()
    # output = io.open(r"Data\temp_testset_space_out.txt.txt", 'w', encoding='utf-8')
    # for line in testset:
    #     output.write(line.strip().split('\t')[0] + u"\t" + ss.useFormalModel(line.strip().split('\t')[1]) + spellchecker.su + "\n")
    # output.close()
    # ------------------------------
    # ss = PTN.PersianTextNormalization()
    # testset = io.open(r"Data\testset_C_E_cw_ew_type_999.txt", 'r', encoding='utf-8').readlines()
    # output = io.open(r"Data\testset_C_E_cw_ew_type_999_normal.txt", 'w', encoding='utf-8')
    # for line in testset:
    #     output.write(ss.useFormalModel(line.strip().split('\t')[0]) + u"\t" + ss.useFormalModel(line.strip().split('\t')[1]) + u'\t' + line.strip().split('\t')[2] + u"\t" +line.strip().split('\t')[3] + u"\t" +line.strip().split('\t')[4] + u"\n")
    # output.close()
    # spellchecker = SpellChecker()
    #
    # # Digikala_testset(spellchecker)
    # # corpus1 = io.open(r"D:\Python\NER\Data\Corpus\Clean\Out_LargeNewsCorpus[Ali].txt_Normal_P11.txt", 'r', encoding='utf-8')
    #
    # # spellchecker.create_PMI_model(corpus1)
    # # corpus = io.open(r"Data\test.txt", 'r', encoding='utf-8')D:\Python\NER\Data\Corpus\Clean
    # # corpus1 = io.open(r"D:\Python\NER\Data\Corpus\Clean\LargeNewsCorpus[Ali].txt", 'r', encoding='utf-8')
    # # corpus = io.open(r"Data\Informal_digi_comment.txt", 'r', encoding='utf-8')
    # # spellchecker.create_dictionary_Informal(corpus)
    # # spellchecker.create_dictionary_formal(corpus1)
    # # corpus = io.open(r"D:\Python\SpellChecker\Data\Dictionary\words_to_update_Dic.txt", 'r', encoding='utf-8')
    # # spellchecker.update_dictionary_formal(corpus)
    # # print "exit"
    # # exit()
    #
    #
    # # spellchecker.remove_less_than_N_from_dictionary(5,u"informal")
    # # spellchecker.clean_dictionary(u"formal")
    # # spellchecker.clean_dictionary(u"informal")
    # # testset = io.open(r"D:\Python\Word embedding\Data\Formal\Corpus\tabnak_comment_clean.txt", 'r', encoding='utf-8')
    # # testset = io.open(r"D:\Python\NER\Data\Corpus\Clean\Out_LargeNewsCorpus[Ali].txt_Normal_P21.txt", 'r', encoding='utf-8')
    # testset = io.open(os.path.join(r"Data",r"testset_C_E_cw_ew_type_851_clean_nomal_final.txt"), 'r', encoding='utf-8').readlines()
    # output = io.open(os.path.join(r"Data","testset_C_E_cw_ew_type_851_clean_nomal_final_out.txt"), 'w', encoding='utf-8')
    # output_log = io.open(os.path.join(r"Data","testset_C_E_cw_ew_type_851_clean_nomal_final_log_out.txt"), 'w', encoding='utf-8')
    # all = 975
    # senNumber = 1
    # c = 0
    # Ranks = 0
    # errors = []
    # Dic_detect_and_correct_nbest = {}
    # Dic_detect_and_correct_1best = {}
    # Dic_detect = {}
    # Dic_not_detect = {}
    # Dic_detect_wrongly = {}
    # Dic_detect_and_notcorrect = {}
    # detect_and_correct_nbest = 0
    # detect_and_correct_1best = 0
    # detect = 0
    # not_detect = 0
    # detect_wrongly = 0
    # detect_and_notcorrect = 0
    # best1 = []
    # errors_in_dic = []
    # correct_not_in_dic = []
    # all_edit = 0
    # import time
    #
    # start_time = time.time()
    #
    # for line in testset:
    #     line_spl = line.strip().split('\t')
    #     line_spl[0] = line_spl[0].strip()
    #     line_spl[1] = line_spl[1].strip()
    #     line_spl[2] = line_spl[2].strip()
    #     line_spl[3] = line_spl[3].strip()
    #     line_spl[4] = line_spl[4].strip()
    #     all_edit += 1
    #     linecounter+=1
    #     print linecounter
    #     temp1 = line_spl[2].split()
    #     if len(temp1) == 2:
    #         if temp1[1] not in spellchecker.dictionary_formal or temp1[0] not in spellchecker.dictionary_formal :
    #             correct_not_in_dic.append(line_spl[2])
    #             continue
    #     else:
    #         if line_spl[2] not in spellchecker.dictionary_formal:
    #             correct_not_in_dic.append(line_spl[2])
    #             continue
    #     if line_spl[3] in spellchecker.dictionary_formal:
    #         errors_in_dic.append(line_spl[3])
    #         continue
    #     output_log.write(str(linecounter).decode() + '\t' + line_spl[3] + '\t-\t' + line_spl[2] + '\t' + line_spl[1] + '\n')
    #
    #     result,errors = spellchecker.useModel(line_spl[1])
    #     for candidate,suggestions in errors:
    #         if candidate in suggestions:
    #             continue
    #         correct_rank = 0
    #         for k in enumerate(suggestions):
    #             if k[1][0] == line_spl[2]:
    #                 correct_rank = k[0]+1
    #                 Ranks += 1 / correct_rank
    #                 break
    #         TEMP = u'0'
    #         if candidate == line_spl[3]:
    #             TEMP = u'1'
    #         output_log.write( str(linecounter).decode() + '\t' + candidate + '\t' +TEMP + '\t' + str(correct_rank).decode() + '\t')
    #
    #         for can,score,kind in suggestions:
    #             output_log.write(can + " " + str(score).decode() + '\t')
    #         output_log.write(u'\n')
    #     senNumber += 1
    #     flag_detect = True
    #     for i,j in errors:
    #         flag = True
    #         if i == line_spl[3]:
    #             flag_detect = False
    #             if i not in Dic_detect:
    #                 Dic_detect[i] = 1
    #             else:
    #                 Dic_detect[i] += 1
    #             detect += 1
    #             if j != [] and j[0][0] == line_spl[2]:
    #                 if j[0][0] not in Dic_detect_and_correct_1best:
    #                     Dic_detect_and_correct_1best[line_spl[2]] = 1
    #                 else:
    #                     Dic_detect_and_correct_1best[line_spl[2]] += 1
    #                 detect_and_correct_1best += 1
    #                 best1.append(senNumber)
    #
    #             for k in j:
    #                 if k[0] == line_spl[2]:
    #                     if k[0] not in Dic_detect_and_correct_nbest:
    #                         Dic_detect_and_correct_nbest[line_spl[2]] = 1
    #                     else:
    #                         Dic_detect_and_correct_nbest[line_spl[2]] += 1
    #                     detect_and_correct_nbest += 1
    #                     flag = False
    #                     break
    #             if flag:
    #                 if line_spl[3] not in Dic_detect_and_notcorrect:
    #                     Dic_detect_and_notcorrect[line_spl[3]] = 1
    #                 else:
    #                     Dic_detect_and_notcorrect[line_spl[3]] += 1
    #                 detect_and_notcorrect += 1
    #         else:
    #             if i not in Dic_detect_wrongly:
    #                 Dic_detect_wrongly[i] = 1
    #             else:
    #                 Dic_detect_wrongly[i] += 1
    #             detect_wrongly += 1
    #     if flag_detect:
    #         if line_spl[3] not in Dic_not_detect:
    #             Dic_not_detect[line_spl[3]] = 1
    #         else:
    #             Dic_not_detect[line_spl[3]] += 1
    #             not_detect += 1
    #     output.write(line_spl[0].strip() + "\t" + result.strip() + "\n")
    #     if line_spl[0].strip() == result.strip():
    #         c+=1
    # output.close()
    # print u"-------------------------------"
    # print u"weights : "
    # print u"insertion = " + str(spellchecker.weight_of_errors['insertion']).decode()
    # print u"deletion = " + str(spellchecker.weight_of_errors['deletion']).decode()
    # print u"transposition = " + str(spellchecker.weight_of_errors['transposition']).decode()
    # print u"substitution = " + str(spellchecker.weight_of_errors['substitution']).decode()
    # print u"merge = " + str(spellchecker.weight_of_errors['merge']).decode()
    # print u"split = " + str(spellchecker.weight_of_errors['split']).decode()
    # print u"halfspace = " + str(spellchecker.weight_of_errors['halfspace']).decode()
    # print u"all_edit = " + str(all_edit)
    # print u"detect = " + str(detect)
    # print u"detect_wrongly = " + str(detect_wrongly)
    # print u"detect_and_correct_nbest = " + str(detect_and_correct_nbest)
    # print u"detect_and_correct_1best = " + str(detect_and_correct_1best)
    # print u"detect_and_notcorrect = " + str(detect_and_notcorrect)
    # print "detection_P = " + str(float(detect)/float(detect + detect_wrongly))
    # print "detection_R = " + str(float(detect)/float(all_edit))
    # print "correction_P = " + str(float(detect_and_correct_1best) / float(detect))
    # print "correction_R = " + str(float(detect_and_correct_1best) / float(all_edit))
    # print "correction_nbest_P = " + str(float(detect_and_correct_nbest) / float(detect))
    # print "correction_nbest_R = " + str(float(detect_and_correct_nbest) / float(all_edit))
    # print "MRR = " + str(float(Ranks) / float(all_edit))
    #
    # # print u"سبک و کوچکاتصال بی سیم و با سیمکیفیت صدای مناسببرند معتبر و قابل اعتمادهمه"
    # # print spellchecker.useModel(u"سبک و کوچکاتصال بی سیم و با سیمکیفیت صدای مناسببرند معتبر و قابل اعتمادهمه")
    # # print u"من خیلی شمشیرب ازی را دوست دارم"
    # #
    # # print spellchecker.useModel(u"من خیلی شمشیرب ازی را دوست دارم")
    #
    # res.close()
    # print("--- %s seconds ---" % (time.time() - start_time))
    # print "end!!!"
    ###########################
