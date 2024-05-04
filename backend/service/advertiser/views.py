import datetime
import json
import sys
import traceback
from flask import request, Response
from flask.views import MethodView
from slugify import slugify_unicode
from models import *
from . import advertiser
from ..uploads.views import files


@advertiser.route('/campaigns/itrc', methods=['GET'])
def advertiser_campaigns_itrc():
    if request.method == 'GET':
        response = []
        campaigns = []
        campaigns = Ad_Campaign.select(Ad_Campaign, Ad_Campaign_Type).where(Ad_Campaign.campaign_active_by_user == 1).join(Ad_Campaign_Type, on=(
            Ad_Campaign.campaign_type == Ad_Campaign_Type.id))

        for query in campaigns:
            record = {
                'campaign_id': query.id,
                'campaign_author_user_id': query.campaign_author_user_id,
                'campaign_updated_user_id': query.campaign_updated_user_id,
                'campaign_name': query.campaign_name,
                'campaign_type': {
                    'campaign_type_name': query.campaign_type.campaign_type_name,
                    'campaign_type_title': query.campaign_type.campaign_type_title
                },
                'campaign_package_title': (
                    None if query.campaign_package is None else query.campaign_package.package_title),
                'campaign_total_budget_main': query.campaign_total_budget_main,
                'campaign_total_budget': query.campaign_total_budget,
                'campaign_daily_budget': query.campaign_daily_budget,
                'campaign_budget_management': query.campaign_budget_management,
                'campaign_native_title': query.campaign_native_title,
                'campaign_adwords_title': query.campaign_adwords_title,
                'campaign_adwords_description': query.campaign_adwords_description,
                'campaign_adwords_email': query.campaign_adwords_email,
                'campaign_adwords_phone': query.campaign_adwords_phone,
                'campaign_adwords_address': query.campaign_adwords_address,
                'campaign_landing_page_url': query.campaign_landing_page_url,
                'campaign_targeted_geography_all': query.campaign_targeted_geography_all,
                'campaign_targeted_geography_iran': query.campaign_targeted_geography_iran,
                'campaign_targeted_geography_not_iran': query.campaign_targeted_geography_not_iran,
                'campaign_targeted_geography_special': query.campaign_targeted_geography_special,
                'campaign_targeted_operating_system_all': query.campaign_targeted_operating_system_all,
                'campaign_targeted_operating_system_special': query.campaign_targeted_operating_system_special,
                'campaign_targeted_subject_all': query.campaign_targeted_subject_all,
                'campaign_targeted_subject_special': query.campaign_targeted_subject_special,
                'campaign_playtime_all': query.campaign_playtime_all,
                'campaign_playtime_special': query.campaign_playtime_special,
                'campaign_playtime_not_24_08': query.campaign_playtime_not_24_08,
                'campaign_playtime_not_08_16': query.campaign_playtime_not_08_16,
                'campaign_playtime_not_16_24': query.campaign_playtime_not_16_24,
                'campaign_network_class_a': query.campaign_network_class_a,
                'campaign_network_class_b': query.campaign_network_class_b,
                'campaign_network_class_c': query.campaign_network_class_c,
                'campaign_retargeting': query.campaign_retargeting,
                'campaign_targeted_keyword_all': query.campaign_targeted_keyword_all,
                'campaign_targeted_keyword_special': query.campaign_targeted_keyword_special,
                'campaign_click_price': query.campaign_click_price,
                'campaign_coef': query.campaign_coef,
                'campaign_active_by_user': query.campaign_active_by_user,
                'campaign_active_by_admin': query.campaign_active_by_admin,
                'campaign_default': query.campaign_default,
                'campaign_is_deleted': query.campaign_is_deleted,
                'campaign_created_at': str(query.campaign_created_at),
                'campaign_updated_at': str(query.campaign_updated_at),
                'keywords': []
            }

            keywords = []
            for keyword_campaign in Ad_Campaign_Targeted_Keyword.select().where(
                            Ad_Campaign_Targeted_Keyword.campaign == query.id):
                keyword_record = {
                    'keyword_id': keyword_campaign.keyword.id,
                    'keyword_title': keyword_campaign.keyword.keyword_title
                }

                keywords.append(keyword_record)

            record['keywords'] = keywords

            response.append(record)
        response = {"status": "ok", "body": response}
        return Response(json.dumps(response, sort_keys=True),
                        mimetype='application/json')


@advertiser.route('/campaign/count', methods=['GET'])
def advertiser_campaign_count():
    if request.method == 'GET':
        result = Ad_Campaign.select().where(
            (Ad_Campaign.campaign_active_by_user == 1) & (Ad_Campaign.campaign_active_by_admin == 0)).count()
        response = {"status": "ok", "body": result}
        return Response(json.dumps(response, sort_keys=True),
                        mimetype='application/json')


@advertiser.route('/campaign/click/price/max', methods=['GET'])
def advertiser_campaign_click_price_max():
    if request.method == 'GET':
        result = Ad_Campaign.select(fn.Max(Ad_Campaign.campaign_click_price)).where(
            Ad_Campaign.campaign_active_by_admin == 1).scalar()
        response = {"status": "ok", "body": result}
        return Response(json.dumps(response, sort_keys=True),
                        mimetype='application/json')


def user_campaigns(user_id):
    response = []
    campaigns = Ad_Campaign.select(Ad_Campaign.id).where(
        (Ad_Campaign.campaign_author_user_id == user_id) & (Ad_Campaign.campaign_active_by_admin == 1) & (
            Ad_Campaign.campaign_is_deleted == 0))

    for query in campaigns:
        response.append(query.id)

    response = {"status": "ok", "body": response}
    return json.dumps(response, sort_keys=True)


