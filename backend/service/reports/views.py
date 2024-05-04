from datetime import datetime
import json
import sys
import traceback
from flask import request, Response
from flask.views import MethodView
from slugify import slugify_unicode
import dateutil.relativedelta
import calendar
from models import *
from . import reports
from ..advertiser.views import user_campaigns
from ..publisher.views import user_websites


@reports.route('/api/show/counter', methods=['POST'])
def ad_show_counter_post_api():
    response = {}
    try:
        # data = json.loads(request.data)
        data = request.json
        result = Ad_Show_Counter.insert(
            ad_show_publisher=data.get('ad_show_publisher_id', None),
            ad_show_campaign=data.get('ad_show_campaign_id', None),
            ad_show_banner_size=data.get('ad_show_banner_size', None),
            ad_show_date_hour=data.get('ad_show_date_hour', None),
            ad_show_date_day=data.get('ad_show_date_day', None),
            ad_show_date_month=data.get('ad_show_date_month', None),
            ad_show_date_year=data.get('ad_show_date_year', None),
            ad_show_date=data.get('ad_show_date', None),
            ad_show_counter=data.get('ad_show_counter', None)
        ).execute()
        response = {"status": "yes"}
    except Exception:
        response = {"status": "no"}
    finally:
        return Response(json.dumps(response, sort_keys=False),
                        mimetype='application/json')


@reports.route('/api/click/counter', methods=['POST'])
def ad_click_counter_post_api():
    response = {}
    try:
        data = request.json
        result = Ad_Click_Counter.insert(
            ad_click_publisher=data.get('ad_click_publisher_id', None),
            ad_click_campaign=data.get('ad_click_campaign_id', None),
            ad_click_banner_size=data.get('ad_click_banner_size', None),
            ad_click_date_hour=data.get('ad_click_date_hour', None),
            ad_click_date_day=data.get('ad_click_date_day', None),
            ad_click_date_month=data.get('ad_click_date_month', None),
            ad_click_date_year=data.get('ad_click_date_year', None),
            ad_click_date=data.get('ad_click_date', None),
            ad_click_counter=data.get('ad_click_counter', None)
        ).execute()
        response = {"status": "yes"}
    except Exception:
        response = {"status": "no"}
    finally:
        return Response(json.dumps(response, sort_keys=False),
                        mimetype='application/json')


@reports.route('/admin/campaign/ctr', methods=['POST'])
def admin_campaign_ctr():
    response = {
        "clicks": {},
        "shows": {}
    }
    data = json.loads(request.data)
    from_date = data['from_date']
    to_date = data['to_date']

    records = Ad_Click_Counter.select(Ad_Click_Counter.ad_click_campaign,
                                      fn.SUM(Ad_Click_Counter.ad_click_counter).alias('click_count')).where(
        Ad_Click_Counter.ad_click_date.between(from_date,
                                               to_date)).group_by(
        Ad_Click_Counter.ad_click_campaign)

    for query in records:
        response["clicks"][query.ad_click_campaign.id] = {'ad_click_counter': int(query.click_count),
                                                          'ad_click_campaign_author_user_id': query.ad_click_campaign.campaign_author_user_id,
                                                          'ad_click_campaign_name': query.ad_click_campaign.campaign_name,
                                                          'ad_click_campaign_type': query.ad_click_campaign.campaign_type.campaign_type_title}

    records = Ad_Show_Counter.select(Ad_Show_Counter.ad_show_campaign,
                                     fn.SUM(Ad_Show_Counter.ad_show_counter).alias('show_count')).where(
        Ad_Show_Counter.ad_show_date.between(from_date,
                                             to_date)).group_by(
        Ad_Show_Counter.ad_show_campaign)

    for query in records:
        response["shows"][query.ad_show_campaign.id] = {'ad_show_counter': int(query.show_count),
                                                        'ad_show_campaign_author_user_id': query.ad_show_campaign.campaign_author_user_id,
                                                        'ad_show_campaign_author_name': query.ad_show_campaign.campaign_name,
                                                        'ad_show_campaign_type': query.ad_show_campaign.campaign_type.campaign_type_title}

    response = {"status": "ok", "body": response}
    return Response(json.dumps(response, sort_keys=True),
                    mimetype='application/json')


