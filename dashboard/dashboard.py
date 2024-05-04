#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, flash, json, redirect, url_for, g, session, Response, Request
import requests
import os
from uuid import uuid4
import struct
import imghdr
from flask_wtf.csrf import CSRFProtect, CSRFError
import redis
from flask_security import Security, PeeweeUserDatastore, login_required, current_user, user_registered, roles_accepted, \
    AnonymousUser

# from security.models import *
from keywords.tag_extraction import *
from forms import *
from security.views import *

from keywords.query_expansion import *

from keywords.Spellchecker import *

from flask_security.utils import login_user
from flask_security.views import _commit

from suds.client import Client
from elasticsearch import Elasticsearch
from datetime import datetime
import dateutil.relativedelta
import jalali
import calendar
import time
from collections import OrderedDict
from urlparse import urlparse
import sys
import traceback
import persian
import urllib
from flask_mail import Mail
from jinja2 import evalcontextfilter, Markup, escape
import re
from flask_security.passwordless import *
from functools import wraps

mail = Mail()
app = Flask(__name__)

# app.config.update(dict(
#     DEBUG=True,
#     MAIL_SERVER='smtp.gmail.com',
#     MAIL_PORT=587,
#     MAIL_USE_TLS=True,
#     MAIL_USE_SSL=False,
#     MAIL_USERNAME='homaplus.mail@gmail.com',
#     MAIL_PASSWORD='11111111q',
# ))

app.config.update(dict(
    DEBUG=True,
    MAIL_SERVER='localhost',
    MAIL_PORT=25,
    MAIL_USE_TLS=True,
    MAIL_USE_SSL=False
))

mail.init_app(app)

csrf = CSRFProtect(app)
app.secret_key = '$2b$12$xXdE64sYdZPJhaHdn98aveSEYB768VYLVSblsYWF84jHDgEKlbqcm'
BACKEND_SERVER_ADDRESS = "http://127.0.0.1:2222"
REDIS_SERVER_ADDRESS = "127.0.0.1"
ELASTICSEARCH_SERVER_ADDRESS = "127.0.0.1"
# 127.0.0.1

MMERCHANT_ID = 'ed9df6c6-7f67-11e7-a66e-000c295eb8fc'
ZARINPAL_WEBSERVICE = 'https://www.zarinpal.com/pg/services/WebGate/wsdl'

SITE_VERIFY_URL = 'https://www.google.com/recaptcha/api/siteverify'
SITE_SECRET = '6LcaHCoUAAAAAMTk5621Skw7GNAvm38PbJXkPwor'    #8tad.ir
# SITE_SECRET = '6LeyUjYUAAAAAEqvt0y7VSR-E18po_zZVXIuTuDF'    #adcore.ir
#SITE_SECRET = '6Le0ClkUAAAAAPzDULZKhS7l6oXPF8IW1HP_U-th'  # ad.ir
RECAPTCHA_RESPONSE_PARAM = 'g-recaptcha-response'

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
APP_STATIC = os.path.join(APP_ROOT, 'static')
UPLOADS_FOLDER = os.path.join(os.path.join(APP_STATIC, 'uploads'))
ALLOWED_EXTENSIONS_BANNER = ['png', 'jpg', 'jpeg', 'gif']
ALLOWED_EXTENSIONS_ATTACHMENT = ['png', 'jpg', 'jpeg', 'txt', 'pdf', 'docx', 'doc']

ALLOWED_FILESIZE_BANNER = 300 * 1024
ALLOWED_FILESIZE_ATTACHMENT = 2 * 1024 * 1024

tagextraction = TagExtraction()
StopWords, Blacklists, BigramTags, TrigramTags, QuadgramTags = tagextraction.Load_Files()
qe = QE()
spellchecker = SpellChecker()



r = redis.StrictRedis(host=REDIS_SERVER_ADDRESS, port=6379, db=0)

app.config['SECURITY_REGISTERABLE'] = True
# app.config['SECURITY_CONFIRMABLE'] = True
app.config['SECURITY_RECOVERABLE'] = True
app.config['SECURITY_CHANGEABLE'] = True
app.config['SECURITY_TRACKABLE'] = True
# app.config['SECURITY_SEND_REGISTER_EMAIL'] = False
app.config['SECURITY_POST_LOGIN_VIEW'] = '/dashboard'
app.config['SECURITY_POST_LOGOUT_VIEW'] = '/'
app.config['SECURITY_EMAIL_SENDER'] = 'no-reply@8tad.ir'

app.config['SECURITY_CHANGE_URL'] = '/dashboard/user/profile/password/edit'
app.config['SECURITY_LOGIN_URL'] = '/accounts/login'
app.config['SECURITY_LOGOUT_URL'] = '/accounts/logout'

app.config['SECURITY_RESET_URL'] = '/accounts/password/reset'
app.config['SECURITY_REGISTER_URL'] = '/accounts/registration'

app.config['SECURITY_CONFIRM_URL'] = '/accounts/confirm'

app.config['SEND_PASSWORD_RESET_NOTICE_EMAIL'] = False
app.config['SEND_PASSWORD_CHANGE_EMAIL'] = False
app.config['SECURITY_SEND_PASSWORD_RESET_NOTICE_EMAIL'] = False

app.config['SECURITY_POST_REGISTER_VIEW'] = '/dashboard'

app.config['SECURITY_PASSWORD_HASH'] = 'bcrypt'
app.config['SECURITY_PASSWORD_SALT'] = '$2b$12$xXdE64sYdZPJhaHdn98aveSEYB768VYLVSblsYWF84jHDgEKlbqcm'

app.config['SECURITY_UNAUTHORIZED_VIEW'] = '/dashboard'

app.config.setdefault('SECURITY_MSG_' + 'CONFIRMATION_REQUIRED', (
    'ایمیل شما نیاز به تایید دارد. لطفا به حساب ایمیل خود مراجعه کنید و آن را تایید نمایید.', 'error'))
app.config.setdefault('SECURITY_MSG_' + 'CONFIRMATION_REQUEST',
                      ('دستورالعمل تایید ایمیل به  %(email)s ارسال شد.', 'info'))
app.config.setdefault('SECURITY_MSG_' + 'ALREADY_CONFIRMED', ('ایمیل شما قبلا تایید شده است.', 'info'))
app.config.setdefault('SECURITY_MSG_' + 'USER_DOES_NOT_EXIST', ('چنین کاربری در سامانه وجود ندارد.', 'error'))
app.config.setdefault('SECURITY_MSG_' + 'INVALID_PASSWORD', ('کلمه عبور اشتباه است.', 'error'))

# Setup Flask-Security
user_datastore = PeeweeUserDatastore(db, User, Role, UserRoles)
security = Security(app, user_datastore, login_form=ExtendedLoginForm, register_form=ExtendedRegisterForm,
                    confirm_register_form=ExtendedRegisterForm,
                    forgot_password_form=ExtendedForgotPasswordForm, change_password_form=ExtendedChangePasswordForm
                    , reset_password_form=ExtendedResetPasswordForm
                    # ,send_confirmation_form=ExtendedSendConfirmationForm
                    )
user_datastore.find_or_create_role(name='superadmin', description='Super Administrator')
user_datastore.find_or_create_role(name='admin', description='Administrator')
user_datastore.find_or_create_role(name='advertiser', description='Advertiser')
user_datastore.find_or_create_role(name='publisher', description='Publisher')


def check_auth(username, password):
    return username == 'itrc' and password == 'secret123$'


def authenticate():
    return Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)

    return decorated


@app.route('/api/url/keyword/suggestion', methods=['POST'])
@csrf.exempt
@requires_auth
def itrc_url_keyword_suggestion():
    data = request.json
    page = ''
    counter = 0
    url = data.get('url', None)
    while page == '':
        try:
            page = requests.get(url)
            break
        except:
            counter += 1
            if counter >= 10:
                break
            print("Connection refused by the server..")
            print("Let me sleep for 1 seconds")
            print("ZZzzzz...")
            time.sleep(1)
            print("Was a nice sleep, now let me continue...")
            continue

    response = []
    try:
        ngrams = tagextraction.HTML_KeywordsExtractionByNewsTagsV2(page.content, StopWords, Blacklists, BigramTags,
                                                                   TrigramTags, QuadgramTags, 5, 10)
        for idx, item in enumerate(ngrams):
            response.append(item)
            if idx == 9:
                break
    except Exception:
        print
        traceback.format_exc(sys.exc_info())

    response = {"status": "ok", "body": response}
    return Response(json.dumps(response, sort_keys=True),
                    mimetype='application/json')


@app.route('/api/query/expansion', methods=['POST'])
@csrf.exempt
@requires_auth
def itrc_query_expansion():
    data = request.json
    keywords = data.get('keywords')
    expansion_keywords = []
    number_of_related_word = 3
    for keyword in keywords:
        temp = qe.useModel_1(str(keyword).strip(), number_of_related_word)
        expansion_keywords.extend(temp)

    return Response(json.dumps(expansion_keywords, sort_keys=False),
                    mimetype='application/json')


@app.route('/api/normalizer/string', methods=['POST'])
@csrf.exempt
def itrc_normalizer():
    if request.method == 'POST':
        data = request.json
        record = {
            'text': data.get('text', None)
        }
        result = requests.post(BACKEND_SERVER_ADDRESS + "/api/normalizer/string?local=false",
                               data=json.dumps(record)).content
        result = json.loads(result)
        return Response(json.dumps(result, sort_keys=True),
                        mimetype='application/json')


@app.route('/api/normalizer/url', methods=['POST'])
@csrf.exempt
def itrc_url():
    if request.method == 'POST':
        data = request.json
        record = {
            'url': data.get('url', None)
        }
        result = requests.post(BACKEND_SERVER_ADDRESS + "/api/normalizer/url",
                               data=json.dumps(record)).content
        result = json.loads(result)
        return Response(json.dumps(result, sort_keys=True),
                        mimetype='application/json')