@advertiser.route('/active/campaigns/min_max', methods=['GET'])
def active_campaigns():
    campaign = Ad_Campaign.select(fn.Min(Ad_Campaign.campaign_click_price).alias('campaign_minimum_cost'), fn.Max(Ad_Campaign.campaign_click_price).alias('campaign_maximum_cost'),
                                   fn.Min(Ad_Campaign.campaign_daily_budget).alias('campaign_minimum_budget'), fn.Max(Ad_Campaign.campaign_daily_budget).alias('campaign_maximum_budget'),
                                   fn.Min(Ad_Campaign.campaign_coef).alias('campaign_minimum_coef'), fn.Max(Ad_Campaign.campaign_coef).alias('campaign_maximum_coef')).where(
        (Ad_Campaign.campaign_active_by_admin == 1) & (
            Ad_Campaign.campaign_is_deleted == 0)).get()

    response = {
            'campaign_minimum_cost': campaign.campaign_minimum_cost,
            'campaign_maximum_cost': campaign.campaign_maximum_cost,
            'campaign_minimum_budget': campaign.campaign_minimum_budget,
            'campaign_maximum_budget': campaign.campaign_maximum_budget,
            'campaign_minimum_coef': campaign.campaign_minimum_coef,
            'campaign_maximum_coef': campaign.campaign_maximum_coef
    }
    response = {"status": "ok", "body": response}
    return Response(json.dumps(response, sort_keys=True),
                    mimetype='application/json')


@advertiser.route('/campaign/landing_page', methods=['GET'])
def campaigns_has_landing_page():
    response = []
    url = str(request.args.get('url'))
    campaigns = Ad_Campaign.select().where((Ad_Campaign.campaign_active_by_admin == 1) & (
            Ad_Campaign.campaign_is_deleted == 0) & (Ad_Campaign.campaign_landing_page_url.contains(url)))

    for campaign in campaigns:
        response.append(campaign.id)

    response = {"status": "ok", "body": response}
    return Response(json.dumps(response, sort_keys=True),
                    mimetype='application/json')


@advertiser.route('/banners/user/<user_id>', methods=['GET'])
def banners_query(user_id):
    response = []
    ids = []
    banners = Ad_Banner.select().where(
        (Ad_Banner.banner_author_user_id == user_id) & (Ad_Banner.banner_file.is_null(False))).order_by(
        SQL("banner_size_id ASC"))

    for query in banners:
        ids.append(query.banner_file)

    result = files(ids)
    result = json.loads(result)
    result = result['body']

    for query in banners:
        record = {
            'banner_id': query.id,
            'banner_author_user_id': query.banner_author_user_id,
            'banner_updated_user_id': query.banner_updated_user_id,
            'banner_size': {'banner_size_id': query.banner_size.id,
                            'banner_size_width': query.banner_size.banner_size_width,
                            'banner_size_height': query.banner_size.banner_size_height},
            'banner_file': {
                'file_path': result[str(query.banner_file)]["file_path"] if str(query.banner_file) in result else '',
                'file_name': result[str(query.banner_file)]["file_name"] if str(query.banner_file) in result else ''},
            'banner_description': query.banner_description,
            'banner_created_at': str(query.banner_created_at),
            'banner_updated_at': str(query.banner_updated_at)
        }
        response.append(record)

    response = {"status": "ok", "body": response}
    return Response(json.dumps(response, sort_keys=True),
                    mimetype='application/json')


@advertiser.route('/blocked/website/user/<user_id>', methods=['GET'])
def blocked_website_query(user_id):
    response = []
    for query in Advertiser_Blocked_Website.select().where(
                    Advertiser_Blocked_Website.blocked_website_author_user_id == user_id):
        record = {
            'blocked_website_id': query.id,
            'blocked_website_author_user_id': query.blocked_website_author_user_id,
            'blocked_website_updated_user_id': query.blocked_website_updated_user_id,
            'blocked_website_url': query.blocked_website_url,
            'blocked_website_created_at': str(query.blocked_website_created_at),
            'blocked_website_updated_at': str(query.blocked_website_updated_at)
        }
        response.append(record)
    response = {"status": "ok", "body": response}
    return Response(json.dumps(response, sort_keys=True),
                    mimetype='application/json')


@advertiser.route('/campaign/<campaign_id>/banners', methods=['GET'])
def campaign_banners(campaign_id):
    response = []
    ids = []
    banners = Ad_Campaign_Ad_Banner.select().where(Ad_Campaign_Ad_Banner.campaign == campaign_id)

    for query in banners:
        ids.append(query.banner.banner_file)

    result = files(ids)
    result = json.loads(result)
    result = result['body']

    for query in banners:
        record = {
            'banner_id': query.banner.id,
            'banner_size': {'banner_size_width': query.banner.banner_size.banner_size_width,
                            'banner_size_height': query.banner.banner_size.banner_size_height},
            'banner_file': {
                'file_path': result[str(query.banner.banner_file)][
                    "file_path"] if query.banner.banner_file is not None else '',
                'file_name': result[str(query.banner.banner_file)][
                    "file_name"] if query.banner.banner_file is not None else ''},
            'banner_description': query.banner.banner_description
        }
        response.append(record)

    response = {"status": "ok", "body": response}
    return Response(json.dumps(response, sort_keys=True),
                    mimetype='application/json')