@reports.route('/admin/one/campaign/ctr', methods=['POST'])
def admin_one_campaign_ctr():
    response = []
    data = json.loads(request.data)
    from_date = data['from_date']
    to_date = data['to_date']
    campaign_id = data['campaign_id']

    records = Ad_Click_Counter.select(Ad_Click_Counter.ad_click_campaign,
                                      fn.SUM(Ad_Click_Counter.ad_click_counter).alias('click_count')).where(
        (Ad_Click_Counter.ad_click_date.between(from_date,
                                                to_date)) & (
        Ad_Click_Counter.ad_click_campaign == campaign_id)).group_by(
        Ad_Click_Counter.ad_click_campaign)

    click_count = 0
    for query in records:
        click_count = int(query.click_count)

    records = Ad_Show_Counter.select(Ad_Show_Counter.ad_show_campaign,
                                     fn.SUM(Ad_Show_Counter.ad_show_counter).alias('show_count')).where((
                                                                                                            Ad_Show_Counter.ad_show_date.between(
                                                                                                                from_date,
                                                                                                                to_date)) & (
                                                                                                        Ad_Show_Counter.ad_show_campaign == campaign_id)).group_by(
        Ad_Show_Counter.ad_show_campaign)

    for query in records:
        response = {'ad_click_counter': click_count, 'ad_show_counter': int(query.show_count),
                    'ad_show_campaign_author_user_id': query.ad_show_campaign.campaign_author_user_id,
                    'ad_show_campaign_author_name': query.ad_show_campaign.campaign_name,
                    'ad_show_campaign_type': query.ad_show_campaign.campaign_type.campaign_type_title,
                    'ad_show_campaign_total_budget': query.ad_show_campaign.campaign_total_budget,
                    'ad_show_campaign_landing_page_url': query.ad_show_campaign.campaign_landing_page_url}

    response = {"status": "ok", "body": response}
    return Response(json.dumps(response, sort_keys=True),
                    mimetype='application/json')


@reports.route('/admin/website/ctr', methods=['POST'])
def admin_publishers_ctr():
    response = {
        "clicks": {},
        "shows": {}
    }
    data = json.loads(request.data)
    from_date = data['from_date']
    to_date = data['to_date']

    records = Ad_Click_Counter.select(Ad_Click_Counter.ad_click_publisher,
                                      fn.SUM(Ad_Click_Counter.ad_click_counter).alias('click_count')).where(
        Ad_Click_Counter.ad_click_date.between(from_date,
                                               to_date)).group_by(
        Ad_Click_Counter.ad_click_publisher)

    for query in records:
        response["clicks"][str(query.ad_click_publisher.publisher_website_url)] = {
            'ad_click_counter': int(query.click_count),
            'ad_click_publisher': query.ad_click_publisher.publisher_website_author_user_id}

    records = Ad_Show_Counter.select(Ad_Show_Counter.ad_show_publisher,
                                     fn.SUM(Ad_Show_Counter.ad_show_counter).alias('show_count')).where(
        Ad_Show_Counter.ad_show_date.between(from_date,
                                             to_date)).group_by(
        Ad_Show_Counter.ad_show_publisher)

    for query in records:
        response["shows"][str(query.ad_show_publisher.publisher_website_url)] = {
            'ad_show_counter': int(query.show_count),
            'ad_show_publisher': query.ad_show_publisher.publisher_website_author_user_id}

    response = {"status": "ok", "body": response}
    return Response(json.dumps(response, sort_keys=True),
                    mimetype='application/json')



@reports.route('/admin/one/website/ctr', methods=['POST'])
def admin_publishers_one_ctr():
    response = []

    data = json.loads(request.data)
    from_date = data['from_date']
    to_date = data['to_date']
    website_id = data['website_id']


    records = Ad_Click_Counter.select(Ad_Click_Counter.ad_click_publisher,
                                      fn.SUM(Ad_Click_Counter.ad_click_counter).alias('click_count')).where((
        Ad_Click_Counter.ad_click_date.between(from_date,
                                               to_date))&(Ad_Click_Counter.ad_click_publisher == website_id)).group_by(
        Ad_Click_Counter.ad_click_publisher)


    ad_click_counter = 0
    for query in records:
        ad_click_counter= int(query.click_count)


    records = Ad_Show_Counter.select(Ad_Show_Counter.ad_show_publisher,
                                     fn.SUM(Ad_Show_Counter.ad_show_counter).alias('show_count')).where((
        Ad_Show_Counter.ad_show_date.between(from_date,
                                             to_date))&(Ad_Show_Counter.ad_show_publisher == website_id)).group_by(
        Ad_Show_Counter.ad_show_publisher)

    for query in records:
        response = {'ad_click_counter': ad_click_counter, 'ad_show_counter': int(query.show_count),
                    'ad_show_publisher': query.ad_show_publisher.publisher_website_author_user_id,
                    'publisher_website_title': query.ad_show_publisher.publisher_website_title,
                    'publisher_website_url': query.ad_show_publisher.publisher_website_url
       }


    response = {"status": "ok", "body": response}
    return Response(json.dumps(response, sort_keys=True),
                    mimetype='application/json')




