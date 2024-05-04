import datetime
import json
import sys
import traceback
from flask import request, Response
from flask.views import MethodView
from slugify import slugify_unicode
from models import *
from . import publisher


@publisher.route('/website/count', methods=['GET'])
def publisher_website_count():
    if request.method == 'GET':
        result = Publisher_Website.select().where(Publisher_Website.publisher_website_active_by_admin == 0).count()
        response = {"status": "ok", "body": result}
        return Response(json.dumps(response, sort_keys=True),
                        mimetype='application/json')


@publisher.route('/website/unique/check', methods=['POST'])
def publisher_website_unique_check():
    data = json.loads(request.data)
    url = data['publisher_website_url']
    result = Publisher_Website.select().where(Publisher_Website.publisher_website_url.contains(url)).count()
    response = {"status": "ok", "body": result}
    return Response(json.dumps(response, sort_keys=True),
                    mimetype='application/json')


def user_websites(user_id):
    response = []
    websites = Publisher_Website.select(Publisher_Website.id).where(
        (Publisher_Website.publisher_website_author_user_id == user_id) & (
            Publisher_Website.publisher_website_active_by_admin == 1) & (
            Publisher_Website.publisher_website_is_deleted == 0))

    for query in websites:
        response.append(query.id)

    response = {"status": "ok", "body": response}
    return json.dumps(response, sort_keys=True)


def user_all_websites(user_id):
    response = []
    websites = Publisher_Website.select(Publisher_Website.id, Publisher_Website.publisher_website_url,
                                        Publisher_Website.publisher_website_percentage).where(
        Publisher_Website.publisher_website_author_user_id == user_id)

    for query in websites:
        record = {
            'publisher_website_id': query.id,
            'publisher_website_url': query.publisher_website_url,
            'publisher_website_percentage': query.publisher_website_percentage
        }
        response.append(record)

    response = {"status": "ok", "body": response}
    return json.dumps(response, sort_keys=True)


