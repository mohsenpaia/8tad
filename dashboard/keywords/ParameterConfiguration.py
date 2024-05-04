#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
##########################################################


##########################################################
# Parameter Configuration
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
##########################################################


##########################################################
# Folders Paths Parameters
MODEL_FOLDER = os.path.join(os.path.dirname(__file__), "Model")
FORMAL_HTML_DATA_FOLDER = os.path.join(os.path.dirname(__file__), "Data", "Formal", "HTML")
FORMAL_CORPUS_DATA_FOLDER = os.path.join(os.path.dirname(__file__), "Data", "Formal", "Corpus")
FORMAL_PROCESSED_DATA_FOLDER = os.path.join(os.path.dirname(__file__), "Data", "Formal", "Processed")
INFORMAL_CORPUS_DATA_FOLDER = os.path.join(os.path.dirname(__file__), "Data", "Informal", "Corpus")

# Web Services Parameters
GET_NEWS_TAGS_WEB_SERVICE_URL = "http://127.0.0.1:8080/api/v1/news/getNewsTags/"
GET_NEWS_STORY_WEB_SERVICE_URL = "http://127.0.0.1:8080/api/v1/news/getNewsStoryByDate/"
SET_GRAPH_PROCESSING_RESULT_WEB_SERVICE_URL = "http://127.0.0.1:8086/setGraphProcessingResults/"
GET_NEWS_BY_FILTERS_WEB_SERVICE_URL = "http://192.168.1.53:5008/getNewsByFilters/"
WEB_SERVICE_AUTHENTICATION = ("homaplus", "hom4+S3cr3t::")

# Alphabets Parameters
PUNCTUATION = """[~!@#$%^&*()-_=+{}\|;:'",<.>/?÷٪×،ـ»«؛؟…↓↑→←™®°∞٫]""".decode("utf-8")
PERSIAN_ALPHABET_FULL = """اآبپتثجچحخدذرزژسشصضطظعغفقکگلمنوهیئ\xE2\x80\x8C""".decode("utf-8")
PERSIAN_ALPHABET_JOINABLE = """بپتثجچحخسشصضطظعغفقکگلمنهیئ""".decode("utf-8")

# Term Information Parameters
TI_N_GRAM = 1
TI_FORMAL_STOP_WORD_PARAMETER = 0.9
TI_INFORMAL_STOP_WORD_PARAMETER = 0.85
TI_MIN_INFORMALITY_CONFIDENCE = 0.97

# Persian Text Normalization Parameters
PTN_HAMZEH_REPLACE_LIST = [("هیات".decode("utf-8"), "هیئت".decode("utf-8")),
                           ("مساله".decode("utf-8"), "مسئله".decode("utf-8")),
                           ("مسوول".decode("utf-8"), "مسئول".decode("utf-8")),
                           ("شوون".decode("utf-8"), "شئون".decode("utf-8")),
                           ("جرات".decode("utf-8"), "جرئت".decode("utf-8")),
                           ("مسالت".decode("utf-8"), "مسئلت".decode("utf-8"))]
PTN_HAMZEH_BLACK_LIST = \
"""ریال
رئال
اوین
اوئن
کوین
کوئن
لیون
لئون
شیون
شئون
ریالی
رئالی
کویری
کوئری
مایو
مائو
برایت
برائت""".decode("utf-8").splitlines()
PTN_N_GRAM = 2
PTN_TERM_MIN_SUPPORT = 5
PTN_TERM_MIN_CONFIDENCE = 0.9