@reports.route('/admin/dashboard/period', methods=['POST'])
def admin_dashboard_period():
    response = {
        "clicks": {},
        "shows": {}
    }

    data = json.loads(request.data)
    from_date = data['from_date']
    to_date = data['to_date']

    from_date_counter = datetime.strptime(to_date, "%Y-%m-%d %H:%M:%S") - dateutil.relativedelta.relativedelta(days=1)

    campaigns_count = Ad_Show_Counter.select().where(
        Ad_Show_Counter.ad_show_date.between(from_date_counter,
                                             to_date)).group_by(
        Ad_Show_Counter.ad_show_campaign).wrapped_count()

    websites_count = Ad_Show_Counter.select().where(
        Ad_Show_Counter.ad_show_date.between(from_date_counter,
                                             to_date)).group_by(
        Ad_Show_Counter.ad_show_publisher).wrapped_count()

    response["campaigns_count"] = campaigns_count
    response["websites_count"] = websites_count

    records = Ad_Click_Counter.select(Ad_Click_Counter.ad_click_date_day, Ad_Click_Counter.ad_click_date_month,
                                      Ad_Click_Counter.ad_click_date_year,
                                      fn.SUM(Ad_Click_Counter.ad_click_counter).alias('click_count')).where(
        Ad_Click_Counter.ad_click_date.between(from_date,
                                               to_date)).group_by(
        SQL("ad_click_date_year, ad_click_date_month, ad_click_date_day")).order_by(
        SQL("ad_click_date_year ASC, ad_click_date_month ASC, ad_click_date_day ASC"))

    response["clicks_count"] = 0
    for query in records:
        z = datetime(int(query.ad_click_date_year), int(query.ad_click_date_month), int(query.ad_click_date_day), 0, 0,
                     0)
        unixtime = calendar.timegm(z.timetuple())
        unixtime = str(unixtime)
        unixtime = unixtime[:10] + "000"
        response["clicks"][unixtime] = int(query.click_count)
        response["clicks_count"] = response["clicks_count"] + int(query.click_count)

    records = Ad_Show_Counter.select(Ad_Show_Counter.ad_show_date_day, Ad_Show_Counter.ad_show_date_month,
                                     Ad_Show_Counter.ad_show_date_year,
                                     fn.SUM(Ad_Show_Counter.ad_show_counter).alias('show_count')).where(
        Ad_Show_Counter.ad_show_date.between(from_date,
                                             to_date)).group_by(
        SQL("ad_show_date_year, ad_show_date_month, ad_show_date_day")).order_by(
        SQL(
            "ad_show_date_year ASC, ad_show_date_month ASC, ad_show_date_day ASC"))

    response["shows_count"] = 0
    for query in records:
        z = datetime(int(query.ad_show_date_year), int(query.ad_show_date_month), int(query.ad_show_date_day), 0, 0,
                     0)
        unixtime = calendar.timegm(z.timetuple())
        unixtime = str(unixtime)
        unixtime = unixtime[:10] + "000"
        response["shows"][unixtime] = int(query.show_count)
        response["shows_count"] = response["shows_count"] + int(query.show_count)

    response = {"status": "ok", "body": response}
    return Response(json.dumps(response, sort_keys=True),
                    mimetype='application/json')