class PublisherChannelRests(MethodView):
    def get(self, id):
        if id is None:
            response = []
            limit = int(100 if request.args.get('limit') is None else request.args.get('limit'))
            page = int(1 if request.args.get('page') is None else request.args.get('page'))
            order = str('DESC' if request.args.get('order') is None else request.args.get('order'))

            channels = []
            if request.args.get('user') is None:
                channels = Publisher_Channel.select().order_by(SQL("publisher_channel_created_at " + order)).paginate(
                    page, limit)

            elif request.args.get('user') is not None and request.args.get('status') is not None:
                channels = Publisher_Channel.select().where(
                    (Publisher_Channel.publisher_channel_author_user_id == request.args.get('user')) &
                    (Publisher_Channel.publisher_channel_is_deleted == 0) &
                    (Publisher_Channel.publisher_channel_active_by_admin == 1))

            elif request.args.get('user') is not None:
                channels = Publisher_Channel.select().where(
                    (Publisher_Channel.publisher_channel_author_user_id == request.args.get('user')) & (
                        Publisher_Channel.publisher_channel_is_deleted == 0)).order_by(
                    SQL("publisher_channel_created_at " + order)).paginate(page, limit)

            for query in channels:
                record = {
                    'publisher_channel_id': query.id,
                    'publisher_channel_author_user_id': query.publisher_channel_author_user_id,
                    'publisher_channel_updated_user_id': query.publisher_channel_updated_user_id,
                    'publisher_channel_title': query.publisher_channel_title,
                    'publisher_channel_admin_username': query.publisher_channel_admin_username,
                    'publisher_channel_url': query.publisher_channel_url,
                    'publisher_channel_description': query.publisher_channel_description,
                    'publisher_channel_picture': query.publisher_channel_picture,
                    'publisher_channel_geography': {
                        'geography_id': query.publisher_channel_geography.id if query.publisher_channel_geography else '',
                        'geography_title': query.publisher_channel_geography.geography_title if query.publisher_channel_geography else ''
                    },
                    'publisher_channel_member_count': query.publisher_channel_member_count,
                    'publisher_channel_grade': query.publisher_channel_grade,
                    'publisher_channel_active_by_admin': query.publisher_channel_active_by_admin,
                    'publisher_channel_percentage': query.publisher_channel_percentage,
                    'publisher_channel_is_deleted': query.publisher_channel_is_deleted,
                    'publisher_channel_created_at': str(query.publisher_channel_created_at),
                    'publisher_channel_updated_at': str(query.publisher_channel_updated_at)
                }
                response.append(record)
            response = {"status": "ok", "body": response}
            return Response(json.dumps(response, sort_keys=True),
                            mimetype='application/json')
        else:
            response = {}
            try:
                channel = Publisher_Channel.get(Publisher_Channel.id == id)
                response = {
                    'publisher_channel_id': channel.id,
                    'publisher_channel_author_user_id': channel.publisher_channel_author_user_id,
                    'publisher_channel_updated_user_id': channel.publisher_channel_updated_user_id,
                    'publisher_channel_title': channel.publisher_channel_title,
                    'publisher_channel_admin_username': channel.publisher_channel_admin_username,
                    'publisher_channel_url': channel.publisher_channel_url,
                    'publisher_channel_description': channel.publisher_channel_description,
                    'publisher_channel_picture': channel.publisher_channel_picture,
                    'publisher_channel_geography': {
                        'geography_id': channel.publisher_channel_geography.id if channel.publisher_channel_geography else '',
                        'geography_title': channel.publisher_channel_geography.geography_title if channel.publisher_channel_geography else ''
                    },
                    'publisher_channel_member_count': channel.publisher_channel_member_count,
                    'publisher_channel_grade': channel.publisher_channel_grade,
                    'publisher_channel_active_by_admin': channel.publisher_channel_active_by_admin,
                    'publisher_channel_percentage': channel.publisher_channel_percentage,
                    'publisher_channel_is_deleted': channel.publisher_channel_is_deleted,
                    'publisher_channel_created_at': str(channel.publisher_channel_created_at),
                    'publisher_channel_updated_at': str(channel.publisher_channel_updated_at)
                }
                response = {"status": "ok", "body": response}
            except Publisher_Channel.DoesNotExist:
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
            print('test')
            print(data.get('publisher_channel_geography', None))
            result = Publisher_Channel.insert(
                publisher_channel_author_user_id=data['publisher_channel_author_user_id'],
                publisher_channel_title=data.get('publisher_channel_title', None),
                publisher_channel_admin_username=data.get('publisher_channel_admin_username', None),
                publisher_channel_url=data.get('publisher_channel_url', None),
                publisher_channel_description=data.get('publisher_channel_description', None),
                publisher_channel_picture=data.get('publisher_channel_picture', None),
                publisher_channel_geography=data.get('publisher_channel_geography', None),
                publisher_channel_member_count=data.get('publisher_channel_member_count', None),
                publisher_channel_grade=0,
                publisher_channel_active_by_admin=False,
                publisher_channel_percentage=50,
                publisher_channel_is_deleted=False,
                publisher_channel_created_at=date.strftime("%Y-%m-%d %H:%M:%S"),
                publisher_channel_updated_at=date.strftime("%Y-%m-%d %H:%M:%S")
            ).execute()

            if data.get('publisher_channel_subject', None) is not None:
                for subject in data['publisher_channel_subject']:
                    Publisher_Channel_Targeted_Subject.create(
                        channel=result,
                        subject=int(subject)
                    )

            if data.get('publisher_channel_ad_type', None) is not None:
                for type in data['publisher_channel_ad_type']:
                    Publisher_Channel_Ad_Type.create(
                        channel=result,
                        type=int(type)
                    )

            response = {"status": "ok", "body": result}
        except Exception:
            print(traceback.format_exc(sys.exc_info()))
            response = {"status": "nok", "body": traceback.format_exc(sys.exc_info())}
        finally:
            return Response(json.dumps(response, sort_keys=False),
                            mimetype='application/json')

    def delete(self, id):
        response = {}
        result = Publisher_Channel.delete().where(Publisher_Channel.id == id).execute()
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
            channel = Publisher_Channel.get(Publisher_Channel.id == id)
            result = Publisher_Channel.update(
                publisher_channel_updated_user_id=data['publisher_channel_updated_user_id'],
                publisher_channel_title=data.get('publisher_channel_title', channel.publisher_channel_title),
                publisher_channel_admin_username=data.get('publisher_channel_admin_username',
                                                          channel.publisher_channel_admin_username),
                publisher_channel_url=data.get('publisher_channel_url', channel.publisher_channel_url),
                publisher_channel_description=data.get('publisher_channel_description',
                                                       channel.publisher_channel_description),
                publisher_channel_picture=data.get('publisher_channel_picture',
                                                   channel.publisher_channel_picture),
                publisher_channel_geography=data.get('publisher_channel_geography',
                                                     channel.publisher_channel_geography),
                publisher_channel_member_count=data.get('publisher_channel_member_count',
                                                        channel.publisher_channel_member_count),

                publisher_channel_grade=data.get('publisher_channel_grade', channel.publisher_channel_grade),
                publisher_channel_active_by_admin=data.get('publisher_channel_active_by_admin',
                                                           channel.publisher_channel_active_by_admin),
                publisher_channel_percentage=data.get('publisher_channel_percentage',
                                                      channel.publisher_channel_percentage),
                publisher_channel_is_deleted=data.get('publisher_channel_is_deleted',
                                                      channel.publisher_channel_is_deleted),
                publisher_channel_updated_at=date.strftime("%Y-%m-%d %H:%M:%S")
            ).where(Publisher_Channel.id == id).execute()

            if data.get('publisher_channel_subject', None) is not None:
                Publisher_Channel_Targeted_Subject.delete().where(
                    Publisher_Channel_Targeted_Subject.channel == id).execute()
                for subject in data['publisher_channel_subject']:
                    Publisher_Channel_Targeted_Subject.create(
                        channel=id,
                        subject=int(subject)
                    )

            if data.get('publisher_channel_ad_type', None) is not None:
                Publisher_Channel_Ad_Type.delete().where(
                    Publisher_Channel_Ad_Type.channel == id).execute()
                for type in data['publisher_channel_ad_type']:
                    Publisher_Channel_Ad_Type.create(
                        channel=id,
                        type=int(type)
                    )

            if result == 0:
                response = {"status": "nok", "body": "Record Does Not Exist"}
            else:
                response = {"status": "ok", "body": result}
        except Exception:
            response = {"status": "nok", "body": traceback.format_exc(sys.exc_info())}
        finally:
            print(response)
            return Response(json.dumps(response, sort_keys=False),
                            mimetype='application/json')