# Automatic Keyphrase Extraction Parameters
AKE_TAG_BLACK_LIST = \
"""همه چیز
جمع خبرنگاران
تحت تاثیر
سلامت نیوز
پایگاه خبری
اقتصاد آنلاین
عضو شورای
جلسه شورای
ورزش سه
پایگاه اطلاع‌رسانی
بدون شک
اتفاق افتاد
نداشته باشند
نزدیک شدن
بیش از حد
شرایط کنونی
دریافت می‌کنند
برچسب ها
تنها راه
دست دادن
قدس آنلاین
دوست دارم
روی زمین
خیلی خوب
پیدا کردن
نمایش داده
پایان یافت
مهم نیست
چند تن
سید محمد
ای کاش
جای خالی
گفتگو با مهر
راه یافت
محمد حسین
محمد رضا
محمد علی
لیگ دسته
خبرگزاری فارس
صفحه نخست
هر چی
همه چی
پشت سر
باشگاه خبرنگاران جوان
web browser
باشگاه خبرنگاران
خبرنگاران جوان
وبگردی باشگاه خبرنگاران جوان
استان‌های باشگاه خبرنگاران
جام‌جم آنلاین
خبرنگار اعزامی
قابل توجه
ارسال به تلگرام
قابل توجهی
سلام علیکم
بسم‌الله الرحمن الرحیم""".decode("utf-8").splitlines()
AKE_N_GRAM = 5
AKE_MIN_TAG_OCCURRENCE = 0
AKE_SAVE_COUNTER = 400

# Text Categorization Parameters
TC_CATEGORY_TRAIN_DOCUMENT_SET_FOLDER = os.path.join(os.path.dirname(__file__), "Data", "Formal", "Text-Categorization-Document-Set", "Category-Train")
TC_CATEGORY_TEST_DOCUMENT_SET_FOLDER = os.path.join(os.path.dirname(__file__), "Data", "Formal", "Text-Categorization-Document-Set", "Category-Test")
TC_SUBCATEGORY_TRAIN_DOCUMENT_SET_FOLDER = os.path.join(os.path.dirname(__file__), "Data", "Formal", "Text-Categorization-Document-Set", "Subcategory-Train")
TC_SUBCATEGORY_TEST_DOCUMENT_SET_FOLDER = os.path.join(os.path.dirname(__file__), "Data", "Formal", "Text-Categorization-Document-Set", "Subcategory-Test")
TC_DEFAULT_CATEGORY = "چندرسانه‌ای".decode("utf-8")
TC_N_GRAM = 2
TC_POWER_PARAMETER_1 = 3
TC_POWER_PARAMETER_2 = 1
TC_FEATURE_VECTOR_SIZE_PARAMETER = 0.6
TC_TERM_MIN_DOCUMENT_FREQUENCY_PARAMETER = 0.25
TC_HIDDEN_NEURON_COUNT = 200
TC_BATCH_SIZE = 128
TC_CATEGORY_EPOCH_COUNT = 3
TC_CATEGORY_LEARNING_RATE = 0.0005
TC_SUBCATEGORY_EPOCH_COUNT = 20
TC_SUBCATEGORY_LEARNING_RATE = 0.001
TC_TITLE_TAG_WEIGHT = 3
TC_MIN_FEATURE_VECTOR_NORM_0 = 20

# Related News Parameters
RN_DOCUMENT_HISTORY_QUEUE_SIZE = 10000
RN_CATEGORY_TAG_WEIGHT = 1.0
RN_N_GRAM = 2
RN_TERM_COUNT_PARAMETER = 0.1
RN_MIN_SIMILARITY = 0.2
RN_MAX_SIMILARITY = 0.8
RN_SAVE_COUNTER = 500

# Trend Detection Parameters
TD_TIME_STEP_COUNT = 10
TD_TIME_WINDOW_SECOND = 86400
TD_MIN_TAG_OCCURRENCE_PARAMETER = 0.5
TD_TRENDING_TAG_COUNT = 40

# News Story Parameters
NS_CURRENT_TIME_WINDOW_SECOND = 86400
NS_RESULT_COUNT_PARAMETER = 0.3
NS_TAG_COUNT_PARAMETER = 0.5

