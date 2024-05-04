#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
##########################################################


##########################################################
# Text Tokenization
# Mohammad Mahdavi
# moh.mahdavi.l@gmail.com
# July 2016
# Homaplus Corporation
# homaplus.com
# All Rights Reserved
# Do not Change, Alter, or Remove this Licence
##########################################################


##########################################################
import re
import nltk
import ParameterConfiguration as PC
##########################################################


##########################################################
class TextTokenization:
    """
    This class implements an text tokenization system.
    """

    def __init__(self):
        """
        This constructor loads models.
        """
        self.punctuation_dictionary = {x: 0 for x in PC.PUNCTUATION}

    def getTokenList(self, text):
        """
        This method tokenizes normalized text.
        """
        token_list = []
        paragraph_list = [x for x in text.split("\n") if x != ""]
        for i, paragraph in enumerate(paragraph_list):
            paragraph_token_list = [x for x in paragraph.split(" ") if x != ""]
            for token in paragraph_token_list:
                character_list = list(token)
                punctuation_free_flag = True
                for character in character_list:
                    if character not in self.punctuation_dictionary:
                        punctuation_free_flag = False
                        break
                if punctuation_free_flag:
                    token_list.append([token, "PUNCTUATION_FREE"])
                    continue
                token_list_before = []
                j = 0
                while character_list[j] in self.punctuation_dictionary:
                    token_list_before.append([character_list[j], "PUNCTUATION_BEFORE"])
                    j += 1
                token_list_after = []
                k = len(character_list) - 1
                while character_list[k] in self.punctuation_dictionary:
                    token_list_after.append([character_list[k], "PUNCTUATION_AFTER"])
                    k -= 1
                token_list_after.reverse()
                token = "".join(character_list)[j: k + 1]
                tag_found_flag = False
                token_list_middle = []
                if not tag_found_flag and re.findall("^[{}]+$".decode("utf-8").format(PC.PERSIAN_ALPHABET_FULL), token, flags=re.UNICODE):
                    token_list_middle.append([token, "PERSIAN"])
                    tag_found_flag = True
                if not tag_found_flag and re.findall("^[\d]+$", token, flags=re.UNICODE):
                    token_list_middle.append([token, "NUMBER_INTEGER"])
                    tag_found_flag = True
                if not tag_found_flag and re.findall("^([\d]+([.،,٫][\d]+)+)$".decode("utf-8"), token, flags=re.UNICODE):
                    token_list_middle.append([token, "NUMBER_DOUBLE"])
                    tag_found_flag = True
                if not tag_found_flag and re.findall("^[\d]{1,2}[/][\d]{1,2}[/][\d]{2,4}$|^[\d]{2,4}[/][\d]{1,2}[/][\d]{1,2}$", token, flags=re.UNICODE):
                    token_list_middle.append([token, "DATE"])
                    tag_found_flag = True
                if not tag_found_flag and re.findall("^[\d]{1,2}[:][\d]{1,2}$|^[\d]{1,2}[:][\d]{1,2}[:][\d]{1,2}$", token, flags=re.UNICODE):
                    token_list_middle.append([token, "TIME"])
                    tag_found_flag = True
                if not tag_found_flag and re.findall("^[\w.\-]+[@][\w_.\-]+$", token, flags=re.IGNORECASE):
                    token_list_middle.append([token, "EMAIL"])
                    tag_found_flag = True
                if not tag_found_flag and re.findall("^(http[s]?://|www\.)[\w.~:/?#@!$&'()*+,;=\-[\]]+$|^[\w.~:/?#@!$&'()*+,;=\-[\]]+(\.com|\.org|\.ir|\.net)$", token, flags=re.IGNORECASE):
                    token_list_middle.append([token, "URL"])
                    tag_found_flag = True
                if not tag_found_flag and re.findall("^[\d]*[a-zA-Z][\w./\-']*$", token, flags=re.IGNORECASE):
                    token_list_middle.append([token, "ENGLISH"])
                    tag_found_flag = True
                if not tag_found_flag:
                    temp_list = re.findall("^(([{0}]+)|([\d]+))([+/~×*_\-])(([{0}]+)|([\d]+))$".decode("utf-8").format(
                        PC.PERSIAN_ALPHABET_FULL), token, flags=re.UNICODE)
                    if temp_list:
                        if temp_list[0][1]:
                            token_list_middle.append([temp_list[0][1], "PERSIAN"])
                        else:
                            token_list_middle.append([temp_list[0][2], "NUMBER_INTEGER"])
                        token_list_middle.append([temp_list[0][3], "PUNCTUATION_MIDDLE"])
                        if temp_list[0][5]:
                            token_list_middle.append([temp_list[0][5], "PERSIAN"])
                        else:
                            token_list_middle.append([temp_list[0][6], "NUMBER_INTEGER"])
                        tag_found_flag = True
                if not tag_found_flag:
                    token_list_middle.append([token, "UNKNOWN"])
                    tag_found_flag = True
                token_list += token_list_before + token_list_middle + token_list_after
            if (i + 1) < len(paragraph_list):
                token_list.append(["\n", "NEWLINE"])
        return token_list

    def getTermList(self, text, n, t):
        """
        This method calculates term list.
        """
        term_list = []
        token_list = self.getTokenList(text)
        phrase_unigram_list_list = []
        temp_list = []
        for token, tag in token_list:
            if tag not in t:
                if temp_list:
                    phrase_unigram_list_list.append(temp_list)
                    temp_list = []
                if tag == "UNKNOWN" and "PERSIAN" in t:
                    unigram_list = re.findall("[{}]+".decode("utf-8").format(PC.PERSIAN_ALPHABET_FULL), token, flags=re.UNICODE)
                    if unigram_list:
                        phrase_unigram_list_list.append(unigram_list)
            else:
                temp_list.append(token)
        if temp_list:
            phrase_unigram_list_list.append(temp_list)
            temp_list = []
        for phrase_unigram_list in phrase_unigram_list_list:
            for i in range(1, n + 1):
                term_list += [" ".join(x) for x in nltk.ngrams(phrase_unigram_list, i)]
        return term_list

    def getSentenceList(self, text):
        """
        This method calculates sentence list.
        """
        token_list = self.getTokenList(text)
        sentence_list = []
        temp_sentence = ""
        use_space_flag = False
        j = 0
        for i, (token, tag) in enumerate(token_list):
            if i < j:
                continue
            if token in ["\n", ".", "!", "?", "؟".decode("utf-8"), "؛".decode("utf-8")]:
                if token != "\n":
                    while i < len(token_list) and token_list[i][1] == "PUNCTUATION_AFTER":
                        temp_sentence += token_list[i][0]
                        i += 1
                    j = i
                if temp_sentence:
                    sentence_list.append(temp_sentence.strip(" "))
                    temp_sentence = ""
            else:
                if not use_space_flag or tag in ["PUNCTUATION_AFTER", "PUNCTUATION_MIDDLE"]:
                    temp_sentence += token
                else:
                    temp_sentence += " " + token
                use_space_flag = True
                if tag in ["PUNCTUATION_BEFORE", "PUNCTUATION_MIDDLE"]:
                    use_space_flag = False
        if temp_sentence:
            sentence_list.append(temp_sentence.strip(" "))
            temp_sentence = ""
        return sentence_list
##########################################################


##########################################################
def main():
    text_tokenization = TextTokenization()
    # text = """سلام! #دنیا!""".decode("utf-8")
    # text_tokenization.getTokenList(text)
    # text_tokenization.getTermList(text, n=2, t=["PERSIAN"])
    # text_tokenization.getSentenceList(text)
##########################################################


##########################################################
if __name__ == "__main__":
    main()
##########################################################