@reports.route('/advertiser/dashboard/period', methods=['POST'])
def advertiser_dashboard_period():
    response = {
        "clicks": {},
        "shows": {}
    }
    data = json.loads(request.data)
    from_date = data['from_date']
    to_date = data['to_date']
    user_id = data['user']

    result = user_campaigns(user_id)
    result = json.loads(result)
    campaigns = result['body']
    response["campaigns_count"] = len(campaigns)

    records = Ad_Click_Counter.select(Ad_Click_Counter.ad_click_date_day, Ad_Click_Counter.ad_click_date_month,
                                      Ad_Click_Counter.ad_click_date_year,
                                      fn.SUM(Ad_Click_Counter.ad_click_counter).alias('click_count')).where(
        (Ad_Click_Counter.ad_click_campaign << campaigns) &
        (Ad_Click_Counter.ad_click_date.between(from_date,
                                                to_date))).group_by(
        SQL("ad_click_date_year, ad_click_date_month, ad_click_date_day")).order_by(
        SQL(
            "ad_click_date_year ASC, ad_click_date_month ASC, ad_click_date_day ASC"))

    response["clicks_count"] = 0
    for query in records:
        z = datetime(int(query.ad_click_date_year), int(query.ad_click_date_month), int(query.ad_click_date_day), 0, 0,
                     0)
        unixtime = calendar.timegm(z.timetuple())
        unixtime = str(unixtime)
        unixtime = unixtime[:10] + "000"
        response["clicks"][unixtime] = int(query.click_count)
        response["clicks_count"] = response["clicks_count"] + int(query.click_count)

    records = Ad_Show_Counter.select(Ad_Show_Counter.ad_show_date_day, Ad_Show_Counter.ad_show_date_month,
                                     Ad_Show_Counter.ad_show_date_year,
                                     fn.SUM(Ad_Show_Counter.ad_show_counter).alias('show_count')).where(
        (Ad_Show_Counter.ad_show_campaign << campaigns) &
        (Ad_Show_Counter.ad_show_date.between(from_date,
                                              to_date))).group_by(
        SQL("ad_show_date_year, ad_show_date_month, ad_show_date_day")).order_by(
        SQL("ad_show_date_year ASC, ad_show_date_month ASC, ad_show_date_day ASC"))

    response["shows_count"] = 0
    for query in records:
        z = datetime(int(query.ad_show_date_year), int(query.ad_show_date_month), int(query.ad_show_date_day), 0, 0,
                     0)
        unixtime = calendar.timegm(z.timetuple())
        unixtime = str(unixtime)
        unixtime = unixtime[:10] + "000"
        response["shows"][unixtime] = int(query.show_count)
        response["shows_count"] = response["shows_count"] + int(query.show_count)

    response = {"status": "ok", "body": response}
    return Response(json.dumps(response, sort_keys=True),
                    mimetype='application/json')


@reports.route('/advertiser/click/period', methods=['POST'])
def advertiser_click_period():
    response = {}
    data = json.loads(request.data)
    from_date = data['from_date']
    to_date = data['to_date']
    campaign_id = data['campaign']

    records = Ad_Click_Counter.select(Ad_Click_Counter.ad_click_date_day, Ad_Click_Counter.ad_click_date_month,
                                      Ad_Click_Counter.ad_click_date_year,
                                      fn.SUM(Ad_Click_Counter.ad_click_counter).alias('click_count')).where(
        (Ad_Click_Counter.ad_click_campaign == campaign_id) &
        (Ad_Click_Counter.ad_click_date.between(from_date, to_date))
    ).group_by(SQL("ad_click_date_year, ad_click_date_month, ad_click_date_day")).order_by(
        SQL("ad_click_date_year ASC, ad_click_date_month ASC, ad_click_date_day ASC"))

    for query in records:
        z = datetime(int(query.ad_click_date_year), int(query.ad_click_date_month), int(query.ad_click_date_day), 0, 0,
                     0)
        unixtime = calendar.timegm(z.timetuple())
        unixtime = str(unixtime)
        unixtime = unixtime[:10] + "000"
        response[unixtime] = int(query.click_count)

    response = {"status": "ok", "body": response}
    return Response(json.dumps(response, sort_keys=True),
                    mimetype='application/json')