class AdCampaignRests(MethodView):
    def get(self, id):
        if id is None:
            response = []
            limit = int(500 if request.args.get('limit') is None else request.args.get('limit'))
            page = int(1 if request.args.get('page') is None else request.args.get('page'))
            order = str('DESC' if request.args.get('order') is None else request.args.get('order'))
            campaigns = []
            if request.args.get('user') is None:
                campaigns = Ad_Campaign.select(Ad_Campaign, Ad_Campaign_Type).join(Ad_Campaign_Type, on=(
                    Ad_Campaign.campaign_type == Ad_Campaign_Type.id)).order_by(
                    SQL("campaign_created_at " + order)).paginate(page, limit)

            elif request.args.get('user') is not None and request.args.get('status') is not None:
                campaigns = Ad_Campaign.select().where(
                    (Ad_Campaign.campaign_author_user_id == request.args.get('user')) &
                    (Ad_Campaign.campaign_is_deleted == 0) &
                    (Ad_Campaign.campaign_active_by_admin == 1))
            elif request.args.get('user') is not None:
                campaigns = Ad_Campaign.select().where(
                    (Ad_Campaign.campaign_author_user_id == request.args.get('user')) &
                    (Ad_Campaign.campaign_is_deleted == 0)
                ).order_by(
                    SQL("campaign_created_at " + order)).paginate(page, limit)

            for query in campaigns:
                record = {
                    'campaign_id': query.id,
                    'campaign_author_user_id': query.campaign_author_user_id,
                    'campaign_updated_user_id': query.campaign_updated_user_id,
                    'campaign_name': query.campaign_name,
                    'campaign_type': {
                        'campaign_type_name': query.campaign_type.campaign_type_name,
                        'campaign_type_title': query.campaign_type.campaign_type_title,
                        'campaign_type_base_price': query.campaign_type.campaign_type_base_price
                    },
                    'campaign_package_title': (
                        None if query.campaign_package is None else query.campaign_package.package_title),
                    'campaign_total_budget_main': query.campaign_total_budget_main,
                    'campaign_total_budget': query.campaign_total_budget,
                    'campaign_daily_budget': query.campaign_daily_budget,
                    'campaign_budget_management': query.campaign_budget_management,
                    'campaign_native_title': query.campaign_native_title,
                    'campaign_adwords_title': query.campaign_adwords_title,
                    'campaign_adwords_description': query.campaign_adwords_description,
                    'campaign_adwords_email': query.campaign_adwords_email,
                    'campaign_adwords_phone': query.campaign_adwords_phone,
                    'campaign_adwords_address': query.campaign_adwords_address,
                    'campaign_landing_page_url': query.campaign_landing_page_url,
                    'campaign_targeted_geography_all': query.campaign_targeted_geography_all,
                    'campaign_targeted_geography_iran': query.campaign_targeted_geography_iran,
                    'campaign_targeted_geography_not_iran': query.campaign_targeted_geography_not_iran,
                    'campaign_targeted_geography_special': query.campaign_targeted_geography_special,
                    'campaign_targeted_operating_system_all': query.campaign_targeted_operating_system_all,
                    'campaign_targeted_operating_system_special': query.campaign_targeted_operating_system_special,
                    'campaign_targeted_subject_all': query.campaign_targeted_subject_all,
                    'campaign_targeted_subject_special': query.campaign_targeted_subject_special,
                    'campaign_playtime_all': query.campaign_playtime_all,
                    'campaign_playtime_special': query.campaign_playtime_special,
                    'campaign_playtime_not_24_08': query.campaign_playtime_not_24_08,
                    'campaign_playtime_not_08_16': query.campaign_playtime_not_08_16,
                    'campaign_playtime_not_16_24': query.campaign_playtime_not_16_24,
                    'campaign_network_class_a': query.campaign_network_class_a,
                    'campaign_network_class_b': query.campaign_network_class_b,
                    'campaign_network_class_c': query.campaign_network_class_c,
                    'campaign_retargeting': query.campaign_retargeting,
                    'campaign_targeted_keyword_all': query.campaign_targeted_keyword_all,
                    'campaign_targeted_keyword_special': query.campaign_targeted_keyword_special,
                    'campaign_click_price': query.campaign_click_price,
                    'campaign_coef': query.campaign_coef,
                    'campaign_active_by_user': query.campaign_active_by_user,
                    'campaign_active_by_admin': query.campaign_active_by_admin,
                    'campaign_default': query.campaign_default,
                    'campaign_is_deleted': query.campaign_is_deleted,
                    'campaign_created_at': str(query.campaign_created_at),
                    'campaign_updated_at': str(query.campaign_updated_at),
                }
                response.append(record)
            response = {"status": "ok", "body": response}
            return Response(json.dumps(response, sort_keys=True),
                            mimetype='application/json')
        else:
            response = {}
            try:
                campaign = Ad_Campaign.get(Ad_Campaign.id == id)
                response = {
                    'campaign_id': campaign.id,
                    'campaign_author_user_id': campaign.campaign_author_user_id,
                    'campaign_updated_user_id': campaign.campaign_updated_user_id,
                    'campaign_name': campaign.campaign_name,
                    'campaign_type': {
                        'campaign_type_name': campaign.campaign_type.campaign_type_name,
                        'campaign_type_title': campaign.campaign_type.campaign_type_title,
                        'campaign_type_base_price': campaign.campaign_type.campaign_type_base_price
                    },
                    'campaign_package_title': (
                        None if campaign.campaign_package is None else campaign.campaign_package.package_title),
                    'campaign_total_budget_main': campaign.campaign_total_budget_main,
                    'campaign_total_budget': campaign.campaign_total_budget,
                    'campaign_daily_budget': campaign.campaign_daily_budget,
                    'campaign_budget_management': campaign.campaign_budget_management,
                    'campaign_native_title': campaign.campaign_native_title,
                    'campaign_adwords_title': campaign.campaign_adwords_title,
                    'campaign_adwords_description': campaign.campaign_adwords_description,
                    'campaign_adwords_email': campaign.campaign_adwords_email,
                    'campaign_adwords_phone': campaign.campaign_adwords_phone,
                    'campaign_adwords_address': campaign.campaign_adwords_address,
                    'campaign_landing_page_url': campaign.campaign_landing_page_url,
                    'campaign_targeted_geography_all': campaign.campaign_targeted_geography_all,
                    'campaign_targeted_geography_iran': campaign.campaign_targeted_geography_iran,
                    'campaign_targeted_geography_not_iran': campaign.campaign_targeted_geography_not_iran,
                    'campaign_targeted_geography_special': campaign.campaign_targeted_geography_special,
                    'campaign_targeted_operating_system_all': campaign.campaign_targeted_operating_system_all,
                    'campaign_targeted_operating_system_special': campaign.campaign_targeted_operating_system_special,
                    'campaign_targeted_subject_all': campaign.campaign_targeted_subject_all,
                    'campaign_targeted_subject_special': campaign.campaign_targeted_subject_special,
                    'campaign_playtime_all': campaign.campaign_playtime_all,
                    'campaign_playtime_special': campaign.campaign_playtime_special,
                    'campaign_playtime_not_24_08': campaign.campaign_playtime_not_24_08,
                    'campaign_playtime_not_08_16': campaign.campaign_playtime_not_08_16,
                    'campaign_playtime_not_16_24': campaign.campaign_playtime_not_16_24,
                    'campaign_network_class_a': campaign.campaign_network_class_a,
                    'campaign_network_class_b': campaign.campaign_network_class_b,
                    'campaign_network_class_c': campaign.campaign_network_class_c,
                    'campaign_retargeting': campaign.campaign_retargeting,
                    'campaign_targeted_keyword_all': campaign.campaign_targeted_keyword_all,
                    'campaign_targeted_keyword_special': campaign.campaign_targeted_keyword_special,
                    'campaign_click_price': campaign.campaign_click_price,
                    'campaign_coef': campaign.campaign_coef,
                    'campaign_active_by_user': campaign.campaign_active_by_user,
                    'campaign_active_by_admin': campaign.campaign_active_by_admin,
                    'campaign_default': campaign.campaign_default,
                    'campaign_is_deleted': campaign.campaign_is_deleted,
                    'campaign_created_at': str(campaign.campaign_created_at),
                    'campaign_updated_at': str(campaign.campaign_updated_at),
                }
                response = {"status": "ok", "body": response}
            except Ad_Campaign.DoesNotExist:
                response = {"status": "nok", "body": "Record Does Not Exist"}
            except Exception:
                response = {"status": "nok", "body": traceback.format_exc(sys.exc_info())}
            finally:
                return Response(json.dumps(response, sort_keys=True),
                                mimetype='application/json')

    def post(self):
        response = {}
        try:
            data = json.loads(request.data)
            date = datetime.datetime.now()
            campaign_type = Ad_Campaign_Type.get(Ad_Campaign_Type.campaign_type_name == data['campaign_type'])
            if campaign_type:
                result = Ad_Campaign.insert(
                    campaign_author_user_id=data['campaign_author_user_id'],
                    campaign_type=campaign_type.id,
                    campaign_coef=10,
                    campaign_active_by_user=False,
                    campaign_active_by_admin=False,
                    campaign_default=False,
                    campaign_is_deleted=False,
                    campaign_created_at=date.strftime("%Y-%m-%d %H:%M:%S"),
                    campaign_updated_at=date.strftime("%Y-%m-%d %H:%M:%S"),
                ).execute()
                response = {"status": "ok", "body": result}
            else:
                response = {"status": "nok", "body": "Campaign Type Does not Exist!"}
        except Exception:
            response = {"status": "nok", "body": traceback.format_exc(sys.exc_info())}
        finally:
            return Response(json.dumps(response, sort_keys=False),
                            mimetype='application/json')

    def delete(self, id):
        response = {}
        result = Ad_Campaign.delete().where(Ad_Campaign.id == id).execute()
        if result == 0:
            response = {"status": "nok", "body": "Record Does Not Exist"}
        else:
            response = {"status": "ok", "body": result}
        return Response(json.dumps(response, sort_keys=False),
                        mimetype='application/json')

    def put(self, id):
        response = {}
        try:
            data = json.loads(request.data)
            date = datetime.datetime.now()
            campaign = Ad_Campaign.get(Ad_Campaign.id == id)
            result = Ad_Campaign.update(
                campaign_updated_user_id=data['campaign_updated_user_id'],
                campaign_name=data.get('campaign_name', campaign.campaign_name),
                campaign_type=data.get('campaign_type', campaign.campaign_type),
                campaign_package=data.get('campaign_package', campaign.campaign_package),
                campaign_total_budget_main=data.get('campaign_total_budget_main', campaign.campaign_total_budget_main),
                campaign_total_budget=data.get('campaign_total_budget', campaign.campaign_total_budget),
                campaign_daily_budget=data.get('campaign_daily_budget', campaign.campaign_daily_budget),
                campaign_budget_management=data.get('campaign_budget_management', campaign.campaign_budget_management),
                campaign_native_title=data.get('campaign_native_title', campaign.campaign_native_title),
                campaign_adwords_title=data.get('campaign_adwords_title', campaign.campaign_adwords_title),
                campaign_adwords_description=data.get('campaign_adwords_description',
                                                      campaign.campaign_adwords_description),
                campaign_adwords_email=data.get('campaign_adwords_email', campaign.campaign_adwords_email),
                campaign_adwords_phone=data.get('campaign_adwords_phone', campaign.campaign_adwords_phone),
                campaign_adwords_address=data.get('campaign_adwords_address', campaign.campaign_adwords_address),
                campaign_landing_page_url=data.get('campaign_landing_page_url', campaign.campaign_landing_page_url),
                campaign_targeted_geography_all=data.get('campaign_targeted_geography_all',
                                                         campaign.campaign_targeted_geography_all),
                campaign_targeted_geography_iran=data.get('campaign_targeted_geography_iran',
                                                          campaign.campaign_targeted_geography_iran),
                campaign_targeted_geography_not_iran=data.get('campaign_targeted_geography_not_iran',
                                                              campaign.campaign_targeted_geography_not_iran),
                campaign_targeted_geography_special=data.get('campaign_targeted_geography_special',
                                                             campaign.campaign_targeted_geography_special),
                campaign_targeted_operating_system_all=data.get('campaign_targeted_operating_system_all',
                                                                campaign.campaign_targeted_operating_system_all),
                campaign_targeted_operating_system_special=data.get('campaign_targeted_operating_system_special',
                                                                    campaign.campaign_targeted_operating_system_special),
                campaign_targeted_subject_all=data.get('campaign_targeted_subject_all',
                                                       campaign.campaign_targeted_subject_all),
                campaign_targeted_subject_special=data.get('campaign_targeted_subject_special',
                                                           campaign.campaign_targeted_subject_special),
                campaign_playtime_all=data.get('campaign_playtime_all', campaign.campaign_playtime_all),
                campaign_playtime_special=data.get('campaign_playtime_special', campaign.campaign_playtime_special),
                campaign_playtime_not_24_08=data.get('campaign_playtime_not_24_08',
                                                     campaign.campaign_playtime_not_24_08),
                campaign_playtime_not_08_16=data.get('campaign_playtime_not_08_16',
                                                     campaign.campaign_playtime_not_08_16),
                campaign_playtime_not_16_24=data.get('campaign_playtime_not_16_24',
                                                     campaign.campaign_playtime_not_16_24),
                campaign_network_class_a=data.get('campaign_network_class_a',
                                                  campaign.campaign_network_class_a),
                campaign_network_class_b=data.get('campaign_network_class_b',
                                                  campaign.campaign_network_class_b),
                campaign_network_class_c=data.get('campaign_network_class_c',
                                                  campaign.campaign_network_class_c),
                campaign_retargeting=data.get('campaign_retargeting',
                                              campaign.campaign_retargeting),
                campaign_targeted_keyword_all=data.get('campaign_targeted_keyword_all',
                                                       campaign.campaign_targeted_keyword_all),
                campaign_targeted_keyword_special=data.get('campaign_targeted_keyword_special',
                                                           campaign.campaign_targeted_keyword_special),
                campaign_click_price=data.get('campaign_click_price', campaign.campaign_click_price),

                campaign_coef=data.get('campaign_coef', campaign.campaign_coef),
                campaign_active_by_user=data.get('campaign_active_by_user', campaign.campaign_active_by_user),
                campaign_active_by_admin=data.get('campaign_active_by_admin', campaign.campaign_active_by_admin),
                campaign_default=data.get('campaign_default', campaign.campaign_default),
                campaign_is_deleted=data.get('campaign_is_deleted', campaign.campaign_is_deleted),
                campaign_updated_at=date.strftime("%Y-%m-%d %H:%M:%S"),
            ).where(Ad_Campaign.id == id).execute()

            if data.get('campaign_os', None) is not None:
                Ad_Campaign_Targeted_Operating_System.delete().where(
                    Ad_Campaign_Targeted_Operating_System.campaign == id).execute()
                for os in data['campaign_os']:
                    Ad_Campaign_Targeted_Operating_System.create(
                        campaign=id,
                        os=int(os)
                    )

            if data.get('campaign_subject', None) is not None:
                Ad_Campaign_Targeted_Subject.delete().where(Ad_Campaign_Targeted_Subject.campaign == id).execute()
                for subject in data['campaign_subject']:
                    Ad_Campaign_Targeted_Subject.create(
                        campaign=id,
                        subject=int(subject)
                    )

            if data.get('campaign_geography', None) is not None:
                Ad_Campaign_Targeted_Geography.delete().where(Ad_Campaign_Targeted_Geography.campaign == id).execute()
                for geography in data['campaign_geography']:
                    Ad_Campaign_Targeted_Geography.create(
                        campaign=id,
                        geography=int(geography)
                    )

            if data.get('campaign_keyword', None) is not None:
                Ad_Campaign_Targeted_Keyword.delete().where(Ad_Campaign_Targeted_Keyword.campaign == id).execute()
                for title in data['campaign_keyword']:
                    try:
                        keyword = Targeted_Keyword.get(Targeted_Keyword.keyword_title == title.encode('utf-8'))
                    except Targeted_Keyword.DoesNotExist:
                        keyword = Targeted_Keyword.create(
                            keyword_author_user_id=data['campaign_updated_user_id'],
                            keyword_title=title,
                            keyword_created_at=date.strftime("%Y-%m-%d %H:%M:%S"),
                            keyword_updated_at=date.strftime("%Y-%m-%d %H:%M:%S")
                        )
                    Ad_Campaign_Targeted_Keyword.create(
                        campaign=id,
                        keyword=keyword.id
                    )

            if result == 0:
                response = {"status": "nok", "body": "Record Does Not Exist"}
            else:
                response = {"status": "ok", "body": result}
        except Exception:
            print(traceback.format_exc(sys.exc_info()))
            response = {"status": "nok", "body": traceback.format_exc(sys.exc_info())}
        finally:
            return Response(json.dumps(response, sort_keys=False),
                            mimetype='application/json')


