#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import datetime
import json
import sys
import os
import traceback
from flask import request, Response
from flask.views import MethodView
from slugify import slugify_unicode
import time
from urlparse import urlparse
import re
import ParameterConfiguration as PC
from bs4 import BeautifulSoup
import urllib2
import unicodedata
from models import *
from . import api
import requests
import codecs
import traceback


def characterNormalizer(text):
    if type(text) == str:
        text = text.decode('utf-8')
    """
    This method is a character normalizer for Persian.
    """
    # Remove Useless Characters
    text = re.sub("[ًٌٍَُِّْٰٖٓٔـۖۚٴ]+".decode("utf-8"), "", text, flags=re.UNICODE)
    text = re.sub(u"[\u200b\u200d\u202b\u202c\u202e\u202d\ufeff\ufe0f]+", "", text, flags=re.UNICODE)
    # Unify Different Half Distance, Space, and New Line Characters
    text = re.sub(
        u"[\u200c\u00ac\u200f\u200e\u202a\u009d\u2029\u0086\u0097\u0090\u0093\u0098\u009e\u206f\u206d]+|(&zwnj;)+",
        "\xE2\x80\x8C".decode("utf-8"), text, flags=re.UNICODE)
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
    text = re.sub("([^{}])\xE2\x80\x8C".decode("utf-8").format(PC.PERSIAN_ALPHABET_JOINABLE), "\g<1>", text,
                  flags=re.UNICODE)
    text = re.sub("\xE2\x80\x8C([^{}])".decode("utf-8").format(PC.PERSIAN_ALPHABET_FULL), "\g<1>", text,
                  flags=re.UNICODE)
    # Remove Yeh Character
    text = re.sub("ه[ \xE2\x80\x8C]ی([^{}]|$)".decode("utf-8").format(PC.PERSIAN_ALPHABET_FULL),
                  "ه\g<1>".decode("utf-8"), text, flags=re.UNICODE)
    # Replace . with Half Distance in Persian Abbreviations
    text = re.sub("(^|[^{0}])([{0}]{{1,2}})([.])([{0}]{{1,2}})([.])([{0}]{{1,2}})([.])([{0}]{{1,2}})([^{0}]|$)".decode(
        "utf-8").format(PC.PERSIAN_ALPHABET_FULL),
                  "\g<1>\g<2>\xE2\x80\x8C\g<4>\xE2\x80\x8C\g<6>\xE2\x80\x8C\g<8>\g<9>".decode("utf-8"), text,
                  flags=re.UNICODE)
    text = re.sub("(^|[^{0}])([{0}]{{1,2}})([.])([{0}]{{1,2}})([.])([{0}]{{1,2}})([^{0}]|$)".decode("utf-8").format(
        PC.PERSIAN_ALPHABET_FULL), "\g<1>\g<2>\xE2\x80\x8C\g<4>\xE2\x80\x8C\g<6>\g<7>".decode("utf-8"), text,
        flags=re.UNICODE)
    text = re.sub(
        "(^|[^{0}])([{0}]{{1,2}})([.])([{0}]{{1,2}})([^{0}]|$)".decode("utf-8").format(PC.PERSIAN_ALPHABET_FULL),
        "\g<1>\g<2>\xE2\x80\x8C\g<4>\g<5>".decode("utf-8"), text, flags=re.UNICODE)
    # Remove In Parentheses Spaces
    text = re.sub("([(«<{{[]) ([{}])".decode("utf-8").format(PC.PERSIAN_ALPHABET_FULL), "\g<1>\g<2>", text,
                  flags=re.UNICODE)
    text = re.sub("([{}]) ([)»>}}\]])".decode("utf-8").format(PC.PERSIAN_ALPHABET_FULL), "\g<1>\g<2>", text,
                  flags=re.UNICODE)
    # Set Space Before Persian and English, Number or Some Punctuations Characters
    text = re.sub("([{}])([a-zA-Z\d(«<{{[])".decode("utf-8").format(PC.PERSIAN_ALPHABET_FULL), "\g<1> \g<2>", text,
                  flags=re.UNICODE)
    text = re.sub("([a-zA-Z\d)»>}}\].،:؛!؟…])([{}])".decode("utf-8").format(PC.PERSIAN_ALPHABET_FULL), "\g<1> \g<2>",
                  text, flags=re.UNICODE)
    # Remove Space Between Persian and Some Punctuations Characters
    text = re.sub("([{}]) ([.،:؛!؟…])".decode("utf-8").format(PC.PERSIAN_ALPHABET_FULL), "\g<1>\g<2>".decode("utf-8"),
                  text, flags=re.UNICODE)
    # Remove Repetitive Characters
    text = re.sub("([{}])\\1{{2,}}".decode("utf-8").format(PC.PERSIAN_ALPHABET_FULL), "\g<1>\g<1>", text,
                  flags=re.UNICODE)

    for punc in list(PC.PUNCTUATION):
        text = text.replace(punc, ' ' + punc + ' ')
    text = re.sub(r"( )( )+|(\t+)".decode('utf-8'), ' ', text, flags=re.UNICODE)
    return ' ' + text + ' '