# Web Crawling Parameters
WC_MIN_HTML_FILE_SIZE = 10000
WC_MIN_JSON_FILE_SIZE = 400

# Text Summarization Parameters
TS_N_GRAM = 2
TS_MIN_SELECTION_SCORE = 0.1

# Word Embedding Parameters
WE_LEARNING_METHOD = 1   # CBOW = 0 and Skip-Gram = 1
WE_VECTOR_SIZE = 200
WE_WINDOW_SIZE = 8
WE_NEGATIVE_SAMPLE_COUNT = 10
WE_ITERATION_COUNT = 20
WE_MIN_TERM_OCCURRENCE = 10
WE_RESULT_COUNT = 20

# Language Modeling Parameters
LM_MIN_TERM_DOCUMENT_FREQUENCY_PARAMETER = 0.45
LM_TIME_STEP_COUNT = 3
LM_LEARNING_RATE = 0.005
LM_BATCH_SIZE = 128
LM_HIDDEN_NEURON_COUNT = 128
LM_EPOCH_COUNT = 300

# Query Autocomplete Parameters
QAC_MAX_SUGGESTION_COUNT = 20

# Persian POS Tagging Parameters
PPOS_TAG_LIST = ["N", "V", "ADJ", "ADV", "P", "PRO", "CON", "IF", "INT", "SPEC",
                 "MORP", "PP", "DET", "OH", "QUA", "PS", "NP", "MQUA"]

# Persian Verb Stemming Parameters
PVS_MIN_VERB_LENGTH = 3
PVS_MIN_VERB_OCCURRENCE_PARAMETER = 0.2
PVS_MIN_VERB_DIFFERENT_TYPE_COUNT = 3
PVS_SPECIAL_SHORT_VERB_DICTIONARY = {"شد".decode("utf-8"): 0, "زد".decode("utf-8"): 0, "کن".decode("utf-8"): 0}
PVS_PREFIX_LIST = [("فرانمی".decode("utf-8"), "-1"),
                   ("فرامی".decode("utf-8"), "1"),
                   ("فران".decode("utf-8"), "-1"),
                   ("فرا".decode("utf-8"), "1"),
                   ("بازنمی".decode("utf-8"), "-1"),
                   ("بازمی".decode("utf-8"), "1"),
                   ("بازن".decode("utf-8"), "-1"),
                   ("باز".decode("utf-8"), "1"),
                   ("درنمی".decode("utf-8"), "-1"),
                   ("درمی".decode("utf-8"), "1"),
                   ("درن".decode("utf-8"), "-1"),
                   ("در".decode("utf-8"), "1"),
                   ("برنمی".decode("utf-8"), "-1"),
                   ("برمی".decode("utf-8"), "1"),
                   ("برن".decode("utf-8"), "-1"),
                   ("بر".decode("utf-8"), "1"),
                   ("نمی".decode("utf-8"), "-1"),
                   ("می".decode("utf-8"), "1"),
                   ("ن".decode("utf-8"), "-1")]
PVS_POSTFIX_LIST = [e.decode("utf-8") for e in ["ایم", "اید", "اند", "ام", "ای", "ست", "یم", "ید", "ند", "م", "ی", "د"]]

# Sentiment Analysis Parameters
SA_BANK_SENTIMENT_DATA_FOLDER = os.path.join(os.path.dirname(__file__), "Data", "Informal", "Sentiment", "bank")
SA_DIGIKALA_SENTIMENT_DATA_FOLDER = os.path.join(os.path.dirname(__file__), "Data", "Informal", "Sentiment", "digikala")
SA_MIN_POSITIVE_SCORE = 1.0
SA_MIN_NEGATIVE_SCORE = 1.0

# Run Project Parameters
RP_INPUT_QUEUE = "post_processing_queue"
RP_OUTPUT_QUEUE = "indexer_job_queue"
RP_TIME_BASED_SERVICE_COUNTER = 300
##########################################################