class AdBannerRests(MethodView):
    def get(self, id):
        if id is None:
            response = []
            limit = int(20 if request.args.get('limit') is None else request.args.get('limit'))
            page = int(1 if request.args.get('page') is None else request.args.get('page'))
            order = str('DESC' if request.args.get('order') is None else request.args.get('order'))
            for query in Ad_Banner.select().order_by(SQL("banner_created_at " + order)).paginate(page, limit):
                record = {
                    'banner_id': query.id,
                    'banner_author_user_id': query.banner_author_user_id,
                    'banner_updated_user_id': query.banner_updated_user_id,
                    'banner_size': query.banner_size,
                    'banner_file': query.banner_file,
                    'banner_description': query.banner_description,
                    'banner_created_at': str(query.banner_created_at),
                    'banner_updated_at': str(query.banner_updated_at)
                }
                response.append(record)
            response = {"status": "ok", "body": response}
            return Response(json.dumps(response, sort_keys=True),
                            mimetype='application/json')
        else:
            response = {}
            try:
                banner = Ad_Banner.get(Ad_Banner.id == id)
                response = {
                    'banner_id': banner.id,
                    'banner_author_user_id': banner.banner_author_user_id,
                    'banner_updated_user_id': banner.banner_updated_user_id,
                    'banner_size': banner.banner_size,
                    'banner_file': banner.banner_file,
                    'banner_description': banner.banner_description,
                    'banner_created_at': str(banner.banner_created_at),
                    'banner_updated_at': str(banner.banner_updated_at)
                }
                response = {"status": "ok", "body": response}
            except Ad_Banner.DoesNotExist:
                response = {"status": "nok", "body": "Record Does Not Exist"}
            except Exception:
                response = {"status": "nok", "body": traceback.format_exc(sys.exc_info())}
            finally:
                return Response(json.dumps(response, sort_keys=True),
                                mimetype='application/json')

    def post(self):
        response = {}
        try:
            data = json.loads(request.data)
            date = datetime.datetime.now()
            result = Ad_Banner.insert(
                banner_author_user_id=data['banner_author_user_id'],
                banner_size=data.get('banner_size', None),
                banner_file=data.get('banner_file', None),
                banner_description=data.get('banner_description', None),
                banner_created_at=date.strftime("%Y-%m-%d %H:%M:%S"),
                banner_updated_at=date.strftime("%Y-%m-%d %H:%M:%S")
            ).execute()
            response = {"status": "ok", "body": result}
        except Exception:
            response = {"status": "nok", "body": traceback.format_exc(sys.exc_info())}
        finally:
            return Response(json.dumps(response, sort_keys=False),
                            mimetype='application/json')

    def delete(self, id):
        response = {}
        result = Ad_Banner.delete().where(Ad_Banner.id == id).execute()
        if result == 0:
            response = {"status": "nok", "body": "Record Does Not Exist"}
        else:
            response = {"status": "ok", "body": result}
        return Response(json.dumps(response, sort_keys=False),
                        mimetype='application/json')

    def put(self, id):
        response = {}
        try:
            data = json.loads(request.data)
            date = datetime.datetime.now()
            banner = Ad_Banner.get(Ad_Banner.id == id)
            result = Ad_Banner.update(
                banner_updated_user_id=data['banner_updated_user_id'],
                banner_size=data.get('banner_size', banner.banner_size),
                banner_file=data.get('banner_file', banner.banner_file),
                banner_description=data.get('banner_description', banner.banner_description),
                banner_updated_at=date.strftime("%Y-%m-%d %H:%M:%S")
            ).where(Ad_Banner.id == id).execute()
            if result == 0:
                response = {"status": "nok", "body": "Record Does Not Exist"}
            else:
                response = {"status": "ok", "body": result}
        except Exception:
            response = {"status": "nok", "body": traceback.format_exc(sys.exc_info())}
        finally:
            return Response(json.dumps(response, sort_keys=False),
                            mimetype='application/json')