@app.route('/dashboard/admin/campaign/ctr/update', methods=['GET'])
@requires_auth
def admin_campaign_ctr_update():
    date = datetime.now()

    to_date = date.strptime(date.strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")
    from_date = to_date - dateutil.relativedelta.relativedelta(hours=24)

    data = {
        'from_date': str(from_date),
        'to_date': str(to_date)
    }

    result = requests.post(BACKEND_SERVER_ADDRESS + "/reports/admin/campaign/ctr",
                           data=json.dumps(data)).content
    result = json.loads(result)
    campaigns = result['body']

    campaign_minimum_ctr = 1
    campaign_maximum_ctr = 0
    for key in campaigns["shows"]:
        r.delete('campaign_ctr_' + str(key))
        ctr = 0
        if key in campaigns["clicks"]:
            ctr = (float(campaigns["clicks"][key]["ad_click_counter"]) / float(
                campaigns["shows"][key]["ad_show_counter"]))
            r.sadd('campaign_ctr_' + str(key), ctr)
        else:
            r.sadd('campaign_ctr_' + str(key), ctr)

        if ctr > campaign_maximum_ctr:
            campaign_maximum_ctr = ctr

        if ctr < campaign_minimum_ctr:
            campaign_minimum_ctr = ctr

    result = requests.get(BACKEND_SERVER_ADDRESS + "/advertiser/active/campaigns/min_max").content
    result = json.loads(result)
    campaign = result['body']

    r.delete('campaign_minimum_ctr')
    r.sadd('campaign_minimum_ctr', campaign_minimum_ctr)

    r.delete('campaign_maximum_ctr')
    r.sadd('campaign_maximum_ctr', campaign_maximum_ctr)

    r.delete('campaign_minimum_cost')
    r.sadd('campaign_minimum_cost', campaign['campaign_minimum_cost'])

    r.delete('campaign_maximum_cost')
    r.sadd('campaign_maximum_cost', campaign['campaign_maximum_cost'])

    r.delete('campaign_minimum_budget')
    r.sadd('campaign_minimum_budget', campaign['campaign_minimum_budget'])

    r.delete('campaign_maximum_budget')
    r.sadd('campaign_maximum_budget', campaign['campaign_maximum_budget'])

    r.delete('campaign_minimum_coef')
    r.sadd('campaign_minimum_coef', campaign['campaign_minimum_coef'])

    r.delete('campaign_maximum_coef')
    r.sadd('campaign_maximum_coef', campaign['campaign_maximum_coef'])

    response = {"status": "yes"}
    return Response(json.dumps(response, sort_keys=False),
                    mimetype='application/json')


# @app.route('/itrc/api/8tad/campaigns', methods=['GET'])
# @requires_auth
# def itrc_api_campaigns():
#     if request.method == 'GET':
#         result = requests.get(BACKEND_SERVER_ADDRESS + "/advertiser/campaigns/itrc").content
#         result = json.loads(result)
#         result = result['body']
#
#         return Response(json.dumps(result, sort_keys=True),
#                         mimetype='application/json')
#
#
# @app.route('/itrc/api/8tad/websites', methods=['GET'])
# @requires_auth
# def itrc_api_websites():
#     if request.method == 'GET':
#         result = requests.get(BACKEND_SERVER_ADDRESS + "/publisher/website").content
#         result = json.loads(result)
#         result = result['body']
#
#         return Response(json.dumps(result, sort_keys=True),
#                         mimetype='application/json')
#
#
# @app.route('/itrc/api/8tad/users', methods=['GET'])
# @requires_auth
# def itrc_api_users():
#     if request.method == 'GET':
#         users = UserRests()
#         result = users.get()
#         result = json.loads(result)
#         result = result['body']
#
#         return Response(json.dumps(result, sort_keys=True),
#                         mimetype='application/json')


@app.route('/dashboard/user/profile/edit', methods=['GET', 'POST'])
@login_required
def user_profile_edit():
    configs = {
        'module': 'پروفایل',
        'action': 'ویرایش اطلاعات کاربری',
        'url': 'user_profile_edit',
        'url_index': 'user_profile_edit'
    }
    form = EditProfileForm()
    if request.method == 'POST':
        if form.validate() == False:
            flash('All fields are required.', 'danger')
            return render_template('general/profile_edit.html', form=form, configs=configs)
        else:
            data = {
                # 'user_email': form.email.data,
                'user_phone': form.phone.data,
                'user_fullname': form.fullname.data,
                'user_account_type': form.account_type.data,
            }

            user = UserRests()
            result = user.put(current_user.get_id(), json.dumps(data))
            result = json.loads(result)
            result = result['body']

            return render_template('general/profile_edit.html', form=form, result=result, configs=configs)
    elif request.method == 'GET':
        user = UserRests()
        result = user.get(current_user.get_id())
        result = json.loads(result)
        result = result['body']

        # form.email.data = result["user_email"]
        form.phone.data = result["user_phone"]
        form.fullname.data = result["user_fullname"]
        form.account_type.data = result["user_account_type"]

        return render_template('general/profile_edit.html', form=form, configs=configs)


@app.route('/dashboard/user/profile/email/edit', methods=['GET', 'POST'])
@login_required
def user_email_edit():
    configs = {
        'module': 'پروفایل',
        'action': 'تغییر ایمیل',
        'url': 'user_email_edit',
        'url_index': 'user_email_edit'
    }
    form = EditProfileEmailForm()
    if request.method == 'POST':
        if form.validate() == False:
            flash('All fields are required.', 'danger')
            return render_template('general/profile_edit.html', form=form, configs=configs)
        else:
            data = {
                'user_email': form.email.data,
            }

            user = UserRests()
            result = user.put(current_user.get_id(), json.dumps(data))
            result = json.loads(result)
            result = result['body']

            return render_template('general/profile_edit.html', form=form, result=result, configs=configs)
    elif request.method == 'GET':
        user = UserRests()
        result = user.get(current_user.get_id())
        result = json.loads(result)
        result = result['body']

        form.email.data = result["user_email"]

        return render_template('general/profile_edit.html', form=form, configs=configs)


@app.route('/dashboard/user/profile/bank/edit', methods=['GET', 'POST'])
@login_required
def user_bank_account_edit():
    configs = {
        'module': 'پروفایل',
        'action': 'ویرایش اطلاعات مالی',
        'url': 'user_bank_account_edit',
        'url_index': 'user_bank_account_edit'
    }
    form = EditBankAccount()
    if request.method == 'POST':
        if form.validate() == False:
            flash('All fields are required.', 'danger')
            return render_template('general/profile_edit.html', form=form, configs=configs)
        else:
            data = {
                'shaba_code': form.shaba_code.data,
                'bank_name': form.bank_name.data,
                'bank_account_number': form.bank_account_number.data,
                'bank_card_number': form.bank_card_number.data,
            }
            bank_account = UserBankAccountRests()
            result = bank_account.get(current_user.get_id())
            result = json.loads(result)
            if result['status'] == 'ok':
                bank_account.put(current_user.get_id(), json.dumps(data))
            elif result['body'] == 'Record Does Not Exist':
                bank_account.post(current_user.get_id(), json.dumps(data))

            return render_template('general/profile_edit.html', form=form, configs=configs)
    elif request.method == 'GET':
        bank_account = UserBankAccountRests()
        result = bank_account.get(current_user.get_id())
        result = json.loads(result)
        if result['status'] == 'ok':
            result = result['body']
            form.shaba_code.data = result["shaba_code"]
            form.bank_name.data = result["bank_name"]
            form.bank_account_number.data = result["bank_account_number"]
            form.bank_card_number.data = result["bank_card_number"]

        return render_template('general/profile_edit.html', form=form, configs=configs)


# @app.route('/native', methods=['GET'])
# def native():
#     element = request.args.get('element_id')
#     return render_template('frontend/native.html', element=element)


@app.route('/', methods=['GET'])
def home():
    return render_template('frontend/index.html')


@app.route('/cron', methods=['GET'])
def cron():
    return 'success'


@app.route('/technology', methods=['GET'])
def technology():
    return render_template('frontend/technology.html')


@app.route('/about', methods=['GET'])
def about():
    return render_template('frontend/about.html')


@app.route('/pricing', methods=['GET'])
def pricing():
    return render_template('frontend/pricing.html')


@app.route('/contact', methods=['GET'])
def contact():
    return render_template('frontend/contact.html')


@app.route('/ads', methods=['GET'])
def ads():
    return render_template('frontend/ads.html')


def publisher_credit_calculation(user_id=None):
    try:
        if user_id is None:
            user_id = str(current_user.get_id())
        else:
            user_id = str(user_id)

        total_benfit = 0
        redis_set_benfit = r.smembers('publisher_total_benefit_' + user_id)
        if len(list(redis_set_benfit)) > 0:
            total_benfit = int(float(list(redis_set_benfit)[0]))

        result = requests.get(
            BACKEND_SERVER_ADDRESS + "/financial/user/" + user_id + "/transactions").content
        result = json.loads(result)
        transactions = result['body']

        total_deposit = 0
        total_withdrawal = 0
        for transaction in transactions:
            total_deposit = total_deposit + int(transaction["transaction_deposit_amount"])
            total_withdrawal = total_withdrawal + int(transaction["transaction_withdrawal_amount"])

        credit = total_benfit + total_deposit - total_withdrawal
        return credit
    except Exception:
        return 0


def campaign_deactivate_function(campaign_id):
    result = requests.get(BACKEND_SERVER_ADDRESS + "/advertiser/campaign/" + str(campaign_id)).content
    result = json.loads(result)
    result = result['body']

    if result['campaign_author_user_id'] != current_user.get_id() and not current_user.has_role('admin'):
        return redirect(url_for('dashboard'))

    r.sadd('campaign_deactivate', campaign_id)

    total_budget = 0
    if result['campaign_active_by_admin']:
        redis_total_budget = r.smembers('campaign_total_budget_' + str(result['campaign_id']))
        if len(list(redis_total_budget)) > 0:
            total_budget = int(float(list(redis_total_budget)[0]))
    else:
        return

    if result['campaign_targeted_geography_all']:
        r.srem('campaign_targeted_geography_not_iran', result['campaign_id'])
        r.srem('campaign_targeted_geography_all', result['campaign_id'])

    if result['campaign_targeted_geography_iran'] or result['campaign_targeted_geography_all']:
        records = requests.get(BACKEND_SERVER_ADDRESS + "/admin/target/geography").content
        records = json.loads(records)
        records = records['body']
        for record in records:
            r.srem('campaign_targeted_geography_' + record['geography_name'], result['campaign_id'])

    if result['campaign_targeted_geography_not_iran']:
        r.srem('campaign_targeted_geography_not_iran', result['campaign_id'])

    if result['campaign_targeted_geography_special']:
        records = requests.get(
            BACKEND_SERVER_ADDRESS + "/advertiser/campaign/geography?campaign=" + str(result['campaign_id'])).content
        records = json.loads(records)
        records = records['body']
        for record in records:
            r.srem('campaign_targeted_geography_' + record["geography"]["geography_name"], result['campaign_id'])

    if result['campaign_targeted_operating_system_all']:
        records = requests.get(BACKEND_SERVER_ADDRESS + "/admin/target/os").content
        records = json.loads(records)
        records = records['body']
        for record in records:
            r.srem('campaign_targeted_operating_system_' + record['os_name'], result['campaign_id'])

    if result['campaign_targeted_operating_system_special']:
        records = requests.get(
            BACKEND_SERVER_ADDRESS + "/advertiser/campaign/os?campaign=" + str(result['campaign_id'])).content
        records = json.loads(records)
        records = records['body']
        for record in records:
            r.srem('campaign_targeted_operating_system_' + record["os"]["os_name"], result['campaign_id'])

    if result['campaign_targeted_subject_all']:
        records = requests.get(BACKEND_SERVER_ADDRESS + "/admin/target/subject").content
        records = json.loads(records)
        records = records['body']
        for record in records:
            r.srem('campaign_targeted_subject_' + str(record['subject_id']), result['campaign_id'])

    if result['campaign_targeted_subject_special']:
        records = requests.get(
            BACKEND_SERVER_ADDRESS + "/advertiser/campaign/subject?campaign=" + str(result['campaign_id'])).content
        records = json.loads(records)
        records = records['body']
        for record in records:
            r.srem('campaign_targeted_subject_' + str(record["subject"]["subject_id"]), result['campaign_id'])

    r.srem('campaign_playtime_00_08', result['campaign_id'])
    r.srem('campaign_playtime_08_16', result['campaign_id'])
    r.srem('campaign_playtime_16_24', result['campaign_id'])

    if result['campaign_network_class_a']:
        r.srem('campaign_network_class_a', result['campaign_id'])

    if result['campaign_network_class_b']:
        r.srem('campaign_network_class_b', result['campaign_id'])

    if result['campaign_network_class_c']:
        r.srem('campaign_network_class_c', result['campaign_id'])

    if result['campaign_retargeting']:
        r.srem('campaign_retargeting', result['campaign_id'])

    if result['campaign_targeted_keyword_special']:
        records = requests.get(
            BACKEND_SERVER_ADDRESS + "/advertiser/campaign/keyword?campaign=" + str(result['campaign_id'])).content
        records = json.loads(records)
        records = records['body']
        for record in records:
            strTitle = record["keyword"]["keyword_title"]
            strTitle = strTitle.replace(" ", "-")
            r.srem('campaign_targeted_keyword_' + strTitle, result['campaign_id'])

    r.delete('campaign_targeted_keywords_' + str(result['campaign_id']))

    if result['campaign_type']['campaign_type_name'] == 'banner' or result['campaign_type'][
        'campaign_type_name'] == 'mobile' or result['campaign_type']['campaign_type_name'] == 'native':
        records = requests.get(
            BACKEND_SERVER_ADDRESS + "/advertiser/campaign/" + str(result['campaign_id']) + "/banners").content
        records = json.loads(records)
        records = records['body']
        for record in records:
            r.srem(
                'campaign_banner_size_' + str(record["banner_size"]["banner_size_width"]) + 'x' + str(
                    record["banner_size"][
                        "banner_size_height"]),
                result['campaign_id'])
            r.delete(
                'campaign_' + str(result['campaign_id']) + '_banner_' + str(
                    record["banner_size"]["banner_size_width"]) + 'x' + str(record["banner_size"][
                                                                                "banner_size_height"]))

        r.delete('campaign_type_' + str(result['campaign_id']))

    if result['campaign_type']['campaign_type_name'] == 'iframe':

        records = requests.get(
            BACKEND_SERVER_ADDRESS + "/advertiser/campaign/" + str(result['campaign_id']) + "/banners").content
        records = json.loads(records)
        records = records['body']
        for record in records:
            r.srem(
                'campaign_banner_size_' + str(record["banner_size"]["banner_size_width"]) + 'x' + str(
                    record["banner_size"][
                        "banner_size_height"]),
                result['campaign_id'])
            r.delete(
                'campaign_' + str(result['campaign_id']) + '_html_' + str(
                    record["banner_size"]["banner_size_width"]) + 'x' + str(record["banner_size"][
                                                                                "banner_size_height"]))

        r.delete('campaign_type_' + str(result['campaign_id']))

    if result['campaign_type']['campaign_type_name'] == 'native':
        r.delete('campaign_' + str(result['campaign_id']) + '_native_title')
        r.srem('campaign_content_list', result['campaign_id'])

    if result['campaign_type']['campaign_type_name'] == 'search_engine':
        r.delete('campaign_' + str(result['campaign_id']) + '_title')
        r.delete('campaign_' + str(result['campaign_id']) + '_description')
        r.delete('campaign_' + str(result['campaign_id']) + '_email')
        r.delete('campaign_' + str(result['campaign_id']) + '_phone')
        r.delete('campaign_' + str(result['campaign_id']) + '_address')
        r.delete('campaign_adwords_list', result['campaign_id'])

    records = requests.get(
        BACKEND_SERVER_ADDRESS + "/advertiser/blocked/website/user/" + str(result['campaign_author_user_id'])).content
    records = json.loads(records)
    records = records['body']

    for record in records:
        r.srem('campaigns_blocked_website_' + urlparse(record["blocked_website_url"]).hostname.replace("www.", ""),
               result['campaign_id'])

    r.delete('campaign_total_budget_' + str(result['campaign_id']))
    r.delete('campaign_daily_budget_' + str(result['campaign_id']))
    r.delete('campaign_variable_daily_budget_' + str(result['campaign_id']))
    r.delete('campaign_budget_management_' + str(result['campaign_id']))
    r.delete('campaign_click_price_' + str(result['campaign_id']))
    r.delete('campaign_coef_' + str(result['campaign_id']))
    r.delete('campaign_landing_page_url_' + str(result['campaign_id']))

    if result['campaign_landing_page_url']:
        r.srem(
            'campaign_landing_page_campaign_' + urlparse(result['campaign_landing_page_url']).hostname.replace("www.",
                                                                                                               ""),
            result['campaign_id'])

    r.delete('campaign_activate_date_' + str(result['campaign_id']))

    data = {}
    if result['campaign_active_by_admin']:
        data = {
            'campaign_updated_user_id': current_user.get_id(),
            'campaign_active_by_admin': False,
            'campaign_total_budget': total_budget
        }
    else:
        data = {
            'campaign_updated_user_id': current_user.get_id(),
            'campaign_active_by_admin': False
        }

    result = requests.put(BACKEND_SERVER_ADDRESS + "/advertiser/campaign/" + str(campaign_id),
                          data=json.dumps(data)).content
    result = json.loads(result)

    if result["status"] == "ok":
        message = json.dumps({"type": "alert-success", "message": "کمپین با موفقیت غیر فعال شد."})
    elif result["status"] == "nok":
        message = json.dumps({"type": "alert-error", "message": "خطایی رخ داده است."})
    session['message'] = message


def website_deactivate_function(website_id):
    result = requests.get(BACKEND_SERVER_ADDRESS + "/publisher/website/" + str(website_id)).content
    result = json.loads(result)
    result = result['body']

    website_url = urlparse(result['publisher_website_url']).hostname.replace("www.", "")

    r.delete('publisher_website_subject_' + website_url)
    r.delete('publisher_website_grade_' + website_url)

    r.srem('publishers_website_banner', website_url)
    r.srem('publishers_website_search_engine', website_url)

    r.srem('publishers_website_' + website_url, website_id)

    r.srem('publishers_website_' + str(website_id), website_url)

    r.delete('publisher_id_website_' + website_url)

    r.delete('publisher_website_percentage_' + website_url)

    r.delete('publisher_website_native_style_' + website_url)

    r.delete('publisher_username_' + website_url)
    r.delete('publisher_password_' + website_url)

    r.delete('website_blocked_campaigns_' + website_url)

    data = {
        'publisher_website_updated_user_id': current_user.get_id(),
        'publisher_website_active_by_admin': False
    }

    result = requests.put(BACKEND_SERVER_ADDRESS + "/publisher/website/" + str(website_id),
                          data=json.dumps(data)).content
    result = json.loads(result)

    if result["status"] == "ok":
        message = json.dumps({"type": "alert-success", "message": "وب سایت با موفقیت غیر فعال شد."})
    elif result["status"] == "nok":
        message = json.dumps({"type": "alert-error", "message": "خطایی رخ داده است."})
    session['message'] = message


@app.route('/dashboard/admin', methods=['GET', 'POST'])
@login_required
@roles_accepted('admin')
def admin_dashboard():
    configs = {
        'module': 'داشبورد مدیر سامانه',
        'action': 'داشبورد',
        'url_index': 'admin_dashboard',
        'page_title': 'داشبورد'
    }

    date = datetime.now()
    to_date = date.strptime(date.strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")
    from_date = to_date - dateutil.relativedelta.relativedelta(days=3)

    data = {
        'from_date': str(from_date)[:10] + ' 00:00:00',
        'to_date': str(to_date)
    }

    result = requests.post(BACKEND_SERVER_ADDRESS + "/reports/admin/dashboard/period",
                           data=json.dumps(data)).content
    result = json.loads(result)
    dashboard = result['body']

    clicks = OrderedDict(sorted(dashboard["clicks"].items(), key=lambda t: t[0]))
    shows = OrderedDict(sorted(dashboard["shows"].items(), key=lambda t: t[0]))

    return render_template('dashboard/admin/index.html', clicks=clicks, shows=shows, dashboard=dashboard,
                           configs=configs)


@app.route('/dashboard/admin/campaign/ctr', methods=['GET', 'POST'])
@login_required
@roles_accepted('admin')
def admin_campaign_ctr():
    configs = {
        'module': 'داشبورد مدیر سامانه',
        'action': 'داشبورد',
        'url_index': 'admin_dashboard',
        'page_title': 'داشبورد'
    }

    date = datetime.now()

    if request.method == 'GET':
        to_date = date.strptime(date.strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")
        from_date = to_date - dateutil.relativedelta.relativedelta(days=2)
    elif request.method == 'POST':
        to_date = date.strptime(persian_date_to_gregorian_date(request.form['to_date']) + " 23:59:59",
                                "%Y-%m-%d %H:%M:%S")
        from_date = date.strptime(persian_date_to_gregorian_date(request.form['from_date']) + " 00:00:00",
                                  "%Y-%m-%d %H:%M:%S")

    data = {
        'from_date': str(from_date),
        'to_date': str(to_date)
    }

    result = requests.post(BACKEND_SERVER_ADDRESS + "/reports/admin/campaign/ctr",
                           data=json.dumps(data)).content
    result = json.loads(result)
    campaigns = result['body']

    ids = []
    for key in campaigns["shows"]:
        ids.append(campaigns["shows"][key]["ad_show_campaign_author_user_id"])

    authors = users(ids)
    authors = json.loads(authors)
    authors = authors['body']

    return render_template('admin/campaign/ctr.html', campaigns=campaigns,
                           configs=configs,
                           from_date=str(from_date)[:10],
                           to_date=str(to_date)[:10],
                           authors=authors
                           )


@app.route('/dashboard/admin/website/ctr', methods=['GET', 'POST'])
@login_required
@roles_accepted('admin')
def admin_website_ctr():
    configs = {
        'module': 'داشبورد مدیر سامانه',
        'action': 'داشبورد',
        'url_index': 'admin_dashboard',
        'page_title': 'داشبورد'
    }

    date = datetime.now()

    if request.method == 'GET':
        to_date = date.strptime(date.strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")
        from_date = to_date - dateutil.relativedelta.relativedelta(days=2)
    elif request.method == 'POST':
        to_date = date.strptime(persian_date_to_gregorian_date(request.form['to_date']) + " 23:59:59",
                                "%Y-%m-%d %H:%M:%S")
        from_date = date.strptime(persian_date_to_gregorian_date(request.form['from_date']) + " 00:00:00",
                                  "%Y-%m-%d %H:%M:%S")

    data = {
        'from_date': str(from_date),
        'to_date': str(to_date)
    }

    result = requests.post(BACKEND_SERVER_ADDRESS + "/reports/admin/website/ctr",
                           data=json.dumps(data)).content
    result = json.loads(result)
    websites = result['body']

    ids = []
    for key in websites["shows"]:
        ids.append(websites["shows"][key]["ad_show_publisher"])

    authors = users(ids)
    authors = json.loads(authors)
    authors = authors['body']

    return render_template('admin/website/ctr.html', websites=websites,
                           configs=configs,
                           from_date=str(from_date)[:10],
                           to_date=str(to_date)[:10],
                           authors=authors
                           )


@app.route('/dashboard/advertiser/campaign/keyword/suggestion', methods=['POST'])
@login_required
@roles_accepted('advertiser')
def campaign_keyword_suggestion(url=None):
    # time1 = int(round(time.time() * 1000))
    page = ''
    counter = 0
    while page == '':
        try:
            if url is None:
                url = request.form.get('landing_page_url')

            page = requests.get(url)
            break
            # print page.content
        except:
            counter += 1
            if counter >= 10:
                break
            print("Connection refused by the server..")
            print("Let me sleep for 1 seconds")
            print("ZZzzzz...")
            time.sleep(1)
            print("Was a nice sleep, now let me continue...")
            continue

    # time2 = int(round(time.time() * 1000))
    # print(time2 - time1)
    response = []
    try:
        # print page.content
        ngrams = tagextraction.HTML_KeywordsExtractionByNewsTagsV2(page.content, StopWords, Blacklists, BigramTags,
                                                                   TrigramTags, QuadgramTags, 5, 10)
        for idx, item in enumerate(ngrams):
            response.append(item)
            if idx == 9:
                break
    except Exception:
        print
        traceback.format_exc(sys.exc_info())

    response = {"status": "ok", "body": response}
    return Response(json.dumps(response, sort_keys=True),
                    mimetype='application/json')


@app.route('/dashboard/user/<user_id>/credit', methods=['GET'])
@login_required
@roles_accepted('admin')
def user_credit(user_id):
    credit = publisher_credit_calculation(user_id)
    return format_currency(credit)


@app.route('/dashboard/user/credit', methods=['GET'])
@login_required
@roles_accepted('advertiser')
def current_user_credit():
    credit = publisher_credit_calculation(current_user.get_id())
    return format_currency(credit)


@app.route('/dashboard/admin/user/<id>/financial', methods=['GET'])
@login_required
@roles_accepted('superadmin')
def user_financial(id):
    user_bank_account = UserBankAccountRests()
    result = user_bank_account.get(id)
    result = json.loads(result)
    user_bank_account = result['body']
    return render_template('admin/user/bank_account.html', user_bank_account=user_bank_account)


@app.route('/dashboard/admin/user/<id>/roles', methods=['GET', 'POST'])
@login_required
@roles_accepted('superadmin')
def user_roles(id):
    if request.method == 'POST':
        data = {
            'roles': request.form.getlist("roles"),
            'user': id
        }
        user_roles = UserRolesRests()
        result = user_roles.post(json.dumps(data))
        result = json.loads(result)
        result = result['body']
        return "success"

    user_roles = UserRolesRests()
    result = user_roles.get(id)
    result = json.loads(result)
    user_roles = result['body']

    roles = RoleRests()
    result = roles.get()
    result = json.loads(result)
    roles = result['body']

    return render_template('admin/user/roles.html', user_roles=user_roles, roles=roles)


@app.route('/dashboard/admin/user/<id>/charge', methods=['POST'])
@login_required
@roles_accepted('superadmin')
def user_charge(id):
    amount = int(request.form.get("amount").replace(",", ""))
    deposit = withdrawal = 0
    if request.form.get("amount_status") == 'deposit':
        deposit = amount
    elif request.form.get("amount_status") == 'withdrawal':
        withdrawal = amount

    data = {
        'transaction_author_user_id': id,
        'transaction_updated_user_id': current_user.get_id(),
        'transaction_deposit_amount': deposit,
        'transaction_withdrawal_amount': withdrawal,
        'transaction_description': request.form.get("description"),
        'transaction_status': 1
    }
    result = requests.post(BACKEND_SERVER_ADDRESS + "/financial/transaction",
                           data=json.dumps(data)).content
    result = json.loads(result)
    result = result['body']

    return str(amount)


@app.route('/dashboard/admin/user/new', methods=['GET', 'POST'])
@login_required
def user_new():
    return redirect(url_for('user'))


@app.route('/dashboard/admin/user/<id>/edit', methods=['GET', 'POST'])
@login_required
@roles_accepted('superadmin')
def user_edit(id):
    configs = {
        'module': 'لیست کاربران',
        'action': 'ویرایش کاربر',
        'url': 'user_edit',
        'url_index': 'user',
        'id': id
    }
    form = EditRegisterForm()
    if request.method == 'POST':
        if form.validate() == False:
            flash('All fields are required.', 'danger')
            return render_template('general/edit.html', form=form, configs=configs)
        else:
            data = {
                # 'user_email': form.email.data,
                'user_phone': form.phone.data,
                'user_fullname': form.fullname.data,
                'user_account_type': form.account_type.data,
                'user_active': form.active.data,
            }

            user = UserRests()
            result = user.put(id, json.dumps(data))
            result = json.loads(result)
            result = result['body']

            return render_template('general/edit.html', form=form, result=result, configs=configs)
    elif request.method == 'GET':
        user = UserRests()
        result = user.get(id)
        result = json.loads(result)
        result = result['body']

        # form.email.data = result["user_email"]
        form.phone.data = result["user_phone"]
        form.fullname.data = result["user_fullname"]
        form.account_type.data = result["user_account_type"]
        form.active.data = result["user_active"]

        return render_template('general/edit.html', form=form, configs=configs)


@app.route('/dashboard/admin/user', methods=['GET', 'POST'])
@app.route('/dashboard/admin/user/<user_id>', methods=['GET', 'POST'])
@login_required
@roles_accepted('superadmin')
def user(user_id=None):
    configs = {
        'url_new': 'user_new',
        'url_edit': 'user_edit',
        'url_index': 'user',
        'module': 'لیست کاربران',
        'action': 'لیست کاربران',
        'url_new_text': 'کاربر جدید',
        'id_name': 'user_id',
        'page_title': 'کاربران - مدیریت کاربران'
    }

    users = UserRests()
    if user_id is None:
        result = users.get()
        result = json.loads(result)
        result = result['body']
    else:
        result = users.get(user_id)
        result = json.loads(result)
        tmp = result['body']
        user = user_datastore.get_user(tmp["user_id"])
        token = generate_login_token(user)
        tmp["user_token"] = token
        result = []
        result.append(tmp)

    form = CreditAdminForm()
    return render_template('admin/user/index.html', result=result, form=form, configs=configs)


@app.route('/dashboard/one/admin/user/<user_id>', methods=['GET', 'POST'])
def user_one(user_id=None):
    users = UserRests()
    result = users.get(user_id)
    result = json.loads(result)
    tmp = result['body']
    response = {"status": "ok", "body": result['body']}
    return Response(json.dumps(response, sort_keys=True),
                    mimetype='application/json')


@app.route('/accounts/login/token/<token>', methods=['GET'])
def token_login(token):
    if request.method == 'GET':
        expired, invalid, user = login_token_status(token)

        if invalid or expired:
            return redirect(url_for('login'))

        login_user(user)
        _commit()
        return redirect(url_for('dashboard'))


# @app.route('/dashboard/admin/website', methods=['GET', 'POST'])
# @login_required
# @roles_accepted('admin')
# def publisher_website_admin():
#     configs = {
#         'url_edit': 'publisher_website_admin_edit',
#         'url_index': 'publisher_website_admin',
#         'module': 'مدیریت وب سایت ها',
#         'action': 'مدیریت وب سایت ها',
#         'id_name': 'publisher_website_id',
#         'page_title': 'سایت ها - مدیریت وب سایت ها'
#     }
#     message = None
#
#     if request.method == 'POST' and request.is_xhr:
#         page = (int(request.values["start"]) / int(request.values["length"])) + 1
#
#         result = requests.get(
#             BACKEND_SERVER_ADDRESS + "/publisher/website?limit=" + request.values["length"] + "&page=" + str(
#                 page)).content
#         result = json.loads(result)
#         result = result['body']
#
#         ids = []
#         for query in result:
#             ids.append(query["publisher_website_author_user_id"])
#
#         authors = users(ids)
#         authors = json.loads(authors)
#         authors = authors['body']
#
#         data = {
#             "draw": int(request.values["draw"]),
#             "recordsTotal": 100,
#             "recordsFiltered": 100,
#             "data": [
#             ]
#         }
#
#         for query in result:
#             record = []
#
#             user = '<a target="_blank" href="' + url_for('user', user_id=query[
#                 'publisher_website_author_user_id']) + '">' + \
#                    authors[str(query['publisher_website_author_user_id'])]['fullname'] + '</a>'
#             record.append(user)
#
#             record.append(query['publisher_website_title'])
#
#             url = '<span style="text-align:left;display:block;" dir="ltr"><a target="_blank" href="' + query[
#                 'publisher_website_url'] + '">' + query['publisher_website_url'] + '</a></span>'
#             record.append(url)
#
#             type = ''
#             if query["publisher_website_type"] == 'banner':
#                 type = 'بنری'
#             elif query["publisher_website_type"] == 'search_engine':
#                 type = 'موتور جستجو'
#             elif query["publisher_website_type"] == 'both':
#                 type = 'بنری و موتور جستجو'
#             record.append(type)
#
#             record.append(query['publisher_website_grade'])
#             record.append(enToPersianNumb(query['publisher_website_percentage']))
#
#             status = 'تایید مدیر: '
#             if query["publisher_website_active_by_admin"]:
#                 temp = 'text-success'
#             else:
#                 temp = 'text-error'
#
#             status += '<span class ="muted ' + temp + '">' + boolean_status(
#                 query["publisher_website_active_by_admin"]) + '</span><br>'
#             status += 'وضعیت حذف: '
#
#             if query["publisher_website_is_deleted"]:
#                 temp = 'text-success'
#             else:
#                 temp = 'text-error'
#
#             status += '<span class ="muted ' + temp + '">' + boolean_status(
#                 query["publisher_website_is_deleted"]) + '</span><br>'
#
#             record.append(status)
#
#             date = enToPersianNumb(gregorian_date_to_persian_date(query["publisher_website_updated_at"]))
#             record.append('<span dir="ltr">' + date + '</span>')
#
#             action = '<div class="btn-group "><a href = "' + url_for(configs['url_edit'], id=query[
#                 "publisher_website_id"]) + '" class ="btn btn-white btn-demo-space" >ویرایش</a>'
#             action += '<a class="btn btn-white dropdown-toggle btn-demo-space" data-toggle="dropdown" href=""><span class="caret"></span></a>'
#
#             action += '<ul class="dropdown-menu row_actions dropdown-menu-right clearfix"><li><a href="' + url_for(
#                 'publisher_dashboard_statistics', website_id=query["publisher_website_id"]) + '">نمایش آمار</a></li>'
#             if not query["publisher_website_active_by_admin"]:
#                 action += '<li><a href="' + url_for('website_activate',
#                                                     website_id=query["publisher_website_id"]) + '">فعال سازی</a></li>'
#
#             if query["publisher_website_active_by_admin"]:
#                 action += '<li><a href="' + url_for('website_deactivate', website_id=query[
#                     "publisher_website_id"]) + '">غیر فعال کردن</a></li>'
#
#             action += '<li><button class="btn btn-default btn-md btn-danger btn-block" value="' + str(
#                 query["publisher_website_id"]) + '" name="action" type="submit">حذف</button></li>'
#             action += '</ul></div>'
#             record.append(action)
#
#             data['data'].append(record)
#
#         return Response(json.dumps(data, sort_keys=True),
#                         mimetype='application/json')
#
#     if request.method == 'POST':
#         website_deactivate_function(request.form['action'])
#         data = {
#             'publisher_website_updated_user_id': current_user.get_id(),
#             'publisher_website_is_deleted': True
#         }
#         result = requests.put(BACKEND_SERVER_ADDRESS + "/publisher/website/" + request.form['action'],
#                               data=json.dumps(data)).content
#         result = json.loads(result)
#
#         if result["status"] == "ok":
#             message = {"type": "alert-success", "message": "رکورد با موفقیت حذف شد."}
#         elif result["status"] == "nok":
#             message = {"type": "alert-error", "message": "خطایی رخ داده است."}
#
#     if session.get('message', None) is not None:
#         message = json.loads(session.pop("message"))
#
#     return render_template('admin/website/index.html', message=message, configs=configs)


@app.route('/dashboard/admin/website', methods=['GET', 'POST'])
@login_required
@roles_accepted('admin')
def publisher_website_admin():
    configs = {
        'url_edit': 'publisher_website_admin_edit',
        'url_index': 'publisher_website_admin',
        'module': 'مدیریت وب سایت ها',
        'action': 'مدیریت وب سایت ها',
        'id_name': 'publisher_website_id',
        'page_title': 'سایت ها - مدیریت وب سایت ها'
    }
    message = None
    if request.method == 'POST':
        website_deactivate_function(request.form['action'])
        data = {
            'publisher_website_updated_user_id': current_user.get_id(),
            'publisher_website_is_deleted': True
        }
        result = requests.put(BACKEND_SERVER_ADDRESS + "/publisher/website/" + request.form['action'],
                              data=json.dumps(data)).content
        result = json.loads(result)

        if result["status"] == "ok":
            message = {"type": "alert-success", "message": "رکورد با موفقیت حذف شد."}
        elif result["status"] == "nok":
            message = {"type": "alert-error", "message": "خطایی رخ داده است."}

    result = requests.get(BACKEND_SERVER_ADDRESS + "/publisher/website").content
    result = json.loads(result)
    result = result['body']

    ids = []
    for query in result:
        ids.append(query["publisher_website_author_user_id"])

    authors = users(ids)
    authors = json.loads(authors)
    authors = authors['body']

    if session.get('message', None) is not None:
        message = json.loads(session.pop("message"))

    return render_template('admin/website/index.html', result=result, authors=authors, message=message, configs=configs)


@app.route('/dashboard/admin/website/<id>/edit', methods=['GET', 'POST'])
@login_required
@roles_accepted('admin')
def publisher_website_admin_edit(id):
    configs = {
        'module': 'لیست وب سایت ها',
        'action': 'ویرایش وب سایت',
        'url': 'publisher_website_admin_edit',
        'url_index': 'publisher_website_admin',
        'id': id,
        'page_title': 'ویرایش وب سایت'
    }
    form = PublisherWebsiteAdminForm()
    if request.method == 'POST':
        website_deactivate_function(id)
        data = {
            'publisher_website_updated_user_id': current_user.get_id(),
            'publisher_website_title': form.title.data,
            'publisher_website_type': form.type.data,
            'publisher_website_url': form.url.data,
            'publisher_website_grade': form.grade.data,
            'publisher_website_percentage': form.percentage.data,
            'publisher_website_subject': form.subjects.data,
            'publisher_website_native_style': form.native_style.data
        }

        result = requests.put(BACKEND_SERVER_ADDRESS + "/publisher/website/" + str(id),
                              data=json.dumps(data)).content
        result = json.loads(result)

        if result["status"] == "ok":
            message = json.dumps({"type": "alert-success", "message": "وب سایت با موفقیت ویرایش شد."})
        elif result["status"] == "nok":
            message = json.dumps({"type": "alert-error", "message": "خطایی رخ داده است."})
        session['message'] = message

        return redirect(url_for('publisher_website_admin_edit', id=id))

    elif request.method == 'GET':
        result = requests.get(BACKEND_SERVER_ADDRESS + "/publisher/website/" + str(id)).content
        result = json.loads(result)
        result = result['body']

        form.url.data = result["publisher_website_url"]
        form.grade.data = result["publisher_website_grade"]
        form.percentage.data = result["publisher_website_percentage"]
        form.title.data = result["publisher_website_title"]
        form.type.data = result["publisher_website_type"]
        form.native_style.data = result["publisher_website_native_style"]

        result = requests.get(BACKEND_SERVER_ADDRESS + "/admin/target/subject").content
        result = json.loads(result)
        result = result['body']
        records = [(record["subject_id"], record["subject_title"]) for record in result]
        form.subjects.choices = records

        subjects = []
        records = requests.get(
            BACKEND_SERVER_ADDRESS + "/publisher/website/subject?website=" + str(id)).content
        records = json.loads(records)
        records = records['body']
        for record in records:
            subjects.append(record["subject"]["subject_id"])
        form.subjects.data = subjects

        message = None
        if session.get('message', None) is not None:
            message = json.loads(session.pop("message"))

        return render_template('general/edit.html', form=form, message=message, configs=configs)


@app.route("/dashboard/admin/website/<website_id>/activate", methods=["GET"])
@login_required
@roles_accepted('admin')
def website_activate(website_id):
    result = requests.get(BACKEND_SERVER_ADDRESS + "/publisher/website/" + str(website_id)).content
    result = json.loads(result)
    result = result['body']

    if not result["publisher_website_grade"]:
        return redirect(url_for('publisher_website_admin'))

    website_url = urlparse(result['publisher_website_url']).hostname.replace("www.", "")

    if result['publisher_website_grade']:
        r.sadd('publisher_website_grade_' + website_url, result['publisher_website_grade'])

    records = requests.get(BACKEND_SERVER_ADDRESS + "/publisher/website/subject?website=" + str(website_id)).content
    records = json.loads(records)
    records = records['body']
    for record in records:
        r.sadd('publisher_website_subject_' + website_url, record["subject"]["subject_id"])

    if result['publisher_website_type'] == 'banner':
        r.sadd('publishers_website_banner', website_url)
    elif result['publisher_website_type'] == 'search_engine':
        r.sadd('publishers_website_search_engine', website_url)
    elif result['publisher_website_type'] == 'both':
        r.sadd('publishers_website_banner', website_url)
        r.sadd('publishers_website_search_engine', website_url)

    r.sadd('publishers_website_' + website_url, website_id)

    r.sadd('publishers_website_' + str(website_id), website_url)

    r.sadd('publisher_id_website_' + website_url, result['publisher_website_author_user_id'])

    r.sadd('publisher_website_percentage_' + website_url, result['publisher_website_percentage'])

    r.sadd('publisher_website_native_style_' + website_url, result['publisher_website_native_style'])

    records = requests.get(
        BACKEND_SERVER_ADDRESS + "/advertiser/blocked/website/user/" + str(
            result['publisher_website_author_user_id'])).content
    records = json.loads(records)
    records = records['body']
    for record in records:
        campaigns = requests.get(
            BACKEND_SERVER_ADDRESS + "/advertiser/campaign/landing_page?url=" + urlparse(
                record["blocked_website_url"]).hostname.replace("www.", "")).content
        campaigns = json.loads(campaigns)
        campaigns = campaigns['body']

        for campaign in campaigns:
            r.sadd('website_blocked_campaigns_' + website_url,
                   campaign)

            # r.sadd('publisher_blocked_website_' + urlparse(record["blocked_website_url"]).hostname.replace("www.", ""),
            #        website_id)

    if result['publisher_website_type'] == 'search_engine' or result['publisher_website_type'] == 'both':
        user = user_datastore.get_user(result["publisher_website_author_user_id"])
        r.sadd('publisher_username_' + website_url, user.email)
        r.sadd('publisher_password_' + website_url, "111111")

    data = {
        'publisher_website_updated_user_id': current_user.get_id(),
        'publisher_website_active_by_admin': True
    }
    result = requests.put(BACKEND_SERVER_ADDRESS + "/publisher/website/" + str(website_id),
                          data=json.dumps(data)).content
    result = json.loads(result)

    if result["status"] == "ok":
        message = json.dumps({"type": "alert-success", "message": "وب سایت با موفقیت فعال شد."})
    elif result["status"] == "nok":
        message = json.dumps({"type": "alert-error", "message": "خطایی رخ داده است."})
    session['message'] = message

    return redirect(url_for('publisher_website_admin'))


@app.route("/dashboard/admin/website/<website_id>/deactivate", methods=["GET"])
@login_required
@roles_accepted('admin')
def website_deactivate(website_id):
    website_deactivate_function(website_id)
    return redirect(url_for('publisher_website_admin'))


@app.route('/dashboard/admin/campaign/<id>/edit', methods=['GET', 'POST'])
@login_required
@roles_accepted('admin')
def campaign_admin_edit(id):
    configs = {
        'module': 'لیست کمپین ها',
        'action': 'ویرایش کمپین',
        'url': 'campaign_admin_edit',
        'url_index': 'campaign_admin',
        'id': id,
        'from_id': "admin-campaign-edit-form",
        'page_title': 'ویرایش کمپین'
    }
    form = CampaignForm()
    if request.method == 'POST':
        campaign_deactivate_function(id)
        data = {
            'campaign_updated_user_id': current_user.get_id(),
            'campaign_name': form.name.data,
            # 'campaign_total_budget': form.total_budget.data.replace(",", ""),
            'campaign_daily_budget': form.daily_budget.data.replace(",", ""),
            'campaign_click_price': form.click_price.data.replace(",", ""),
            'campaign_budget_management': form.budget_management.data,
            'campaign_landing_page_url': form.landing_page_url.data,
            'campaign_coef': form.coef.data
        }
        result = requests.put(BACKEND_SERVER_ADDRESS + "/advertiser/campaign/" + str(id),
                              data=json.dumps(data)).content
        result = json.loads(result)
        if result["status"] == "ok":
            message = {"type": "alert-success", "message": "کمپین با موفقیت ویرایش شد."}
        elif result["status"] == "nok":
            message = {"type": "alert-error", "message": "خطایی رخ داده است."}

        return render_template('admin/campaign/edit.html', form=form, message=message, configs=configs)
    elif request.method == 'GET':
        result = requests.get(BACKEND_SERVER_ADDRESS + "/advertiser/campaign/" + str(id)).content
        result = json.loads(result)
        result = result['body']
        form.name.data = result["campaign_name"]
        # form.total_budget.data = result["campaign_total_budget"]
        form.daily_budget.data = result["campaign_daily_budget"]
        form.click_price.data = result["campaign_click_price"]
        form.budget_management.data = result["campaign_budget_management"]
        form.landing_page_url.data = result["campaign_landing_page_url"]
        form.coef.data = result["campaign_coef"]
        return render_template('admin/campaign/edit.html', form=form, configs=configs)


@app.route('/dashboard/admin/campaign', methods=['GET', 'POST'])
@login_required
@roles_accepted('admin')
def campaign_admin():
    configs = {
        'url_edit': 'advertiser_campaign_edit',
        'url_index': 'campaign_admin',
        'module': 'مدیریت کمپین ها',
        'action': 'مدیریت کمپین ها',
        'id_name': 'campaign_id',
        'page_title': 'کمپین ها - مدیریت کمپین ها'
    }
    message = None
    if request.method == 'POST':
        campaign = requests.get(BACKEND_SERVER_ADDRESS + "/advertiser/campaign/" + str(request.form['action'])).content
        campaign = json.loads(campaign)
        campaign = campaign['body']

        if campaign['campaign_active_by_user']:
            total_budget = 0
            if campaign['campaign_active_by_admin']:
                redis_total_budget = r.smembers('campaign_total_budget_' + str(campaign['campaign_id']))
                if len(list(redis_total_budget)) > 0:
                    total_budget = int(float(list(redis_total_budget)[0]))
                campaign_deactivate_function(request.form['action'])
            else:
                total_budget = int(campaign['campaign_total_budget'])

            data = {
                'transaction_author_user_id': campaign['campaign_author_user_id'],
                'transaction_updated_user_id': current_user.get_id(),
                'transaction_deposit_amount': total_budget,
                'transaction_withdrawal_amount': 0,
                'transaction_description': 'بازگشت بودجه کمپین' + " " + campaign["campaign_name"],
                'transaction_status': 1
            }
            result = requests.post(BACKEND_SERVER_ADDRESS + "/financial/transaction",
                                   data=json.dumps(data)).content
            result = json.loads(result)

        data = {
            'campaign_updated_user_id': current_user.get_id(),
            'campaign_is_deleted': True,
            'campaign_active_by_user': False
        }
        result = requests.put(BACKEND_SERVER_ADDRESS + "/advertiser/campaign/" + request.form['action'],
                              data=json.dumps(data)).content
        result = json.loads(result)

        if result["status"] == "ok":
            message = {"type": "alert-success", "message": "رکورد با موفقیت حذف شد."}
        elif result["status"] == "nok":
            message = {"type": "alert-error", "message": "خطایی رخ داده است."}

    result = requests.get(BACKEND_SERVER_ADDRESS + "/advertiser/campaign").content
    result = json.loads(result)
    result = result['body']

    ids = []
    for query in result:
        ids.append(query["campaign_author_user_id"])

    authors = users(ids)
    authors = json.loads(authors)
    authors = authors['body']

    if session.get('message', None) is not None:
        message = json.loads(session.pop("message"))

    return render_template('admin/campaign/index.html', result=result, authors=authors, message=message,
                           configs=configs)


@app.route("/dashboard/admin/campaign/<campaign_id>/default/activate", methods=["GET"])
@login_required
@roles_accepted('admin')
def campaign_default_activate(campaign_id):
    campaign = requests.get(BACKEND_SERVER_ADDRESS + "/advertiser/campaign/" + str(campaign_id)).content
    campaign = json.loads(campaign)
    campaign = campaign['body']

    if not campaign['campaign_active_by_user']:
        message = json.dumps({"type": "", "message": "کمپین توسط آگهی دهنده فعال نشده است."})
        session['message'] = message
        return redirect(url_for('campaign_admin'))

    if campaign['campaign_default']:
        message = json.dumps({"type": "", "message": "کمپین قبلا به عنوان پیش فرض مشخص شده است."})
        session['message'] = message
        return redirect(url_for('campaign_admin'))

    if campaign['campaign_type']['campaign_type_name'] == 'banner' or campaign['campaign_type'][
        'campaign_type_name'] == 'mobile':

        if campaign['campaign_type']['campaign_type_name'] == 'banner':
            result = requests.get(BACKEND_SERVER_ADDRESS + "/admin/banner/size?type=desktop").content
        else:
            result = requests.get(BACKEND_SERVER_ADDRESS + "/admin/banner/size?type=mobile").content

        result = json.loads(result)
        banner_sizes = result['body']

        result = requests.get(
            BACKEND_SERVER_ADDRESS + "/advertiser/campaign/banner?campaign=" + str(campaign_id)).content
        result = json.loads(result)
        campaign_banners = result['body']

        if len(banner_sizes) == len(campaign_banners):
            r.sadd('campaign_adsense_default', campaign_id)
            data = {
                'campaign_updated_user_id': current_user.get_id(),
                'campaign_default': True
            }
            result = requests.put(BACKEND_SERVER_ADDRESS + "/advertiser/campaign/" + str(campaign_id),
                                  data=json.dumps(data)).content
            result = json.loads(result)

            if result["status"] == "ok":
                message = json.dumps({"type": "alert-success", "message": "کمپین با موفقیت پیش فرض شد."})
            elif result["status"] == "nok":
                message = json.dumps({"type": "alert-error", "message": "خطایی رخ داده است."})
            session['message'] = message
        else:
            message = json.dumps({"type": "", "message": "کمپین برای حالت پیش فرض باید کل سایزهای بنر را داشته باشد."})
            session['message'] = message

    if campaign['campaign_type']['campaign_type_name'] == 'search_engine':
        r.sadd('campaign_adwords_default', campaign_id)
        data = {
            'campaign_updated_user_id': current_user.get_id(),
            'campaign_default': True
        }
        result = requests.put(BACKEND_SERVER_ADDRESS + "/advertiser/campaign/" + str(campaign_id),
                              data=json.dumps(data)).content
        result = json.loads(result)

        if result["status"] == "ok":
            message = json.dumps({"type": "alert-success", "message": "کمپین با موفقیت پیش فرض شد."})
        elif result["status"] == "nok":
            message = json.dumps({"type": "alert-error", "message": "خطایی رخ داده است."})
        session['message'] = message

    return redirect(url_for('campaign_admin'))


@app.route("/dashboard/admin/campaign/<campaign_id>/default/deactivate", methods=["GET"])
@login_required
@roles_accepted('admin')
def campaign_default_deactivate(campaign_id):
    r.srem('campaign_adwords_default', campaign_id)
    r.srem('campaign_adsense_default', campaign_id)
    data = {
        'campaign_updated_user_id': current_user.get_id(),
        'campaign_default': False
    }
    result = requests.put(BACKEND_SERVER_ADDRESS + "/advertiser/campaign/" + str(campaign_id),
                          data=json.dumps(data)).content
    result = json.loads(result)

    if result["status"] == "ok":
        message = json.dumps({"type": "alert-success", "message": "کمپین با موفقیت از حالت پیش فرض خارج شد."})
    elif result["status"] == "nok":
        message = json.dumps({"type": "alert-error", "message": "خطایی رخ داده است."})
    session['message'] = message

    return redirect(url_for('campaign_admin'))


@app.route("/dashboard/admin/campaign/<campaign_id>/deactivate", methods=["GET"])
@login_required
@roles_accepted('admin')
def campaign_deactivate(campaign_id):
    campaign_deactivate_function(campaign_id)
    return redirect(url_for('campaign_admin'))


@app.route("/dashboard/advertiser/campaign/<campaign_id>/deactivate", methods=["GET"])
@login_required
@roles_accepted('advertiser')
def campaign_deactivate_advertiser(campaign_id):
    campaign_deactivate_function(campaign_id)
    return redirect(url_for('advertiser_campaign'))


@app.route("/dashboard/admin/campaign/<campaign_id>/activate", methods=["GET"])
@login_required
@roles_accepted('admin')
def campaign_activate(campaign_id):
    result = requests.get(BACKEND_SERVER_ADDRESS + "/advertiser/campaign/" + str(campaign_id)).content
    result = json.loads(result)
    result = result['body']

    if not result['campaign_active_by_user']:
        message = json.dumps({"type": "", "message": "کمپین توسط آگهی دهنده فعال نشده است."})
        session['message'] = message
        return redirect(url_for('campaign_admin'))

    if result['campaign_active_by_admin']:
        message = json.dumps({"type": "", "message": "کمپین قبلا فعال شده است."})
        session['message'] = message
        return redirect(url_for('campaign_admin'))

    if result['campaign_targeted_geography_all']:
        r.sadd('campaign_targeted_geography_not_iran', result['campaign_id'])
        r.sadd('campaign_targeted_geography_all', result['campaign_id'])

    if result['campaign_targeted_geography_iran'] or result['campaign_targeted_geography_all']:
        records = requests.get(BACKEND_SERVER_ADDRESS + "/admin/target/geography").content
        records = json.loads(records)
        records = records['body']
        for record in records:
            r.sadd('campaign_targeted_geography_' + record['geography_name'], result['campaign_id'])

    if result['campaign_targeted_geography_not_iran']:
        r.sadd('campaign_targeted_geography_not_iran', result['campaign_id'])

    if result['campaign_targeted_geography_special']:
        records = requests.get(
            BACKEND_SERVER_ADDRESS + "/advertiser/campaign/geography?campaign=" + str(result['campaign_id'])).content
        records = json.loads(records)
        records = records['body']
        for record in records:
            r.sadd('campaign_targeted_geography_' + record["geography"]["geography_name"], result['campaign_id'])

    if result['campaign_targeted_operating_system_all']:
        records = requests.get(BACKEND_SERVER_ADDRESS + "/admin/target/os").content
        records = json.loads(records)
        records = records['body']
        for record in records:
            r.sadd('campaign_targeted_operating_system_' + record['os_name'], result['campaign_id'])

    if result['campaign_targeted_operating_system_special']:
        records = requests.get(
            BACKEND_SERVER_ADDRESS + "/advertiser/campaign/os?campaign=" + str(result['campaign_id'])).content
        records = json.loads(records)
        records = records['body']
        for record in records:
            r.sadd('campaign_targeted_operating_system_' + record["os"]["os_name"], result['campaign_id'])

    if result['campaign_targeted_subject_all']:
        records = requests.get(BACKEND_SERVER_ADDRESS + "/admin/target/subject").content
        records = json.loads(records)
        records = records['body']
        for record in records:
            r.sadd('campaign_targeted_subject_' + str(record['subject_id']), result['campaign_id'])

    if result['campaign_targeted_subject_special']:
        records = requests.get(
            BACKEND_SERVER_ADDRESS + "/advertiser/campaign/subject?campaign=" + str(result['campaign_id'])).content
        records = json.loads(records)
        records = records['body']
        for record in records:
            r.sadd('campaign_targeted_subject_' + str(record["subject"]["subject_id"]), result['campaign_id'])

    if result['campaign_playtime_special']:
        r.sadd('campaign_playtime_00_08', result['campaign_id'])
        r.sadd('campaign_playtime_08_16', result['campaign_id'])
        r.sadd('campaign_playtime_16_24', result['campaign_id'])

        if result['campaign_playtime_not_24_08']:
            r.srem('campaign_playtime_00_08', result['campaign_id'])

        if result['campaign_playtime_not_08_16']:
            r.srem('campaign_playtime_08_16', result['campaign_id'])

        if result['campaign_playtime_not_16_24']:
            r.srem('campaign_playtime_16_24', result['campaign_id'])

    if result['campaign_playtime_all']:
        r.sadd('campaign_playtime_00_08', result['campaign_id'])
        r.sadd('campaign_playtime_08_16', result['campaign_id'])
        r.sadd('campaign_playtime_16_24', result['campaign_id'])

    if result['campaign_network_class_a']:
        r.sadd('campaign_network_class_a', result['campaign_id'])

    if result['campaign_network_class_b']:
        r.sadd('campaign_network_class_b', result['campaign_id'])

    if result['campaign_network_class_c']:
        r.sadd('campaign_network_class_c', result['campaign_id'])

    if result['campaign_retargeting']:
        r.sadd('campaign_retargeting', result['campaign_id'])

    if result['campaign_targeted_keyword_special']:
        records = requests.get(
            BACKEND_SERVER_ADDRESS + "/advertiser/campaign/keyword?campaign=" + str(result['campaign_id'])).content
        records = json.loads(records)
        records = records['body']
        for record in records:
            strTitle = record["keyword"]["keyword_title"]
            strTitle = strTitle.replace(" ", "-")
            r.sadd('campaign_targeted_keyword_' + strTitle, result['campaign_id'])
            r.sadd('campaign_targeted_keywords_' + str(result['campaign_id']), strTitle)

    if result['campaign_type']['campaign_type_name'] == 'banner' or result['campaign_type'][
        'campaign_type_name'] == 'mobile' or result['campaign_type']['campaign_type_name'] == 'native':
        records = requests.get(
            BACKEND_SERVER_ADDRESS + "/advertiser/campaign/" + str(result['campaign_id']) + "/banners").content
        records = json.loads(records)
        records = records['body']
        for record in records:
            r.sadd(
                'campaign_banner_size_' + str(record["banner_size"]["banner_size_width"]) + 'x' + str(
                    record["banner_size"][
                        "banner_size_height"]),
                result['campaign_id'])
            r.sadd(
                'campaign_' + str(result['campaign_id']) + '_banner_' + str(
                    record["banner_size"]["banner_size_width"]) + 'x' + str(record["banner_size"][
                                                                                "banner_size_height"]),
                record["banner_file"]["file_path"] + '/' + record["banner_file"]["file_name"])

        r.sadd('campaign_type_' + str(result['campaign_id']), 'banner')

    if result['campaign_type']['campaign_type_name'] == 'iframe':
        records = requests.get(
            BACKEND_SERVER_ADDRESS + "/advertiser/campaign/" + str(result['campaign_id']) + "/banners").content
        records = json.loads(records)
        records = records['body']
        for record in records:
            r.sadd(
                'campaign_banner_size_' + str(record["banner_size"]["banner_size_width"]) + 'x' + str(
                    record["banner_size"][
                        "banner_size_height"]),
                result['campaign_id'])
            r.sadd(
                'campaign_' + str(result['campaign_id']) + '_html_' + str(
                    record["banner_size"]["banner_size_width"]) + 'x' + str(record["banner_size"][
                                                                                "banner_size_height"]),
                record["banner_description"])

        r.sadd('campaign_type_' + str(result['campaign_id']), 'html')

    if result['campaign_type']['campaign_type_name'] == 'native':
        r.sadd('campaign_' + str(result['campaign_id']) + '_native_title', result['campaign_native_title'])
        r.sadd('campaign_content_list', result['campaign_id'])

    if result['campaign_type']['campaign_type_name'] == 'search_engine':
        r.sadd('campaign_' + str(result['campaign_id']) + '_title', result['campaign_adwords_title'])
        r.sadd('campaign_' + str(result['campaign_id']) + '_description', result['campaign_adwords_description'])
        r.sadd('campaign_' + str(result['campaign_id']) + '_email', result['campaign_adwords_email'])
        r.sadd('campaign_' + str(result['campaign_id']) + '_phone', result['campaign_adwords_phone'])
        r.sadd('campaign_' + str(result['campaign_id']) + '_address', result['campaign_adwords_address'])
        r.sadd('campaign_adwords_list', result['campaign_id'])

    records = requests.get(
        BACKEND_SERVER_ADDRESS + "/advertiser/blocked/website/user/" + str(result['campaign_author_user_id'])).content
    records = json.loads(records)
    records = records['body']

    for record in records:
        r.sadd('campaigns_blocked_website_' + urlparse(record["blocked_website_url"]).hostname.replace("www.", ""),
               result['campaign_id'])

    r.sadd('campaign_total_budget_' + str(result['campaign_id']), result['campaign_total_budget'])
    r.sadd('campaign_daily_budget_' + str(result['campaign_id']), result['campaign_daily_budget'])
    r.sadd('campaign_budget_management_' + str(result['campaign_id']), result['campaign_budget_management'])
    r.sadd('campaign_click_price_' + str(result['campaign_id']), result['campaign_click_price'])
    r.sadd('campaign_coef_' + str(result['campaign_id']), result['campaign_coef'])

    if result['campaign_landing_page_url']:
        r.sadd(
            'campaign_landing_page_campaign_' + urlparse(result['campaign_landing_page_url']).hostname.replace("www.",
                                                                                                               ""),
            result['campaign_id'])

    r.sadd('campaign_landing_page_url_' + str(result['campaign_id']), result['campaign_landing_page_url'])

    date = datetime.now()
    r.sadd('campaign_activate_date_' + str(result['campaign_id']), date.strftime("%Y-%m-%d%H:%M:%S"))

    r.srem('campaign_deactivate', result['campaign_id'])

    data = {
        'campaign_updated_user_id': current_user.get_id(),
        'campaign_active_by_admin': True
    }
    result = requests.put(BACKEND_SERVER_ADDRESS + "/advertiser/campaign/" + str(result['campaign_id']),
                          data=json.dumps(data)).content
    result = json.loads(result)

    if result["status"] == "ok":
        message = json.dumps({"type": "alert-success", "message": "کمپین با موفقیت فعال شد."})
    elif result["status"] == "nok":
        message = json.dumps({"type": "alert-error", "message": "خطایی رخ داده است."})
    session['message'] = message

    # print(r.smembers('a'))

    # r.set('campaign_total_budget', result['campaign_total_budget'])
    # r.set('campaign_daily_budget', result['campaign_daily_budget'])
    return redirect(url_for('campaign_admin'))


def allowed_file(filename, extensions):
    filename = filename.lower()
    return '.' in filename and filename.rsplit('.', 1)[1] in extensions


def get_image_size(fname):
    with open(fname, 'rb') as fhandle:
        head = fhandle.read(24)
        if len(head) != 24:
            return
        if imghdr.what(fname) == 'png':
            check = struct.unpack('>i', head[4:8])[0]
            if check != 0x0d0a1a0a:
                return
            width, height = struct.unpack('>ii', head[16:24])
        elif imghdr.what(fname) == 'gif':
            width, height = struct.unpack('<HH', head[6:10])
        elif imghdr.what(fname) == 'jpeg':
            try:
                fhandle.seek(0)  # Read 0xff next
                size = 2
                ftype = 0
                while not 0xc0 <= ftype <= 0xcf:
                    fhandle.seek(size, 1)
                    byte = fhandle.read(1)
                    while ord(byte) == 0xff:
                        byte = fhandle.read(1)
                    ftype = ord(byte)
                    size = struct.unpack('>H', fhandle.read(2))[0] - 2
                # We are at a SOFn block
                fhandle.seek(1, 1)  # Skip `precision' byte.
                height, width = struct.unpack('>HH', fhandle.read(4))
            except Exception:  # IGNORE:W0703
                return
        else:
            return
        return width, height


@app.route("/dashboard/upload/banner", methods=["POST"])
@login_required
def upload_banner():
    """Handle the upload of a file."""
    form = request.form

    # Create a unique "session ID" for this particular batch of uploads.
    upload_key = str(uuid4())

    # Is the upload using Ajax, or a direct POST by the form?
    is_ajax = False
    if form.get("__ajax", None) == "true":
        is_ajax = True

    # Target folder for these uploads.
    target = UPLOADS_FOLDER + "/{}".format(upload_key)
    try:
        os.mkdir(target)
    except:
        if is_ajax:
            return ajax_response(False,
                                 "Couldn't create upload directory: {}".format(
                                     target))
        else:
            return "Couldn't create upload directory: {}".format(target)

    files = []
    for upload in request.files.getlist("file"):
        filename = upload.filename.rsplit("/")[0]
        if allowed_file(filename, ALLOWED_EXTENSIONS_BANNER):
            destination = "/".join([target, filename])
            upload.save(destination)
            dimension = get_image_size(destination)
            file_size = os.stat(destination).st_size
            if file_size <= ALLOWED_FILESIZE_BANNER:
                result = requests.get(
                    BACKEND_SERVER_ADDRESS + "/admin/banner/size/query?width=" + str(dimension[0]) + "&height=" + str(
                        dimension[1])).content
                result = json.loads(result)

                if result['status'] == "ok":
                    banner_size = result['body']
                    data = {
                        'file_author_user_id': current_user.get_id(),
                        'file_name': filename,
                        'file_path': upload_key
                    }
                    result = requests.post(BACKEND_SERVER_ADDRESS + "/uploads/library", data=json.dumps(data)).content
                    result = json.loads(result)
                    file_id = result['body']

                    data = {
                        'banner_author_user_id': current_user.get_id(),
                        'banner_size': banner_size["banner_size_id"],
                        'banner_file': file_id
                    }
                    result = requests.post(BACKEND_SERVER_ADDRESS + "/advertiser/banner", data=json.dumps(data)).content
                    result = json.loads(result)
                    banner_id = result['body']

                    files.append({'folder_name': upload_key, 'file_name': filename,
                                  'file_id': banner_id, 'file_width': str(dimension[0]),
                                  'file_height': str(dimension[1]), 'upload_status': 'ok',
                                  'status_message': 'The file was successfully uploaded'})
                else:
                    try:
                        os.remove(destination)
                    except OSError as e:
                        print("Error: %s - %s." % (e.filename, e.strerror))
                    if is_ajax:
                        files.append({'file_name': filename,
                                      'file_width': str(dimension[0]),
                                      'file_height': str(dimension[1]),
                                      'upload_status': 'nok',
                                      'status_message': 'Not allowed standard banner size'})

            else:
                try:
                    os.remove(destination)
                except OSError as e:
                    print("Error: %s - %s." % (e.filename, e.strerror))
                if is_ajax:
                    files.append({'file_name': filename,
                                  'file_width': str(dimension[0]),
                                  'file_height': str(dimension[1]),
                                  'upload_status': 'nok',
                                  'status_message': 'Not allowed standard file size (file size > {}KB)'.format(
                                      str(ALLOWED_FILESIZE_BANNER / 1024))})

        else:
            if is_ajax:
                files.append({'file_name': filename,
                              'upload_status': 'nok',
                              'status_message': 'Not allowed file extension'})

    if is_ajax:
        try:
            os.rmdir(target)
        except OSError as e:
            print("Error: %s - %s." % (e.filename, e.strerror))

        result = {}
        result['status'] = 'OK'
        result['files'] = files
        return json.dumps(result)


def ajax_response(status, msg):
    status_code = "ok" if status else "error"
    return json.dumps(dict(
        status=status_code,
        msg=msg,
    ))


@app.route("/dashboard/upload/attachment", methods=["POST"])
@login_required
def upload_attachment():
    """Handle the upload of a file."""
    form = request.form

    # Create a unique "session ID" for this particular batch of uploads.
    upload_key = str(uuid4())

    # Is the upload using Ajax, or a direct POST by the form?
    is_ajax = False
    if form.get("__ajax", None) == "true":
        is_ajax = True

    # Target folder for these uploads.
    target = UPLOADS_FOLDER + "/{}".format(upload_key)
    try:
        os.mkdir(target)
    except:
        if is_ajax:
            return ajax_response(False,
                                 "Couldn't create upload directory: {}".format(
                                     target))
        else:
            return "Couldn't create upload directory: {}".format(target)

    files = []
    for upload in request.files.getlist("file"):
        filename = upload.filename.rsplit("/")[0]
        if allowed_file(filename, ALLOWED_EXTENSIONS_ATTACHMENT):
            destination = "/".join([target, filename])
            upload.save(destination)

            file_size = os.stat(destination).st_size
            if file_size <= ALLOWED_FILESIZE_ATTACHMENT:
                data = {
                    'file_author_user_id': current_user.get_id(),
                    'file_name': filename,
                    'file_path': upload_key
                }
                result = requests.post(BACKEND_SERVER_ADDRESS + "/uploads/library", data=json.dumps(data)).content
                result = json.loads(result)
                file_id = result['body']

                data = {
                    'attachment_author_user_id': current_user.get_id(),
                    'attachment_file': file_id
                }
                result = requests.post(BACKEND_SERVER_ADDRESS + "/ticketing/ticket/attachment",
                                       data=json.dumps(data)).content
                result = json.loads(result)
                attachment_id = result['body']

                files.append({'folder_name': upload_key, 'file_name': filename,
                              'file_id': attachment_id})
            else:
                try:
                    os.remove(destination)
                except OSError as e:
                    print("Error: %s - %s." % (e.filename, e.strerror))
                if is_ajax:
                    return ajax_response(False, "Not allowed standard file size: {}".format(filename))
                else:
                    return "Not allowed standard file size: {}".format(filename)

        else:
            try:
                os.rmdir(target)
            except OSError as e:
                print("Error: %s - %s." % (e.filename, e.strerror))
            if is_ajax:
                return ajax_response(False, "Not allowed file extension: {}".format(filename))
            else:
                return "Not allowed file extension: {}".format(filename)
    if is_ajax:
        result = {}
        result['status'] = 'OK'
        result['files'] = files
        return json.dumps(result)
    else:
        return redirect(url_for("upload_complete", uuid=upload_key))


@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.has_role('superadmin'):
        return redirect(url_for('user'))

    if current_user.has_role('admin'):
        return redirect(url_for('admin_dashboard'))

    if current_user.has_role('advertiser'):
        return redirect(url_for('advertiser_dashboard'))

    if current_user.has_role('publisher'):
        return redirect(url_for('publisher_dashboard'))

    return render_template("index.html", title="title")


@app.route('/dashboard/admin/target/os', methods=['GET', 'POST'])
@login_required
@roles_accepted('admin')
def operating_system():
    configs = {
        'url_new': 'operating_system_new',
        'url_edit': 'operating_system_edit',
        'url_index': 'operating_system',
        'module': 'لیست سیستم عامل ها',
        'action': 'لیست سیستم عامل ها',
        'url_new_text': 'سیستم عامل جدید',
        'id_name': 'os_id',
        'page_title': 'تنظیمات هدفمندی - سیستم عامل',
        'fields': [
            {
                'name': 'os_type',
                'title': 'نوع دستگاه',
                'order': 1,
                'hide': '',
                'width': '30%',
                'class': 'class=defaultSort'
            },
            {
                'name': 'os_name',
                'title': 'نام سیستم عامل',
                'order': 2,
                'hide': '',
                'width': '30%',
            },
            {
                'name': 'os_title',
                'title': 'عنوان سیستم عامل',
                'order': 3,
                'hide': '',
                'width': '29%'
            }]
    }
    message = None
    if request.method == 'POST':
        result = requests.delete(BACKEND_SERVER_ADDRESS + "/admin/target/os/" + request.form['action']).content
        result = json.loads(result)

        if result["status"] == "ok":
            message = {"type": "alert-success", "message": "رکورد با موفقیت حذف شد."}
        elif result["status"] == "nok":
            message = {"type": "alert-error", "message": "خطایی رخ داده است."}

    result = requests.get(BACKEND_SERVER_ADDRESS + "/admin/target/os").content
    result = json.loads(result)
    result = result['body']
    return render_template('general/index.html', result=result, message=message, configs=configs)


@app.route('/dashboard/admin/target/os/new', methods=['GET', 'POST'])
@login_required
@roles_accepted('admin')
def operating_system_new():
    configs = {
        'module': 'لیست سیستم عامل ها',
        'action': 'سیستم عامل جدید',
        'url': 'operating_system_new',
        'url_index': 'operating_system',
        'page_title': 'سیستم عامل جدید'
    }
    form = TargetedOperatingSystemForm()
    if request.method == 'POST':
        if form.validate() == False:
            flash('All fields are required.', 'danger')
            return render_template('general/new.html', form=form, configs=configs)
        else:
            data = {
                'os_author_user_id': current_user.get_id(),
                'os_name': form.name.data,
                'os_title': form.title.data,
                'os_type': form.type.data
            }
            result = requests.post(BACKEND_SERVER_ADDRESS + "/admin/target/os", data=json.dumps(data)).content
            result = json.loads(result)

            if result["status"] == "ok":
                message = json.dumps({"type": "alert-success", "message": "سیستم عامل با موفقیت ثبت شد."})
            elif result["status"] == "nok":
                message = json.dumps({"type": "alert-error", "message": "خطایی رخ داده است."})
            session['message'] = message

            return redirect(url_for('operating_system_new'))
    elif request.method == 'GET':
        message = None
        if session.get('message', None) is not None:
            message = json.loads(session.pop("message"))
        return render_template('general/new.html', form=form, message=message, configs=configs)


@app.route('/dashboard/admin/target/os/<id>/edit', methods=['GET', 'POST'])
@login_required
@roles_accepted('admin')
def operating_system_edit(id):
    configs = {
        'module': 'لیست سیستم عامل ها',
        'action': 'ویرایش سیستم عامل',
        'url': 'operating_system_edit',
        'url_index': 'operating_system',
        'id': id,
        'page_title': 'ویرایش سیستم عامل'
    }
    form = TargetedOperatingSystemForm()
    if request.method == 'POST':
        if form.validate() == False:
            flash('All fields are required.', 'danger')
            return render_template('general/edit.html', form=form, configs=configs)
        else:
            data = {
                'os_updated_user_id': current_user.get_id(),
                'os_name': form.name.data,
                'os_title': form.title.data,
                'os_type': form.type.data
            }
            result = requests.put(BACKEND_SERVER_ADDRESS + "/admin/target/os/" + str(id),
                                  data=json.dumps(data)).content
            result = json.loads(result)

            if result["status"] == "ok":
                message = {"type": "alert-success", "message": "سیستم عامل با موفقیت ویرایش شد."}
            elif result["status"] == "nok":
                message = {"type": "alert-error", "message": "خطایی رخ داده است."}

            return render_template('general/edit.html', form=form, message=message, configs=configs)
    elif request.method == 'GET':
        result = requests.get(BACKEND_SERVER_ADDRESS + "/admin/target/os/" + str(id)).content
        result = json.loads(result)
        result = result['body']
        form.name.data = result["os_name"]
        form.title.data = result["os_title"]
        form.type.data = result["os_type"]
        return render_template('general/edit.html', form=form, configs=configs)


@app.route('/dashboard/admin/advertising/type', methods=['GET', 'POST'])
@login_required
@roles_accepted('admin')
def advertising_type():
    configs = {
        'url_new': 'advertising_type_new',
        'url_edit': 'advertising_type_edit',
        'url_index': 'advertising_type',
        'module': 'لیست نوع تبلیغات',
        'action': 'لیست نوع تبلیغات',
        'url_new_text': 'نوع جدید',
        'id_name': 'type_id',
        'page_title': 'انواع تبلیغات',
        'fields': [
            {
                'name': 'type_media',
                'title': 'نوع رسانه',
                'order': 1,
                'hide': '',
                'width': '30%'
            },
            {
                'name': 'type_name',
                'title': 'نام',
                'order': 2,
                'hide': '',
                'width': '30%',
                'class': 'class=defaultSort'
            },
            {
                'name': 'type_title',
                'title': 'عنوان',
                'order': 3,
                'hide': '',
                'width': '29%'
            }]
    }
    message = None
    if request.method == 'POST':
        result = requests.delete(BACKEND_SERVER_ADDRESS + "/admin/advertising/type/" + request.form['action']).content
        result = json.loads(result)

        if result["status"] == "ok":
            message = {"type": "alert-success", "message": "رکورد با موفقیت حذف شد."}
        elif result["status"] == "nok":
            message = {"type": "alert-error", "message": "خطایی رخ داده است."}

    result = requests.get(BACKEND_SERVER_ADDRESS + "/admin/advertising/type").content
    result = json.loads(result)
    result = result['body']
    return render_template('general/index.html', result=result, message=message, configs=configs)


@app.route('/dashboard/admin/advertising/type/new', methods=['GET', 'POST'])
@login_required
@roles_accepted('admin')
def advertising_type_new():
    configs = {
        'module': 'لیست نوع تبلیغات',
        'action': 'نوع جدید',
        'url': 'advertising_type_new',
        'url_index': 'advertising_type',
        'page_title': 'نوع جدید'
    }
    form = AdvertisingTypeForm()
    if request.method == 'POST':
        if form.validate() == False:
            flash('All fields are required.', 'danger')
            return render_template('general/new.html', form=form, configs=configs)
        else:
            data = {
                'type_author_user_id': current_user.get_id(),
                'type_name': form.name.data,
                'type_title': form.title.data,
                'type_media': form.type.data
            }
            result = requests.post(BACKEND_SERVER_ADDRESS + "/admin/advertising/type", data=json.dumps(data)).content
            result = json.loads(result)

            if result["status"] == "ok":
                message = json.dumps({"type": "alert-success", "message": "موضوع با موفقیت ثبت شد."})
            elif result["status"] == "nok":
                message = json.dumps({"type": "alert-error", "message": "خطایی رخ داده است."})
            session['message'] = message

            return redirect(url_for('advertising_type_new'))
    elif request.method == 'GET':
        message = None
        if session.get('message', None) is not None:
            message = json.loads(session.pop("message"))
        return render_template('general/new.html', form=form, message=message, configs=configs)


@app.route('/dashboard/admin/advertising/type/<id>/edit', methods=['GET', 'POST'])
@login_required
@roles_accepted('admin')
def advertising_type_edit(id):
    configs = {
        'module': 'لیست نوع تبلیغات',
        'action': 'ویرایش نوع',
        'url': 'advertising_type_edit',
        'url_index': 'advertising_type',
        'id': id,
        'page_title': 'ویرایش نوع تبلیغات'
    }
    form = AdvertisingTypeForm()
    if request.method == 'POST':
        if form.validate() == False:
            flash('All fields are required.', 'danger')
            return render_template('general/edit.html', form=form, configs=configs)
        else:
            data = {
                'type_updated_user_id': current_user.get_id(),
                'type_name': form.name.data,
                'type_title': form.title.data,
                'type_media': form.type.data
            }
            result = requests.put(BACKEND_SERVER_ADDRESS + "/admin/advertising/type/" + str(id),
                                  data=json.dumps(data)).content
            result = json.loads(result)

            if result["status"] == "ok":
                message = {"type": "alert-success", "message": "موضوع با موفقیت ویرایش شد."}
            elif result["status"] == "nok":
                message = {"type": "alert-error", "message": "خطایی رخ داده است."}

            return render_template('general/edit.html', form=form, message=message, configs=configs)
    elif request.method == 'GET':
        result = requests.get(BACKEND_SERVER_ADDRESS + "/admin/advertising/type/" + str(id)).content
        result = json.loads(result)
        result = result['body']
        form.name.data = result["type_name"]
        form.title.data = result["type_title"]
        form.type.data = result["type_media"]
        return render_template('general/edit.html', form=form, configs=configs)


@app.route('/dashboard/admin/target/subject', methods=['GET', 'POST'])
@login_required
@roles_accepted('admin')
def targeted_subject():
    configs = {
        'url_new': 'targeted_subject_new',
        'url_edit': 'targeted_subject_edit',
        'url_index': 'targeted_subject',
        'module': 'لیست موضوع ها',
        'action': 'لیست موضوع ها',
        'url_new_text': 'موضوع جدید',
        'id_name': 'subject_id',
        'page_title': 'تنظیمات هدفمندی - موضوعی',
        'fields': [
            {
                'name': 'subject_type',
                'title': 'نوع رسانه',
                'order': 1,
                'hide': '',
                'width': '30%'
            },
            {
                'name': 'subject_name',
                'title': 'نام',
                'order': 2,
                'hide': '',
                'width': '30%',
                'class': 'class=defaultSort'
            },
            {
                'name': 'subject_title',
                'title': 'عنوان',
                'order': 3,
                'hide': '',
                'width': '29%'
            }]
    }
    message = None
    if request.method == 'POST':
        result = requests.delete(BACKEND_SERVER_ADDRESS + "/admin/target/subject/" + request.form['action']).content
        result = json.loads(result)

        if result["status"] == "ok":
            message = {"type": "alert-success", "message": "رکورد با موفقیت حذف شد."}
        elif result["status"] == "nok":
            message = {"type": "alert-error", "message": "خطایی رخ داده است."}

    result = requests.get(BACKEND_SERVER_ADDRESS + "/admin/target/subject").content
    result = json.loads(result)
    result = result['body']
    return render_template('general/index.html', result=result, message=message, configs=configs)


@app.route('/dashboard/admin/target/subject/new', methods=['GET', 'POST'])
@login_required
@roles_accepted('admin')
def targeted_subject_new():
    configs = {
        'module': 'لیست موضوع ها',
        'action': 'موضوع جدید',
        'url': 'targeted_subject_new',
        'url_index': 'targeted_subject',
        'page_title': 'موضوع جدید'
    }
    form = TargetedSubjectForm()
    if request.method == 'POST':
        if form.validate() == False:
            flash('All fields are required.', 'danger')
            return render_template('general/new.html', form=form, configs=configs)
        else:
            data = {
                'subject_author_user_id': current_user.get_id(),
                'subject_name': form.name.data,
                'subject_title': form.title.data,
                'subject_type': form.type.data
            }
            result = requests.post(BACKEND_SERVER_ADDRESS + "/admin/target/subject", data=json.dumps(data)).content
            result = json.loads(result)

            if result["status"] == "ok":
                message = json.dumps({"type": "alert-success", "message": "موضوع با موفقیت ثبت شد."})
            elif result["status"] == "nok":
                message = json.dumps({"type": "alert-error", "message": "خطایی رخ داده است."})
            session['message'] = message

            return redirect(url_for('targeted_subject_new'))
    elif request.method == 'GET':
        message = None
        if session.get('message', None) is not None:
            message = json.loads(session.pop("message"))
        return render_template('general/new.html', form=form, message=message, configs=configs)


@app.route('/dashboard/admin/target/subject/<id>/edit', methods=['GET', 'POST'])
@login_required
@roles_accepted('admin')
def targeted_subject_edit(id):
    configs = {
        'module': 'لیست موضوع ها',
        'action': 'ویرایش موضوع',
        'url': 'targeted_subject_edit',
        'url_index': 'targeted_subject',
        'id': id,
        'page_title': 'ویرایش موضوع'
    }
    form = TargetedSubjectForm()
    if request.method == 'POST':
        if form.validate() == False:
            flash('All fields are required.', 'danger')
            return render_template('general/edit.html', form=form, configs=configs)
        else:
            data = {
                'subject_updated_user_id': current_user.get_id(),
                'subject_name': form.name.data,
                'subject_title': form.title.data,
                'subject_type': form.type.data
            }
            result = requests.put(BACKEND_SERVER_ADDRESS + "/admin/target/subject/" + str(id),
                                  data=json.dumps(data)).content
            result = json.loads(result)

            if result["status"] == "ok":
                message = {"type": "alert-success", "message": "موضوع با موفقیت ویرایش شد."}
            elif result["status"] == "nok":
                message = {"type": "alert-error", "message": "خطایی رخ داده است."}

            return render_template('general/edit.html', form=form, message=message, configs=configs)
    elif request.method == 'GET':
        result = requests.get(BACKEND_SERVER_ADDRESS + "/admin/target/subject/" + str(id)).content
        result = json.loads(result)
        result = result['body']
        form.name.data = result["subject_name"]
        form.title.data = result["subject_title"]
        form.type.data = result["subject_type"]
        return render_template('general/edit.html', form=form, configs=configs)


@app.route('/dashboard/admin/target/geography', methods=['GET', 'POST'])
@login_required
@roles_accepted('admin')
def targeted_geography():
    configs = {
        'url_new': 'targeted_geography_new',
        'url_edit': 'targeted_geography_edit',
        'url_index': 'targeted_geography',
        'module': 'لیست مناطق',
        'action': 'لیست مناطق',
        'url_new_text': 'منطقه جدید',
        'id_name': 'geography_id',
        'page_title': 'تنظیمات هدفمندی - جغرافیایی',
        'fields': [
            {
                'name': 'geography_name',
                'title': 'نام منطقه',
                'order': 2,
                'hide': '',
                'width': '30%',
                'class': 'class=defaultSort'
            },
            {
                'name': 'geography_title',
                'title': 'عنوان منطقه',
                'order': 3,
                'hide': '',
                'width': '29%'
            }]
    }
    message = None
    if request.method == 'POST':
        result = requests.delete(BACKEND_SERVER_ADDRESS + "/admin/target/geography/" + request.form['action']).content
        result = json.loads(result)

        if result["status"] == "ok":
            message = {"type": "alert-success", "message": "رکورد با موفقیت حذف شد."}
        elif result["status"] == "nok":
            message = {"type": "alert-error", "message": "خطایی رخ داده است."}

    result = requests.get(BACKEND_SERVER_ADDRESS + "/admin/target/geography").content
    result = json.loads(result)
    result = result['body']
    return render_template('general/index.html', result=result, message=message, configs=configs)


@app.route('/dashboard/admin/target/geography/new', methods=['GET', 'POST'])
@login_required
@roles_accepted('admin')
def targeted_geography_new():
    configs = {
        'module': 'لیست مناطق',
        'action': 'منطقه جدید',
        'url': 'targeted_geography_new',
        'url_index': 'targeted_geography',
        'page_title': 'منطقه جدید'
    }
    form = TargetedGeographyForm()
    if request.method == 'POST':
        if form.validate() == False:
            flash('All fields are required.', 'danger')
            return render_template('general/new.html', form=form, configs=configs)
        else:
            data = {
                'geography_author_user_id': current_user.get_id(),
                'geography_name': form.name.data,
                'geography_title': form.title.data
            }
            result = requests.post(BACKEND_SERVER_ADDRESS + "/admin/target/geography",
                                   data=json.dumps(data)).content
            result = json.loads(result)

            if result["status"] == "ok":
                message = json.dumps({"type": "alert-success", "message": "منطقه با موفقیت ثبت شد."})
            elif result["status"] == "nok":
                message = json.dumps({"type": "alert-error", "message": "خطایی رخ داده است."})
            session['message'] = message

            return redirect(url_for('targeted_geography_new'))
    elif request.method == 'GET':
        message = None
        if session.get('message', None) is not None:
            message = json.loads(session.pop("message"))
        return render_template('general/new.html', form=form, message=message, configs=configs)


@app.route('/dashboard/admin/target/geography/<id>/edit', methods=['GET', 'POST'])
@login_required
@roles_accepted('admin')
def targeted_geography_edit(id):
    configs = {
        'module': 'لیست مناطق',
        'action': 'ویرایش منطقه',
        'url': 'targeted_geography_edit',
        'url_index': 'targeted_geography',
        'id': id,
        'page_title': 'ویرایش منطقه'
    }
    form = TargetedGeographyForm()
    if request.method == 'POST':
        if form.validate() == False:
            flash('All fields are required.', 'danger')
            return render_template('general/edit.html', form=form, configs=configs)
        else:
            data = {
                'geography_updated_user_id': current_user.get_id(),
                'geography_name': form.name.data,
                'geography_title': form.title.data
            }
            result = requests.put(BACKEND_SERVER_ADDRESS + "/admin/target/geography/" + str(id),
                                  data=json.dumps(data)).content
            result = json.loads(result)

            if result["status"] == "ok":
                message = {"type": "alert-success", "message": "منطقه با موفقیت ویرایش شد."}
            elif result["status"] == "nok":
                message = {"type": "alert-error", "message": "خطایی رخ داده است."}

            return render_template('general/edit.html', form=form, message=message, configs=configs)
    elif request.method == 'GET':
        result = requests.get(BACKEND_SERVER_ADDRESS + "/admin/target/geography/" + str(id)).content
        result = json.loads(result)
        result = result['body']
        form.name.data = result["geography_name"]
        form.title.data = result["geography_title"]
        return render_template('general/edit.html', form=form, configs=configs)


@app.route('/dashboard/admin/target/keyword', methods=['GET', 'POST'])
@login_required
@roles_accepted('admin')
def targeted_keyword():
    configs = {
        'url_new': 'targeted_keyword_new',
        'url_edit': 'targeted_keyword_edit',
        'url_index': 'targeted_keyword',
        'module': 'لیست کلمات کلیدی',
        'action': 'لیست کلمات کلیدی',
        'url_new_text': 'کلمه کلیدی جدید',
        'id_name': 'keyword_id',
        'page_title': 'تنظیمات هدفمندی - کلمات کلیدی',
        'fields': [
            {
                'name': 'keyword_title',
                'title': 'عنوان',
                'order': 2,
                'hide': '',
                'width': '29%',
                'class': 'class=defaultSort'
            }]
    }
    if request.method == 'POST':
        message = requests.delete(BACKEND_SERVER_ADDRESS + "/admin/target/keyword/" + request.form['action'])

    result = requests.get(BACKEND_SERVER_ADDRESS + "/admin/target/keyword").content
    result = json.loads(result)
    result = result['body']
    return render_template('general/index.html', result=result, configs=configs)


@app.route('/dashboard/admin/target/keyword/new', methods=['GET', 'POST'])
@login_required
@roles_accepted('admin')
def targeted_keyword_new():
    configs = {
        'module': 'لیست کلمات کلیدی',
        'action': 'کلمه کلیدی جدید',
        'url': 'targeted_keyword_new',
        'url_index': 'targeted_keyword',
        'page_title': 'کلمه کلیدی جدید'
    }
    form = TargetedKeywordForm()
    if request.method == 'POST':
        if form.validate() == False:
            flash('All fields are required.', 'danger')
            return render_template('general/new.html', form=form, configs=configs)
        else:
            data = {
                'keyword_author_user_id': current_user.get_id(),
                'keyword_title': form.title.data
            }
            result = requests.post(BACKEND_SERVER_ADDRESS + "/admin/target/keyword", data=json.dumps(data)).content
            result = json.loads(result)
            result = result['body']
            return render_template('general/new.html', form=form, result=result, configs=configs)
    elif request.method == 'GET':
        return render_template('general/new.html', form=form, configs=configs)


@app.route('/dashboard/admin/target/keyword/<id>/edit', methods=['GET', 'POST'])
@login_required
@roles_accepted('admin')
def targeted_keyword_edit(id):
    configs = {
        'module': 'لیست کلمات کلیدی',
        'action': 'ویرایش کلمه کلیدی',
        'url': 'targeted_keyword_edit',
        'url_index': 'targeted_keyword',
        'id': id,
        'page_title': 'ویرایش کلمه کلیدی'
    }
    form = TargetedKeywordForm()
    if request.method == 'POST':
        if form.validate() == False:
            flash('All fields are required.', 'danger')
            return render_template('general/edit.html', form=form, configs=configs)
        else:
            data = {
                'keyword_updated_user_id': current_user.get_id(),
                'keyword_title': form.title.data
            }
            result = requests.put(BACKEND_SERVER_ADDRESS + "/admin/target/keyword/" + str(id),
                                  data=json.dumps(data)).content
            result = json.loads(result)
            result = result['body']
            return render_template('general/edit.html', form=form, result=result, configs=configs)
    elif request.method == 'GET':
        result = requests.get(BACKEND_SERVER_ADDRESS + "/admin/target/keyword/" + str(id)).content
        result = json.loads(result)
        result = result['body']
        form.title.data = result["keyword_title"]
        return render_template('general/edit.html', form=form, configs=configs)


@app.route('/dashboard/admin/campaign/type', methods=['GET', 'POST'])
@login_required
@roles_accepted('admin')
def campaign_type():
    configs = {
        'url_new': 'campaign_type_new',
        'url_edit': 'campaign_type_edit',
        'url_index': 'campaign_type',
        'module': 'لیست انواع کمپین',
        'action': 'لیست انواع کمپین',
        'url_new_text': 'نوع کمپین جدید',
        'id_name': 'campaign_type_id',
        'page_title': 'انواع کمپین - مدیریت نوع کمپین',
        'fields': [
            {
                'name': 'campaign_type_name',
                'title': 'نام',
                'order': 2,
                'hide': '',
                'width': '30%',
                'class': 'class=defaultSort'
            },
            {
                'name': 'campaign_type_title',
                'title': 'عنوان',
                'order': 3,
                'hide': '',
                'width': '29%'
            },
            {
                'name': 'campaign_type_base_price',
                'title': 'قیمت پایه',
                'order': 4,
                'hide': '',
                'width': '29%'
            },
            {
                'name': 'campaign_type_special_for',
                'title': 'مخصوص',
                'order': 5,
                'hide': '',
                'width': '29%'
            },
            {
                'name': 'campaign_type_description',
                'title': 'توضیحات',
                'order': 6,
                'hide': 'phone,tablet',
                'width': '29%'
            }
        ]
    }
    message = None
    if request.method == 'POST':
        result = requests.delete(BACKEND_SERVER_ADDRESS + "/admin/campaign/type/" + request.form['action']).content
        result = json.loads(result)

        if result["status"] == "ok":
            message = {"type": "alert-success", "message": "رکورد با موفقیت حذف شد."}
        elif result["status"] == "nok":
            message = {"type": "alert-error", "message": "خطایی رخ داده است."}

    result = requests.get(BACKEND_SERVER_ADDRESS + "/admin/campaign/type").content
    result = json.loads(result)
    result = result['body']
    return render_template('general/index.html', result=result, message=message, configs=configs)


@app.route('/dashboard/admin/campaign/type/new', methods=['GET', 'POST'])
@login_required
@roles_accepted('admin')
def campaign_type_new():
    configs = {
        'module': 'لیست انواع کمپین',
        'action': 'نوع کمپین جدید',
        'url': 'campaign_type_new',
        'url_index': 'campaign_type',
        'page_title': 'نوع کمپین جدید'
    }
    form = CampaignTypeForm()
    if request.method == 'POST':
        if form.validate() == False:
            flash('All fields are required.', 'danger')
            return render_template('general/new.html', form=form, configs=configs)
        else:
            data = {
                'campaign_type_author_user_id': current_user.get_id(),
                'campaign_type_name': form.name.data,
                'campaign_type_title': form.title.data,
                'campaign_type_base_price': form.base_price.data,
                'campaign_type_special_for': form.special_for.data,
                'campaign_type_description': form.description.data,
                'campaign_type_icon': form.icon.data
            }
            result = requests.post(BACKEND_SERVER_ADDRESS + "/admin/campaign/type", data=json.dumps(data)).content
            result = json.loads(result)

            if result["status"] == "ok":
                message = json.dumps({"type": "alert-success", "message": "نوع کمپین با موفقیت ثبت شد."})
            elif result["status"] == "nok":
                message = json.dumps({"type": "alert-error", "message": "خطایی رخ داده است."})
            session['message'] = message

            return redirect(url_for('campaign_type_new'))
    elif request.method == 'GET':
        message = None
        if session.get('message', None) is not None:
            message = json.loads(session.pop("message"))
        return render_template('general/new.html', form=form, message=message, configs=configs)


@app.route('/dashboard/admin/campaign/type/<id>/edit', methods=['GET', 'POST'])
@login_required
@roles_accepted('admin')
def campaign_type_edit(id):
    configs = {
        'module': 'لیست انواع کمپین',
        'action': 'ویرایش نوع کمپین',
        'url': 'campaign_type_edit',
        'url_index': 'campaign_type',
        'id': id,
        'page_title': 'ویرایش نوع کمپین'
    }
    form = CampaignTypeForm()
    if request.method == 'POST':
        if form.validate() == False:
            flash('All fields are required.', 'danger')
            return render_template('general/edit.html', form=form, configs=configs)
        else:
            data = {
                'campaign_type_updated_user_id': current_user.get_id(),
                'campaign_type_name': form.name.data,
                'campaign_type_title': form.title.data,
                'campaign_type_base_price': form.base_price.data,
                'campaign_type_special_for': form.special_for.data,
                'campaign_type_description': form.description.data,
                'campaign_type_icon': form.icon.data
            }
            result = requests.put(BACKEND_SERVER_ADDRESS + "/admin/campaign/type/" + str(id),
                                  data=json.dumps(data)).content
            result = json.loads(result)

            if result["status"] == "ok":
                message = {"type": "alert-success", "message": "نوع کمپین با موفقیت ویرایش شد."}
            elif result["status"] == "nok":
                message = {"type": "alert-error", "message": "خطایی رخ داده است."}

            return render_template('general/edit.html', form=form, message=message, configs=configs)
    elif request.method == 'GET':
        result = requests.get(BACKEND_SERVER_ADDRESS + "/admin/campaign/type/" + str(id)).content
        result = json.loads(result)
        result = result['body']
        form.name.data = result["campaign_type_name"]
        form.title.data = result["campaign_type_title"]
        form.base_price.data = result["campaign_type_base_price"]
        form.special_for.data = result["campaign_type_special_for"]
        form.description.data = result["campaign_type_description"]
        form.icon.data = result["campaign_type_icon"]
        return render_template('general/edit.html', form=form, configs=configs)


@app.route('/dashboard/admin/package', methods=['GET', 'POST'])
@login_required
@roles_accepted('admin')
def package():
    configs = {
        'url_new': 'package_new',
        'url_edit': 'package_edit',
        'url_index': 'package',
        'module': 'لیست  بسته ها',
        'action': 'لیست  بسته ها',
        'url_new_text': 'بسته جدید',
        'id_name': 'package_id',
        'fields': [
            {
                'name': 'package_author_user_id',
                'title': 'نویسنده',
                'order': 1,
                'hide': '',
                'width': '30%'
            },
            {
                'name': 'package_title',
                'title': 'عنوان',
                'order': 2,
                'hide': '',
                'width': '30%'
            },
            {
                'name': 'package_price',
                'title': 'قیمت',
                'order': 3,
                'hide': '',
                'width': '29%'
            },
            {
                'name': 'package_discount',
                'title': 'تخفیف',
                'order': 4,
                'hide': '',
                'width': '29%'
            },
            {
                'name': 'package_click_count',
                'title': 'تعداد کلیک',
                'order': 5,
                'hide': 'phone,tablet',
                'width': '29%'
            },
            {
                'name': 'package_impression_count',
                'title': 'تعداد نمایش',
                'order': 6,
                'hide': 'phone,tablet',
                'width': '29%'
            },
            {
                'name': 'package_description',
                'title': 'توضیحات',
                'order': 7,
                'hide': 'phone,tablet',
                'width': '29%'
            }
        ]
    }
    if request.method == 'POST':
        message = requests.delete(BACKEND_SERVER_ADDRESS + "/admin/package/" + request.form['action'])

    result = requests.get(BACKEND_SERVER_ADDRESS + "/admin/package").content
    result = json.loads(result)
    result = result['body']
    return render_template('general/index.html', result=result, configs=configs)


@app.route('/dashboard/admin/package/new', methods=['GET', 'POST'])
@login_required
@roles_accepted('admin')
def package_new():
    configs = {
        'module': 'لیست  بسته ها',
        'action': 'بسته جدید',
        'url': 'package_new',
        'url_index': 'package'
    }
    form = PackageForm()
    if request.method == 'POST':
        if form.validate() == False:
            flash('All fields are required.', 'danger')
            return render_template('general/new.html', form=form, configs=configs)
        else:
            data = {
                'package_author_user_id': current_user.get_id(),
                'package_title': form.title.data,
                'package_price': form.price.data,
                'package_discount': form.discount.data,
                'package_click_count': form.click_count.data,
                'package_impression_count': form.impression_count.data,
                'package_description': form.description.data
            }
            result = requests.post(BACKEND_SERVER_ADDRESS + "/admin/package", data=json.dumps(data)).content
            result = json.loads(result)
            result = result['body']
            return render_template('general/new.html', form=form, result=result, configs=configs)
    elif request.method == 'GET':
        return render_template('general/new.html', form=form, configs=configs)


@app.route('/dashboard/admin/package/<id>/edit', methods=['GET', 'POST'])
@login_required
@roles_accepted('admin')
def package_edit(id):
    configs = {
        'module': 'لیست  بسته ها',
        'action': 'ویرایش بسته',
        'url': 'package_edit',
        'url_index': 'package',
        'id': id
    }
    form = PackageForm()
    if request.method == 'POST':
        if form.validate() == False:
            flash('All fields are required.', 'danger')
            return render_template('general/edit.html', form=form, configs=configs)
        else:
            data = {
                'package_updated_user_id': current_user.get_id(),
                'package_title': form.title.data,
                'package_price': form.price.data,
                'package_discount': form.discount.data,
                'package_click_count': form.click_count.data,
                'package_impression_count': form.impression_count.data,
                'package_description': form.description.data
            }
            result = requests.put(BACKEND_SERVER_ADDRESS + "/admin/package/" + str(id),
                                  data=json.dumps(data)).content
            result = json.loads(result)
            result = result['body']
            return render_template('general/edit.html', form=form, result=result, configs=configs)
    elif request.method == 'GET':
        result = requests.get(BACKEND_SERVER_ADDRESS + "/admin/package/" + str(id)).content
        result = json.loads(result)
        result = result['body']
        form.title.data = result["package_title"]
        form.price.data = result["package_price"]
        form.discount.data = result["package_discount"]
        form.click_count.data = result["package_click_count"]
        form.impression_count.data = result["package_impression_count"]
        form.description.data = result["package_description"]
        return render_template('general/edit.html', form=form, configs=configs)


@app.route('/dashboard/admin/banner/size', methods=['GET', 'POST'])
@login_required
@roles_accepted('admin')
def banner_size():
    configs = {
        'url_new': 'banner_size_new',
        'url_edit': 'banner_size_edit',
        'url_index': 'banner_size',
        'module': 'لیست اندازه بنرها',
        'action': 'لیست اندازه بنرها',
        'url_new_text': 'اندازه جدید',
        'id_name': 'banner_size_id',
        'page_title': 'بنرها - اندازه بنرها',
        'fields': [
            {
                'name': 'banner_size_type',
                'title': 'نوع دستگاه',
                'order': 1,
                'hide': '',
                'width': '30%',
                'class': 'class=defaultSort'
            },
            {
                'name': 'banner_size_width',
                'title': 'عرض بنر',
                'order': 2,
                'hide': '',
                'width': '29%',
            },
            {
                'name': 'banner_size_height',
                'title': 'طول بنر',
                'order': 3,
                'hide': '',
                'width': '30%'
            }

        ]
    }
    message = None
    if request.method == 'POST':
        result = requests.delete(BACKEND_SERVER_ADDRESS + "/admin/banner/size/" + request.form['action']).content
        result = json.loads(result)

        if result["status"] == "ok":
            message = {"type": "alert-success", "message": "رکورد با موفقیت حذف شد."}
        elif result["status"] == "nok":
            message = {"type": "alert-error", "message": "خطایی رخ داده است."}

    result = requests.get(BACKEND_SERVER_ADDRESS + "/admin/banner/size").content
    result = json.loads(result)
    result = result['body']

    return render_template('general/index.html', result=result, message=message, configs=configs)


@app.route('/dashboard/admin/banner/size/new', methods=['GET', 'POST'])
@login_required
@roles_accepted('admin')
def banner_size_new():
    configs = {
        'module': 'لیست اندازه بنرها',
        'action': 'اندازه جدید',
        'url': 'banner_size_new',
        'url_index': 'banner_size',
        'from_id': 'banner-size-form',
        'page_title': 'اندازه جدید'
    }
    form = BannerSizeForm()
    if request.method == 'POST':
        if form.validate() == False:
            flash('All fields are required.', 'danger')
            return render_template('general/new.html', form=form, configs=configs)
        else:
            data = {
                'banner_size_author_user_id': current_user.get_id(),
                'banner_size_height': form.height.data,
                'banner_size_width': form.width.data,
                'banner_size_type': form.type.data
            }
            result = requests.post(BACKEND_SERVER_ADDRESS + "/admin/banner/size", data=json.dumps(data)).content
            result = json.loads(result)

            if result["status"] == "ok":
                message = json.dumps({"type": "alert-success", "message": "اطلاعات با موفقیت ثبت شد."})
            elif result["status"] == "nok":
                message = json.dumps({"type": "alert-error", "message": "خطایی رخ داده است."})
            session['message'] = message

            return redirect(url_for('banner_size_new'))
    elif request.method == 'GET':
        message = None
        if session.get('message', None) is not None:
            message = json.loads(session.pop("message"))
        return render_template('general/new.html', form=form, message=message, configs=configs)


@app.route('/dashboard/admin/banner/size/<id>/edit', methods=['GET', 'POST'])
@login_required
@roles_accepted('admin')
def banner_size_edit(id):
    configs = {
        'module': 'لیست اندازه بنرها',
        'action': 'ویرایش اندازه',
        'url': 'banner_size_edit',
        'url_index': 'banner_size',
        'from_id': 'banner-size-form',
        'id': id,
        'page_title': 'ویرایش اندازه'
    }
    form = BannerSizeForm()
    if request.method == 'POST':
        if form.validate() == False:
            flash('All fields are required.', 'danger')
            return render_template('general/edit.html', form=form, configs=configs)
        else:
            data = {
                'banner_size_updated_user_id': current_user.get_id(),
                'banner_size_height': form.height.data,
                'banner_size_width': form.width.data,
                'banner_size_type': form.type.data
            }
            result = requests.put(BACKEND_SERVER_ADDRESS + "/admin/banner/size/" + str(id),
                                  data=json.dumps(data)).content
            result = json.loads(result)

            if result["status"] == "ok":
                message = {"type": "alert-success", "message": "اطلاعات با موفقیت ویرایش شد."}
            elif result["status"] == "nok":
                message = {"type": "alert-error", "message": "خطایی رخ داده است."}

            return render_template('general/edit.html', form=form, message=message, configs=configs)
    elif request.method == 'GET':
        result = requests.get(BACKEND_SERVER_ADDRESS + "/admin/banner/size/" + str(id)).content
        result = json.loads(result)
        result = result['body']
        form.height.data = result["banner_size_height"]
        form.width.data = result["banner_size_width"]
        form.type.data = result["banner_size_type"]
        return render_template('general/edit.html', form=form, configs=configs)


@app.route('/dashboard/advertiser/campaign', methods=['GET', 'POST'])
@login_required
@roles_accepted('advertiser')
def advertiser_campaign():
    configs = {
        'url_new': 'advertiser_campaign_new',
        'url_edit': 'advertiser_campaign_edit',
        'url_index': 'advertiser_campaign',
        'module': 'لیست کمپین ها',
        'action': 'لیست کمپین ها',
        'url_new_text': 'ساخت کمپین جدید',
        'id_name': 'campaign_id',
        'page_title': 'کمپین های من'
    }
    message = None
    if request.method == 'POST':
        campaign = requests.get(BACKEND_SERVER_ADDRESS + "/advertiser/campaign/" + str(request.form['action'])).content
        campaign = json.loads(campaign)
        campaign = campaign['body']

        if campaign['campaign_author_user_id'] != current_user.get_id() and not current_user.has_role('admin'):
            return redirect(url_for('dashboard'))

        if campaign['campaign_active_by_user']:
            total_budget = 0
            if campaign['campaign_active_by_admin']:
                redis_total_budget = r.smembers('campaign_total_budget_' + str(campaign['campaign_id']))
                if len(list(redis_total_budget)) > 0:
                    total_budget = int(float(list(redis_total_budget)[0]))
                campaign_deactivate_function(request.form['action'])
            else:
                total_budget = int(campaign['campaign_total_budget'])

            data = {
                'transaction_author_user_id': campaign['campaign_author_user_id'],
                'transaction_updated_user_id': current_user.get_id(),
                'transaction_deposit_amount': total_budget,
                'transaction_withdrawal_amount': 0,
                'transaction_description': 'بازگشت بودجه کمپین' + " " + campaign["campaign_name"],
                'transaction_status': 1
            }
            result = requests.post(BACKEND_SERVER_ADDRESS + "/financial/transaction",
                                   data=json.dumps(data)).content
            result = json.loads(result)

        data = {
            'campaign_updated_user_id': current_user.get_id(),
            'campaign_is_deleted': True,
            'campaign_active_by_user': False
        }
        result = requests.put(BACKEND_SERVER_ADDRESS + "/advertiser/campaign/" + request.form['action'],
                              data=json.dumps(data)).content
        result = json.loads(result)

        if result["status"] == "ok":
            message = {"type": "alert-success", "message": "رکورد با موفقیت حذف شد."}
        elif result["status"] == "nok":
            message = {"type": "alert-error", "message": "خطایی رخ داده است."}

    result = requests.get(BACKEND_SERVER_ADDRESS + "/advertiser/campaign?user=" + str(current_user.get_id())).content
    result = json.loads(result)
    result = result['body']

    form = CampaignCreditForm()

    if session.get('message', None) is not None:
        if message is None:
            message = json.loads(session.pop("message"))
        else:
            session.pop("message")

    return render_template('campaign/index.html', result=result, message=message, form=form, configs=configs)


@app.route('/dashboard/advertiser/campaign/<campaign_id>/budget/increase', methods=['POST'])
@login_required
@roles_accepted('advertiser')
def advertiser_campaign_budget_increase(campaign_id):
    if request.method == 'POST':
        if request.form.get("amount") is not None:
            amount = request.form.get("amount").replace(",", "")
        else:
            return redirect(url_for('advertiser_campaign'))

        if amount == '0' or amount == '':
            return redirect(url_for('advertiser_campaign'))

        campaign = requests.get(BACKEND_SERVER_ADDRESS + "/advertiser/campaign/" + str(campaign_id)).content
        campaign = json.loads(campaign)
        campaign = campaign['body']

        if campaign['campaign_author_user_id'] != current_user.get_id() and not current_user.has_role('admin'):
            return redirect(url_for('dashboard'))

        credit = publisher_credit_calculation()
        if int(amount) > credit:
            return redirect(url_for('credit_charge', credit=int(amount) - credit))

        total_budget = 0
        if campaign['campaign_active_by_admin']:
            redis_total_budget = r.smembers('campaign_total_budget_' + str(campaign['campaign_id']))
            if len(list(redis_total_budget)) > 0:
                total_budget = int(float(list(redis_total_budget)[0]))
        else:
            total_budget = int(campaign['campaign_total_budget'])

        campaign_deactivate_function(campaign_id)

        total_budget = total_budget + int(amount)

        total_budget_main = int(amount)
        if campaign['campaign_total_budget_main'] is not None:
            total_budget_main = int(campaign['campaign_total_budget_main']) + int(amount)

        print total_budget_main

        data = {
            'campaign_updated_user_id': current_user.get_id(),
            'campaign_total_budget': total_budget,
            'campaign_total_budget_main': total_budget_main
        }

        result = requests.put(BACKEND_SERVER_ADDRESS + "/advertiser/campaign/" + str(campaign_id),
                              data=json.dumps(data)).content
        result = json.loads(result)
        result = result['body']

        data = {
            'transaction_author_user_id': campaign['campaign_author_user_id'],
            'transaction_updated_user_id': current_user.get_id(),
            'transaction_deposit_amount': 0,
            'transaction_withdrawal_amount': amount,
            'transaction_description': 'افزایش بودجه کمپین ' + campaign['campaign_name'],
            'transaction_status': 1
        }
        result = requests.post(BACKEND_SERVER_ADDRESS + "/financial/transaction",
                               data=json.dumps(data)).content
        result = json.loads(result)
        result = result['body']

        message = json.dumps({"type": "alert-success", "message": "افزایش بودجه کمپین با موفقیت انجام شد."})
        session['message'] = message

        return redirect(url_for('advertiser_campaign'))


@app.route('/dashboard/advertiser/campaign/<campaign_id>/click/price/edit', methods=['POST'])
@login_required
@roles_accepted('advertiser')
def advertiser_campaign_click_price_edit(campaign_id):
    if request.method == 'POST':
        campaign = requests.get(BACKEND_SERVER_ADDRESS + "/advertiser/campaign/" + str(campaign_id)).content
        campaign = json.loads(campaign)
        campaign = campaign['body']
        base_price = int(campaign["campaign_type"]["campaign_type_base_price"])

        amount = (base_price if request.form.get("amount") is None else request.form.get("amount"))

        if int(amount) < base_price:
            amount = base_price
        data = {
            'campaign_updated_user_id': current_user.get_id(),
            'campaign_click_price': amount
        }
        result = requests.put(BACKEND_SERVER_ADDRESS + "/advertiser/campaign/" + str(campaign_id),
                              data=json.dumps(data)).content
        result = json.loads(result)
        result = result['body']
        return format_currency(amount)


@app.route('/dashboard/advertiser/query/expansion', methods=['GET', 'POST'])
@login_required
@roles_accepted('advertiser')
def query_expansion(keywords=None):
    data = json.loads(request.data)
    if keywords is None:
        keywords = data.get('keywords')

    expansion_keywords = []
    number_of_related_word = 3
    for keyword in keywords:
        temp = qe.useModel_1(str(keyword).strip(), number_of_related_word)
        expansion_keywords.extend(temp)

    return Response(json.dumps(expansion_keywords, sort_keys=False),
                    mimetype='application/json')


@app.route('/api/query/expansion', methods=['POST'])
@csrf.exempt
def api_query_expansion():
    if request.method == 'POST':
        data = json.loads(request.data)
        query = data.get('query', None)

        # query = "dream💜 💜purpell"

        # print query
        number_of_related_word = 10
        keywords = qe.useModel_1(str(query).strip(), number_of_related_word)
        result = ""
        # print keywords
        # print poword
        for keyword in keywords:
            result = result + str(keyword) + " "

        response = {"status": "yes", "body": str(result)}
        return Response(json.dumps(response, sort_keys=True),
                        mimetype='application/json')


@app.route('/api/spell/checker', methods=['POST'])
@csrf.exempt
def api_spell_checker():
    if request.method == 'POST':
        data = json.loads(request.data)
        query = data.get('query', None)
        result = spellchecker.useModel(str(query))
        response = {"status": "yes", "body": str(result)}
        return Response(json.dumps(response, sort_keys=True),
                        mimetype='application/json')


@app.route('/dashboard/advertiser/campaign/new', methods=['GET', 'POST'])
@login_required
@roles_accepted('advertiser')
def advertiser_campaign_new():
    if request.method == 'GET':
        configs = {
            'url_index': 'advertiser_campaign',
            'module': 'کمپین های من',
            'action': 'ایجاد کمپین جدید',
        }
        result = requests.get(BACKEND_SERVER_ADDRESS + "/admin/campaign/type").content
        result = json.loads(result)
        types = result['body']
        return render_template('campaign/step_one.html', configs=configs, types=types)


@app.route('/dashboard/advertiser/campaign/type/<type_name>/new', methods=['GET'])
@login_required
@roles_accepted('advertiser')
def advertiser_campaign_create(type_name):
    if request.method == 'GET':
        data = {
            'campaign_author_user_id': current_user.get_id(),
            'campaign_type': type_name
        }
        result = requests.post(BACKEND_SERVER_ADDRESS + "/advertiser/campaign", data=json.dumps(data)).content
        result = json.loads(result)
        result = result['body']
        return redirect(url_for('advertiser_campaign_steps', campaign_id=result, campaign_step='two'))


@app.route('/dashboard/advertiser/campaign/<campaign_id>/step/<campaign_step>/new', methods=['GET', 'POST'])
@login_required
@roles_accepted('advertiser')
def advertiser_campaign_steps(campaign_id, campaign_step):
    configs = {
        'url': 'advertiser_campaign_steps',
        'url_index': 'advertiser_campaign',
        'module': 'کمپین های من',
        'action': 'ایجاد کمپین جدید',
        'campaign_id': campaign_id,
        'campaign_step': campaign_step,
        'campaign_type_name': 'banner',
        'page_title': 'ایجاد کمپین جدید'
    }

    if request.method == 'GET':
        campaign = requests.get(BACKEND_SERVER_ADDRESS + "/advertiser/campaign/" + str(campaign_id)).content
        campaign = json.loads(campaign)
        campaign = campaign['body']

        if campaign['campaign_author_user_id'] != current_user.get_id() and not current_user.has_role('admin'):
            return redirect(url_for('dashboard'))

        if campaign_step == "one":
            result = requests.get(BACKEND_SERVER_ADDRESS + "/admin/campaign/type").content
            result = json.loads(result)
            types = result['body']
            configs['campaign_type_name'] = campaign["campaign_type"]["campaign_type_name"]
            return render_template('campaign/step_one.html', configs=configs, types=types)

        if campaign_step == "two":
            form = CampaignNameForm()
            form.name.data = ('' if campaign["campaign_name"] is None else campaign["campaign_name"])
            configs['campaign_type_name'] = campaign["campaign_type"]["campaign_type_name"]
            configs['from_id'] = 'advertiser-campaign-step-two'
            return render_template('campaign/step_two.html', form=form, configs=configs)

        if campaign_step == "three":
            form = CampaignBudgetForm()
            form.total_budget.data = (
                '' if campaign["campaign_total_budget"] is None else campaign["campaign_total_budget"])
            form.daily_budget.data = (
                '' if campaign["campaign_daily_budget"] is None else campaign["campaign_daily_budget"])

            if campaign['campaign_active_by_user']:
                form.total_budget.render_kw = {"placeholder": "", "dir": "ltr", "readonly": "true"}

            configs['campaign_type_name'] = campaign["campaign_type"]["campaign_type_name"]
            return render_template('campaign/step_three.html', form=form, configs=configs)

        if campaign_step == "four":

            if campaign["campaign_type"]["campaign_type_name"] == 'native':
                title = (
                    '' if campaign["campaign_native_title"] is None else campaign["campaign_native_title"])
                result = requests.get(
                    BACKEND_SERVER_ADDRESS + "/advertiser/banners/user/" + str(current_user.get_id())).content
                result = json.loads(result)
                banners = result['body']

                result = requests.get(BACKEND_SERVER_ADDRESS + "/admin/banner/size?type=native").content
                result = json.loads(result)
                banner_sizes = result['body']

                result = requests.get(
                    BACKEND_SERVER_ADDRESS + "/advertiser/campaign/banner?campaign=" + str(campaign_id)).content
                result = json.loads(result)
                campaign_banners = result['body']

                configs['campaign_type_name'] = campaign["campaign_type"]["campaign_type_name"]
                return render_template('campaign/step_four_native.html', campaign_banners=campaign_banners,
                                       banners=banners,
                                       banner_sizes=banner_sizes,
                                       title=title,
                                       configs=configs)

            if campaign["campaign_type"]["campaign_type_name"] == 'mobile':
                result = requests.get(
                    BACKEND_SERVER_ADDRESS + "/advertiser/banners/user/" + str(current_user.get_id())).content
                result = json.loads(result)
                banners = result['body']

                result = requests.get(BACKEND_SERVER_ADDRESS + "/admin/banner/size?type=mobile").content
                result = json.loads(result)
                banner_sizes = result['body']

                result = requests.get(
                    BACKEND_SERVER_ADDRESS + "/advertiser/campaign/banner?campaign=" + str(campaign_id)).content
                result = json.loads(result)
                campaign_banners = result['body']

                configs['campaign_type_name'] = campaign["campaign_type"]["campaign_type_name"]
                return render_template('campaign/step_four.html', campaign_banners=campaign_banners, banners=banners,
                                       banner_sizes=banner_sizes,
                                       configs=configs)

            if campaign["campaign_type"]["campaign_type_name"] == 'banner':
                result = requests.get(
                    BACKEND_SERVER_ADDRESS + "/advertiser/banners/user/" + str(current_user.get_id())).content
                result = json.loads(result)
                banners = result['body']

                result = requests.get(BACKEND_SERVER_ADDRESS + "/admin/banner/size?type=desktop").content
                result = json.loads(result)
                banner_sizes = result['body']

                result = requests.get(
                    BACKEND_SERVER_ADDRESS + "/advertiser/campaign/banner?campaign=" + str(campaign_id)).content
                result = json.loads(result)
                campaign_banners = result['body']

                configs['campaign_type_name'] = campaign["campaign_type"]["campaign_type_name"]
                return render_template('campaign/step_four.html', campaign_banners=campaign_banners, banners=banners,
                                       banner_sizes=banner_sizes,
                                       configs=configs)

            if campaign["campaign_type"]["campaign_type_name"] == 'iframe':

                result = requests.get(BACKEND_SERVER_ADDRESS + "/admin/banner/size?type=desktop").content
                result = json.loads(result)
                banner_sizes = result['body']

                result = requests.get(
                    BACKEND_SERVER_ADDRESS + "/advertiser/campaign/banner?campaign=" + str(campaign_id)).content
                result = json.loads(result)
                campaign_banners = result['body']

                configs['campaign_type_name'] = campaign["campaign_type"]["campaign_type_name"]
                return render_template('campaign/step_four_iframe.html', campaign_banners=campaign_banners,
                                       banner_sizes=banner_sizes,
                                       configs=configs)

            elif campaign["campaign_type"]["campaign_type_name"] == 'search_engine':
                form = CampaignAdwordsDescriptionForm()
                form.title.data = (
                    '' if campaign["campaign_adwords_title"] is None else campaign["campaign_adwords_title"])
                form.description.data = (
                    '' if campaign["campaign_adwords_description"] is None else campaign[
                        "campaign_adwords_description"])
                form.email.data = (
                    '' if campaign["campaign_adwords_email"] is None else campaign[
                        "campaign_adwords_email"])
                form.phone.data = (
                    '' if campaign["campaign_adwords_phone"] is None else campaign[
                        "campaign_adwords_phone"])
                form.address.data = (
                    '' if campaign["campaign_adwords_address"] is None else campaign[
                        "campaign_adwords_address"])
                configs['campaign_type_name'] = campaign["campaign_type"]["campaign_type_name"]
                return render_template('campaign/step_four_search_engine.html', form=form, configs=configs)

        if campaign_step == "five":
            form = CampaignLandingPageForm()
            form.landing_page_url.data = (
                '' if campaign["campaign_landing_page_url"] is None else campaign["campaign_landing_page_url"])
            configs['campaign_type_name'] = campaign["campaign_type"]["campaign_type_name"]
            configs['from_id'] = 'advertiser-campaign-step-five'
            return render_template('campaign/step_five.html', form=form, configs=configs)

        if campaign_step == "six":
            form = TargetingForm()

            result = requests.get(BACKEND_SERVER_ADDRESS + "/admin/target/geography").content
            result = json.loads(result)
            result = result['body']
            records = [(record["geography_id"], record["geography_title"]) for record in result]
            form.states.choices = records

            geography = ''
            if campaign["campaign_targeted_geography_all"]:
                geography = 'all'
            elif campaign["campaign_targeted_geography_iran"]:
                geography = 'iran'
            elif campaign["campaign_targeted_geography_not_iran"]:
                geography = 'not_iran'
            elif campaign["campaign_targeted_geography_special"]:
                geography = 'special'

            if campaign["campaign_type"]["campaign_type_name"] == 'mobile':
                result = requests.get(BACKEND_SERVER_ADDRESS + "/admin/target/os?type=mobile").content
            else:
                result = requests.get(BACKEND_SERVER_ADDRESS + "/admin/target/os").content

            result = json.loads(result)
            result = result['body']
            records = [(record["os_id"], record["os_title"]) for record in result]
            form.operating_systems.choices = records

            os = ''
            if campaign["campaign_targeted_operating_system_all"]:
                os = 'all'
            elif campaign["campaign_targeted_operating_system_special"]:
                os = 'special'

            if campaign["campaign_type"]["campaign_type_name"] == 'mobile':
                os = 'special'

            result = requests.get(BACKEND_SERVER_ADDRESS + "/admin/target/subject").content
            result = json.loads(result)
            result = result['body']
            records = [(record["subject_id"], record["subject_title"]) for record in result]
            form.subjects.choices = records

            subject = ''
            if campaign["campaign_targeted_subject_all"]:
                subject = 'all'
            elif campaign["campaign_targeted_subject_special"]:
                subject = 'special'

            playtime = ''
            if campaign["campaign_playtime_all"]:
                playtime = 'all'
            elif campaign["campaign_playtime_special"]:
                playtime = 'special'

            site_grade = ''
            if campaign["campaign_network_class_a"]:
                site_grade = 'class_a'
            elif campaign["campaign_network_class_b"]:
                site_grade = 'class_b'
            elif campaign["campaign_network_class_c"]:
                site_grade = 'class_c'

            keyword = ''
            if campaign["campaign_targeted_keyword_all"]:
                keyword = 'all'
            elif campaign["campaign_targeted_keyword_special"]:
                keyword = 'special'

            retargeting = ''
            if campaign["campaign_retargeting"]:
                retargeting = 'yes'
            else:
                retargeting = 'no'

            form.geography.data = geography
            form.operating_system.data = os
            form.subject.data = subject
            form.site_grade.data = site_grade
            form.playtime.data = playtime
            form.keyword.data = keyword
            form.price.data = campaign["campaign_click_price"]
            form.retargeting_code.data = '<script type="text/javascript">!function(i,t){"use strict";t.write(' + '\'' + '<div style="display: none;"><iframe src = "http://31.184.132.191:4444/cgi-bin/cookie.sh" height="0" width="0" frameborder="0" scrolling="no" ></iframe></div>' + '\'' + ')}(this,document);</script>'
            form.retargeting.data = retargeting

            states = []
            if campaign["campaign_targeted_geography_special"]:
                records = requests.get(
                    BACKEND_SERVER_ADDRESS + "/advertiser/campaign/geography?campaign=" + str(campaign_id)).content
                records = json.loads(records)
                records = records['body']
                for record in records:
                    states.append(record["geography"]["geography_id"])
            form.states.data = states

            operating_systems = []
            if campaign["campaign_targeted_operating_system_special"]:
                records = requests.get(
                    BACKEND_SERVER_ADDRESS + "/advertiser/campaign/os?campaign=" + str(campaign_id)).content
                records = json.loads(records)
                records = records['body']
                for record in records:
                    operating_systems.append(record["os"]["os_id"])
            form.operating_systems.data = operating_systems

            if campaign["campaign_type"]["campaign_type_name"] == 'mobile' and len(operating_systems) == 0:
                for record in form.operating_systems.choices:
                    operating_systems.append(record[0])
                form.operating_systems.data = operating_systems

            subjects = []
            if campaign["campaign_targeted_subject_special"]:
                records = requests.get(
                    BACKEND_SERVER_ADDRESS + "/advertiser/campaign/subject?campaign=" + str(campaign_id)).content
                records = json.loads(records)
                records = records['body']
                for record in records:
                    subjects.append(record["subject"]["subject_id"])
            form.subjects.data = subjects

            keywords = []
            if campaign["campaign_targeted_keyword_special"]:
                records = requests.get(
                    BACKEND_SERVER_ADDRESS + "/advertiser/campaign/keyword?campaign=" + str(campaign_id)).content
                records = json.loads(records)
                records = records['body']
                for record in records:
                    keywords.append((record["keyword"]["keyword_title"], record["keyword"]["keyword_title"]))

            form.keywords.choices = keywords

            playtime_special = []
            if campaign["campaign_playtime_not_24_08"]:
                playtime_special.append('not_24_08')
            if campaign["campaign_playtime_not_08_16"]:
                playtime_special.append('not_08_16')
            if campaign["campaign_playtime_not_16_24"]:
                playtime_special.append('not_16_24')

            form.playtime_special.data = playtime_special
            configs['campaign_type_name'] = campaign["campaign_type"]["campaign_type_name"]

            if campaign["campaign_type"]["campaign_type_name"] == 'search_engine':
                del form.keyword

            return render_template('campaign/step_six.html', form=form,
                                   base_price=campaign['campaign_type']['campaign_type_base_price'],
                                   landing_page_url=campaign['campaign_landing_page_url'], configs=configs)
        if campaign_step == "seven":
            states = []
            if campaign["campaign_targeted_geography_special"]:
                records = requests.get(
                    BACKEND_SERVER_ADDRESS + "/advertiser/campaign/geography?campaign=" + str(campaign_id)).content
                records = json.loads(records)
                records = records['body']
                for record in records:
                    states.append(record["geography"]["geography_title"])

            operating_systems = []
            if campaign["campaign_targeted_operating_system_special"]:
                records = requests.get(
                    BACKEND_SERVER_ADDRESS + "/advertiser/campaign/os?campaign=" + str(campaign_id)).content
                records = json.loads(records)
                records = records['body']
                for record in records:
                    operating_systems.append(record["os"]["os_title"])

            subjects = []
            if campaign["campaign_targeted_subject_special"]:
                records = requests.get(
                    BACKEND_SERVER_ADDRESS + "/advertiser/campaign/subject?campaign=" + str(campaign_id)).content
                records = json.loads(records)
                records = records['body']
                for record in records:
                    subjects.append(record["subject"]["subject_title"])

            keywords = []
            if campaign["campaign_targeted_keyword_special"]:
                records = requests.get(
                    BACKEND_SERVER_ADDRESS + "/advertiser/campaign/keyword?campaign=" + str(campaign_id)).content
                records = json.loads(records)
                records = records['body']
                for record in records:
                    keywords.append(record["keyword"]["keyword_title"])

            result = requests.get(
                BACKEND_SERVER_ADDRESS + "/advertiser/campaign/banner?campaign=" + str(campaign_id)).content
            result = json.loads(result)
            campaign_banners = result['body']

            result = requests.get(
                BACKEND_SERVER_ADDRESS + "/advertiser/campaign/click/price/max").content
            result = json.loads(result)
            campaigns_max_click_price = result['body']
            return render_template('campaign/step_seven.html', campaign=campaign,
                                   campaign_banners_len=len(campaign_banners), states=states,
                                   operating_systems=operating_systems, subjects=subjects, keywords=keywords,
                                   campaigns_max_click_price=campaigns_max_click_price, configs=configs)

    if request.method == 'POST':
        campaign = requests.get(BACKEND_SERVER_ADDRESS + "/advertiser/campaign/" + str(campaign_id)).content
        campaign = json.loads(campaign)
        campaign = campaign['body']

        if campaign['campaign_author_user_id'] != current_user.get_id() and not current_user.has_role('admin'):
            return redirect(url_for('dashboard'))

        if campaign_step == "two":
            form = CampaignNameForm()
            if form.validate() == False:
                flash('All fields are required.', 'danger')
                return render_template('campaign/step_two.html', form=form, configs=configs)
            else:
                data = {
                    'campaign_updated_user_id': current_user.get_id(),
                    'campaign_name': form.name.data
                }
                result = requests.put(BACKEND_SERVER_ADDRESS + "/advertiser/campaign/" + str(campaign_id),
                                      data=json.dumps(data)).content
                result = json.loads(result)
                result = result['body']
                return redirect(url_for('advertiser_campaign_steps', campaign_id=campaign_id, campaign_step='three'))

        if campaign_step == "three":
            form = CampaignBudgetForm()
            if form.validate() == False:
                flash('All fields are required.', 'danger')
                return render_template('campaign/step_three.html', form=form, configs=configs)
            else:
                campaign_deactivate_function(campaign_id)

                data = {}
                if campaign['campaign_active_by_user']:
                    data = {
                        'campaign_updated_user_id': current_user.get_id(),
                        'campaign_daily_budget': form.daily_budget.data.replace(",", "")
                    }
                else:
                    data = {
                        'campaign_updated_user_id': current_user.get_id(),
                        'campaign_daily_budget': form.daily_budget.data.replace(",", ""),
                        'campaign_total_budget': form.total_budget.data.replace(",", ""),
                        'campaign_total_budget_main': form.total_budget.data.replace(",", "")
                    }

                result = requests.put(BACKEND_SERVER_ADDRESS + "/advertiser/campaign/" + str(campaign_id),
                                      data=json.dumps(data)).content
                result = json.loads(result)
                result = result['body']
                return redirect(url_for('advertiser_campaign_steps', campaign_id=campaign_id, campaign_step='four'))

        if campaign_step == "four":

            if campaign["campaign_type"]["campaign_type_name"] == 'native':
                campaign_deactivate_function(campaign_id)
                result = requests.delete(
                    BACKEND_SERVER_ADDRESS + "/advertiser/campaign/banner?campaign=" + str(campaign_id)).content
                result = json.loads(result)
                result = result['body']
                for banner in request.form.getlist('banners'):
                    if banner:
                        data = {
                            'campaign': campaign_id,
                            'banner': banner
                        }
                        result = requests.post(BACKEND_SERVER_ADDRESS + "/advertiser/campaign/banner",
                                               data=json.dumps(data)).content
                        result = json.loads(result)
                        result = result['body']

                data = {
                    'campaign_updated_user_id': current_user.get_id(),
                    'campaign_native_title': ('' if request.form.get('title') is None else request.form.get('title'))
                }

                result = requests.put(BACKEND_SERVER_ADDRESS + "/advertiser/campaign/" + str(campaign_id),
                                      data=json.dumps(data)).content
                result = json.loads(result)
                result = result['body']

            if campaign["campaign_type"]["campaign_type_name"] == 'banner' or campaign["campaign_type"][
                "campaign_type_name"] == 'mobile':
                campaign_deactivate_function(campaign_id)
                result = requests.delete(
                    BACKEND_SERVER_ADDRESS + "/advertiser/campaign/banner?campaign=" + str(campaign_id)).content
                result = json.loads(result)
                result = result['body']
                for banner in request.form.getlist('banners'):
                    if banner:
                        data = {
                            'campaign': campaign_id,
                            'banner': banner
                        }
                        result = requests.post(BACKEND_SERVER_ADDRESS + "/advertiser/campaign/banner",
                                               data=json.dumps(data)).content
                        result = json.loads(result)
                        result = result['body']

            if campaign["campaign_type"]["campaign_type_name"] == 'iframe':
                campaign_deactivate_function(campaign_id)
                result = requests.delete(
                    BACKEND_SERVER_ADDRESS + "/advertiser/campaign/banner?campaign=" + str(campaign_id)).content
                result = json.loads(result)
                result = result['body']

                result = requests.get(BACKEND_SERVER_ADDRESS + "/admin/banner/size?type=desktop").content
                result = json.loads(result)
                banner_sizes = result['body']

                for banner_size in banner_sizes:
                    banner_html = request.form.getlist('banners[' + str(banner_size['banner_size_width']) + '][' + str(
                        banner_size['banner_size_height']) + ']')[0]
                    if banner_html:
                        data = {
                            'banner_author_user_id': current_user.get_id(),
                            'banner_size': banner_size['banner_size_id'],
                            'banner_description': banner_html
                        }

                        result = requests.post(BACKEND_SERVER_ADDRESS + "/advertiser/banner",
                                               data=json.dumps(data)).content
                        result = json.loads(result)
                        banner_id = result['body']

                        data = {
                            'campaign': campaign_id,
                            'banner': banner_id
                        }
                        result = requests.post(BACKEND_SERVER_ADDRESS + "/advertiser/campaign/banner",
                                               data=json.dumps(data)).content
                        result = json.loads(result)
                        result = result['body']



            elif campaign["campaign_type"]["campaign_type_name"] == 'search_engine':
                form = CampaignAdwordsDescriptionForm()
                if form.validate() == False:
                    flash('All fields are required.', 'danger')
                    return render_template('campaign/step_two.html', form=form, configs=configs)
                else:
                    campaign_deactivate_function(campaign_id)
                    data = {
                        'campaign_updated_user_id': current_user.get_id(),
                        'campaign_adwords_title': form.title.data,
                        'campaign_adwords_description': form.description.data,
                        'campaign_adwords_email': form.email.data,
                        'campaign_adwords_phone': form.phone.data,
                        'campaign_adwords_address': form.address.data
                    }
                    result = requests.put(BACKEND_SERVER_ADDRESS + "/advertiser/campaign/" + str(campaign_id),
                                          data=json.dumps(data)).content
                    result = json.loads(result)
                    result = result['body']

            return redirect(url_for('advertiser_campaign_steps', campaign_id=campaign_id, campaign_step='five'))

        if campaign_step == "five":
            form = CampaignLandingPageForm()
            if form.validate() == False:
                flash('All fields are required.', 'danger')
                return render_template('campaign/step_five.html', form=form, configs=configs)
            else:
                campaign_deactivate_function(campaign_id)
                data = {
                    'campaign_updated_user_id': current_user.get_id(),
                    'campaign_landing_page_url': form.landing_page_url.data
                }
                result = requests.put(BACKEND_SERVER_ADDRESS + "/advertiser/campaign/" + str(campaign_id),
                                      data=json.dumps(data)).content
                result = json.loads(result)
                result = result['body']
                return redirect(url_for('advertiser_campaign_steps', campaign_id=campaign_id, campaign_step='six'))
        if campaign_step == "six":
            form = TargetingForm()
            campaign_deactivate_function(campaign_id)
            base_price = int(campaign["campaign_type"]["campaign_type_base_price"])
            click_price = (base_price if form.price.data is None else form.price.data)
            if click_price < base_price:
                click_price = base_price
            data = {
                'campaign_updated_user_id': current_user.get_id(),
                'campaign_targeted_geography_all': (True if form.geography.data == 'all' else False),
                'campaign_targeted_geography_iran': (True if form.geography.data == 'iran' else False),
                'campaign_targeted_geography_not_iran': (True if form.geography.data == 'not_iran' else False),
                'campaign_targeted_geography_special': (True if form.geography.data == 'special' else False),
                'campaign_targeted_operating_system_all': (True if form.operating_system.data == 'all' else False),
                'campaign_targeted_operating_system_special': (
                    True if form.operating_system.data == 'special' else False),
                'campaign_targeted_subject_all': (True if form.subject.data == 'all' else False),
                'campaign_targeted_subject_special': (True if form.subject.data == 'special' else False),
                'campaign_playtime_all': (True if form.playtime.data == 'all' else False),
                'campaign_playtime_special': (True if form.playtime.data == 'special' else False),
                'campaign_playtime_not_24_08': ((
                                                    True if 'not_24_08' in form.playtime_special.data else False) if form.playtime.data == 'special' else False),
                'campaign_playtime_not_08_16': ((
                                                    True if 'not_08_16' in form.playtime_special.data else False) if form.playtime.data == 'special' else False),
                'campaign_playtime_not_16_24': ((
                                                    True if 'not_16_24' in form.playtime_special.data else False) if form.playtime.data == 'special' else False),

                'campaign_click_price': click_price,
                'campaign_network_class_a': (True if form.site_grade.data == 'class_a' else False),
                'campaign_network_class_b': (True if form.site_grade.data == 'class_b' else False),
                'campaign_network_class_c': (True if form.site_grade.data == 'class_c' else False),
                'campaign_retargeting': (True if form.retargeting.data == 'yes' else False)
            }

            if form.geography.data == 'special':
                data['campaign_geography'] = form.states.data

            if form.operating_system.data == 'special':
                data['campaign_os'] = form.operating_systems.data

            if form.subject.data == 'special':
                data['campaign_subject'] = form.subjects.data

            if campaign["campaign_type"]["campaign_type_name"] == 'search_engine':
                data['campaign_targeted_keyword_all'] = False
                data['campaign_targeted_keyword_special'] = True
                data['campaign_keyword'] = form.keywords.data
            elif campaign["campaign_type"]["campaign_type_name"] == 'banner' or campaign["campaign_type"][
                "campaign_type_name"] == 'mobile' or campaign["campaign_type"]["campaign_type_name"] == 'native':
                data['campaign_targeted_keyword_all'] = (True if form.keyword.data == 'all' else False)
                data['campaign_targeted_keyword_special'] = (True if form.keyword.data == 'special' else False)
                if form.keyword.data == 'special':
                    data['campaign_keyword'] = form.keywords.data

            result = requests.put(BACKEND_SERVER_ADDRESS + "/advertiser/campaign/" + str(campaign_id),
                                  data=json.dumps(data)).content
            result = json.loads(result)
            result = result['body']

            if current_user.has_role('admin') and current_user.get_id() != campaign['campaign_author_user_id']:
                return redirect(url_for('campaign_admin'))

            if campaign['campaign_active_by_user']:
                return redirect(url_for('advertiser_campaign'))

            return redirect(url_for('advertiser_campaign_steps', campaign_id=campaign_id, campaign_step='seven'))
        if campaign_step == "seven":
            pass


@app.route('/dashboard/advertiser/campaign/<id>/edit', methods=['GET', 'POST'])
@login_required
@roles_accepted('advertiser')
def advertiser_campaign_edit(id):
    pass


@app.route('/dashboard/advertiser/blocked/website', methods=['GET', 'POST'])
@login_required
@roles_accepted('advertiser')
def blocked_website():
    configs = {
        'url_new': 'blocked_website_new',
        'url_edit': 'blocked_website_edit',
        'url_index': 'blocked_website',
        'module': 'لیست نمایش دهنده های مسدود',
        'action': 'لیست نمایش دهنده های مسدود',
        'url_new_text': 'اضافه کردن نمایش دهنده',
        'id_name': 'blocked_website_id',
        'page_title': 'نمایش دهنده های مسدود',
        'fields': [
            {
                'name': 'blocked_website_url',
                'title': 'آدرس',
                'order': 2,
                'hide': '',
                'width': '29%'
            },
            {
                'name': 'blocked_website_created_at',
                'title': 'تاریخ',
                'order': 3,
                'hide': '',
                'width': '29%',
                'class': 'class=defaultSort'
            }
        ]
    }
    message = None
    if request.method == 'POST':
        website = requests.get(
            BACKEND_SERVER_ADDRESS + "/advertiser/blocked/website/" + str(request.form['action'])).content
        website = json.loads(website)
        website = website['body']

        if website['blocked_website_author_user_id'] != current_user.get_id() and not current_user.has_role('admin'):
            return redirect(url_for('dashboard'))

        result = requests.delete(
            BACKEND_SERVER_ADDRESS + "/advertiser/blocked/website/" + request.form['action']).content
        result = json.loads(result)

        records = requests.get(
            BACKEND_SERVER_ADDRESS + "/advertiser/campaign?user=" + str(
                current_user.get_id()) + "&status=active").content
        records = json.loads(records)
        records = records['body']

        for record in records:
            r.srem('campaigns_blocked_website_' + urlparse(website['blocked_website_url']).hostname.replace("www.", ""),
                   record['campaign_id'])

        if result["status"] == "ok":
            message = {"type": "alert-success", "message": "رکورد با موفقیت حذف شد."}
        elif result["status"] == "nok":
            message = {"type": "alert-error", "message": "خطایی رخ داده است."}

    result = requests.get(
        BACKEND_SERVER_ADDRESS + "/advertiser/blocked/website?user=" + str(current_user.get_id())).content
    result = json.loads(result)
    result = result['body']
    return render_template('general/index.html', result=result, message=message, configs=configs)


@app.route('/dashboard/advertiser/blocked/website/new', methods=['GET', 'POST'])
@login_required
@roles_accepted('advertiser')
def blocked_website_new():
    configs = {
        'module': 'لیست نمایش دهنده های مسدود',
        'action': 'اضافه کردن نمایش دهنده',
        'url': 'blocked_website_new',
        'url_index': 'blocked_website',
        'from_id': 'advertiser-blocked-website',
        'page_title': 'اضافه کردن وب سایت'
    }
    form = BlockedWebsiteForm()
    if request.method == 'POST':
        if form.validate() == False:
            flash('All fields are required.', 'danger')
            return render_template('general/new.html', form=form, configs=configs)
        else:
            data = {
                'blocked_website_author_user_id': current_user.get_id(),
                'blocked_website_url': form.url.data
            }
            result = requests.post(BACKEND_SERVER_ADDRESS + "/advertiser/blocked/website",
                                   data=json.dumps(data)).content
            result = json.loads(result)

            records = requests.get(
                BACKEND_SERVER_ADDRESS + "/advertiser/campaign?user=" + str(
                    current_user.get_id()) + "&status=active").content
            records = json.loads(records)
            records = records['body']

            for record in records:
                r.sadd('campaigns_blocked_website_' + urlparse(form.url.data).hostname.replace("www.", ""),
                       record['campaign_id'])

            if result["status"] == "ok":
                message = json.dumps({"type": "alert-success", "message": "وب سایت با موفقیت ثبت شد."})
            elif result["status"] == "nok":
                message = json.dumps({"type": "alert-error", "message": "خطایی رخ داده است."})
            session['message'] = message

            return redirect(url_for('blocked_website_new'))
    elif request.method == 'GET':
        message = None
        if session.get('message', None) is not None:
            message = json.loads(session.pop("message"))
        return render_template('general/new.html', form=form, message=message, configs=configs)


@app.route('/dashboard/advertiser/blocked/website/<id>/edit', methods=['GET', 'POST'])
@login_required
@roles_accepted('advertiser')
def blocked_website_edit(id):
    configs = {
        'module': 'لیست نمایش دهنده های مسدود',
        'action': 'ویرایش نمایش دهنده',
        'url': 'blocked_website_edit',
        'url_index': 'blocked_website',
        'from_id': 'advertiser-blocked-website',
        'id': id,
        'page_title': 'ویرایش نمایش دهنده'
    }
    form = BlockedWebsiteForm()
    if request.method == 'POST':
        if form.validate() == False:
            flash('All fields are required.', 'danger')
            return render_template('general/edit.html', form=form, configs=configs)
        else:
            website = requests.get(BACKEND_SERVER_ADDRESS + "/advertiser/blocked/website/" + str(id)).content
            website = json.loads(website)
            website = website['body']

            if website['blocked_website_author_user_id'] != current_user.get_id() and not current_user.has_role(
                    'admin'):
                return redirect(url_for('dashboard'))

            data = {
                'blocked_website_updated_user_id': current_user.get_id(),
                'blocked_website_url': form.url.data
            }
            result = requests.put(BACKEND_SERVER_ADDRESS + "/advertiser/blocked/website/" + str(id),
                                  data=json.dumps(data)).content
            result = json.loads(result)

            records = requests.get(
                BACKEND_SERVER_ADDRESS + "/advertiser/campaign?user=" + str(
                    current_user.get_id()) + "&status=active").content
            records = json.loads(records)
            records = records['body']

            for record in records:
                r.srem(
                    'campaigns_blocked_website_' + urlparse(website['blocked_website_url']).hostname.replace("www.",
                                                                                                             ""),
                    record['campaign_id'])
                r.sadd('campaigns_blocked_website_' + urlparse(form.url.data).hostname.replace("www.", ""),
                       record['campaign_id'])

            if result["status"] == "ok":
                message = {"type": "alert-success", "message": "وب سایت با موفقیت ویرایش شد."}
            elif result["status"] == "nok":
                message = {"type": "alert-error", "message": "خطایی رخ داده است."}

            return render_template('general/edit.html', form=form, message=message, configs=configs)

    elif request.method == 'GET':
        result = requests.get(BACKEND_SERVER_ADDRESS + "/advertiser/blocked/website/" + str(id)).content
        result = json.loads(result)
        result = result['body']

        if result['blocked_website_author_user_id'] != current_user.get_id() and not current_user.has_role('admin'):
            return redirect(url_for('dashboard'))

        form.url.data = result["blocked_website_url"]

        return render_template('general/edit.html', form=form, configs=configs)


@app.route('/dashboard/publisher/website/code', methods=['GET'])
@login_required
@roles_accepted('publisher')
def publisher_website_code():
    configs = {
        'url': 'publisher_website_code',
        'url_index': 'publisher_website_code',
        'module': 'دریافت کد',
        'action': 'دریافت کد',
        'page_title': 'دریافت کد'
    }

    result = requests.get(BACKEND_SERVER_ADDRESS + "/admin/banner/size?type=desktop").content
    result = json.loads(result)
    banners = result['body']

    result = requests.get(BACKEND_SERVER_ADDRESS + "/publisher/website?user=" + str(current_user.get_id())).content
    result = json.loads(result)
    websites = result['body']

    return render_template('publisher/code/new.html', websites=websites, banners=banners, configs=configs)


@app.route('/dashboard/publisher/blocked/website', methods=['GET', 'POST'])
@login_required
@roles_accepted('publisher')
def publisher_blocked_website():
    configs = {
        'url_new': 'publisher_blocked_website_new',
        'url_edit': 'publisher_blocked_website_edit',
        'url_index': 'publisher_blocked_website',
        'module': 'لیست آگهی دهنده های مسدود',
        'action': 'لیست آگهی دهنده های مسدود',
        'url_new_text': 'اضافه کردن آگهی دهنده',
        'id_name': 'blocked_website_id',
        'page_title': 'آگهی دهنده های مسدود',
        'fields': [
            {
                'name': 'blocked_website_url',
                'title': 'آدرس',
                'order': 2,
                'hide': '',
                'width': '29%'
            },
            {
                'name': 'blocked_website_created_at',
                'title': 'تاریخ',
                'order': 3,
                'hide': '',
                'width': '29%',
                'class': 'class=defaultSort'
            }
        ]
    }
    message = None
    if request.method == 'POST':
        website = requests.get(
            BACKEND_SERVER_ADDRESS + "/advertiser/blocked/website/" + str(request.form['action'])).content
        website = json.loads(website)
        website = website['body']

        if website['blocked_website_author_user_id'] != current_user.get_id() and not current_user.has_role('admin'):
            return redirect(url_for('dashboard'))

        result = requests.delete(
            BACKEND_SERVER_ADDRESS + "/advertiser/blocked/website/" + request.form['action']).content
        result = json.loads(result)

        records = requests.get(
            BACKEND_SERVER_ADDRESS + "/publisher/website?user=" + str(
                current_user.get_id()) + "&status=active").content
        records = json.loads(records)
        records = records['body']

        campaigns = requests.get(
            BACKEND_SERVER_ADDRESS + "/advertiser/campaign/landing_page?url=" + urlparse(
                website['blocked_website_url']).hostname.replace("www.", "")).content
        campaigns = json.loads(campaigns)
        campaigns = campaigns['body']

        for record in records:
            for campaign in campaigns:
                r.srem('website_blocked_campaigns_' + urlparse(record['publisher_website_url']).hostname.replace("www.",
                                                                                                                 ""),
                       campaign)

        if result["status"] == "ok":
            message = {"type": "alert-success", "message": "رکورد با موفقیت حذف شد."}
        elif result["status"] == "nok":
            message = {"type": "alert-error", "message": "خطایی رخ داده است."}

    result = requests.get(
        BACKEND_SERVER_ADDRESS + "/advertiser/blocked/website?user=" + str(current_user.get_id())).content
    result = json.loads(result)
    result = result['body']
    return render_template('general/index.html', result=result, message=message, configs=configs)


@app.route('/dashboard/publisher/blocked/website/new', methods=['GET', 'POST'])
@login_required
@roles_accepted('publisher')
def publisher_blocked_website_new():
    configs = {
        'module': 'لیست آگهی دهنده های مسدود',
        'action': 'اضافه کردن آگهی دهنده',
        'url': 'publisher_blocked_website_new',
        'url_index': 'publisher_blocked_website',
        'from_id': 'publisher-blocked-website',
        'page_title': 'اضافه کردن وب سایت'
    }
    form = BlockedWebsiteForm()
    if request.method == 'POST':
        if form.validate() == False:
            flash('All fields are required.', 'danger')
            return render_template('general/new.html', form=form, configs=configs)
        else:
            data = {
                'blocked_website_author_user_id': current_user.get_id(),
                'blocked_website_url': form.url.data
            }
            result = requests.post(BACKEND_SERVER_ADDRESS + "/advertiser/blocked/website",
                                   data=json.dumps(data)).content
            result = json.loads(result)

            records = requests.get(
                BACKEND_SERVER_ADDRESS + "/publisher/website?user=" + str(
                    current_user.get_id()) + "&status=active").content
            records = json.loads(records)
            records = records['body']

            campaigns = requests.get(
                BACKEND_SERVER_ADDRESS + "/advertiser/campaign/landing_page?url=" + urlparse(
                    form.url.data).hostname.replace("www.", "")).content
            campaigns = json.loads(campaigns)
            campaigns = campaigns['body']

            for record in records:
                for campaign in campaigns:
                    r.sadd('website_blocked_campaigns_' + urlparse(record['publisher_website_url']).hostname.replace(
                        "www.", ""),
                           campaign)

            if result["status"] == "ok":
                message = json.dumps({"type": "alert-success", "message": "وب سایت با موفقیت ثبت شد."})
            elif result["status"] == "nok":
                message = json.dumps({"type": "alert-error", "message": "خطایی رخ داده است."})
            session['message'] = message

            return redirect(url_for('publisher_blocked_website_new'))
    elif request.method == 'GET':
        message = None
        if session.get('message', None) is not None:
            message = json.loads(session.pop("message"))
        return render_template('general/new.html', form=form, message=message, configs=configs)


@app.route('/dashboard/publisher/blocked/website/<id>/edit', methods=['GET', 'POST'])
@login_required
@roles_accepted('publisher')
def publisher_blocked_website_edit(id):
    configs = {
        'module': 'لیست آگهی دهنده های مسدود',
        'action': 'ویرایش آگهی دهنده',
        'url': 'publisher_blocked_website_edit',
        'url_index': 'publisher_blocked_website',
        'from_id': 'publisher-blocked-website',
        'id': id,
        'page_title': 'ویرایش نمایش دهنده'
    }
    form = BlockedWebsiteForm()
    if request.method == 'POST':
        if form.validate() == False:
            flash('All fields are required.', 'danger')
            return render_template('general/edit.html', form=form, configs=configs)
        else:
            website = requests.get(BACKEND_SERVER_ADDRESS + "/advertiser/blocked/website/" + str(id)).content
            website = json.loads(website)
            website = website['body']

            if website['blocked_website_author_user_id'] != current_user.get_id() and not current_user.has_role(
                    'admin'):
                return redirect(url_for('dashboard'))

            data = {
                'blocked_website_updated_user_id': current_user.get_id(),
                'blocked_website_url': form.url.data
            }
            result = requests.put(BACKEND_SERVER_ADDRESS + "/advertiser/blocked/website/" + str(id),
                                  data=json.dumps(data)).content
            result = json.loads(result)

            records = requests.get(
                BACKEND_SERVER_ADDRESS + "/publisher/website?user=" + str(
                    current_user.get_id()) + "&status=active").content
            records = json.loads(records)
            records = records['body']

            pre_campaigns = requests.get(
                BACKEND_SERVER_ADDRESS + "/advertiser/campaign/landing_page?url=" + urlparse(
                    website['blocked_website_url']).hostname.replace("www.", "")).content
            pre_campaigns = json.loads(pre_campaigns)
            pre_campaigns = pre_campaigns['body']

            campaigns = requests.get(
                BACKEND_SERVER_ADDRESS + "/advertiser/campaign/landing_page?url=" + urlparse(
                    form.url.data).hostname.replace("www.", "")).content
            campaigns = json.loads(campaigns)
            campaigns = campaigns['body']

            for record in records:
                for campaign in pre_campaigns:
                    r.srem('website_blocked_campaigns_' + urlparse(record['publisher_website_url']).hostname.replace(
                        "www.", ""),
                           campaign)

                for campaign in campaigns:
                    r.sadd('website_blocked_campaigns_' + urlparse(record['publisher_website_url']).hostname.replace(
                        "www.", ""),
                           campaign)

            if result["status"] == "ok":
                message = {"type": "alert-success", "message": "وب سایت با موفقیت ویرایش شد."}
            elif result["status"] == "nok":
                message = {"type": "alert-error", "message": "خطایی رخ داده است."}

            return render_template('general/edit.html', form=form, message=message, configs=configs)

    elif request.method == 'GET':
        result = requests.get(BACKEND_SERVER_ADDRESS + "/advertiser/blocked/website/" + str(id)).content
        result = json.loads(result)
        result = result['body']

        if result['blocked_website_author_user_id'] != current_user.get_id() and not current_user.has_role('admin'):
            return redirect(url_for('dashboard'))

        form.url.data = result["blocked_website_url"]

        return render_template('general/edit.html', form=form, configs=configs)


@app.route('/dashboard/publisher/channel/new', methods=['GET', 'POST'])
@login_required
@roles_accepted('publisher')
def publisher_channel_new():
    configs = {
        'module': 'لیست کانال ها',
        'action': 'ثبت کانال جدید',
        'url': 'publisher_channel_new',
        'url_index': 'publisher_channel',
        'from_id': 'publisher-channel-form',
        'page_title': 'ثبت کانال جدید',
    }
    form = PublisherChannelForm()
    if request.method == 'POST':
        data = {
            'publisher_channel_author_user_id': current_user.get_id(),
            'publisher_channel_title': form.title.data,
            'publisher_channel_admin_username': form.admin_username.data,
            'publisher_channel_url': form.url.data,
            'publisher_channel_description': form.description.data,
            'publisher_channel_subject': form.subjects.data,
            'publisher_channel_ad_type': form.ad_type.data
        }

        if form.geography.data:
            data['publisher_channel_geography'] = form.geography.data

        if form.picture.data:
            data['publisher_channel_picture'] = form.picture.data

        result = requests.post(BACKEND_SERVER_ADDRESS + "/publisher/channel",
                               data=json.dumps(data)).content
        result = json.loads(result)

        if result["status"] == "ok":
            message = json.dumps({"type": "alert-success", "message": "کانال شما با موفقیت ثبت شد."})
        elif result["status"] == "nok":
            message = json.dumps({"type": "alert-error", "message": "خطایی رخ داده است."})
        session['message'] = message

        return redirect(url_for('publisher_channel_new'))
    elif request.method == 'GET':
        result = requests.get(BACKEND_SERVER_ADDRESS + "/admin/advertising/type?type=telegram").content
        result = json.loads(result)
        result = result['body']
        records = [(record["type_id"], record["type_title"]) for record in result]
        form.ad_type.choices = records

        ad_type = []
        form.ad_type.data = ad_type

        result = requests.get(BACKEND_SERVER_ADDRESS + "/admin/target/subject?type=telegram").content
        result = json.loads(result)
        result = result['body']
        records = [(record["subject_id"], record["subject_title"]) for record in result]
        form.subjects.choices = records

        subjects = []
        form.subjects.data = subjects

        result = requests.get(BACKEND_SERVER_ADDRESS + "/admin/target/geography").content
        result = json.loads(result)
        result = result['body']
        records = []
        records.append(('', 'همه استان ها'))
        for record in result:
            records.append((record["geography_id"], record["geography_title"]))
        form.geography.choices = records

        message = None
        if session.get('message', None) is not None:
            message = json.loads(session.pop("message"))

        return render_template('general/new.html', form=form, message=message, configs=configs)


@app.route('/dashboard/publisher/channel/<id>/edit', methods=['GET', 'POST'])
@login_required
@roles_accepted('publisher')
def publisher_channel_edit(id):
    configs = {
        'module': 'لیست کانال ها',
        'action': 'ویرایش کانال',
        'url': 'publisher_channel_edit',
        'url_index': 'publisher_channel',
        'from_id': 'publisher-channel-form',
        'id': id,
        'page_title': 'ویرایش کانال',
    }
    form = PublisherChannelForm()
    if request.method == 'POST':
        result = requests.get(BACKEND_SERVER_ADDRESS + "/publisher/channel/" + str(id)).content
        result = json.loads(result)
        result = result['body']

        if result['publisher_channel_author_user_id'] != current_user.get_id() and not current_user.has_role(
                'admin'):
            return redirect(url_for('dashboard'))

        data = {
            'publisher_channel_updated_user_id': current_user.get_id(),
            'publisher_channel_title': form.title.data,
            'publisher_channel_admin_username': form.admin_username.data,
            'publisher_channel_url': form.url.data,
            'publisher_channel_description': form.description.data,
            'publisher_channel_subject': form.subjects.data,
            'publisher_channel_ad_type': form.ad_type.data
        }

        if form.geography.data:
            data['publisher_channel_geography'] = form.geography.data
        else:
            data['publisher_channel_geography'] = None

        if form.picture.data:
            data['publisher_channel_picture'] = form.picture.data

        result = requests.put(BACKEND_SERVER_ADDRESS + "/publisher/channel/" + str(id),
                              data=json.dumps(data)).content
        result = json.loads(result)

        if result["status"] == "ok":
            message = {"type": "alert-success", "message": "کانال شما با موفقیت ویرایش شد."}
        elif result["status"] == "nok":
            message = {"type": "alert-error", "message": "خطایی رخ داده است."}

        return redirect(url_for('publisher_channel_edit', id=id))

    elif request.method == 'GET':
        result = requests.get(BACKEND_SERVER_ADDRESS + "/publisher/channel/" + str(id)).content
        result = json.loads(result)
        channel = result['body']

        if channel['publisher_channel_author_user_id'] != current_user.get_id() and not current_user.has_role('admin'):
            return redirect(url_for('dashboard'))

        result = requests.get(BACKEND_SERVER_ADDRESS + "/admin/advertising/type?type=telegram").content
        result = json.loads(result)
        result = result['body']
        records = [(record["type_id"], record["type_title"]) for record in result]
        form.ad_type.choices = records

        ad_type = []
        records = requests.get(
            BACKEND_SERVER_ADDRESS + "/publisher/channel/advertising/type?channel=" + str(id)).content
        records = json.loads(records)
        records = records['body']
        for record in records:
            ad_type.append(record["type"]["type_id"])
        form.ad_type.data = ad_type

        result = requests.get(BACKEND_SERVER_ADDRESS + "/admin/target/subject?type=telegram").content
        result = json.loads(result)
        result = result['body']
        records = [(record["subject_id"], record["subject_title"]) for record in result]
        form.subjects.choices = records

        subjects = []
        records = requests.get(
            BACKEND_SERVER_ADDRESS + "/publisher/channel/subject?channel=" + str(id)).content
        records = json.loads(records)
        records = records['body']
        for record in records:
            subjects.append(record["subject"]["subject_id"])
        form.subjects.data = subjects

        result = requests.get(BACKEND_SERVER_ADDRESS + "/admin/target/geography").content
        result = json.loads(result)
        result = result['body']
        records = []
        records.append(('', 'همه استان ها'))
        for record in result:
            records.append((record["geography_id"], record["geography_title"]))
        form.geography.choices = records

        form.geography.data = str(channel['publisher_channel_geography']['geography_id'])

        form.title.data = channel['publisher_channel_title']
        form.admin_username.data = channel['publisher_channel_admin_username']
        form.url.data = channel['publisher_channel_url']
        form.description.data = channel['publisher_channel_description']
        form.picture.data = channel['publisher_channel_picture']

        message = None
        if session.get('message', None) is not None:
            message = json.loads(session.pop("message"))

        return render_template('general/edit.html', form=form, configs=configs, message=message)


@app.route('/dashboard/publisher/channel', methods=['GET', 'POST'])
@login_required
@roles_accepted('publisher')
def publisher_channel():
    configs = {
        'url_new': 'publisher_channel_new',
        'url_edit': 'publisher_channel_edit',
        'url_index': 'publisher_channel',
        'module': 'لیست کانال ها',
        'action': 'لیست کانال ها',
        'url_new_text': 'ثبت کانال جدید',
        'id_name': 'publisher_channel_id',
        'page_title': 'کانال های من'
    }
    message = None
    if request.method == 'POST':
        result = requests.get(BACKEND_SERVER_ADDRESS + "/publisher/channel/" + str(request.form['action'])).content
        result = json.loads(result)
        result = result['body']

        if result['publisher_channel_author_user_id'] != current_user.get_id() and not current_user.has_role('admin'):
            return redirect(url_for('dashboard'))

        data = {
            'publisher_channel_updated_user_id': current_user.get_id(),
            'publisher_channel_is_deleted': True
        }
        result = requests.put(BACKEND_SERVER_ADDRESS + "/publisher/channel/" + request.form['action'],
                              data=json.dumps(data)).content
        result = json.loads(result)

        if result["status"] == "ok":
            message = {"type": "alert-success", "message": "رکورد با موفقیت حذف شد."}
        elif result["status"] == "nok":
            message = {"type": "alert-error", "message": "خطایی رخ داده است."}

    result = requests.get(BACKEND_SERVER_ADDRESS + "/publisher/channel?user=" + str(current_user.get_id())).content
    result = json.loads(result)
    result = result['body']
    return render_template('publisher/channel/index.html', result=result, message=message, configs=configs)


@app.route('/dashboard/publisher/website', methods=['GET', 'POST'])
@login_required
@roles_accepted('publisher')
def publisher_website():
    configs = {
        'url_new': 'publisher_website_new',
        'url_edit': 'publisher_website_edit',
        'url_index': 'publisher_website',
        'module': 'لیست وب سایت ها',
        'action': 'لیست وب سایت ها',
        'url_new_text': 'ثبت وب سایت جدید',
        'id_name': 'publisher_website_id',
        'page_title': 'سایت های من'
    }
    message = None
    if request.method == 'POST':
        result = requests.get(BACKEND_SERVER_ADDRESS + "/publisher/website/" + str(request.form['action'])).content
        result = json.loads(result)
        result = result['body']

        if result['publisher_website_author_user_id'] != current_user.get_id() and not current_user.has_role('admin'):
            return redirect(url_for('dashboard'))

        website_deactivate_function(request.form['action'])

        data = {
            'publisher_website_updated_user_id': current_user.get_id(),
            'publisher_website_is_deleted': True
        }
        result = requests.put(BACKEND_SERVER_ADDRESS + "/publisher/website/" + request.form['action'],
                              data=json.dumps(data)).content
        result = json.loads(result)

        if result["status"] == "ok":
            message = {"type": "alert-success", "message": "رکورد با موفقیت حذف شد."}
        elif result["status"] == "nok":
            message = {"type": "alert-error", "message": "خطایی رخ داده است."}

    result = requests.get(BACKEND_SERVER_ADDRESS + "/publisher/website?user=" + str(current_user.get_id())).content
    result = json.loads(result)
    result = result['body']
    return render_template('publisher/website/index.html', result=result, message=message, configs=configs)


@app.route('/dashboard/publisher/website/new', methods=['GET', 'POST'])
@login_required
@roles_accepted('publisher')
def publisher_website_new():
    configs = {
        'module': 'لیست وب سایت ها',
        'action': 'ثبت وب سایت جدید',
        'url': 'publisher_website_new',
        'url_index': 'publisher_website',
        'from_id': 'publisher-website-form',
        'page_title': 'ثبت وب سایت جدید',
    }
    form = PublisherWebsiteForm()
    if request.method == 'POST':
        data = {
            'publisher_website_url': urlparse(form.url.data).hostname.replace("www.", "")
        }

        result = requests.post(BACKEND_SERVER_ADDRESS + "/publisher/website/unique/check",
                               data=json.dumps(data)).content
        result = json.loads(result)
        result = result['body']

        if result > 0:
            message = json.dumps({"type": "alert-error", "message": "این وب سایت قبلا ثبت شده است."})
            session['message'] = message
            return redirect(url_for('publisher_website_new'))

        data = {
            'publisher_website_author_user_id': current_user.get_id(),
            'publisher_website_title': form.title.data,
            'publisher_website_type': form.type.data,
            'publisher_website_url': form.url.data,
            'publisher_website_subject': form.subjects.data
        }
        result = requests.post(BACKEND_SERVER_ADDRESS + "/publisher/website",
                               data=json.dumps(data)).content
        result = json.loads(result)

        if result["status"] == "ok":
            message = json.dumps({"type": "alert-success", "message": "وب سایت شما با موفقیت ثبت شد."})
        elif result["status"] == "nok":
            message = json.dumps({"type": "alert-error", "message": "خطایی رخ داده است."})
        session['message'] = message

        return redirect(url_for('publisher_website_new'))
    elif request.method == 'GET':
        result = requests.get(BACKEND_SERVER_ADDRESS + "/admin/target/subject").content
        result = json.loads(result)
        result = result['body']
        records = [(record["subject_id"], record["subject_title"]) for record in result]
        form.subjects.choices = records

        subjects = []
        form.subjects.data = subjects
        form.type.data = "banner"

        message = None
        if session.get('message', None) is not None:
            message = json.loads(session.pop("message"))

        return render_template('general/new.html', form=form, message=message, configs=configs)


@app.route('/dashboard/publisher/website/<id>/edit', methods=['GET', 'POST'])
@login_required
@roles_accepted('publisher')
def publisher_website_edit(id):
    configs = {
        'module': 'لیست وب سایت ها',
        'action': 'ویرایش وب سایت',
        'url': 'publisher_website_edit',
        'url_index': 'publisher_website',
        'from_id': 'publisher-website-form',
        'id': id,
        'page_title': 'ویرایش وب سایت',
    }
    form = PublisherWebsiteForm()
    if request.method == 'POST':
        result = requests.get(BACKEND_SERVER_ADDRESS + "/publisher/website/" + str(id)).content
        result = json.loads(result)
        result = result['body']

        if result['publisher_website_author_user_id'] != current_user.get_id() and not current_user.has_role(
                'admin'):
            return redirect(url_for('dashboard'))

        website_deactivate_function(id)
        data = {
            'publisher_website_updated_user_id': current_user.get_id(),
            'publisher_website_title': form.title.data,
            'publisher_website_type': form.type.data,
            'publisher_website_url': form.url.data,
            'publisher_website_subject': form.subjects.data
        }
        result = requests.put(BACKEND_SERVER_ADDRESS + "/publisher/website/" + str(id),
                              data=json.dumps(data)).content
        result = json.loads(result)

        if result["status"] == "ok":
            message = {"type": "alert-success", "message": "وب سایت با موفقیت ویرایش شد."}
        elif result["status"] == "nok":
            message = {"type": "alert-error", "message": "خطایی رخ داده است."}

        return redirect(url_for('publisher_website_edit', id=id))

    elif request.method == 'GET':
        result = requests.get(BACKEND_SERVER_ADDRESS + "/publisher/website/" + str(id)).content
        result = json.loads(result)
        result = result['body']

        if result['publisher_website_author_user_id'] != current_user.get_id() and not current_user.has_role('admin'):
            return redirect(url_for('dashboard'))

        form.title.data = result["publisher_website_title"]
        form.type.data = result["publisher_website_type"]
        form.url.data = result["publisher_website_url"]

        result = requests.get(BACKEND_SERVER_ADDRESS + "/admin/target/subject").content
        result = json.loads(result)
        result = result['body']
        records = [(record["subject_id"], record["subject_title"]) for record in result]
        form.subjects.choices = records

        subjects = []
        records = requests.get(
            BACKEND_SERVER_ADDRESS + "/publisher/website/subject?website=" + str(id)).content
        records = json.loads(records)
        records = records['body']
        for record in records:
            subjects.append(record["subject"]["subject_id"])
        form.subjects.data = subjects

        message = None
        # if session.get('message', None) is not None:
        #     message = json.loads(session.pop("message"))

        return render_template('general/edit.html', form=form, configs=configs, message=message)


@app.route('/dashboard/user/<user_id>/transaction', methods=['GET', 'POST'])
@app.route('/dashboard/user/transaction', methods=['GET', 'POST'])
@login_required
def financial_transaction(user_id=None):
    configs = {
        'url_index': 'financial_transaction',
        'module': 'لیست تراکنش های مالی',
        'action': 'لیست تراکنش های مالی',
        'id_name': 'transaction_id',
        'page_title': 'لیست تراکنش های مالی'
    }
    if request.method == 'POST':
        message = requests.delete(BACKEND_SERVER_ADDRESS + "/financial/transaction/" + request.form['action'])

    if user_id is None:
        user_id = current_user.get_id()
    result = requests.get(BACKEND_SERVER_ADDRESS + "/financial/transaction?user=" + str(user_id)).content
    result = json.loads(result)
    result = result['body']

    message = None
    if session.get('message', None) is not None:
        message = json.loads(session.pop("message"))

    return render_template('financial/index.html', result=result, message=message, configs=configs)


@app.route('/dashboard/admin/credit/request', methods=['GET', 'POST'])
@login_required
@roles_accepted('admin')
def credit_request_admin():
    configs = {
        'url_new': 'credit_request_admin_new',
        'url_edit': 'credit_request_admin_edit',
        'url_index': 'credit_request_admin',
        'module': 'لیست درخواست های برداشت',
        'action': 'لیست درخواست های برداشت',
        'url_new_text': 'درخواست جدید',
        'id_name': 'request_id',
        'page_title': 'درخواست های برداشت'
    }
    message = None
    if request.method == 'POST':
        result = requests.delete(
            BACKEND_SERVER_ADDRESS + "/financial/user/credit/request/" + request.form['action']).content
        result = json.loads(result)
        if result["status"] == "ok":
            message = {"type": "alert-success", "message": "رکورد با موفقیت حذف شد."}
        elif result["status"] == "nok":
            message = {"type": "alert-error", "message": "خطایی رخ داده است."}

    result = requests.get(BACKEND_SERVER_ADDRESS + "/financial/user/credit/request").content
    result = json.loads(result)
    result = result['body']

    ids = []
    for query in result:
        ids.append(query["request_author_user_id"])

    authors = users(ids)
    authors = json.loads(authors)
    authors = authors['body']

    return render_template('admin/financial/index.html', result=result, authors=authors, message=message,
                           configs=configs)


@app.route('/dashboard/admin/credit/request/new', methods=['GET', 'POST'])
@login_required
@roles_accepted('admin')
def credit_request_admin_new():
    pass


@app.route('/dashboard/admin/credit/request/<id>/edit', methods=['GET', 'POST'])
@login_required
@roles_accepted('admin')
def credit_request_admin_edit(id):
    configs = {
        'module': 'لیست درخواست های برداشت',
        'action': 'ویرایش درخواست',
        'url': 'credit_request_admin_edit',
        'url_index': 'credit_request_admin',
        'from_id': 'credit_request_admin',
        'id': id
    }
    form = CreditRequestAdminForm()
    if request.method == 'POST':
        if form.validate() == False:
            flash('All fields are required.', 'danger')
            return render_template('general/edit.html', form=form, configs=configs)
        else:
            if form.amount_paid.data == '':
                data = {
                    'request_updated_user_id': current_user.get_id(),
                    'request_status': form.status.data,
                    'request_description': form.description.data
                }
                result = requests.put(BACKEND_SERVER_ADDRESS + "/financial/user/credit/request/" + str(id),
                                      data=json.dumps(data)).content

                result = requests.get(BACKEND_SERVER_ADDRESS + "/financial/user/credit/request/" + str(id)).content
                result = json.loads(result)

                if result["status"] == "ok":
                    message = {"type": "alert-success", "message": "درخواست با موفقیت ویرایش شد."}
                elif result["status"] == "nok":
                    message = {"type": "alert-error", "message": "خطایی رخ داده است."}

            elif (int(form.amount_paid.data) > 0) and (int(form.amount_paid.data) <= int(form.amount.data)):
                data = {
                    'request_updated_user_id': current_user.get_id(),
                    'request_amount': form.amount.data,
                    'request_amount_paid': form.amount_paid.data,
                    'request_status': 'paid',
                    'request_description': form.description.data
                }
                result = requests.put(BACKEND_SERVER_ADDRESS + "/financial/user/credit/request/" + str(id),
                                      data=json.dumps(data)).content

                result = requests.get(BACKEND_SERVER_ADDRESS + "/financial/user/credit/request/" + str(id)).content
                result = json.loads(result)
                result = result['body']

                data = {
                    'transaction_author_user_id': result['request_author_user_id'],
                    'transaction_updated_user_id': current_user.get_id(),
                    'transaction_deposit_amount': 0,
                    'transaction_withdrawal_amount': int(form.amount.data),
                    'transaction_description': 'درخواست برداشت توسط کاربر',
                    'transaction_status': 1
                }
                result = requests.post(BACKEND_SERVER_ADDRESS + "/financial/transaction",
                                       data=json.dumps(data)).content
                result = json.loads(result)

                if result["status"] == "ok":
                    message = {"type": "alert-success", "message": "درخواست با موفقیت ویرایش شد."}
                elif result["status"] == "nok":
                    message = {"type": "alert-error", "message": "خطایی رخ داده است."}
            else:
                if int(form.amount_paid.data) > int(form.amount.data):
                    message = {"type": "", "message": "مبلغ واریز شده نمی تواند بیشتر از مبلغ درخواستی باشد."}
                if int(form.amount_paid.data) <= 0:
                    message = {"type": "", "message": "مبلغ واریز شده باید بیشتر از صفر باشد."}
                print "test"

            return render_template('general/edit.html', form=form, message=message, configs=configs)
    elif request.method == 'GET':
        result = requests.get(BACKEND_SERVER_ADDRESS + "/financial/user/credit/request/" + str(id)).content
        result = json.loads(result)
        result = result['body']

        form.amount.data = result["request_amount"]
        form.amount_paid.data = result["request_amount_paid"]
        form.status.data = result["request_status"]
        form.description.data = result["request_description"]

        return render_template('general/edit.html', form=form, configs=configs)


@app.route('/dashboard/publisher/credit/request', methods=['GET', 'POST'])
@roles_accepted('publisher')
@login_required
def credit_request():
    configs = {
        'url_new': 'credit_request_new',
        'url_edit': 'credit_request_edit',
        'url_index': 'credit_request',
        'module': 'لیست درخواست ها',
        'action': 'لیست درخواست ها',
        'url_new_text': 'ثبت درخواست جدید',
        'id_name': 'request_id',
        'page_title': 'درخواست های برداشت'
    }

    message = None
    if request.method == 'POST':
        result = requests.get(
            BACKEND_SERVER_ADDRESS + "/financial/user/credit/request/" + str(request.form['action'])).content
        result = json.loads(result)
        result = result['body']

        if result['request_author_user_id'] != current_user.get_id():
            return redirect(url_for('dashboard'))

        if result['request_amount_paid']:
            message = json.dumps({"type": "alert-error", "message": "این رکورد را نمی توانید حذف کنید."})
            session['message'] = message
            return redirect(url_for('credit_request'))

        result = requests.delete(
            BACKEND_SERVER_ADDRESS + "/financial/user/credit/request/" + request.form['action']).content
        result = json.loads(result)

        if result["status"] == "ok":
            message = {"type": "alert-success", "message": "رکورد با موفقیت حذف شد."}
        elif result["status"] == "nok":
            message = {"type": "alert-error", "message": "خطایی رخ داده است."}

    result = requests.get(
        BACKEND_SERVER_ADDRESS + "/financial/user/credit/request?user=" + str(current_user.get_id())).content
    result = json.loads(result)
    result = result['body']

    message = None
    if session.get('message', None) is not None:
        message = json.loads(session.pop("message"))

    return render_template('financial/user/index.html', result=result, message=message, configs=configs)


@app.route('/dashboard/publisher/credit/request/new', methods=['GET', 'POST'])
@roles_accepted('publisher')
@login_required
def credit_request_new():
    configs = {
        'module': 'لیست درخواست های برداشت',
        'action': 'ثبت درخواست برداشت',
        'url': 'credit_request_new',
        'url_index': 'credit_request',
        'from_id': 'publisher-credit-request-form',
        'page_title': 'ثبت درخواست برداشت'
    }
    form = CreditRequestForm()
    if request.method == 'POST':
        if form.validate() == False:
            flash('All fields are required.', 'danger')
            return render_template('financial/request.html', form=form, configs=configs)
        else:

            curr_user = current_user.get_id()

            user_bank_account = UserBankAccountRests()
            result = user_bank_account.get(curr_user)
            result = json.loads(result)
            user_bank_account = result['body']

            try:
                if user_bank_account['shaba_code'] == '' or user_bank_account['bank_account_number'] == '' or \
                                user_bank_account['bank_card_number'] == '':
                    message = json.dumps({"type": "alert-error", "message": "لطفا اطلاعات مالی خود را کامل کنید."})
                    session['message'] = message
                    return redirect(url_for('credit_request_new'))
            except Exception:
                message = json.dumps({"type": "alert-error", "message": "لطفا اطلاعات مالی خود را کامل کنید."})
                session['message'] = message
                return redirect(url_for('credit_request_new'))

            data = {
                'request_author_user_id': curr_user,
                'request_amount': form.amount.data.replace(",", "")
            }
            result = requests.post(BACKEND_SERVER_ADDRESS + "/financial/user/credit/request",
                                   data=json.dumps(data)).content
            result = json.loads(result)

            if result["status"] == "ok":
                message = json.dumps({"type": "alert-success", "message": "درخواست شما با موفقیت ارسال شد."})
            elif result["status"] == "nok":
                message = json.dumps({"type": "alert-error", "message": "خطایی رخ داده است."})
            session['message'] = message
            return redirect(url_for('credit_request_new'))

    elif request.method == 'GET':
        message = None
        if session.get('message', None) is not None:
            message = json.loads(session.pop("message"))

        return render_template('financial/request.html', form=form,
                               configs=configs, message=message)


@app.route('/dashboard/publisher/credit/request/<id>/edit', methods=['GET', 'POST'])
@roles_accepted('publisher')
@login_required
def credit_request_edit(id):
    configs = {
        'module': 'لیست درخواست های برداشت',
        'action': 'ویرایش درخواست برداشت',
        'url': 'credit_request_edit',
        'url_index': 'credit_request',
        'from_id': 'publisher-credit-request-form',
        'page_title': 'ویرایش درخواست برداشت',
        'id': id
    }

    result = requests.get(
        BACKEND_SERVER_ADDRESS + "/financial/user/credit/request/" + str(id)).content
    result = json.loads(result)
    result = result['body']

    if result['request_author_user_id'] != current_user.get_id():
        return redirect(url_for('dashboard'))

    if result['request_amount_paid']:
        message = json.dumps({"type": "alert-error", "message": "این رکورد را نمی توانید ویرایش کنید."})
        session['message'] = message
        return redirect(url_for('credit_request'))

    form = CreditRequestForm()

    if request.method == 'POST':
        if form.validate() == False:
            flash('All fields are required.', 'danger')
            return render_template('financial/request_edit.html', form=form, configs=configs)
        else:

            curr_user = current_user.get_id()

            data = {
                'request_updated_user_id': curr_user,
                'request_amount': form.amount.data.replace(",", "")
            }
            result = requests.put(BACKEND_SERVER_ADDRESS + "/financial/user/credit/request/" + str(id),
                                  data=json.dumps(data)).content
            result = json.loads(result)

            if result["status"] == "ok":
                message = json.dumps({"type": "alert-success", "message": "درخواست با موفقیت ویرایش شد."})
            elif result["status"] == "nok":
                message = json.dumps({"type": "alert-error", "message": "خطایی رخ داده است."})
            session['message'] = message
            return redirect(url_for('credit_request_edit', id=id))

    if request.method == 'GET':
        message = None
        if session.get('message', None) is not None:
            message = json.loads(session.pop("message"))

        form.amount.data = result['request_amount']

        return render_template('financial/request_edit.html', form=form,
                               configs=configs, message=message)


@app.route('/dashboard/advertiser/credit/charge', methods=['GET', 'POST'])
@roles_accepted('advertiser')
@login_required
def credit_charge():
    configs = {
        'module': 'لیست تراکنش های مالی',
        'action': 'افزایش اعتبار',
        'url': 'credit_charge',
        'url_index': 'financial_transaction',
        'from_id': 'advertiser-credit-charge-form',
        'page_title': 'افزایش اعتبار'
    }
    form = CreditForm()
    if request.method == 'POST':
        if form.validate() == False:
            flash('All fields are required.', 'danger')
            return render_template('general/new.html', form=form, configs=configs)
        else:
            client = Client(ZARINPAL_WEBSERVICE)
            amount = form.amount.data.replace(",", "")
            amount = int(amount) / 10
            description = u'افزایش اعتبار'
            email = ''
            mobile = ''
            service_result = client.service.PaymentRequest(MMERCHANT_ID,
                                                           amount,
                                                           description,
                                                           email,
                                                           mobile,
                                                           str(url_for('credit_verify', _external=True)))

            data = {
                'transaction_author_user_id': current_user.get_id(),
                'transaction_updated_user_id': current_user.get_id(),
                'transaction_deposit_amount': amount * 10,
                'transaction_withdrawal_amount': 0,
                'transaction_first_status': service_result.Status,
                'transaction_authority': service_result.Authority,
                'transaction_status': 0
            }

            result = requests.post(BACKEND_SERVER_ADDRESS + "/financial/transaction",
                                   data=json.dumps(data)).content
            result = json.loads(result)
            result = result['body']

            if service_result.Status == 100:
                return redirect('https://www.zarinpal.com/pg/StartPay/' + service_result.Authority)
            else:
                return 'Error'
                # return render_template('general/new.html', form=form, result=result, configs=configs)

    elif request.method == 'GET':
        if request.args.get('credit'):
            form.amount.data = request.args.get('credit')

        message = None
        if session.get('message', None) is not None:
            message = json.loads(session.pop("message"))

        return render_template('financial/new.html', form=form, message=message, configs=configs)


@app.route('/dashboard/advertiser/credit/verify', methods=['GET', 'POST'])
def credit_verify():
    client = Client(ZARINPAL_WEBSERVICE)
    data = {}
    if request.args.get('Status') == 'OK':
        transaction = requests.get(
            BACKEND_SERVER_ADDRESS + "/financial/transaction/" + str(request.args['Authority'])).content
        transaction = json.loads(transaction)
        transaction = transaction['body']

        service_result = client.service.PaymentVerification(MMERCHANT_ID,
                                                            request.args['Authority'],
                                                            int(transaction["transaction_deposit_amount"]) / 10)
        data['transaction_updated_user_id'] = transaction['transaction_author_user_id']
        if service_result.Status == 100:
            data['transaction_second_status'] = service_result.Status
            data['transaction_reference_id'] = service_result.RefID
            data['transaction_description'] = 'درگاه پرداخت زرین پال'
            data['transaction_status'] = 1

            result = requests.put(BACKEND_SERVER_ADDRESS + "/financial/transaction/" + str(request.args['Authority']),
                                  data=json.dumps(data)).content
            result = json.loads(result)

            if result["status"] == "ok":
                message = json.dumps({"type": "alert-success", "message": "پرداخت شما با موفقیت انجام شد."})
            elif result["status"] == "nok":
                message = json.dumps({"type": "alert-error", "message": "خطایی رخ داده است."})
            session['message'] = message
            return redirect(url_for('financial_transaction'))


        elif service_result.Status == 101:
            data['transaction_second_status'] = service_result.Status
            data['transaction_description'] = 'ZarinPal Transaction Submitted.'
            data['transaction_status'] = 0
            result = requests.put(BACKEND_SERVER_ADDRESS + "/financial/transaction/" + str(request.args['Authority']),
                                  data=json.dumps(data)).content
            message = json.dumps({"type": "alert-danger", "message": "روند پرداخت با خطا مواجه شد."})
            session['message'] = message
            return redirect(url_for('credit_charge'))

        else:
            data['transaction_second_status'] = service_result.Status
            data['transaction_description'] = 'ZarinPal Transaction Failed.'
            data['transaction_status'] = 0
            result = requests.put(BACKEND_SERVER_ADDRESS + "/financial/transaction/" + str(request.args['Authority']),
                                  data=json.dumps(data)).content
            message = json.dumps({"type": "alert-danger", "message": "روند پرداخت با خطا مواجه شد."})
            session['message'] = message
            return redirect(url_for('credit_charge'))
    else:
        data['transaction_second_status'] = 'NOK'
        data['transaction_description'] = 'ZarinPal Transaction Failed or Canceled by User'
        data['transaction_status'] = 0
        result = requests.put(BACKEND_SERVER_ADDRESS + "/financial/transaction/" + str(request.args['Authority']),
                              data=json.dumps(data)).content

        message = json.dumps({"type": "alert-danger", "message": "روند پرداخت با خطا مواجه شد."})
        session['message'] = message
        return redirect(url_for('credit_charge'))


@app.route('/dashboard/advertiser', methods=['GET', 'POST'])
@login_required
@roles_accepted('advertiser')
def advertiser_dashboard():
    configs = {
        'module': 'داشبورد آگهی دهنده',
        'action': 'داشبورد',
        'url_index': 'advertiser_dashboard',
        'page_title': 'داشبورد'
    }

    date = datetime.now()

    if request.method == 'GET':
        to_date = date.strptime(date.strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")
        from_date = to_date - dateutil.relativedelta.relativedelta(days=4)

    elif request.method == 'POST':
        to_date = date.strptime(persian_date_to_gregorian_date(request.form['to_date']) + " 23:59:59",
                                "%Y-%m-%d %H:%M:%S")
        from_date = date.strptime(persian_date_to_gregorian_date(request.form['from_date']) + " 00:00:00",
                                  "%Y-%m-%d %H:%M:%S")
        delta = to_date - from_date
        if delta.days > 5:
            message = json.dumps({"type": "alert-error", "message": "بازه گزارش باید بین 5 روز باشد."})
            session['message'] = message
            return (redirect(url_for("advertiser_dashboard")))

    data = {
        'from_date': str(from_date),
        'to_date': str(to_date),
        'user': current_user.get_id()
    }

    result = requests.post(BACKEND_SERVER_ADDRESS + "/reports/advertiser/dashboard/period",
                           data=json.dumps(data)).content
    result = json.loads(result)
    dashboard = result['body']

    result = requests.get(
        BACKEND_SERVER_ADDRESS + "/advertiser/campaign?user=" + str(current_user.get_id()) + "&status=active").content
    result = json.loads(result)
    campaigns = result['body']
    remaining_budget = 0
    for campaign in campaigns:
        redis_set_budget = r.smembers('campaign_total_budget_' + str(campaign['campaign_id']))
        campaign_budget = 0
        if len(list(redis_set_budget)) > 0:
            campaign_budget = int(float(list(redis_set_budget)[0]))
        remaining_budget = remaining_budget + campaign_budget

    dashboard["remaining_budget"] = remaining_budget

    clicks = OrderedDict(sorted(dashboard["clicks"].items(), key=lambda t: t[0]))
    shows = OrderedDict(sorted(dashboard["shows"].items(), key=lambda t: t[0]))

    message = None
    if session.get('message', None) is not None:
        message = json.loads(session.pop("message"))

    return render_template('dashboard/advertiser/index.html',
                           to_date=str(to_date)[:10],
                           from_date=str(from_date)[:10],
                           message=message,
                           clicks=clicks,
                           shows=shows,
                           dashboard=dashboard,
                           configs=configs)


@app.route('/dashboard/advertiser/campaign/<campaign_id>/statistics', methods=['GET', 'POST'])
@login_required
@roles_accepted('advertiser')
def advertiser_dashboard_statistics(campaign_id):
    campaign = requests.get(BACKEND_SERVER_ADDRESS + "/advertiser/campaign/" + str(campaign_id)).content
    campaign = json.loads(campaign)
    campaign = campaign['body']

    if campaign['campaign_author_user_id'] != current_user.get_id() and not current_user.has_role('admin'):
        return redirect(url_for('dashboard'))

    configs = {
        'module': 'کمپین های من',
        'action': 'آمار ماهیانه کمپین' + ' "' + str(campaign['campaign_name']) + '"',
        'url_index': 'advertiser_campaign',
        'campaign_id': campaign_id
    }

    date = datetime.now()
    if request.method == 'GET':
        to_date = date.strptime(date.strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")
        from_date = to_date - dateutil.relativedelta.relativedelta(days=10)
    elif request.method == 'POST':
        to_date = date.strptime(persian_date_to_gregorian_date(request.form['to_date']) + " 23:59:59",
                                "%Y-%m-%d %H:%M:%S")
        from_date = date.strptime(persian_date_to_gregorian_date(request.form['from_date']) + " 00:00:00",
                                  "%Y-%m-%d %H:%M:%S")

    data = {
        'from_date': str(from_date),
        'to_date': str(to_date),
        'campaign': campaign_id
    }
    result = requests.post(BACKEND_SERVER_ADDRESS + "/reports/advertiser/click/period",
                           data=json.dumps(data)).content
    result = json.loads(result)
    clicks = result['body']

    result = requests.post(BACKEND_SERVER_ADDRESS + "/reports/advertiser/show/period",
                           data=json.dumps(data)).content
    result = json.loads(result)
    shows = result['body']

    clicks_shows = {}
    delta = to_date - from_date

    for i in range(0, delta.days + 1):
        tmp_date = to_date - dateutil.relativedelta.relativedelta(days=i)
        tmp_date = tmp_date.strftime('%Y-%m-%d')
        z = datetime(int(tmp_date[:4]), int(tmp_date[5:7]), int(tmp_date[8:10]), 0, 0, 0)
        unixtime = calendar.timegm(z.timetuple())
        unixtime = str(unixtime)
        unixtime = unixtime[:10]
        clicks_shows[unixtime] = {"click": clicks.get(unixtime + "000", 0), "show": shows.get(unixtime + "000", 0)}

    clicks_shows = OrderedDict(sorted(clicks_shows.items(), reverse=True, key=lambda t: t[0]))

    clicks = OrderedDict(sorted(clicks.items(), key=lambda t: t[0]))
    shows = OrderedDict(sorted(shows.items(), key=lambda t: t[0]))

    return render_template('dashboard/advertiser/statistics.html', clicks=clicks, shows=shows,
                           clicks_shows=clicks_shows,
                           to_date=str(to_date)[:10],
                           from_date=str(from_date)[:10],
                           configs=configs)


@app.route('/dashboard/advertiser/campaign/<campaign_id>/day/<day>/statistics', methods=['GET', 'POST'])
@login_required
@roles_accepted('advertiser')
def advertiser_dashboard_daily_statistics(campaign_id, day):
    campaign = requests.get(BACKEND_SERVER_ADDRESS + "/advertiser/campaign/" + str(campaign_id)).content
    campaign = json.loads(campaign)
    campaign = campaign['body']

    configs = {
        'module': 'داشبورد آگهی دهنده',
        'action': 'جزئیات نمایش کمپین' + ' "' + campaign['campaign_name'] + '"',
        'url_index': 'advertiser_dashboard',
        'campaign_id': campaign_id,
        'day': day,
        'campaign_name': campaign['campaign_name']
    }

    date = time.strftime("%Y-%m-%d", time.localtime(float(day)))
    data = {
        'from_date': date + " 00:00:00",
        'to_date': date + " 23:59:59",
        'campaign': campaign_id
    }
    result = requests.post(BACKEND_SERVER_ADDRESS + "/reports/advertiser/click/daily",
                           data=json.dumps(data)).content
    result = json.loads(result)
    clicks = result['body']

    result = requests.post(BACKEND_SERVER_ADDRESS + "/reports/advertiser/show/daily",
                           data=json.dumps(data)).content
    result = json.loads(result)
    shows = result['body']

    clicks = OrderedDict(sorted(clicks.items(), key=lambda t: t[0]))
    shows = OrderedDict(sorted(shows.items(), key=lambda t: t[0]))

    if campaign["campaign_type"]["campaign_type_name"] == 'banner' or campaign["campaign_type"][
        "campaign_type_name"] == 'mobile' or campaign["campaign_type"]["campaign_type_name"] == 'native':
        result = requests.post(BACKEND_SERVER_ADDRESS + "/reports/advertiser/show/publishers/daily?banner=1",
                               data=json.dumps(data)).content
        result = json.loads(result)
        publisher_shows = result['body']

        result = requests.post(BACKEND_SERVER_ADDRESS + "/reports/advertiser/click/publishers/daily?banner=1",
                               data=json.dumps(data)).content
        result = json.loads(result)
        publisher_clicks = result['body']

        return render_template('dashboard/advertiser/daily_statistics.html', clicks=clicks, shows=shows,
                               publisher_shows=publisher_shows,
                               publisher_clicks=publisher_clicks, configs=configs)

    elif campaign["campaign_type"]["campaign_type_name"] == 'search_engine':
        result = requests.post(BACKEND_SERVER_ADDRESS + "/reports/advertiser/show/publishers/daily?banner=0",
                               data=json.dumps(data)).content

        result = json.loads(result)
        publisher_shows = result['body']

        result = requests.post(BACKEND_SERVER_ADDRESS + "/reports/advertiser/click/publishers/daily?banner=0",
                               data=json.dumps(data)).content

        result = json.loads(result)
        publisher_clicks = result['body']

        return render_template('dashboard/advertiser/daily_statistics_search_engine.html', clicks=clicks, shows=shows,
                               publisher_shows=publisher_shows,
                               publisher_clicks=publisher_clicks, configs=configs)


@app.route('/dashboard/advertiser/campaign/<campaign_id>/day/<day>/details', methods=['GET', 'POST'])
@login_required
@roles_accepted('advertiser')
def advertiser_dashboard_daily_details(campaign_id, day):
    campaign = requests.get(BACKEND_SERVER_ADDRESS + "/advertiser/campaign/" + str(campaign_id)).content
    campaign = json.loads(campaign)
    campaign = campaign['body']

    configs = {
        'module': 'داشبورد آگهی دهنده',
        'action': 'جزئیات کلیک کمپین' + ' "' + campaign['campaign_name'] + '"',
        'url_index': 'advertiser_dashboard',
        'campaign_id': campaign_id,
        'campaign_name': campaign['campaign_name'],
        'day': day
    }

    date = time.strftime("%Y-%m-%d", time.localtime(float(day)))
    es = Elasticsearch([{'host': ELASTICSEARCH_SERVER_ADDRESS, 'port': 9200}])
    gte = date + "00:00:00"
    lte = date + "23:59:59"
    campaign_id = campaign_id

    if request.args.get('website') is None:
        query = '{"size" : 10000, "query": {"bool": {"must": [{"term": {"CampaignID": "' + str(
            campaign_id) + '"}}, {"range": {"Time": {"gte": "' + gte + '","lte": "' + lte + '","format": "yyyy-MM-ddHH:mm:ss"}}}]}}}'

    else:
        if request.args.get('banner') is not None:
            query = '{"size" : 10000, "query": {"bool": {"must": [{"term": {"CampaignID": "' + str(
                campaign_id) + '"}}, {"term": {"QueryOrSize": "' + request.args.get(
                'banner') + '"}}, {"term" : {"SiteID" : "' + request.args.get(
                'website') + '"}}, {"range": {"Time": {"gte": "' + gte + '","lte": "' + lte + '","format": "yyyy-MM-ddHH:mm:ss"}}}]}}}'
        else:
            query = '{"size" : 10000, "query": {"bool": {"must": [{"term": {"CampaignID": "' + str(
                campaign_id) + '"}}, {"term" : {"SiteID" : "' + request.args.get(
                'website') + '"}}, {"range": {"Time": {"gte": "' + gte + '","lte": "' + lte + '","format": "yyyy-MM-ddHH:mm:ss"}}}]}}}'

    query = json.loads(query)

    clicks = {}
    if campaign["campaign_type"]["campaign_type_name"] == "search_engine":
        clicks = es.search(index='logs', doc_type='clickAdWordsLog', body=query)
        clicks = clicks["hits"]["hits"]
    elif campaign["campaign_type"]["campaign_type_name"] == "banner" or campaign["campaign_type"][
        "campaign_type_name"] == "mobile" or campaign["campaign_type"]["campaign_type_name"] == 'native':
        clicks = es.search(index='logs', doc_type='clickAdSenseLog', body=query)
        clicks = clicks["hits"]["hits"]

    return render_template('dashboard/advertiser/daily_clicks_details.html', clicks=clicks,
                           configs=configs)


@app.route("/dashboard/advertiser/campaign/<campaign_id>/activate", methods=["GET"])
@login_required
@roles_accepted('advertiser')
def campaign_advertiser_activate(campaign_id):
    campaign = requests.get(BACKEND_SERVER_ADDRESS + "/advertiser/campaign/" + str(campaign_id)).content
    campaign = json.loads(campaign)
    campaign = campaign['body']

    if campaign["campaign_active_by_user"]:
        message = json.dumps({"type": "", "message": "کمپین شما فعال است."})
        session['message'] = message
        return (redirect(url_for("advertiser_campaign")))

    if not campaign["campaign_total_budget"] or campaign["campaign_total_budget"] == 0:
        message = json.dumps({"type": "", "message": "لطفا بودجه بندی کمپین خود را مشخص نمایید."})
        session['message'] = message
        return (redirect(url_for("advertiser_campaign")))

    total_budget = campaign["campaign_total_budget"]
    credit = publisher_credit_calculation()

    if (int(total_budget) - int(credit)) > 0:
        message = json.dumps({"type": "",
                              "message": "اعتبار شما برای فعال سازی این کمپین کافی نیست. لطفا نسبت به افزایش اعتبار خود اقدام نمایید."})
        session['message'] = message
        return (redirect(url_for("advertiser_campaign")))

    data = {
        'transaction_author_user_id': campaign['campaign_author_user_id'],
        'transaction_updated_user_id': current_user.get_id(),
        'transaction_deposit_amount': 0,
        'transaction_withdrawal_amount': int(total_budget),
        'transaction_description': 'پرداخت هزینه کمپین' + " " + campaign["campaign_name"],
        'transaction_status': 1
    }
    result = requests.post(BACKEND_SERVER_ADDRESS + "/financial/transaction",
                           data=json.dumps(data)).content
    result = json.loads(result)
    result = result['body']

    data = {
        'campaign_updated_user_id': current_user.get_id(),
        'campaign_active_by_user': True
    }
    result = requests.put(BACKEND_SERVER_ADDRESS + "/advertiser/campaign/" + str(campaign['campaign_id']),
                          data=json.dumps(data)).content
    result = json.loads(result)
    result = result['body']

    message = json.dumps({"type": "alert-success", "message": "کمپین شما با موفقیت فعال شد."})
    session['message'] = message

    return (redirect(url_for("advertiser_campaign")))


@app.route('/dashboard/publisher', methods=['GET', 'POST'])
@login_required
@roles_accepted('publisher')
def publisher_dashboard():
    configs = {
        'module': 'داشبورد نمایش دهنده',
        'action': 'داشبورد',
        'url_index': 'publisher_dashboard',
        'page_title': 'داشبورد'
    }

    date = datetime.now()
    to_date = date.strptime(date.strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")
    from_date = to_date - dateutil.relativedelta.relativedelta(days=4)

    data = {
        'from_date': str(from_date)[:10] + ' 00:00:00',
        'to_date': str(to_date),
        'user': current_user.get_id()
    }
    result = requests.post(BACKEND_SERVER_ADDRESS + "/reports/publisher/dashboard/period",
                           data=json.dumps(data)).content
    result = json.loads(result)
    dashboard = result['body']

    clicks = OrderedDict(sorted(dashboard["clicks"].items(), key=lambda t: t[0]))
    shows = OrderedDict(sorted(dashboard["shows"].items(), key=lambda t: t[0]))

    total_benfit = 0
    redis_set_benfit = r.smembers('publisher_total_benefit_' + str(current_user.get_id()))
    if len(list(redis_set_benfit)) > 0:
        total_benfit = int(float(list(redis_set_benfit)[0]))

    dashboard["total_benfit"] = total_benfit

    return render_template('dashboard/publisher/index.html', clicks=clicks, shows=shows, dashboard=dashboard,
                           configs=configs)


@app.route('/dashboard/publisher/website/<website_id>/statistics', methods=['GET', 'POST'])
@login_required
@roles_accepted('publisher')
def publisher_dashboard_statistics(website_id):
    website = requests.get(BACKEND_SERVER_ADDRESS + "/publisher/website/" + str(website_id)).content
    website = json.loads(website)
    website = website['body']

    configs = {
        'module': 'سایت های من',
        'action': 'آمار ماهیانه وب سایت' + ' "' + website['publisher_website_title'] + '"',
        'url_index': 'publisher_website',
        'website_id': website_id
    }

    date = datetime.now()

    if request.method == 'GET':
        to_date = date.strptime(date.strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S")
        from_date = to_date - dateutil.relativedelta.relativedelta(days=10)
    elif request.method == 'POST':
        to_date = date.strptime(persian_date_to_gregorian_date(request.form['to_date']) + " 23:59:59",
                                "%Y-%m-%d %H:%M:%S")
        from_date = date.strptime(persian_date_to_gregorian_date(request.form['from_date']) + " 00:00:00",
                                  "%Y-%m-%d %H:%M:%S")

    data = {
        'from_date': str(from_date),
        'to_date': str(to_date),
        'website': website_id
    }
    result = requests.post(BACKEND_SERVER_ADDRESS + "/reports/publisher/click/period",
                           data=json.dumps(data)).content
    result = json.loads(result)
    clicks = result['body']

    result = requests.post(BACKEND_SERVER_ADDRESS + "/reports/publisher/show/period",
                           data=json.dumps(data)).content
    result = json.loads(result)
    shows = result['body']

    clicks_shows = {}
    delta = to_date - from_date

    for i in range(0, delta.days + 1):
        tmp_date = to_date - dateutil.relativedelta.relativedelta(days=i)
        tmp_date = tmp_date.strftime('%Y-%m-%d')
        z = datetime(int(tmp_date[:4]), int(tmp_date[5:7]), int(tmp_date[8:10]), 0, 0, 0)
        unixtime = calendar.timegm(z.timetuple())
        unixtime = str(unixtime)
        unixtime = unixtime[:10]
        clicks_shows[unixtime] = {"click": clicks.get(unixtime + "000", 0), "show": shows.get(unixtime + "000", 0)}

    clicks_shows = OrderedDict(sorted(clicks_shows.items(), reverse=True, key=lambda t: t[0]))

    clicks = OrderedDict(sorted(clicks.items(), key=lambda t: t[0]))
    shows = OrderedDict(sorted(shows.items(), key=lambda t: t[0]))

    return render_template('dashboard/publisher/statistics.html', clicks=clicks, shows=shows,
                           clicks_shows=clicks_shows,
                           to_date=str(to_date)[:10],
                           from_date=str(from_date)[:10],
                           configs=configs)


@app.route('/dashboard/publisher/website/<website_id>/day/<day>/statistics', methods=['GET', 'POST'])
@login_required
@roles_accepted('publisher')
def publisher_dashboard_daily_statistics(website_id, day):
    website = requests.get(BACKEND_SERVER_ADDRESS + "/publisher/website/" + str(website_id)).content
    website = json.loads(website)
    website = website['body']

    configs = {
        'module': 'داشبورد نمایش دهنده',
        'action': 'جزئیات نمایش وب سایت' + ' "' + website['publisher_website_title'] + '"',
        'url_index': 'publisher_dashboard',
        'website_id': website_id,
        'website_title': website['publisher_website_title'],
        'day': day
    }
    date = time.strftime("%Y-%m-%d", time.localtime(float(day)))
    data = {
        'from_date': date + " 00:00:00",
        'to_date': date + " 23:59:59",
        'website': website_id
    }
    result = requests.post(BACKEND_SERVER_ADDRESS + "/reports/publisher/click/daily",
                           data=json.dumps(data)).content
    result = json.loads(result)
    clicks = result['body']

    result = requests.post(BACKEND_SERVER_ADDRESS + "/reports/publisher/show/daily",
                           data=json.dumps(data)).content
    result = json.loads(result)
    shows = result['body']

    result = requests.post(BACKEND_SERVER_ADDRESS + "/reports/publisher/show/banners/daily",
                           data=json.dumps(data)).content
    result = json.loads(result)
    banners_shows = result['body']

    result = requests.post(BACKEND_SERVER_ADDRESS + "/reports/publisher/click/banners/daily",
                           data=json.dumps(data)).content
    result = json.loads(result)
    banners_clicks = result['body']

    return render_template('dashboard/publisher/daily_statistics.html', clicks=clicks, shows=shows,
                           banners_shows=banners_shows,
                           banners_clicks=banners_clicks, configs=configs)


@app.route('/dashboard/publisher/website/<website_id>/day/<day>/details', methods=['GET', 'POST'])
@login_required
@roles_accepted('publisher')
def publisher_dashboard_daily_details(website_id, day):
    website = requests.get(BACKEND_SERVER_ADDRESS + "/publisher/website/" + str(website_id)).content
    website = json.loads(website)
    website = website['body']

    configs = {
        'module': 'داشبورد نمایش دهنده',
        'action': 'جزئیات نمایش وب سایت' + ' "' + website['publisher_website_title'] + '"',
        'url_index': 'publisher_dashboard',
        'website_id': website_id,
        'website_title': website['publisher_website_title'],
        'day': day
    }

    date = time.strftime("%Y-%m-%d", time.localtime(float(day)))
    es = Elasticsearch([{'host': ELASTICSEARCH_SERVER_ADDRESS, 'port': 9200}])
    gte = date + "00:00:00"
    lte = date + "23:59:59"

    clicks = {}
    if request.args.get('banner') is None and request.args.get('search_engine') is None:
        query = '{"size" : 10000, "query": {"bool": {"must": [{"term" : {"SiteID" : "' + website_id + '"}},{"range": {"Time": {"gte": "' + gte + '","lte": "' + lte + '","format": "yyyy-MM-ddHH:mm:ss"}}}]}}}'
        print query
        query = json.loads(query)
        adSense_clicks = es.search(index='logs', doc_type='clickAdSenseLog', body=query)
        adWords_clicks = es.search(index='logs', doc_type='clickAdWordsLog', body=query)
        clicks = adSense_clicks["hits"]["hits"] + adWords_clicks["hits"]["hits"]
    if request.args.get('banner'):
        query = '{"size" : 10000, "query": {"bool": {"must": [{"term" : {"SiteID" : "' + website_id + '"}}, {"term": {"QueryOrSize" : "' + request.args.get(
            'banner') + '"}},{"range": {"Time": {"gte": "' + gte + '","lte": "' + lte + '","format": "yyyy-MM-ddHH:mm:ss"}}}]}}}'
        query = json.loads(query)
        clicks = es.search(index='logs', doc_type='clickAdSenseLog', body=query)
        clicks = clicks["hits"]["hits"]
    if request.args.get('search_engine'):
        query = '{"size" : 10000, "query": {"bool": {"must": [{"term" : {"SiteID" : "' + website_id + '"}},{"range": {"Time": {"gte": "' + gte + '","lte": "' + lte + '","format": "yyyy-MM-ddHH:mm:ss"}}}]}}}'
        query = json.loads(query)
        clicks = es.search(index='logs', doc_type='clickAdWordsLog', body=query)
        clicks = clicks["hits"]["hits"]
    return render_template('dashboard/publisher/daily_clicks_details.html',
                           website_percentage=float(website["publisher_website_percentage"]) / 100,
                           clicks=clicks,
                           configs=configs)


@app.route('/dashboard/admin/ticket/category', methods=['GET', 'POST'])
@login_required
@roles_accepted('admin')
def ticket_category():
    configs = {
        'url_new': 'ticket_category_new',
        'url_edit': 'ticket_category_edit',
        'url_index': 'ticket_category',
        'module': 'مدیریت بخش ها',
        'action': 'مدیریت بخش ها',
        'url_new_text': 'بخش جدید',
        'id_name': 'category_id',
        'page_title': 'تیکت ها - مدیریت بخش ها',
        'fields': [
            {
                'name': 'category_name',
                'title': 'نام',
                'order': 2,
                'hide': '',
                'width': '30%',
                'class': 'class=defaultSort'
            },
            {
                'name': 'category_title',
                'title': 'عنوان',
                'order': 3,
                'hide': '',
                'width': '29%'
            }
        ]
    }
    message = None
    if request.method == 'POST':
        result = requests.delete(
            BACKEND_SERVER_ADDRESS + "/ticketing/ticket/category/" + request.form['action']).content
        result = json.loads(result)

        if result["status"] == "ok":
            message = {"type": "alert-success", "message": "رکورد با موفقیت حذف شد."}
        elif result["status"] == "nok":
            message = {"type": "alert-error", "message": "خطایی رخ داده است."}

    result = requests.get(BACKEND_SERVER_ADDRESS + "/ticketing/ticket/category").content
    result = json.loads(result)
    result = result['body']
    return render_template('general/index.html', result=result, message=message, configs=configs)


@app.route('/dashboard/admin/ticket/category/new', methods=['GET', 'POST'])
@login_required
@roles_accepted('admin')
def ticket_category_new():
    configs = {
        'module': 'لیست بخش های تیکت',
        'action': 'بخش جدید',
        'url': 'ticket_category_new',
        'url_index': 'ticket_category',
        'page_title': 'بخش جدید'
    }
    form = TicketCategoryForm()
    if request.method == 'POST':
        if form.validate() == False:
            flash('All fields are required.', 'danger')
            return render_template('general/new.html', form=form, configs=configs)
        else:
            data = {
                'category_author_user_id': current_user.get_id(),
                'category_name': form.name.data,
                'category_title': form.title.data
            }
            result = requests.post(BACKEND_SERVER_ADDRESS + "/ticketing/ticket/category", data=json.dumps(data)).content
            result = json.loads(result)

            if result["status"] == "ok":
                message = json.dumps({"type": "alert-success", "message": "بخش تیکت با موفقیت ثبت شد."})
            elif result["status"] == "nok":
                message = json.dumps({"type": "alert-error", "message": "خطایی رخ داده است."})
            session['message'] = message

            return redirect(url_for('ticket_category_new'))
    elif request.method == 'GET':
        message = None
        if session.get('message', None) is not None:
            message = json.loads(session.pop("message"))
        return render_template('general/new.html', form=form, message=message, configs=configs)


@app.route('/dashboard/admin/ticket/category/<id>/edit', methods=['GET', 'POST'])
@login_required
@roles_accepted('admin')
def ticket_category_edit(id):
    configs = {
        'module': 'لیست بخش های تیکت',
        'action': 'ویرایش بخش',
        'url': 'ticket_category_edit',
        'url_index': 'ticket_category',
        'id': id,
        'page_title': 'ویرایش بخش'
    }
    form = TicketCategoryForm()
    if request.method == 'POST':
        if form.validate() == False:
            flash('All fields are required.', 'danger')
            return render_template('general/edit.html', form=form, configs=configs)
        else:
            data = {
                'category_updated_user_id': current_user.get_id(),
                'category_name': form.name.data,
                'category_title': form.title.data
            }
            result = requests.put(BACKEND_SERVER_ADDRESS + "/ticketing/ticket/category/" + str(id),
                                  data=json.dumps(data)).content
            result = json.loads(result)

            if result["status"] == "ok":
                message = {"type": "alert-success", "message": "بخش تیکت با موفقیت ویرایش شد."}
            elif result["status"] == "nok":
                message = {"type": "alert-error", "message": "خطایی رخ داده است."}

            return render_template('general/edit.html', form=form, message=message, configs=configs)
    elif request.method == 'GET':
        result = requests.get(BACKEND_SERVER_ADDRESS + "/ticketing/ticket/category/" + str(id)).content
        result = json.loads(result)
        result = result['body']
        form.name.data = result["category_name"]
        form.title.data = result["category_title"]
        return render_template('general/edit.html', form=form, configs=configs)


@app.route('/dashboard/admin/ticket', methods=['GET', 'POST'])
@login_required
@roles_accepted('admin')
def ticket_admin():
    configs = {
        'url_new': 'ticket_new',
        'url_index': 'ticket_admin',
        'module': 'مدیریت تیکت ها',
        'action': 'مدیریت تیکت ها',
        'id_name': 'ticket_id',
        'page_title': 'تیکت ها - مدیریت تیکت ها',
    }

    result = requests.get(BACKEND_SERVER_ADDRESS + "/ticketing/ticket").content
    result = json.loads(result)
    result = result['body']

    ids = []
    for query in result:
        ids.append(query["ticket_author_user_id"])

    authors = users(ids)
    authors = json.loads(authors)
    authors = authors['body']

    return render_template('admin/ticket/index.html', result=result, authors=authors, configs=configs)


@app.route('/dashboard/user/ticket/new', methods=['GET', 'POST'])
@login_required
def ticket_new():
    configs = {
        'module': 'لیست تیکت ها',
        'action': 'تیکت جدید',
        'url': 'ticket_new',
        'url_index': 'ticket',
        'page_title': 'تیکت جدید',
        'from_id': 'ticket-new-form'
    }
    form = TicketForm()
    if request.method == 'POST':
        ticket_author_user_id = current_user.get_id()
        is_admin = current_user.has_role('admin')
        if is_admin:
            ticket_author_user_id = form.user.data

        data = {
            'ticket_author_user_id': ticket_author_user_id,
            'ticket_category': form.category.data,
            'ticket_priority': form.priority.data,
            'ticket_title': form.title.data
        }
        result = requests.post(BACKEND_SERVER_ADDRESS + "/ticketing/ticket", data=json.dumps(data)).content
        result = json.loads(result)
        result = result["body"]

        data = {
            'reply_author_user_id': current_user.get_id(),
            'ticket': result,
            'reply_description': form.description.data,
            'reply_attachment': request.form.getlist('attachments')
        }
        result = requests.post(BACKEND_SERVER_ADDRESS + "/ticketing/ticket/reply", data=json.dumps(data)).content
        result = json.loads(result)

        if is_admin:
            user = UserRests()
            user_result = user.get(ticket_author_user_id)
            user_result = json.loads(user_result)
            user_result = user_result['body']
            requests.get(
                'http://ip.sms.ir/SendMessage.ashx?user=09139610206&pass=84c527&text=تیکتی%20از%20طرف%20کارشناسان%20سامانه%20تبلیغات%20هشتاد%20برای%20شما%20ارسال%20شد.%208tad.ir&to=' +
                user_result['user_phone'] + '&lineNo=30004505002814')

        if result["status"] == "ok":
            message = json.dumps({"type": "alert-success", "message": "تیکت با موفقیت ثبت شد."})
        elif result["status"] == "nok":
            message = json.dumps({"type": "alert-error", "message": "خطایی رخ داده است."})
        session['message'] = message

        return redirect(url_for('ticket_new'))
    elif request.method == 'GET':
        message = None
        if session.get('message', None) is not None:
            message = json.loads(session.pop("message"))

        result = requests.get(BACKEND_SERVER_ADDRESS + "/ticketing/ticket/category").content
        result = json.loads(result)
        result = result['body']
        records = [(record["category_id"], record["category_title"]) for record in result]
        form.category.choices = records

        if current_user.has_role('admin'):
            users = UserRests()
            result = users.get()
            result = json.loads(result)
            result = result['body']
            records = []
            for record in result:
                records.append((record["user_id"], record["user_fullname"]))
            form.user.choices = records
        else:
            del form.user

        return render_template('ticket/new.html', form=form, message=message, configs=configs)


@app.route('/dashboard/user/ticket', methods=['GET', 'POST'])
@login_required
def ticket():
    configs = {
        'url_new': 'ticket_new',
        'url_index': 'ticket',
        'module': 'لیست تیکت ها',
        'action': 'لیست تیکت ها',
        'url_new_text': 'تیکت جدید',
        'id_name': 'ticket_id',
        'page_title': 'تیکت ها - لیست تیکت ها',
    }
    result = requests.get(BACKEND_SERVER_ADDRESS + "/ticketing/ticket?user=" + str(current_user.get_id())).content
    result = json.loads(result)
    result = result['body']
    return render_template('ticket/index.html', result=result, configs=configs)


@app.route('/dashboard/user/ticket/<id>/close', methods=['POST'])
@login_required
def ticket_close(id):
    result = requests.get(BACKEND_SERVER_ADDRESS + "/ticketing/ticket/" + str(id)).content
    result = json.loads(result)
    ticket = result['body']

    if ticket['ticket_author_user_id'] != current_user.get_id() and not current_user.has_role('admin'):
        return redirect(url_for('dashboard'))

    data = {
        'ticket_updated_user_id': current_user.get_id(),
        'ticket_status': 'close'
    }
    result = requests.put(BACKEND_SERVER_ADDRESS + "/ticketing/ticket/" + str(id), data=json.dumps(data)).content
    result = json.loads(result)

    if result["status"] == "ok":
        message = json.dumps({"type": "alert-success", "message": "تیکت با موفقیت بسته شد."})
    elif result["status"] == "nok":
        message = json.dumps({"type": "alert-error", "message": "خطایی رخ داده است."})
    session['message'] = message

    return redirect(url_for('ticket_show', id=id))


@app.route('/dashboard/admin/ticket/<id>/edit', methods=['GET', 'POST'])
@login_required
@roles_accepted('admin')
def ticket_edit(id):
    configs = {
        'module': 'مدیریت تیکت ها',
        'action': 'ویرایش تیکت',
        'url': 'ticket_edit',
        'url_index': 'ticket_admin',
        'id': id
    }
    form = TicketAdminForm()
    if request.method == 'POST':
        data = {
            'ticket_updated_user_id': current_user.get_id(),
            'ticket_category': form.category.data,
            'ticket_priority': form.priority.data,
            'ticket_title': form.title.data,
            'ticket_status': form.status.data
        }

        result = requests.put(BACKEND_SERVER_ADDRESS + "/ticketing/ticket/" + str(id),
                              data=json.dumps(data)).content
        result = json.loads(result)

        if result["status"] == "ok":
            message = {"type": "alert-success", "message": "تیکت با موفقیت ویرایش شد."}
        elif result["status"] == "nok":
            message = {"type": "alert-error", "message": "خطایی رخ داده است."}

        return redirect(url_for('ticket_edit', id=id))

    elif request.method == 'GET':
        result = requests.get(BACKEND_SERVER_ADDRESS + "/ticketing/ticket/" + str(id)).content
        result = json.loads(result)
        result = result['body']

        form.priority.data = result["ticket_priority"]
        form.title.data = result["ticket_title"]
        form.status.data = result["ticket_status"]
        form.category.data = str(result["ticket_category"]["ticket_category_id"])

        result = requests.get(BACKEND_SERVER_ADDRESS + "/ticketing/ticket/category").content
        result = json.loads(result)
        result = result['body']
        records = [(record["category_id"], record["category_title"]) for record in result]
        form.category.choices = records

        return render_template('general/edit.html', form=form, configs=configs)


@app.route('/dashboard/admin/ticket/<id>/show', endpoint="ticket_show_admin", methods=['GET', 'POST'])
@app.route('/dashboard/user/ticket/<id>/show', methods=['GET', 'POST'])
@login_required
def ticket_show(id):
    configs = {
        'module': 'لیست تیکت ها',
        'action': 'پاسخ به تیکت',
        'url': 'ticket_show',
        'url_index': 'ticket',
        'page_title': 'پاسخ به تیکت',
        'from_id': 'ticket-new-form',
        'id': id
    }

    if request.endpoint == 'ticket_show_admin':
        configs['url_index'] = 'ticket_admin'

    form = TicketReplyForm()
    if request.method == 'POST':
        result = requests.get(BACKEND_SERVER_ADDRESS + "/ticketing/ticket/" + str(id)).content
        result = json.loads(result)
        result = result['body']

        if result['ticket_author_user_id'] != current_user.get_id() and not current_user.has_role('admin'):
            return redirect(url_for('dashboard'))

        data = {
            'ticket_updated_user_id': current_user.get_id(),
            'ticket_status': ('respond' if current_user.has_role('admin') else 'open')
        }

        if result['ticket_author_user_id'] == current_user.get_id():
            data['ticket_viewed_by_admin'] = False
            data['ticket_viewed_by_user'] = True
        else:
            data['ticket_viewed_by_admin'] = True
            data['ticket_viewed_by_user'] = False

        ticket_author_user_id = result['ticket_author_user_id']

        result = requests.put(BACKEND_SERVER_ADDRESS + "/ticketing/ticket/" + str(id), data=json.dumps(data)).content
        result = json.loads(result)

        data = {
            'reply_author_user_id': current_user.get_id(),
            'ticket': id,
            'reply_description': form.description.data,
            'reply_attachment': request.form.getlist('attachments')
        }
        result = requests.post(BACKEND_SERVER_ADDRESS + "/ticketing/ticket/reply", data=json.dumps(data)).content
        result = json.loads(result)

        if ticket_author_user_id != current_user.get_id():
            user = UserRests()
            user_result = user.get(ticket_author_user_id)
            user_result = json.loads(user_result)
            user_result = user_result['body']
            requests.get(
                'http://ip.sms.ir/SendMessage.ashx?user=09139610206&pass=84c527&text=تیکتی%20از%20طرف%20کارشناسان%20سامانه%20تبلیغات%20هشتاد%20برای%20شما%20ارسال%20شد.%208tad.ir&to=' +
                user_result['user_phone'] + '&lineNo=30004505002814')

        if result["status"] == "ok":
            message = json.dumps({"type": "alert-success", "message": "پاسخ تیکت با موفقیت ارسال شد."})
        elif result["status"] == "nok":
            message = json.dumps({"type": "alert-error", "message": "خطایی رخ داده است."})
        session['message'] = message

        return redirect(url_for(request.endpoint, id=id))
    elif request.method == 'GET':
        result = requests.get(BACKEND_SERVER_ADDRESS + "/ticketing/ticket/" + str(id)).content
        result = json.loads(result)
        ticket = result['body']

        if ticket['ticket_author_user_id'] != current_user.get_id() and not current_user.has_role('admin'):
            return redirect(url_for('dashboard'))

        data = {
            'ticket_updated_user_id': current_user.get_id(),
            'ticket_updated_at': False
        }
        if ticket['ticket_author_user_id'] == current_user.get_id():
            data['ticket_viewed_by_user'] = True
        else:
            data['ticket_viewed_by_admin'] = True

        result = requests.put(BACKEND_SERVER_ADDRESS + "/ticketing/ticket/" + str(id),
                              data=json.dumps(data)).content

        message = None
        if session.get('message', None) is not None:
            message = json.loads(session.pop("message"))

        result = requests.get(
            BACKEND_SERVER_ADDRESS + "/ticketing/ticket/reply?ticket=" + str(id)).content
        result = json.loads(result)
        replies = result['body']

        ids = []
        for key, value in replies.iteritems():
            ids.append(value["reply_author_user_id"])

        authors = users(ids)
        authors = json.loads(authors)
        authors = authors['body']

        replies = OrderedDict(sorted(replies.items(), key=lambda x: int(x[0])))

        return render_template('ticket/show.html', form=form, ticket=ticket, replies=replies, authors=authors,
                               message=message, configs=configs)


@app.template_filter('default_title')
def default_title(title):
    if title is not None:
        return title
    else:
        return "default"


@app.template_filter('boolean_status')
def boolean_status(status):
    if status:
        return '<i class="fa fa-check" aria-hidden="true"></i>'
    else:
        return '<i class="fa fa-times" aria-hidden="true"></i>'


@app.template_filter('persian_date_to_gregorian_date')
def persian_date_to_gregorian_date(date):
    date = str(date)
    date_gregorian = jalali.Persian(date[:10]).gregorian_string()
    return date_gregorian


@app.template_filter('gregorian_date_to_persian_date')
def gregorian_date_to_persian_date(date):
    date = str(date)
    date_persian = jalali.Gregorian(date[:10]).persian_string() + date[10:]
    return date_persian


@app.template_filter('gregorian_date_to_persian_date_local')
def gregorian_date_to_persian_date_local(date):
    date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    date = date + dateutil.relativedelta.relativedelta(hours=3, minutes=30)
    date = str(date)
    date_persian = jalali.Gregorian(date[:10]).persian_string() + date[10:]
    return date_persian


@app.template_filter('epoch_date_to_persian_date')
def epoch_date_to_persian_date(date):
    date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(date)))
    date_persian = jalali.Gregorian(date[:10]).persian_string()
    return date_persian


@app.template_filter('date_add_space')
def date_add_space(date):
    return date[:10] + " " + date[10:]


@app.template_filter('url_and_banner_size_separation')
def url_and_banner_size_separation(url_size):
    idx = url_size.rfind('_')
    idx2 = url_size.find('_')
    return '<td class="text-left" dir="ltr"><a href="' + url_size[0:idx2] + '" target="_blank">' + url_size[
                                                                                                   0:idx2] + '</td><td>' + url_size[
                                                                                                                           idx + 1:] + '</td>'


@app.template_filter('url_separation')
def url_separation(url_size):
    idx = url_size.find('_')
    return url_size[0:idx]


@app.template_filter('website_id_separation')
def website_id_separation(url_size):
    idx = url_size.rfind('_')
    idx2 = url_size.find('_')
    return url_size[idx2 + 1:idx]


@app.template_filter('banner_separation')
def banner_separation(url_size):
    idx = url_size.rfind('_')
    return url_size[idx + 1:]


@app.template_filter('format_currency')
def format_currency(s):
    s = str(s)
    if len(s) <= 3: return s
    return format_currency(s[:-3]) + ',' + s[-3:]


@app.template_filter('enToPersianNumb')
def enToPersianNumb(s):
    s = str(s)
    return persian.enToPersianNumb(s)


@app.template_filter('campaign_total_budget')
def campaign_total_budget(campaign_id):
    total_budget = 0
    redis_total_budget = r.smembers('campaign_total_budget_' + str(campaign_id))
    if len(list(redis_total_budget)) > 0:
        total_budget = int(float(list(redis_total_budget)[0]))
    return str(total_budget)


@app.template_filter()
@evalcontextfilter
def linebreaks(eval_ctx, value):
    """Converts newlines into <p> and <br />s."""
    value = re.sub(r'\r\n|\r|\n', '\n', value)  # normalize newlines
    paras = re.split('\n{2,}', value)
    paras = [u'<p>%s</p>' % p.replace('\n', '<br />') for p in paras]
    paras = u'\n\n'.join(paras)
    return Markup(paras)


@app.template_filter()
@evalcontextfilter
def linebreaksbr(eval_ctx, value):
    """Converts newlines into <p> and <br />s."""
    value = re.sub(r'\r\n|\r|\n', '\n', value)  # normalize newlines
    paras = re.split('\n{2,}', value)
    paras = [u'%s' % p.replace('\n', '<br />') for p in paras]
    paras = u'\n\n'.join(paras)
    return Markup(paras)


@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    return render_template('csrf_error.html', reason=e.description), 400


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def error_500(e):
    return render_template('500.html'), 500


@app.before_request
def _db_connect():
    # if (
    #                     request.endpoint == 'security.login' or request.endpoint == 'security.register' or request.endpoint == 'security.forgot_password') and request.method == 'POST':
    #     try:
    #         token = request.form.get(RECAPTCHA_RESPONSE_PARAM)
    #         resp = urllib.urlopen(
    #             SITE_VERIFY_URL, urllib.urlencode(
    #                 {'secret': SITE_SECRET, 'response': token}, True)).read()
    #
    #         if not json.loads(resp).get("success"):
    #             return redirect('/accounts/login')
    #
    #     except Exception:
    #         pass

    if not db.is_closed():
        db.close()
    db.connect()


# This hook ensures that the connection is closed when we've finished
# processing the request.
@app.teardown_request
def _db_close(exc):
    if not db.is_closed():
        db.close()


@app.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    # response.headers["Expires"] = "0"
    # response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.context_processor
def inject_credit():
    user = None
    credit = None
    credit_request_count = website_count = campaign_count = ticket_count = 0
    try:
        if current_user.get_id() is not None:
            user = user_datastore.get_user(current_user.get_id())
            credit = publisher_credit_calculation()
            if current_user.has_role('admin'):
                result = requests.get(BACKEND_SERVER_ADDRESS + "/financial/credit/request/count").content
                result = json.loads(result)
                credit_request_count = result['body']

                result = requests.get(BACKEND_SERVER_ADDRESS + "/publisher/website/count").content
                result = json.loads(result)
                website_count = result['body']

                result = requests.get(BACKEND_SERVER_ADDRESS + "/advertiser/campaign/count").content
                result = json.loads(result)
                campaign_count = result['body']

                result = requests.get(BACKEND_SERVER_ADDRESS + "/ticketing/ticket/count").content
                result = json.loads(result)
                ticket_count = result['body']

            return dict(my_credit=credit, my_name=user.fullname, credit_request_count=credit_request_count,
                        website_count=website_count, campaign_count=campaign_count, ticket_count=ticket_count)

        return dict(my_credit=credit, my_name=user, credit_request_count=credit_request_count,
                    website_count=website_count, campaign_count=campaign_count, ticket_count=ticket_count)
    except Exception:
        return dict(my_credit=credit, my_name=user, credit_request_count=credit_request_count,
                    website_count=website_count, campaign_count=campaign_count, ticket_count=ticket_count)


@user_registered.connect_via(app)
def user_registered_sighandler(sender, user, confirm_token):
    if user.account_type == 'advertiser':
        advertiser = user_datastore.find_role("advertiser")
        user_datastore.add_role_to_user(user, advertiser)
    elif user.account_type == 'publisher':
        publisher = user_datastore.find_role("publisher")
        user_datastore.add_role_to_user(user, publisher)
    else:
        advertiser = user_datastore.find_role("advertiser")
        user_datastore.add_role_to_user(user, advertiser)
        publisher = user_datastore.find_role("publisher")
        user_datastore.add_role_to_user(user, publisher)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3333, debug=True, threaded=True)