def url_to_clean_text(html):
    try:
        # soup = BeautifulSoup(html.strip(), 'html.parser')
        # body = soup.find_all('body')[0]
        # body = HTML_ExtractContent(str(body))
        # clean_body = characterNormalizer(body)
        soup = BeautifulSoup(html.strip(), 'html.parser')
        s = soup.prettify()
        body = HTML_ExtractContent(s)
        clean_body = characterNormalizer(body)
    except:
        return 'test'

    return ' ' + clean_body + ' '


def HTML_ExtractContent(HTML):
    if type(HTML) == unicode:
        HTML = HTML.encode('utf-8')
    HTML = HTML.replace('\r\n', ' ')
    HTML = HTML.replace('\n', ' ')
    HTML = HTML.replace('\r', ' ')
    HTML = HTML.replace('\t', ' ')
    # HTML = re.sub(
    #     r"(<!--.*?-->)|(<ul.*?</ul>)|(<head[^e].*?</head>)|(<a[^r].*?</a>)|(<li.*?</li>)|(<h\d.*?</h\d>)|(<footer.*?</footer>)|(<script.*?</script>)|(<header.*?</header>)".decode(
    #         'utf-8'), ' ', HTML, flags=re.UNICODE)
    HTML = re.sub(
        r"(<!--.*?-->)".decode(
            'utf-8'), ' ', HTML, flags=re.UNICODE)
    HTML = re.sub(
        r"(<ul.*?</ul>)".decode(
            'utf-8'), ' ', HTML, flags=re.UNICODE)
    HTML = re.sub(
        r"(<head[^e].*?</head>)".decode(
            'utf-8'), ' ', HTML, flags=re.UNICODE)
    HTML = re.sub(
        r"(<a[^r].*?</a>)".decode(
            'utf-8'), ' ', HTML, flags=re.UNICODE)
    HTML = re.sub(
        r"(<li.*?</li>)".decode(
            'utf-8'), ' ', HTML, flags=re.UNICODE)
    HTML = re.sub(
        r"(<h\d.*?</h\d>)".decode(
            'utf-8'), ' ', HTML, flags=re.UNICODE)
    # HTML = re.sub(
    #     r"(<footer.*?</footer>)".decode(
    #         'utf-8'), ' ', HTML, flags=re.UNICODE)
    HTML = re.sub(
        r"(<script.*?</script>)".decode(
            'utf-8'), ' ', HTML, flags=re.UNICODE)
    HTML = re.sub(
        r"(<footer.*?</footer>)".decode(
            'utf-8'), ' ', HTML, flags=re.UNICODE)
    HTML = re.sub(
        r"(<header.*?</header>)".decode(
            'utf-8'), ' ', HTML, flags=re.UNICODE)

    # HTML = re.sub(
    #     r"(<!--.*?-->)|(<ul.*?</ul>)|(<head[^e].*?</head>)|(<a[^r].*?</a>)|(<li.*?</li>)|(<h\d.*?</h\d>)|(<footer.*?</footer>)|(<script.*?</script>)|(<header.*?</header>)".decode(
    #         'utf-8'), ' ', HTML, flags=re.UNICODE)
    HTML = re.sub(r"([a-zA-Z0-9])".decode('utf-8'), ' ', HTML, flags=re.UNICODE)
    HTML = re.sub(r"( )( )+|(\t+)".decode('utf-8'), ' ', HTML, flags=re.UNICODE)
    # HTML = HTML.replace('،', ' ').replace('%', ' ').replace('}', ' ').replace('|', ' ').replace('{', ' ')\
    #     .replace('[', ' ').replace(']', ' ').replace('>', ' ').replace('<', ' ').replace('"', ' ').replace('_', ' ')\
    #     .replace('/', ' ').replace(':', ' ').replace(';', ' ').replace('=', ' ').replace('=', ' ').replace('-',' ')
    # HTML = re.sub(r"( )( )+|(\t+)".decode('utf-8'), ' ', HTML, flags=re.UNICODE)
    HTML = HTML.replace('÷', ' ').replace('٪', ' ').replace('×', ' ').replace('،', ' ').replace('ـ', ' ')
    HTML = HTML.replace('»', ' ').replace('«', ' ').replace('؛', ' ').replace('٫', ' ').replace('∞', ' ')
    HTML = HTML.replace('°', ' ').replace('®', ' ').replace('™', ' ').replace('←', ' ')
    HTML = HTML.replace('↑', ' ').replace('↓', ' ').replace('…', ' ').replace('؟', ' ')

    PUNCTUATION = """[~!@#$%^&*()-_=+{}\|;:'",<.>/?]"""
    for punc in PUNCTUATION:
        HTML = HTML.replace(punc, ' ')
        # print HTML
    # for punc in list(PC.PUNCTUATION):
    #
    #     HTML.replace(punc.encode('utf-8'), ' ' + punc.encode('utf-8') + ' ')
    # HTML = re.sub('('+ PC.PUNCTUATION + ')', " \g<0> ", HTML, flags=re.UNICODE)
    HTML = re.sub(r"( )( )+|(\t+)".decode('utf-8'), ' ', HTML, flags=re.UNICODE)
    return HTML