class AdCampaignAdBannerRests(MethodView):
    def get(self, id):
        if id is None:
            response = []
            campaign_id = request.args.get('campaign')
            ids = []
            banners = Ad_Campaign_Ad_Banner.select().where(Ad_Campaign_Ad_Banner.campaign == campaign_id)

            for query in banners:
                ids.append(query.banner.banner_file)

            result = files(ids)
            result = json.loads(result)
            result = result['body']

            for query in banners:
                record = {
                    'ad_Campaign_ad_banner_id': query.id,
                    'campaign': query.campaign.id,
                    'banner': {
                        'banner_id': query.banner.id,
                        'banner_author_user_id': query.banner.banner_author_user_id,
                        'banner_updated_user_id': query.banner.banner_updated_user_id,
                        'banner_size': query.banner.banner_size.id,
                        'banner_file': {
                            'file_path': result[str(query.banner.banner_file)][
                                "file_path"] if query.banner.banner_file is not None else '',
                            'file_name': result[str(query.banner.banner_file)][
                                "file_name"] if query.banner.banner_file is not None else ''},
                        'banner_description': query.banner.banner_description,
                        'banner_created_at': str(query.banner.banner_created_at),
                        'banner_updated_at': str(query.banner.banner_updated_at)
                    }
                }
                response.append(record)

            response = {"status": "ok", "body": response}
            return Response(json.dumps(response, sort_keys=True),
                            mimetype='application/json')
        else:
            pass

    def post(self):
        response = {}
        try:
            data = json.loads(request.data)
            result = Ad_Campaign_Ad_Banner.insert(
                campaign=data.get('campaign', None),
                banner=data.get('banner', None),
            ).execute()
            response = {"status": "ok", "body": result}
        except Exception:
            response = {"status": "nok", "body": traceback.format_exc(sys.exc_info())}
        finally:
            return Response(json.dumps(response, sort_keys=False),
                            mimetype='application/json')

    def delete(self, id):
        response = {}
        if id is None:
            campaign_id = request.args.get('campaign')
            result = Ad_Campaign_Ad_Banner.delete().where(Ad_Campaign_Ad_Banner.campaign == campaign_id).execute()
        else:
            result = Ad_Campaign_Ad_Banner.delete().where(Ad_Campaign_Ad_Banner.id == id).execute()

        if result == 0:
            response = {"status": "nok", "body": "Record Does Not Exist"}
        else:
            response = {"status": "ok", "body": result}
        return Response(json.dumps(response, sort_keys=False),
                        mimetype='application/json')

    def put(self, id):
        pass