class PublisherChannelTargetedSubjectRests(MethodView):
    def get(self, id):
        if id is None:
            response = []
            channel_id = request.args.get('channel')
            for query in Publisher_Channel_Targeted_Subject.select().where(
                            Publisher_Channel_Targeted_Subject.channel == channel_id):
                record = {
                    'publisher_channel_targeted_subject_id': query.id,
                    'channel': query.channel.id,
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
            result = Publisher_Channel_Targeted_Subject.insert(
                channel=data.get('channel', None),
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
            channel_id = request.args.get('channel')
            result = Publisher_Channel_Targeted_Subject.delete().where(
                Publisher_Channel_Targeted_Subject.channel == channel_id).execute()
        else:
            result = Publisher_Channel_Targeted_Subject.delete().where(
                Publisher_Channel_Targeted_Subject.id == id).execute()
        if result == 0:
            response = {"status": "nok", "body": "Record Does Not Exist"}
        else:
            response = {"status": "ok", "body": result}
        return Response(json.dumps(response, sort_keys=False),
                        mimetype='application/json')

    def put(self, id):
        pass


class PublisherChannelAdTypeRests(MethodView):
    def get(self, id):
        if id is None:
            response = []
            channel_id = request.args.get('channel')
            for query in Publisher_Channel_Ad_Type.select().where(
                            Publisher_Channel_Ad_Type.channel == channel_id):
                record = {
                    'publisher_channel_targeted_subject_id': query.id,
                    'channel': query.channel.id,
                    'type': {
                        'type_id': query.type.id,
                        'type_author_user_id': query.type.type_author_user_id,
                        'type_updated_user_id': query.type.type_updated_user_id,
                        'type_name': query.type.type_name,
                        'type_title': query.type.type_title,
                        'type_media': query.type.type_media,
                        'type_created_at': str(query.type.type_created_at),
                        'type_updated_at': str(query.type.type_updated_at)
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
            result = Publisher_Channel_Ad_Type.insert(
                channel=data.get('channel', None),
                type=data.get('type', None),
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
            channel_id = request.args.get('channel')
            result = Publisher_Channel_Ad_Type.delete().where(
                Publisher_Channel_Ad_Type.channel == channel_id).execute()
        else:
            result = Publisher_Channel_Ad_Type.delete().where(
                Publisher_Channel_Ad_Type.id == id).execute()
        if result == 0:
            response = {"status": "nok", "body": "Record Does Not Exist"}
        else:
            response = {"status": "ok", "body": result}
        return Response(json.dumps(response, sort_keys=False),
                        mimetype='application/json')

    def put(self, id):
        pass


class PublisherWebsiteRests(MethodView):
    def get(self, id):
        if id is None:
            response = []
            limit = int(200 if request.args.get('limit') is None else request.args.get('limit'))
            page = int(1 if request.args.get('page') is None else request.args.get('page'))
            order = str('DESC' if request.args.get('order') is None else request.args.get('order'))

            channels = []
            if request.args.get('user') is None:
                websites = Publisher_Website.select().order_by(SQL("publisher_website_created_at " + order)).paginate(
                    page, limit)

            elif request.args.get('user') is not None and request.args.get('status') is not None:
                websites = Publisher_Website.select().where(
                    (Publisher_Website.publisher_website_author_user_id == request.args.get('user')) &
                    (Publisher_Website.publisher_website_is_deleted == 0) &
                    (Publisher_Website.publisher_website_active_by_admin == 1))

            elif request.args.get('user') is not None:
                websites = Publisher_Website.select().where(
                    (Publisher_Website.publisher_website_author_user_id == request.args.get('user')) & (
                        Publisher_Website.publisher_website_is_deleted == 0)).order_by(
                    SQL("publisher_website_created_at " + order)).paginate(page, limit)

            for query in websites:
                record = {
                    'publisher_website_id': query.id,
                    'publisher_website_author_user_id': query.publisher_website_author_user_id,
                    'publisher_website_updated_user_id': query.publisher_website_updated_user_id,
                    'publisher_website_title': query.publisher_website_title,
                    'publisher_website_type': query.publisher_website_type,
                    'publisher_website_url': query.publisher_website_url,
                    'publisher_website_grade': query.publisher_website_grade,
                    'publisher_website_active_by_admin': query.publisher_website_active_by_admin,
                    'publisher_website_percentage': query.publisher_website_percentage,
                    'publisher_website_native_style': query.publisher_website_native_style,
                    'publisher_website_is_deleted': query.publisher_website_is_deleted,
                    'publisher_website_created_at': str(query.publisher_website_created_at),
                    'publisher_website_updated_at': str(query.publisher_website_updated_at)
                }
                response.append(record)
            response = {"status": "ok", "body": response}
            return Response(json.dumps(response, sort_keys=True),
                            mimetype='application/json')
        else:
            response = {}
            try:
                website = Publisher_Website.get(Publisher_Website.id == id)
                response = {
                    'publisher_website_id': website.id,
                    'publisher_website_author_user_id': website.publisher_website_author_user_id,
                    'publisher_website_updated_user_id': website.publisher_website_updated_user_id,
                    'publisher_website_title': website.publisher_website_title,
                    'publisher_website_type': website.publisher_website_type,
                    'publisher_website_url': website.publisher_website_url,
                    'publisher_website_grade': website.publisher_website_grade,
                    'publisher_website_active_by_admin': website.publisher_website_active_by_admin,
                    'publisher_website_percentage': website.publisher_website_percentage,
                    'publisher_website_native_style': website.publisher_website_native_style,
                    'publisher_website_is_deleted': website.publisher_website_is_deleted,
                    'publisher_website_created_at': str(website.publisher_website_created_at),
                    'publisher_website_updated_at': str(website.publisher_website_updated_at)
                }
                response = {"status": "ok", "body": response}
            except Publisher_Website.DoesNotExist:
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
            result = Publisher_Website.insert(
                publisher_website_author_user_id=data['publisher_website_author_user_id'],
                publisher_website_title=data.get('publisher_website_title', None),
                publisher_website_type=data.get('publisher_website_type', None),
                publisher_website_url=data.get('publisher_website_url', None),
                publisher_website_grade="class_c",
                publisher_website_active_by_admin=False,
                publisher_website_percentage=50,
                publisher_website_native_style=data.get('publisher_website_native_style', None),
                publisher_website_is_deleted=False,
                publisher_website_created_at=date.strftime("%Y-%m-%d %H:%M:%S"),
                publisher_website_updated_at=date.strftime("%Y-%m-%d %H:%M:%S")
            ).execute()

            if data.get('publisher_website_subject', None) is not None:
                for subject in data['publisher_website_subject']:
                    Publisher_Website_Targeted_Subject.create(
                        website=result,
                        subject=int(subject)
                    )

            response = {"status": "ok", "body": result}
        except Exception:
            response = {"status": "nok", "body": traceback.format_exc(sys.exc_info())}
        finally:
            return Response(json.dumps(response, sort_keys=False),
                            mimetype='application/json')

    def delete(self, id):
        response = {}
        result = Publisher_Website.delete().where(Publisher_Website.id == id).execute()
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
            website = Publisher_Website.get(Publisher_Website.id == id)
            result = Publisher_Website.update(
                publisher_website_updated_user_id=data['publisher_website_updated_user_id'],
                publisher_website_title=data.get('publisher_website_title', website.publisher_website_title),
                publisher_website_type=data.get('publisher_website_type',
                                                website.publisher_website_type),
                publisher_website_url=data.get('publisher_website_url', website.publisher_website_url),
                publisher_website_grade=data.get('publisher_website_grade', website.publisher_website_grade),
                publisher_website_active_by_admin=data.get('publisher_website_active_by_admin',
                                                           website.publisher_website_active_by_admin),
                publisher_website_percentage=data.get('publisher_website_percentage',
                                                      website.publisher_website_percentage),
                publisher_website_native_style=data.get('publisher_website_native_style',
                                                        website.publisher_website_native_style),
                publisher_website_is_deleted=data.get('publisher_website_is_deleted',
                                                      website.publisher_website_is_deleted),
                publisher_website_updated_at=date.strftime("%Y-%m-%d %H:%M:%S")
            ).where(Publisher_Website.id == id).execute()

            if data.get('publisher_website_subject', None) is not None:
                Publisher_Website_Targeted_Subject.delete().where(
                    Publisher_Website_Targeted_Subject.website == id).execute()
                for subject in data['publisher_website_subject']:
                    Publisher_Website_Targeted_Subject.create(
                        website=id,
                        subject=int(subject)
                    )

            if result == 0:
                response = {"status": "nok", "body": "Record Does Not Exist"}
            else:
                response = {"status": "ok", "body": result}
        except Exception:
            response = {"status": "nok", "body": traceback.format_exc(sys.exc_info())}
        finally:
            print(response)
            return Response(json.dumps(response, sort_keys=False),
                            mimetype='application/json')


class PublisherWebsiteTargetedSubjectRests(MethodView):
    def get(self, id):
        if id is None:
            response = []
            website_id = request.args.get('website')
            for query in Publisher_Website_Targeted_Subject.select().where(
                            Publisher_Website_Targeted_Subject.website == website_id):
                record = {
                    'publisher_website_targeted_subject_id': query.id,
                    'website': query.website.id,
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
            result = Publisher_Website_Targeted_Subject.insert(
                website=data.get('website', None),
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
            website_id = request.args.get('website')
            result = Publisher_Website_Targeted_Subject.delete().where(
                Publisher_Website_Targeted_Subject.website == website_id).execute()
        else:
            result = Publisher_Website_Targeted_Subject.delete().where(
                Publisher_Website_Targeted_Subject.id == id).execute()
        if result == 0:
            response = {"status": "nok", "body": "Record Does Not Exist"}
        else:
            response = {"status": "ok", "body": result}
        return Response(json.dumps(response, sort_keys=False),
                        mimetype='application/json')

    def put(self, id):
        pass


def register_api(view, endpoint, url, pk='id', pk_type='int'):
    view_func = view.as_view(endpoint)
    publisher.add_url_rule(url, defaults={pk: None},
                           view_func=view_func, methods=['GET', 'DELETE'])
    publisher.add_url_rule(url, view_func=view_func, methods=['POST', ])
    publisher.add_url_rule('%s/<%s:%s>' % (url, pk_type, pk),
                           view_func=view_func,
                           methods=['GET', 'PUT', 'DELETE'])


register_api(PublisherWebsiteRests, 'PublisherWebsiteRests', '/website', pk='id')
register_api(PublisherWebsiteTargetedSubjectRests, 'PublisherWebsiteTargetedSubjectRests', '/website/subject', pk='id')
register_api(PublisherChannelRests, 'PublisherChannelRests', '/channel', pk='id')
register_api(PublisherChannelTargetedSubjectRests, 'PublisherChannelTargetedSubjectRests', '/channel/subject', pk='id')
register_api(PublisherChannelAdTypeRests, 'PublisherChannelAdTypeRests', '/channel/advertising/type', pk='id')


@publisher.before_request
def _db_connect():
    if not db.is_closed():
        db.close()
    db.connect()


# This hook ensures that the connection is closed when we've finished
# processing the request.
@publisher.teardown_request
def _db_close(exc):
    if not db.is_closed():
        db.close()