@api.route('/normalizer/string', methods=['POST'])
def string_normalizer_api():
    response = {}
    try:

        # file = codecs.open(os.path.join(r"/home","ubuntu","campaigns.txt"), "a", "utf-8")

        if request.args.get('local') is None:
           data = request.json
        else:
           data = json.loads(request.data)

        normalized_text = characterNormalizer(data.get('text', None))

        # file.write(u"normalized_text" + '\n')
        # file.write(normalized_text + '\n')


        data = {
            'query': normalized_text
        }

        result = requests.post("http://127.0.0.1/api/spell/checker", data=json.dumps(data)).content
        result = json.loads(result)
        spell_checker_result = result['body']

        data = {
            'query': spell_checker_result
        }

        # file.write(u"spellchecker" + '\n')
        # file.write(spell_checker_result + '\n')

        result = requests.post("http://127.0.0.1/api/query/expansion", data=json.dumps(data)).content
        result = json.loads(result)
        query_expansion = result['body']

        # file.write(u"queryexpansion" + '\n')
        # file.write(result.decode("utf-8") + '\n')

        text = normalized_text.encode('utf-8').strip() + " " + spell_checker_result.encode(
            'utf-8').strip() + " " + query_expansion.encode('utf-8').strip()
        # text = (' ').join(list(set(text.split())))

        # file.write(u"text" + '\n')
        # file.write(text.decode("utf-8") + '\n')

        # file.close()
        response = {"status": "yes", "body": characterNormalizer(text)}

    except Exception:
        print
        traceback.format_exc(sys.exc_info())
        response = {"status": "no"}
    finally:
        return Response(json.dumps(response, sort_keys=False),
                        mimetype='application/json')


@api.route('/normalizer/url', methods=['POST'])
def url_normalizer_api():
    response = {}
    try:
        # data = request.json
        data = json.loads(request.data)
        # print data.get('url', None)
        clean_url = url_to_clean_text(data.get('url', None))
        response = {"status": "yes", "body": clean_url}
    except Exception:
        response = {"status": "no"}
    finally:
        return Response(json.dumps(response, sort_keys=False),
                        mimetype='application/json')