class AdCampaignTargetedOperatingSystemRests(MethodView):
    def get(self, id):
        if id is None:
            response = []
            campaign_id = request.args.get('campaign')
            for query in Ad_Campaign_Targeted_Operating_System.select().where(
                            Ad_Campaign_Targeted_Operating_System.campaign == campaign_id):
                record = {
                    'ad_campaign_targeted_operating_system_id': query.id,
                    'campaign': query.campaign.id,
                    'os': {
                        'os_id': query.os.id,
                        'os_author_user_id': query.os.os_author_user_id,
                        'os_updated_user_id': query.os.os_updated_user_id,
                        'os_name': query.os.os_name,
                        'os_title': query.os.os_title,
                        'os_created_at': str(query.os.os_created_at),
                        'os_updated_at': str(query.os.os_updated_at)
                    }
                }
                response.append(record)
            response = {"status": "ok", "body": response}
            return Response(json.dumps(response, sort_keys=True),
                            mimetype='application/json')
        else:
            pass

    def post(self):
        response = {}
        try:
            data = json.loads(request.data)
            result = Ad_Campaign_Targeted_Operating_System.insert(
                campaign=data.get('campaign', None),
                os=data.get('os', None),
            ).execute()
            response = {"status": "ok", "body": result}
        except Exception:
            response = {"status": "nok", "body": traceback.format_exc(sys.exc_info())}
        finally:
            return Response(json.dumps(response, sort_keys=False),
                            mimetype='application/json')

    def delete(self, id):
        response = {}
        if id is None:
            campaign_id = request.args.get('campaign')
            result = Ad_Campaign_Targeted_Operating_System.delete().where(
                Ad_Campaign_Targeted_Operating_System.campaign == campaign_id).execute()
        else:
            result = Ad_Campaign_Targeted_Operating_System.delete().where(
                Ad_Campaign_Targeted_Operating_System.id == id).execute()
        if result == 0:
            response = {"status": "nok", "body": "Record Does Not Exist"}
        else:
            response = {"status": "ok", "body": result}
        return Response(json.dumps(response, sort_keys=False),
                        mimetype='application/json')

    def put(self, id):
        pass