@reports.route('/advertiser/show/period', methods=['POST'])
def advertiser_show_period():
    response = {}
    data = json.loads(request.data)
    from_date = data['from_date']
    to_date = data['to_date']
    campaign_id = data['campaign']

    records = Ad_Show_Counter.select(Ad_Show_Counter.ad_show_date_day, Ad_Show_Counter.ad_show_date_month,
                                     Ad_Show_Counter.ad_show_date_year,
                                     fn.SUM(Ad_Show_Counter.ad_show_counter).alias('show_count')).where(
        (Ad_Show_Counter.ad_show_campaign == campaign_id) &
        (Ad_Show_Counter.ad_show_date.between(from_date, to_date))
    ).group_by(SQL("ad_show_date_year, ad_show_date_month, ad_show_date_day")).order_by(
        SQL("ad_show_date_year ASC, ad_show_date_month ASC, ad_show_date_day ASC"))

    for query in records:
        z = datetime(int(query.ad_show_date_year), int(query.ad_show_date_month), int(query.ad_show_date_day), 0, 0, 0)
        unixtime = calendar.timegm(z.timetuple())
        unixtime = str(unixtime)
        unixtime = unixtime[:10] + "000"
        response[unixtime] = int(query.show_count)

    response = {"status": "ok", "body": response}
    return Response(json.dumps(response, sort_keys=True),
                    mimetype='application/json')


@reports.route('/advertiser/click/daily', methods=['POST'])
def advertiser_click_daily():
    response = {}
    data = json.loads(request.data)
    from_date = data['from_date']
    to_date = data['to_date']
    campaign_id = data['campaign']

    records = Ad_Click_Counter.select(Ad_Click_Counter.ad_click_date_hour,
                                      Ad_Click_Counter.ad_click_date_day,
                                      Ad_Click_Counter.ad_click_date_month,
                                      Ad_Click_Counter.ad_click_date_year,
                                      fn.SUM(Ad_Click_Counter.ad_click_counter).alias('click_count')).where(
        (Ad_Click_Counter.ad_click_campaign == campaign_id) &
        (Ad_Click_Counter.ad_click_date.between(from_date,
                                                to_date))
    ).group_by(Ad_Click_Counter.ad_click_date_hour).order_by(
        SQL("ad_click_date_hour ASC"))

    for query in records:
        z = datetime(int(query.ad_click_date_year), int(query.ad_click_date_month), int(query.ad_click_date_day),
                     int(query.ad_click_date_hour), 0, 0)
        unixtime = calendar.timegm(z.timetuple())
        unixtime = str(unixtime)
        unixtime = unixtime[:10] + "000"
        response[unixtime] = int(query.click_count)

    response = {"status": "ok", "body": response}
    return Response(json.dumps(response, sort_keys=True),
                    mimetype='application/json')


@reports.route('/advertiser/show/daily', methods=['POST'])
def advertiser_show_daily():
    response = {}
    data = json.loads(request.data)
    from_date = data['from_date']
    to_date = data['to_date']
    campaign_id = data['campaign']

    records = Ad_Show_Counter.select(Ad_Show_Counter.ad_show_date_hour,
                                     Ad_Show_Counter.ad_show_date_day,
                                     Ad_Show_Counter.ad_show_date_month,
                                     Ad_Show_Counter.ad_show_date_year,
                                     fn.SUM(Ad_Show_Counter.ad_show_counter).alias('show_count')).where(
        (Ad_Show_Counter.ad_show_campaign == campaign_id) &
        (Ad_Show_Counter.ad_show_date.between(from_date,
                                              to_date))
    ).group_by(Ad_Show_Counter.ad_show_date_hour).order_by(
        SQL("ad_show_date_hour ASC"))

    for query in records:
        z = datetime(int(query.ad_show_date_year), int(query.ad_show_date_month), int(query.ad_show_date_day),
                     int(query.ad_show_date_hour), 0, 0)
        unixtime = calendar.timegm(z.timetuple())
        unixtime = str(unixtime)
        unixtime = unixtime[:10] + "000"
        response[unixtime] = int(query.show_count)

    response = {"status": "ok", "body": response}
    return Response(json.dumps(response, sort_keys=True),
                    mimetype='application/json')


@reports.route('/advertiser/click/publishers/daily', methods=['POST'])
def advertiser_click_daily_by_publishers():
    response = {}
    data = json.loads(request.data)
    from_date = data['from_date']
    to_date = data['to_date']
    campaign_id = data['campaign']

    if int(request.args.get('banner')) == 1:
        clicks = Ad_Click_Counter.select(Ad_Click_Counter.ad_click_banner_size, Ad_Click_Counter.ad_click_publisher,
                                         fn.SUM(Ad_Click_Counter.ad_click_counter).alias('click_count')).where(
            (Ad_Click_Counter.ad_click_campaign == campaign_id) &
            (Ad_Click_Counter.ad_click_date.between(from_date,
                                                    to_date))
        ).group_by(Ad_Click_Counter.ad_click_publisher, Ad_Click_Counter.ad_click_banner_size)

        for query in clicks:
            response[query.ad_click_publisher.publisher_website_url + "_" + str(
                query.ad_click_publisher.id) + "_" + query.ad_click_banner_size] = int(
                query.click_count)
    else:
        clicks = Ad_Click_Counter.select(Ad_Click_Counter.ad_click_publisher,
                                         fn.SUM(Ad_Click_Counter.ad_click_counter).alias('click_count')).where(
            (Ad_Click_Counter.ad_click_campaign == campaign_id) &
            (Ad_Click_Counter.ad_click_date.between(from_date,
                                                    to_date))
        ).group_by(Ad_Click_Counter.ad_click_publisher)

        for query in clicks:
            response[query.ad_click_publisher.publisher_website_url] = int(
                query.click_count)

    response = {"status": "ok", "body": response}
    return Response(json.dumps(response, sort_keys=True),
                    mimetype='application/json')


@reports.route('/advertiser/show/publishers/daily', methods=['POST'])
def advertiser_show_daily_by_publishers():
    response = {}
    data = json.loads(request.data)
    from_date = data['from_date']
    to_date = data['to_date']
    campaign_id = data['campaign']

    if int(request.args.get('banner')) == 1:
        shows = Ad_Show_Counter.select(Ad_Show_Counter.ad_show_banner_size, Ad_Show_Counter.ad_show_publisher,
                                       fn.SUM(Ad_Show_Counter.ad_show_counter).alias('show_count')).where(
            (Ad_Show_Counter.ad_show_campaign == campaign_id) &
            (Ad_Show_Counter.ad_show_date.between(from_date,
                                                  to_date))
        ).group_by(Ad_Show_Counter.ad_show_publisher, Ad_Show_Counter.ad_show_banner_size)

        for query in shows:
            response[query.ad_show_publisher.publisher_website_url + "_" + str(
                query.ad_show_publisher.id) + "_" + query.ad_show_banner_size] = int(
                query.show_count)

    else:
        shows = Ad_Show_Counter.select(Ad_Show_Counter.ad_show_publisher,
                                       fn.SUM(Ad_Show_Counter.ad_show_counter).alias('show_count')).where(
            (Ad_Show_Counter.ad_show_campaign == campaign_id) &
            (Ad_Show_Counter.ad_show_date.between(from_date,
                                                  to_date))
        ).group_by(Ad_Show_Counter.ad_show_publisher)

        for query in shows:
            response[query.ad_show_publisher.publisher_website_url] = int(
                query.show_count)

    response = {"status": "ok", "body": response}
    return Response(json.dumps(response, sort_keys=True),
                    mimetype='application/json')


@reports.route('/publisher/dashboard/period', methods=['POST'])
def publisher_dashboard_period():
    response = {
        "clicks": {},
        "shows": {}
    }
    data = json.loads(request.data)
    from_date = data['from_date']
    to_date = data['to_date']
    user_id = data['user']

    result = user_websites(user_id)
    result = json.loads(result)
    websites = result['body']
    response["websites_count"] = len(websites)

    records = Ad_Click_Counter.select(Ad_Click_Counter.ad_click_date_day, Ad_Click_Counter.ad_click_date_month,
                                      Ad_Click_Counter.ad_click_date_year,
                                      fn.SUM(Ad_Click_Counter.ad_click_counter).alias('click_count')).where(
        (Ad_Click_Counter.ad_click_publisher << websites) &
        (Ad_Click_Counter.ad_click_date.between(from_date,
                                                to_date))).group_by(
        SQL("ad_click_date_year, ad_click_date_month, ad_click_date_day")).order_by(
        SQL(
            "ad_click_date_year ASC, ad_click_date_month ASC, ad_click_date_day ASC"))

    response["clicks_count"] = 0
    for query in records:
        z = datetime(int(query.ad_click_date_year), int(query.ad_click_date_month), int(query.ad_click_date_day), 0, 0,
                     0)
        unixtime = calendar.timegm(z.timetuple())
        unixtime = str(unixtime)
        unixtime = unixtime[:10] + "000"
        response["clicks"][unixtime] = int(query.click_count)
        response["clicks_count"] = response["clicks_count"] + int(query.click_count)

    records = Ad_Show_Counter.select(Ad_Show_Counter.ad_show_date_day, Ad_Show_Counter.ad_show_date_month,
                                     Ad_Show_Counter.ad_show_date_year,
                                     fn.SUM(Ad_Show_Counter.ad_show_counter).alias('show_count')).where(
        (Ad_Show_Counter.ad_show_publisher << websites) &
        (Ad_Show_Counter.ad_show_date.between(from_date,
                                              to_date))).group_by(
        SQL("ad_show_date_year, ad_show_date_month, ad_show_date_day")).order_by(
        SQL(
            "ad_show_date_year ASC, ad_show_date_month ASC, ad_show_date_day ASC"))

    response["shows_count"] = 0
    for query in records:
        z = datetime(int(query.ad_show_date_year), int(query.ad_show_date_month), int(query.ad_show_date_day), 0, 0,
                     0)
        unixtime = calendar.timegm(z.timetuple())
        unixtime = str(unixtime)
        unixtime = unixtime[:10] + "000"
        response["shows"][unixtime] = int(query.show_count)
        response["shows_count"] = response["shows_count"] + int(query.show_count)

    response = {"status": "ok", "body": response}
    return Response(json.dumps(response, sort_keys=True),
                    mimetype='application/json')