class AdCampaignTargetedSubjectRests(MethodView):
    def get(self, id):
        if id is None:
            response = []
            campaign_id = request.args.get('campaign')
            for query in Ad_Campaign_Targeted_Subject.select().where(
                            Ad_Campaign_Targeted_Subject.campaign == campaign_id):
                record = {
                    'ad_campaign_targeted_subject_id': query.id,
                    'campaign': query.campaign.id,
                    'subject': {
                        'subject_id': query.subject.id,
                        'subject_author_user_id': query.subject.subject_author_user_id,
                        'subject_updated_user_id': query.subject.subject_updated_user_id,
                        'subject_name': query.subject.subject_name,
                        'subject_title': query.subject.subject_title,
                        'subject_created_at': str(query.subject.subject_created_at),
                        'subject_updated_at': str(query.subject.subject_updated_at)
                    }
                }
                response.append(record)
            response = {"status": "ok", "body": response}
            return Response(json.dumps(response, sort_keys=True),
                            mimetype='application/json')
        else:
            pass

    def post(self):
        response = {}
        try:
            data = json.loads(request.data)
            result = Ad_Campaign_Targeted_Subject.insert(
                campaign=data.get('campaign', None),
                subject=data.get('subject', None),
            ).execute()
            response = {"status": "ok", "body": result}
        except Exception:
            response = {"status": "nok", "body": traceback.format_exc(sys.exc_info())}
        finally:
            return Response(json.dumps(response, sort_keys=False),
                            mimetype='application/json')

    def delete(self, id):
        response = {}
        if id is None:
            campaign_id = request.args.get('campaign')
            result = Ad_Campaign_Targeted_Subject.delete().where(
                Ad_Campaign_Targeted_Subject.campaign == campaign_id).execute()
        else:
            result = Ad_Campaign_Targeted_Subject.delete().where(Ad_Campaign_Targeted_Subject.id == id).execute()
        if result == 0:
            response = {"status": "nok", "body": "Record Does Not Exist"}
        else:
            response = {"status": "ok", "body": result}
        return Response(json.dumps(response, sort_keys=False),
                        mimetype='application/json')

    def put(self, id):
        pass


class AdCampaignTargetedGeographyRests(MethodView):
    def get(self, id):
        if id is None:
            response = []
            campaign_id = request.args.get('campaign')
            for query in Ad_Campaign_Targeted_Geography.select().where(
                            Ad_Campaign_Targeted_Geography.campaign == campaign_id):
                record = {
                    'ad_campaign_targeted_geography_id': query.id,
                    'campaign': query.campaign.id,
                    'geography': {
                        'geography_id': query.geography.id,
                        'geography_author_user_id': query.geography.geography_author_user_id,
                        'geography_updated_user_id': query.geography.geography_updated_user_id,
                        'geography_name': query.geography.geography_name,
                        'geography_title': query.geography.geography_title,
                        'geography_created_at': str(query.geography.geography_created_at),
                        'geography_updated_at': str(query.geography.geography_updated_at)
                    }
                }
                response.append(record)
            response = {"status": "ok", "body": response}
            return Response(json.dumps(response, sort_keys=True),
                            mimetype='application/json')
        else:
            pass

    def post(self):
        response = {}
        try:
            data = json.loads(request.data)
            result = Ad_Campaign_Targeted_Geography.insert(
                campaign=data.get('campaign', None),
                geography=data.get('geography', None),
            ).execute()
            response = {"status": "ok", "body": result}
        except Exception:
            response = {"status": "nok", "body": traceback.format_exc(sys.exc_info())}
        finally:
            return Response(json.dumps(response, sort_keys=False),
                            mimetype='application/json')

    def delete(self, id):
        response = {}
        if id is None:
            campaign_id = request.args.get('campaign')
            result = Ad_Campaign_Targeted_Geography.delete().where(
                Ad_Campaign_Targeted_Geography.campaign == campaign_id).execute()
        else:
            result = Ad_Campaign_Targeted_Geography.delete().where(Ad_Campaign_Targeted_Geography.id == id).execute()
        if result == 0:
            response = {"status": "nok", "body": "Record Does Not Exist"}
        else:
            response = {"status": "ok", "body": result}
        return Response(json.dumps(response, sort_keys=False),
                        mimetype='application/json')

    def put(self, id):
        pass


class AdCampaignTargetedKeywordRests(MethodView):
    def get(self, id):
        if id is None:
            response = []
            campaign_id = request.args.get('campaign')
            for query in Ad_Campaign_Targeted_Keyword.select().where(
                            Ad_Campaign_Targeted_Keyword.campaign == campaign_id):
                record = {
                    'ad_campaign_targeted_keyword_id': query.id,
                    'campaign': query.campaign.id,
                    'keyword': {
                        'keyword_id': query.keyword.id,
                        'keyword_author_user_id': query.keyword.keyword_author_user_id,
                        'keyword_updated_user_id': query.keyword.keyword_updated_user_id,
                        'keyword_title': query.keyword.keyword_title,
                        'keyword_created_at': str(query.keyword.keyword_created_at),
                        'keyword_updated_at': str(query.keyword.keyword_updated_at)
                    }
                }
                response.append(record)
            response = {"status": "ok", "body": response}
            return Response(json.dumps(response, sort_keys=True),
                            mimetype='application/json')
        else:
            pass

    def post(self):
        response = {}
        try:
            data = json.loads(request.data)
            result = Ad_Campaign_Targeted_Keyword.insert(
                campaign=data.get('campaign', None),
                keyword=data.get('keyword', None),
            ).execute()
            response = {"status": "ok", "body": result}
        except Exception:
            response = {"status": "nok", "body": traceback.format_exc(sys.exc_info())}
        finally:
            return Response(json.dumps(response, sort_keys=False),
                            mimetype='application/json')

    def delete(self, id):
        response = {}
        if id is None:
            campaign_id = request.args.get('campaign')
            result = Ad_Campaign_Targeted_Keyword.delete().where(
                Ad_Campaign_Targeted_Keyword.campaign == campaign_id).execute()
        else:
            result = Ad_Campaign_Targeted_Keyword.delete().where(Ad_Campaign_Targeted_Keyword.id == id).execute()
        if result == 0:
            response = {"status": "nok", "body": "Record Does Not Exist"}
        else:
            response = {"status": "ok", "body": result}
        return Response(json.dumps(response, sort_keys=False),
                        mimetype='application/json')

    def put(self, id):
        pass