@reports.route('/publisher/click/period', methods=['POST'])
def publisher_click_period():
    response = {}
    data = json.loads(request.data)
    from_date = data['from_date']
    to_date = data['to_date']
    website_id = data['website']

    records = Ad_Click_Counter.select(Ad_Click_Counter.ad_click_date_day, Ad_Click_Counter.ad_click_date_month,
                                      Ad_Click_Counter.ad_click_date_year,
                                      fn.SUM(Ad_Click_Counter.ad_click_counter).alias('click_count')).where(
        (Ad_Click_Counter.ad_click_publisher == website_id) &
        (Ad_Click_Counter.ad_click_date.between(from_date, to_date))
    ).group_by(SQL("ad_click_date_year, ad_click_date_month, ad_click_date_day")).order_by(
        SQL("ad_click_date_year ASC, ad_click_date_month ASC, ad_click_date_day ASC"))

    for query in records:
        z = datetime(int(query.ad_click_date_year), int(query.ad_click_date_month), int(query.ad_click_date_day), 0, 0,
                     0)
        unixtime = calendar.timegm(z.timetuple())
        unixtime = str(unixtime)
        unixtime = unixtime[:10] + "000"
        response[unixtime] = int(query.click_count)

    response = {"status": "ok", "body": response}
    return Response(json.dumps(response, sort_keys=True),
                    mimetype='application/json')


@reports.route('/publisher/show/period', methods=['POST'])
def publisher_show_period():
    response = {}
    data = json.loads(request.data)
    from_date = data['from_date']
    to_date = data['to_date']
    website_id = data['website']

    records = Ad_Show_Counter.select(Ad_Show_Counter.ad_show_date_day, Ad_Show_Counter.ad_show_date_month,
                                     Ad_Show_Counter.ad_show_date_year,
                                     fn.SUM(Ad_Show_Counter.ad_show_counter).alias('show_count')).where(
        (Ad_Show_Counter.ad_show_publisher == website_id) &
        (Ad_Show_Counter.ad_show_date.between(from_date, to_date))
    ).group_by(SQL("ad_show_date_year, ad_show_date_month, ad_show_date_day")).order_by(
        SQL("ad_show_date_year ASC, ad_show_date_month ASC, ad_show_date_day ASC"))

    for query in records:
        z = datetime(int(query.ad_show_date_year), int(query.ad_show_date_month), int(query.ad_show_date_day), 0, 0, 0)
        unixtime = calendar.timegm(z.timetuple())
        unixtime = str(unixtime)
        unixtime = unixtime[:10] + "000"
        response[unixtime] = int(query.show_count)

    response = {"status": "ok", "body": response}
    return Response(json.dumps(response, sort_keys=True),
                    mimetype='application/json')


@reports.route('/publisher/click/daily', methods=['POST'])
def publisher_click_daily():
    response = {}
    data = json.loads(request.data)
    from_date = data['from_date']
    to_date = data['to_date']
    website_id = data['website']

    records = Ad_Click_Counter.select(Ad_Click_Counter.ad_click_date_hour,
                                      Ad_Click_Counter.ad_click_date_day,
                                      Ad_Click_Counter.ad_click_date_month,
                                      Ad_Click_Counter.ad_click_date_year,
                                      fn.SUM(Ad_Click_Counter.ad_click_counter).alias('click_count')).where(
        (Ad_Click_Counter.ad_click_publisher == website_id) &
        (Ad_Click_Counter.ad_click_date.between(from_date,
                                                to_date))
    ).group_by(Ad_Click_Counter.ad_click_date_hour).order_by(
        SQL("ad_click_date_hour ASC"))

    for query in records:
        z = datetime(int(query.ad_click_date_year), int(query.ad_click_date_month), int(query.ad_click_date_day),
                     int(query.ad_click_date_hour), 0, 0)
        unixtime = calendar.timegm(z.timetuple())
        unixtime = str(unixtime)
        unixtime = unixtime[:10] + "000"
        response[unixtime] = int(query.click_count)

    response = {"status": "ok", "body": response}
    return Response(json.dumps(response, sort_keys=True),
                    mimetype='application/json')


@reports.route('/publisher/show/daily', methods=['POST'])
def publisher_show_daily():
    response = {}
    data = json.loads(request.data)
    from_date = data['from_date']
    to_date = data['to_date']
    website_id = data['website']

    records = Ad_Show_Counter.select(Ad_Show_Counter.ad_show_date_hour,
                                     Ad_Show_Counter.ad_show_date_day,
                                     Ad_Show_Counter.ad_show_date_month,
                                     Ad_Show_Counter.ad_show_date_year,
                                     fn.SUM(Ad_Show_Counter.ad_show_counter).alias('show_count')).where(
        (Ad_Show_Counter.ad_show_publisher == website_id) &
        (Ad_Show_Counter.ad_show_date.between(from_date,
                                              to_date))
    ).group_by(Ad_Show_Counter.ad_show_date_hour).order_by(
        SQL("ad_show_date_hour ASC"))

    for query in records:
        z = datetime(int(query.ad_show_date_year), int(query.ad_show_date_month), int(query.ad_show_date_day),
                     int(query.ad_show_date_hour), 0, 0)
        unixtime = calendar.timegm(z.timetuple())
        unixtime = str(unixtime)
        unixtime = unixtime[:10] + "000"
        response[unixtime] = int(query.show_count)

    response = {"status": "ok", "body": response}
    return Response(json.dumps(response, sort_keys=True),
                    mimetype='application/json')


@reports.route('/publisher/click/banners/daily', methods=['POST'])
def publisher_click_daily_by_banners():
    response = {}
    data = json.loads(request.data)
    from_date = data['from_date']
    to_date = data['to_date']
    website_id = data['website']

    clicks = Ad_Click_Counter.select(Ad_Click_Counter.ad_click_banner_size,
                                     fn.SUM(Ad_Click_Counter.ad_click_counter).alias('click_count')).where(
        (Ad_Click_Counter.ad_click_publisher == website_id) &
        (Ad_Click_Counter.ad_click_date.between(from_date,
                                                to_date))
    ).group_by(Ad_Click_Counter.ad_click_banner_size)

    for query in clicks:
        response[query.ad_click_banner_size] = int(query.click_count)

    response = {"status": "ok", "body": response}
    return Response(json.dumps(response, sort_keys=True),
                    mimetype='application/json')


@reports.route('/publisher/show/banners/daily', methods=['POST'])
def publisher_show_daily_by_banners():
    response = {}
    data = json.loads(request.data)
    from_date = data['from_date']
    to_date = data['to_date']
    website_id = data['website']

    shows = Ad_Show_Counter.select(Ad_Show_Counter.ad_show_banner_size,
                                   fn.SUM(Ad_Show_Counter.ad_show_counter).alias('show_count')).where(
        (Ad_Show_Counter.ad_show_publisher == website_id) &
        (Ad_Show_Counter.ad_show_date.between(from_date,
                                              to_date))
    ).group_by(Ad_Show_Counter.ad_show_banner_size)

    for query in shows:
        response[query.ad_show_banner_size] = int(query.show_count)

    response = {"status": "ok", "body": response}
    return Response(json.dumps(response, sort_keys=True),
                    mimetype='application/json')


@reports.before_request
def _db_connect():
    if not db.is_closed():
        db.close()
    db.connect()


# This hook ensures that the connection is closed when we've finished
# processing the request.
@reports.teardown_request
def _db_close(exc):
    if not db.is_closed():
        db.close()