class AdvertiserBlockedWebsiteRests(MethodView):
    def get(self, id):
        if id is None:
            response = []
            limit = int(20 if request.args.get('limit') is None else request.args.get('limit'))
            page = int(1 if request.args.get('page') is None else request.args.get('page'))
            order = str('DESC' if request.args.get('order') is None else request.args.get('order'))

            websites = []
            if request.args.get('user') is None:
                websites = Advertiser_Blocked_Website.select().order_by(
                    SQL("blocked_website_created_at " + order)).paginate(page, limit)
            else:
                websites = Advertiser_Blocked_Website.select().where(
                    Advertiser_Blocked_Website.blocked_website_author_user_id == request.args.get('user')).order_by(
                    SQL("blocked_website_created_at " + order)).paginate(page, limit)

            for query in websites:
                record = {
                    'blocked_website_id': query.id,
                    'blocked_website_author_user_id': query.blocked_website_author_user_id,
                    'blocked_website_updated_user_id': query.blocked_website_updated_user_id,
                    'blocked_website_url': query.blocked_website_url,
                    'blocked_website_created_at': str(query.blocked_website_created_at),
                    'blocked_website_updated_at': str(query.blocked_website_updated_at)
                }
                response.append(record)
            response = {"status": "ok", "body": response}
            return Response(json.dumps(response, sort_keys=True),
                            mimetype='application/json')
        else:
            response = {}
            try:
                blocked_website = Advertiser_Blocked_Website.get(Advertiser_Blocked_Website.id == id)
                response = {
                    'blocked_website_id': blocked_website.id,
                    'blocked_website_author_user_id': blocked_website.blocked_website_author_user_id,
                    'blocked_website_updated_user_id': blocked_website.blocked_website_updated_user_id,
                    'blocked_website_url': blocked_website.blocked_website_url,
                    'blocked_website_created_at': str(blocked_website.blocked_website_created_at),
                    'blocked_website_updated_at': str(blocked_website.blocked_website_updated_at)
                }
                response = {"status": "ok", "body": response}
            except Advertiser_Blocked_Website.DoesNotExist:
                response = {"status": "nok", "body": "Record Does Not Exist"}
            except Exception:
                response = {"status": "nok", "body": traceback.format_exc(sys.exc_info())}
            finally:
                return Response(json.dumps(response, sort_keys=True),
                                mimetype='application/json')

    def post(self):
        response = {}
        try:
            data = json.loads(request.data)
            date = datetime.datetime.now()
            result = Advertiser_Blocked_Website.insert(
                blocked_website_author_user_id=data['blocked_website_author_user_id'],
                blocked_website_url=data.get('blocked_website_url', None),
                blocked_website_created_at=date.strftime("%Y-%m-%d %H:%M:%S"),
                blocked_website_updated_at=date.strftime("%Y-%m-%d %H:%M:%S")
            ).execute()
            response = {"status": "ok", "body": result}
        except Exception:
            response = {"status": "nok", "body": traceback.format_exc(sys.exc_info())}
        finally:
            return Response(json.dumps(response, sort_keys=False),
                            mimetype='application/json')

    def delete(self, id):
        response = {}
        result = Advertiser_Blocked_Website.delete().where(Advertiser_Blocked_Website.id == id).execute()
        if result == 0:
            response = {"status": "nok", "body": "Record Does Not Exist"}
        else:
            response = {"status": "ok", "body": result}
        return Response(json.dumps(response, sort_keys=False),
                        mimetype='application/json')

    def put(self, id):
        response = {}
        try:
            data = json.loads(request.data)
            date = datetime.datetime.now()
            blocked_website = Advertiser_Blocked_Website.get(Advertiser_Blocked_Website.id == id)
            result = Advertiser_Blocked_Website.update(
                blocked_website_updated_user_id=data['blocked_website_updated_user_id'],
                blocked_website_url=data.get('blocked_website_url', blocked_website.blocked_website_url),
                blocked_website_updated_at=date.strftime("%Y-%m-%d %H:%M:%S")
            ).where(Advertiser_Blocked_Website.id == id).execute()
            if result == 0:
                response = {"status": "nok", "body": "Record Does Not Exist"}
            else:
                response = {"status": "ok", "body": result}
        except Exception:
            response = {"status": "nok", "body": traceback.format_exc(sys.exc_info())}
        finally:
            return Response(json.dumps(response, sort_keys=False),
                            mimetype='application/json')


def register_api(view, endpoint, url, pk='id', pk_type='int'):
    view_func = view.as_view(endpoint)
    advertiser.add_url_rule(url, defaults={pk: None},
                            view_func=view_func, methods=['GET', 'DELETE'])
    advertiser.add_url_rule(url, view_func=view_func, methods=['POST', ])
    advertiser.add_url_rule('%s/<%s:%s>' % (url, pk_type, pk),
                            view_func=view_func,
                            methods=['GET', 'PUT', 'DELETE'])


register_api(AdCampaignRests, 'AdCampaignRests', '/campaign', pk='id')
register_api(AdBannerRests, 'AdBannerRests', '/banner', pk='id')
register_api(AdCampaignAdBannerRests, 'AdCampaignAdBannerRests', '/campaign/banner', pk='id')
register_api(AdCampaignTargetedOperatingSystemRests, 'AdCampaignTargetedOperatingSystemRests', '/campaign/os', pk='id')
register_api(AdCampaignTargetedSubjectRests, 'AdCampaignTargetedSubjectRests', '/campaign/subject', pk='id')
register_api(AdCampaignTargetedGeographyRests, 'AdCampaignTargetedGeographyRests', '/campaign/geography', pk='id')
register_api(AdCampaignTargetedKeywordRests, 'AdCampaignTargetedKeywordRests', '/campaign/keyword', pk='id')
register_api(AdvertiserBlockedWebsiteRests, 'AdvertiserBlockedWebsiteRests', '/blocked/website', pk='id')


@advertiser.before_request
def _db_connect():
    if not db.is_closed():
        db.close()
    db.connect()


# This hook ensures that the connection is closed when we've finished
# processing the request.
@advertiser.teardown_request
def _db_close(exc):
    if not db.is_closed():
        db.close()
