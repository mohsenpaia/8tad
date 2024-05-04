import datetime
import json
import sys
import traceback
from flask import request, Response
from flask.views import MethodView
from slugify import slugify_unicode
from models import *
from . import admin


@admin.route('/banner/size/query', methods=['GET'])
def banner_size_query():
    width = request.args.get('width')
    height = request.args.get('height')
    response = {}
    try:
        banner_size = Ad_Banner_Size.select().where(
            (Ad_Banner_Size.banner_size_width == width) & (Ad_Banner_Size.banner_size_height == height)).get()
        response = {
            'banner_size_id': banner_size.id,
            'banner_size_author_user_id': banner_size.banner_size_author_user_id,
            'banner_size_updated_user_id': banner_size.banner_size_updated_user_id,
            'banner_size_width': banner_size.banner_size_width,
            'banner_size_height': banner_size.banner_size_height,
            'banner_size_type': banner_size.banner_size_type,
            'banner_size_created_at': str(banner_size.banner_size_created_at),
            'banner_size_updated_at': str(banner_size.banner_size_updated_at)
        }
        response = {"status": "ok", "body": response}
    except Ad_Banner_Size.DoesNotExist:
        response = {"status": "nok", "body": "Record Does Not Exist"}
    except Exception:
        response = {"status": "nok", "body": traceback.format_exc(sys.exc_info())}
    finally:
        return Response(json.dumps(response, sort_keys=True),
                        mimetype='application/json')


class AdCampaignTypeRests(MethodView):
    def get(self, id):
        if id is None:
            response = []
            limit = int(20 if request.args.get('limit') is None else request.args.get('limit'))
            page = int(1 if request.args.get('page') is None else request.args.get('page'))
            order = str('DESC' if request.args.get('order') is None else request.args.get('order'))
            for query in Ad_Campaign_Type.select().order_by(SQL("campaign_type_created_at " + order)).paginate(page,
                                                                                                               limit):
                record = {
                    'campaign_type_id': query.id,
                    'campaign_type_author_user_id': query.campaign_type_author_user_id,
                    'campaign_type_updated_user_id': query.campaign_type_updated_user_id,
                    'campaign_type_name': query.campaign_type_name,
                    'campaign_type_title': query.campaign_type_title,
                    'campaign_type_base_price': query.campaign_type_base_price,
                    'campaign_type_special_for': query.campaign_type_special_for,
                    'campaign_type_description': query.campaign_type_description,
                    'campaign_type_icon': query.campaign_type_icon,
                    'campaign_type_created_at': str(query.campaign_type_created_at),
                    'campaign_type_updated_at': str(query.campaign_type_updated_at)
                }
                response.append(record)
            response = {"status": "ok", "body": response}
            return Response(json.dumps(response, sort_keys=True),
                            mimetype='application/json')
        else:
            response = {}
            try:
                campaign_type = Ad_Campaign_Type.get(Ad_Campaign_Type.id == id)
                response = {
                    'campaign_type_id': campaign_type.id,
                    'campaign_type_author_user_id': campaign_type.campaign_type_author_user_id,
                    'campaign_type_updated_user_id': campaign_type.campaign_type_updated_user_id,
                    'campaign_type_name': campaign_type.campaign_type_name,
                    'campaign_type_title': campaign_type.campaign_type_title,
                    'campaign_type_base_price': campaign_type.campaign_type_base_price,
                    'campaign_type_special_for': campaign_type.campaign_type_special_for,
                    'campaign_type_description': campaign_type.campaign_type_description,
                    'campaign_type_icon': campaign_type.campaign_type_icon,
                    'campaign_type_created_at': str(campaign_type.campaign_type_created_at),
                    'campaign_type_updated_at': str(campaign_type.campaign_type_updated_at)
                }
                response = {"status": "ok", "body": response}
            except Ad_Campaign_Type.DoesNotExist:
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
            result = Ad_Campaign_Type.insert(
                campaign_type_author_user_id=data['campaign_type_author_user_id'],
                campaign_type_name=data.get('campaign_type_name', None),
                campaign_type_title=data.get('campaign_type_title', None),
                campaign_type_base_price=data.get('campaign_type_base_price', None),
                campaign_type_special_for=data.get('campaign_type_special_for', None),
                campaign_type_description=data.get('campaign_type_description', None),
                campaign_type_icon=data.get('campaign_type_icon', None),
                campaign_type_created_at=date.strftime("%Y-%m-%d %H:%M:%S"),
                campaign_type_updated_at=date.strftime("%Y-%m-%d %H:%M:%S")
            ).execute()
            response = {"status": "ok", "body": result}
        except Exception:
            response = {"status": "nok", "body": traceback.format_exc(sys.exc_info())}
        finally:
            return Response(json.dumps(response, sort_keys=False),
                            mimetype='application/json')

    def delete(self, id):
        response = {}
        result = Ad_Campaign_Type.delete().where(Ad_Campaign_Type.id == id).execute()
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
            campaign_type = Ad_Campaign_Type.get(Ad_Campaign_Type.id == id)
            result = Ad_Campaign_Type.update(
                campaign_type_updated_user_id=data['campaign_type_updated_user_id'],
                campaign_type_name=data.get('campaign_type_name', campaign_type.campaign_type_name),
                campaign_type_title=data.get('campaign_type_title', campaign_type.campaign_type_title),
                campaign_type_base_price=data.get('campaign_type_base_price', campaign_type.campaign_type_base_price),
                campaign_type_special_for=data.get('campaign_type_special_for',
                                                   campaign_type.campaign_type_special_for),
                campaign_type_description=data.get('campaign_type_description',
                                                   campaign_type.campaign_type_description),
                campaign_type_icon=data.get('campaign_type_icon', campaign_type.campaign_type_icon),
                campaign_type_updated_at=date.strftime("%Y-%m-%d %H:%M:%S")
            ).where(Ad_Campaign_Type.id == id).execute()
            print()
            if result == 0:
                response = {"status": "nok", "body": "Record Does Not Exist"}
            else:
                response = {"status": "ok", "body": result}
        except Exception:
            response = {"status": "nok", "body": traceback.format_exc(sys.exc_info())}
        finally:
            return Response(json.dumps(response, sort_keys=False),
                            mimetype='application/json')


class AdPackageRests(MethodView):
    def get(self, id):
        if id is None:
            response = []
            limit = int(20 if request.args.get('limit') is None else request.args.get('limit'))
            page = int(1 if request.args.get('page') is None else request.args.get('page'))
            order = str('DESC' if request.args.get('order') is None else request.args.get('order'))
            for query in Ad_Package.select().order_by(SQL("package_created_at " + order)).paginate(page, limit):
                record = {
                    'package_id': query.id,
                    'package_author_user_id': query.package_author_user_id,
                    'package_updated_user_id': query.package_updated_user_id,
                    'package_title': query.package_title,
                    'package_price': query.package_price,
                    'package_discount': query.package_discount,
                    'package_click_count': query.package_click_count,
                    'package_impression_count': query.package_impression_count,
                    'package_description': query.package_description,
                    'package_created_at': str(query.package_created_at),
                    'package_updated_at': str(query.package_updated_at)
                }
                response.append(record)
            response = {"status": "ok", "body": response}
            return Response(json.dumps(response, sort_keys=True),
                            mimetype='application/json')
        else:
            response = {}
            try:
                package = Ad_Package.get(Ad_Package.id == id)
                response = {
                    'package_id': package.id,
                    'package_author_user_id': package.package_author_user_id,
                    'package_updated_user_id': package.package_updated_user_id,
                    'package_title': package.package_title,
                    'package_price': package.package_price,
                    'package_discount': package.package_discount,
                    'package_click_count': package.package_click_count,
                    'package_impression_count': package.package_impression_count,
                    'package_description': package.package_description,
                    'package_created_at': str(package.package_created_at),
                    'package_updated_at': str(package.package_updated_at)
                }
                response = {"status": "ok", "body": response}
            except Ad_Package.DoesNotExist:
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
            result = Ad_Package.insert(
                package_author_user_id=data['package_author_user_id'],
                package_title=data.get('package_title', None),
                package_price=data.get('package_price', None),
                package_discount=data.get('package_discount', None),
                package_click_count=data.get('package_click_count', None),
                package_impression_count=data.get('package_impression_count', None),
                package_description=data.get('package_description', None),
                package_created_at=date.strftime("%Y-%m-%d %H:%M:%S"),
                package_updated_at=date.strftime("%Y-%m-%d %H:%M:%S")
            ).execute()
            response = {"status": "ok", "body": result}
        except Exception:
            response = {"status": "nok", "body": traceback.format_exc(sys.exc_info())}
        finally:
            return Response(json.dumps(response, sort_keys=False),
                            mimetype='application/json')

    def delete(self, id):
        response = {}
        result = Ad_Package.delete().where(Ad_Package.id == id).execute()
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
            package = Ad_Package.get(Ad_Package.id == id)
            result = Ad_Package.update(
                package_updated_user_id=data['package_updated_user_id'],
                package_title=data.get('package_title', package.package_title),
                package_price=data.get('package_price', package.package_price),
                package_discount=data.get('package_discount', package.package_discount),
                package_click_count=data.get('package_click_count', package.package_click_count),
                package_impression_count=data.get('package_impression_count', package.package_impression_count),
                package_description=data.get('package_description', package.package_description),
                package_updated_at=date.strftime("%Y-%m-%d %H:%M:%S")
            ).where(Ad_Package.id == id).execute()
            if result == 0:
                response = {"status": "nok", "body": "Record Does Not Exist"}
            else:
                response = {"status": "ok", "body": result}
        except Exception:
            response = {"status": "nok", "body": traceback.format_exc(sys.exc_info())}
        finally:
            return Response(json.dumps(response, sort_keys=False),
                            mimetype='application/json')


class AdBannerSizeRests(MethodView):
    def get(self, id):
        if id is None:
            response = []
            limit = int(20 if request.args.get('limit') is None else request.args.get('limit'))
            page = int(1 if request.args.get('page') is None else request.args.get('page'))
            order = str('DESC' if request.args.get('order') is None else request.args.get('order'))
            type = str('desktop' if request.args.get('type') is None else request.args.get('type'))

            banner_sizes = []
            if request.args.get('type'):
               banner_sizes = Ad_Banner_Size.select().where(Ad_Banner_Size.banner_size_type == type).order_by(
                SQL("banner_size_created_at " + order)).paginate(page, limit)
            else:
                banner_sizes = Ad_Banner_Size.select().order_by(
                    SQL("banner_size_created_at " + order)).paginate(page, limit)

            for query in banner_sizes:
                record = {
                    'banner_size_id': query.id,
                    'banner_size_author_user_id': query.banner_size_author_user_id,
                    'banner_size_updated_user_id': query.banner_size_updated_user_id,
                    'banner_size_width': query.banner_size_width,
                    'banner_size_height': query.banner_size_height,
                    'banner_size_type': query.banner_size_type,
                    'banner_size_created_at': str(query.banner_size_created_at),
                    'banner_size_updated_at': str(query.banner_size_updated_at)
                }
                response.append(record)
            response = {"status": "ok", "body": response}
            return Response(json.dumps(response, sort_keys=True),
                            mimetype='application/json')
        else:
            response = {}
            try:
                banner_size = Ad_Banner_Size.get(Ad_Banner_Size.id == id)
                response = {
                    'banner_size_id': banner_size.id,
                    'banner_size_author_user_id': banner_size.banner_size_author_user_id,
                    'banner_size_updated_user_id': banner_size.banner_size_updated_user_id,
                    'banner_size_width': banner_size.banner_size_width,
                    'banner_size_height': banner_size.banner_size_height,
                    'banner_size_type': banner_size.banner_size_type,
                    'banner_size_created_at': str(banner_size.banner_size_created_at),
                    'banner_size_updated_at': str(banner_size.banner_size_updated_at)
                }
                response = {"status": "ok", "body": response}
            except Ad_Banner_Size.DoesNotExist:
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
            result = Ad_Banner_Size.insert(
                banner_size_author_user_id=data['banner_size_author_user_id'],
                banner_size_width=data.get('banner_size_width', None),
                banner_size_height=data.get('banner_size_height', None),
                banner_size_type= data.get('banner_size_type', None),
                banner_size_created_at=date.strftime("%Y-%m-%d %H:%M:%S"),
                banner_size_updated_at=date.strftime("%Y-%m-%d %H:%M:%S")
            ).execute()
            response = {"status": "ok", "body": result}
        except Exception:
            response = {"status": "nok", "body": traceback.format_exc(sys.exc_info())}
        finally:
            return Response(json.dumps(response, sort_keys=False),
                            mimetype='application/json')

    def delete(self, id):
        response = {}
        result = Ad_Banner_Size.delete().where(Ad_Banner_Size.id == id).execute()
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
            banner_size = Ad_Banner_Size.get(Ad_Banner_Size.id == id)
            result = Ad_Banner_Size.update(
                banner_size_updated_user_id=data['banner_size_updated_user_id'],
                banner_size_width=data.get('banner_size_width', banner_size.banner_size_width),
                banner_size_height=data.get('banner_size_height', banner_size.banner_size_height),
                banner_size_type=data.get('banner_size_type', banner_size.banner_size_type),
                banner_size_updated_at=date.strftime("%Y-%m-%d %H:%M:%S")
            ).where(Ad_Banner_Size.id == id).execute()
            if result == 0:
                response = {"status": "nok", "body": "Record Does Not Exist"}
            else:
                response = {"status": "ok", "body": result}
        except Exception:
            response = {"status": "nok", "body": traceback.format_exc(sys.exc_info())}
        finally:
            return Response(json.dumps(response, sort_keys=False),
                            mimetype='application/json')


class AdTypeRests(MethodView):
    def get(self, id):
        if id is None:
            response = []
            limit = int(20 if request.args.get('limit') is None else request.args.get('limit'))
            page = int(1 if request.args.get('page') is None else request.args.get('page'))
            order = str('DESC' if request.args.get('order') is None else request.args.get('order'))
            type = str('web' if request.args.get('type') is None else request.args.get('type'))

            types = []
            if request.args.get('type'):
                types = Ad_Type.select().where(Ad_Type.type_media == type).order_by(SQL("type_created_at " + order)).paginate(page, limit)
            else:
                types = Ad_Type.select().order_by(SQL("type_created_at " + order)).paginate(page, limit)

            for query in types:
                record = {
                    'type_id': query.id,
                    'type_author_user_id': query.type_author_user_id,
                    'type_updated_user_id': query.type_updated_user_id,
                    'type_name': query.type_name,
                    'type_title': query.type_title,
                    'type_media': query.type_media,
                    'type_created_at': str(query.type_created_at),
                    'type_updated_at': str(query.type_updated_at)
                }
                response.append(record)
            response = {"status": "ok", "body": response}
            return Response(json.dumps(response, sort_keys=True),
                            mimetype='application/json')
        else:
            response = {}
            try:
                type = Ad_Type.get(Ad_Type.id == id)
                response = {
                    'type_id': type.id,
                    'type_author_user_id': type.type_author_user_id,
                    'type_updated_user_id': type.type_updated_user_id,
                    'type_name': type.type_name,
                    'type_title': type.type_title,
                    'type_media': type.type_media,
                    'type_created_at': str(type.type_created_at),
                    'type_updated_at': str(type.type_updated_at)
                }
                response = {"status": "ok", "body": response}
            except Ad_Type.DoesNotExist:
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
            result = Ad_Type.insert(
                type_author_user_id=data['type_author_user_id'],
                type_name=data.get('type_name', None),
                type_title=data.get('type_title', None),
                type_media=data.get('type_media', None),
                type_created_at=date.strftime("%Y-%m-%d %H:%M:%S"),
                type_updated_at=date.strftime("%Y-%m-%d %H:%M:%S")
            ).execute()
            response = {"status": "ok", "body": result}
        except Exception:
            response = {"status": "nok", "body": traceback.format_exc(sys.exc_info())}
        finally:
            return Response(json.dumps(response, sort_keys=False),
                            mimetype='application/json')

    def delete(self, id):
        response = {}
        result = Ad_Type.delete().where(Ad_Type.id == id).execute()
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
            type = Ad_Type.get(Ad_Type.id == id)
            result = Ad_Type.update(
                type_updated_user_id=data['type_updated_user_id'],
                type_name=data.get('type_name', type.type_name),
                type_title=data.get('type_title', type.type_title),
                type_media=data.get('type_media', type.type_media),
                type_updated_at=date.strftime("%Y-%m-%d %H:%M:%S")
            ).where(Ad_Type.id == id).execute()
            if result == 0:
                response = {"status": "nok", "body": "Record Does Not Exist"}
            else:
                response = {"status": "ok", "body": result}
        except Exception:
            response = {"status": "nok", "body": traceback.format_exc(sys.exc_info())}
        finally:
            return Response(json.dumps(response, sort_keys=False),
                            mimetype='application/json')




class TargetedOperatingSystemRests(MethodView):
    def get(self, id):
        if id is None:
            response = []
            limit = int(20 if request.args.get('limit') is None else request.args.get('limit'))
            page = int(1 if request.args.get('page') is None else request.args.get('page'))
            order = str('DESC' if request.args.get('order') is None else request.args.get('order'))
            type = str('desktop' if request.args.get('type') is None else request.args.get('type'))

            operating_systems = []
            if request.args.get('type'):
                operating_systems = Targeted_Operating_System.select().where(Targeted_Operating_System.os_type == type).order_by(SQL("os_created_at " + order)).paginate(page, limit)
            else:
                operating_systems = Targeted_Operating_System.select().order_by(
                    SQL("os_created_at " + order)).paginate(page, limit)

            for query in operating_systems:
                record = {
                    'os_id': query.id,
                    'os_author_user_id': query.os_author_user_id,
                    'os_updated_user_id': query.os_updated_user_id,
                    'os_name': query.os_name,
                    'os_title': query.os_title,
                    'os_type': query.os_type,
                    'os_created_at': str(query.os_created_at),
                    'os_updated_at': str(query.os_updated_at)
                }
                response.append(record)
            response = {"status": "ok", "body": response}
            return Response(json.dumps(response, sort_keys=True),
                            mimetype='application/json')
        else:
            response = {}
            try:
                operating_system = Targeted_Operating_System.get(Targeted_Operating_System.id == id)
                response = {
                    'os_id': operating_system.id,
                    'os_author_user_id': operating_system.os_author_user_id,
                    'os_updated_user_id': operating_system.os_updated_user_id,
                    'os_name': operating_system.os_name,
                    'os_title': operating_system.os_title,
                    'os_type': operating_system.os_type,
                    'os_created_at': str(operating_system.os_created_at),
                    'os_updated_at': str(operating_system.os_updated_at)
                }
                response = {"status": "ok", "body": response}
            except Targeted_Operating_System.DoesNotExist:
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
            result = Targeted_Operating_System.insert(
                os_author_user_id=data['os_author_user_id'],
                os_name=data.get('os_name', None),
                os_title=data.get('os_title', None),
                os_type=data.get('os_type', None),
                os_created_at=date.strftime("%Y-%m-%d %H:%M:%S"),
                os_updated_at=date.strftime("%Y-%m-%d %H:%M:%S")
            ).execute()
            response = {"status": "ok", "body": result}
        except Exception:
            response = {"status": "nok", "body": traceback.format_exc(sys.exc_info())}
        finally:
            print(request.data)
            print(response)
            return Response(json.dumps(response, sort_keys=False),
                            mimetype='application/json')

    def delete(self, id):
        response = {}
        result = Targeted_Operating_System.delete().where(Targeted_Operating_System.id == id).execute()
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
            operating_system = Targeted_Operating_System.get(Targeted_Operating_System.id == id)
            result = Targeted_Operating_System.update(
                os_updated_user_id=data['os_updated_user_id'],
                os_name=data.get('os_name', operating_system.os_name),
                os_title=data.get('os_title', operating_system.os_title),
                os_type=data.get('os_type', operating_system.os_type),
                os_updated_at=date.strftime("%Y-%m-%d %H:%M:%S")
            ).where(Targeted_Operating_System.id == id).execute()
            if result == 0:
                response = {"status": "nok", "body": "Record Does Not Exist"}
            else:
                response = {"status": "ok", "body": result}
            print(data)
        except Exception:
            response = {"status": "nok", "body": traceback.format_exc(sys.exc_info())}
        finally:
            return Response(json.dumps(response, sort_keys=False),
                            mimetype='application/json')


class TargetedSubjectRests(MethodView):
    def get(self, id):
        if id is None:
            response = []
            limit = int(20 if request.args.get('limit') is None else request.args.get('limit'))
            page = int(1 if request.args.get('page') is None else request.args.get('page'))
            order = str('DESC' if request.args.get('order') is None else request.args.get('order'))
            type = str('web' if request.args.get('type') is None else request.args.get('type'))

            subjects = []
            if request.args.get('type'):
                subjects = Targeted_Subject.select().where(Targeted_Subject.subject_type == type).order_by(SQL("subject_created_at " + order)).paginate(page, limit)
            else:
                subjects = Targeted_Subject.select().order_by(SQL("subject_created_at " + order)).paginate(page, limit)

            for query in subjects:
                record = {
                    'subject_id': query.id,
                    'subject_author_user_id': query.subject_author_user_id,
                    'subject_updated_user_id': query.subject_updated_user_id,
                    'subject_name': query.subject_name,
                    'subject_title': query.subject_title,
                    'subject_type': query.subject_type,
                    'subject_created_at': str(query.subject_created_at),
                    'subject_updated_at': str(query.subject_updated_at)
                }
                response.append(record)
            response = {"status": "ok", "body": response}
            return Response(json.dumps(response, sort_keys=True),
                            mimetype='application/json')
        else:
            response = {}
            try:
                subject = Targeted_Subject.get(Targeted_Subject.id == id)
                response = {
                    'subject_id': subject.id,
                    'subject_author_user_id': subject.subject_author_user_id,
                    'subject_updated_user_id': subject.subject_updated_user_id,
                    'subject_name': subject.subject_name,
                    'subject_title': subject.subject_title,
                    'subject_type': subject.subject_type,
                    'subject_created_at': str(subject.subject_created_at),
                    'subject_updated_at': str(subject.subject_updated_at)
                }
                response = {"status": "ok", "body": response}
            except Targeted_Subject.DoesNotExist:
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
            result = Targeted_Subject.insert(
                subject_author_user_id=data['subject_author_user_id'],
                subject_name=data.get('subject_name', None),
                subject_title=data.get('subject_title', None),
                subject_type=data.get('subject_type', None),
                subject_created_at=date.strftime("%Y-%m-%d %H:%M:%S"),
                subject_updated_at=date.strftime("%Y-%m-%d %H:%M:%S")
            ).execute()
            response = {"status": "ok", "body": result}
        except Exception:
            response = {"status": "nok", "body": traceback.format_exc(sys.exc_info())}
        finally:
            return Response(json.dumps(response, sort_keys=False),
                            mimetype='application/json')

    def delete(self, id):
        response = {}
        result = Targeted_Subject.delete().where(Targeted_Subject.id == id).execute()
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
            subject = Targeted_Subject.get(Targeted_Subject.id == id)
            result = Targeted_Subject.update(
                subject_updated_user_id=data['subject_updated_user_id'],
                subject_name=data.get('subject_name', subject.subject_name),
                subject_title=data.get('subject_title', subject.subject_title),
                subject_type=data.get('subject_type', subject.subject_type),
                subject_updated_at=date.strftime("%Y-%m-%d %H:%M:%S")
            ).where(Targeted_Subject.id == id).execute()
            if result == 0:
                response = {"status": "nok", "body": "Record Does Not Exist"}
            else:
                response = {"status": "ok", "body": result}
        except Exception:
            response = {"status": "nok", "body": traceback.format_exc(sys.exc_info())}
        finally:
            return Response(json.dumps(response, sort_keys=False),
                            mimetype='application/json')


class TargetedGeographyRests(MethodView):
    def get(self, id):
        if id is None:
            response = []
            limit = int(100 if request.args.get('limit') is None else request.args.get('limit'))
            page = int(1 if request.args.get('page') is None else request.args.get('page'))
            order = str('DESC' if request.args.get('order') is None else request.args.get('order'))
            for query in Targeted_Geography.select().order_by(SQL("geography_created_at " + order)).paginate(page,
                                                                                                             limit):
                record = {
                    'geography_id': query.id,
                    'geography_author_user_id': query.geography_author_user_id,
                    'geography_updated_user_id': query.geography_updated_user_id,
                    'geography_name': query.geography_name,
                    'geography_title': query.geography_title,
                    'geography_created_at': str(query.geography_created_at),
                    'geography_updated_at': str(query.geography_updated_at)
                }
                response.append(record)
            response = {"status": "ok", "body": response}
            return Response(json.dumps(response, sort_keys=True),
                            mimetype='application/json')
        else:
            response = {}
            try:
                geography = Targeted_Geography.get(Targeted_Geography.id == id)
                response = {
                    'geography_id': geography.id,
                    'geography_author_user_id': geography.geography_author_user_id,
                    'geography_updated_user_id': geography.geography_updated_user_id,
                    'geography_name': geography.geography_name,
                    'geography_title': geography.geography_title,
                    'geography_created_at': str(geography.geography_created_at),
                    'geography_updated_at': str(geography.geography_updated_at)
                }
                response = {"status": "ok", "body": response}
            except Targeted_Geography.DoesNotExist:
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
            result = Targeted_Geography.insert(
                geography_author_user_id=data['geography_author_user_id'],
                geography_name=data.get('geography_name', None),
                geography_title=data.get('geography_title', None),
                geography_created_at=date.strftime("%Y-%m-%d %H:%M:%S"),
                geography_updated_at=date.strftime("%Y-%m-%d %H:%M:%S")
            ).execute()
            response = {"status": "ok", "body": result}
        except Exception:
            response = {"status": "nok", "body": traceback.format_exc(sys.exc_info())}
        finally:
            return Response(json.dumps(response, sort_keys=False),
                            mimetype='application/json')

    def delete(self, id):
        response = {}
        result = Targeted_Geography.delete().where(Targeted_Geography.id == id).execute()
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
            geography = Targeted_Geography.get(Targeted_Geography.id == id)
            result = Targeted_Geography.update(
                geography_updated_user_id=data['geography_updated_user_id'],
                geography_name=data.get('geography_name', geography.geography_name),
                geography_title=data.get('geography_title', geography.geography_title),
                geography_updated_at=date.strftime("%Y-%m-%d %H:%M:%S")
            ).where(Targeted_Geography.id == id).execute()
            if result == 0:
                response = {"status": "nok", "body": "Record Does Not Exist"}
            else:
                response = {"status": "ok", "body": result}
        except Exception:
            response = {"status": "nok", "body": traceback.format_exc(sys.exc_info())}
        finally:
            return Response(json.dumps(response, sort_keys=False),
                            mimetype='application/json')


class TargetedKeywordRests(MethodView):
    def get(self, id):
        if id is None:
            response = []
            limit = int(20 if request.args.get('limit') is None else request.args.get('limit'))
            page = int(1 if request.args.get('page') is None else request.args.get('page'))
            order = str('DESC' if request.args.get('order') is None else request.args.get('order'))
            for query in Targeted_Keyword.select().order_by(SQL("keyword_created_at " + order)).paginate(page, limit):
                record = {
                    'keyword_id': query.id,
                    'keyword_author_user_id': query.keyword_author_user_id,
                    'keyword_updated_user_id': query.keyword_updated_user_id,
                    'keyword_title': query.keyword_title,
                    'keyword_created_at': str(query.keyword_created_at),
                    'keyword_updated_at': str(query.keyword_updated_at)
                }
                response.append(record)
            response = {"status": "ok", "body": response}
            return Response(json.dumps(response, sort_keys=True),
                            mimetype='application/json')
        else:
            response = {}
            try:
                keyword = Targeted_Keyword.get(Targeted_Keyword.id == id)
                response = {
                    'keyword_id': keyword.id,
                    'keyword_author_user_id': keyword.keyword_author_user_id,
                    'keyword_updated_user_id': keyword.keyword_updated_user_id,
                    'keyword_title': keyword.keyword_title,
                    'keyword_created_at': str(keyword.keyword_created_at),
                    'keyword_updated_at': str(keyword.keyword_updated_at)
                }
                response = {"status": "ok", "body": response}
            except Targeted_Keyword.DoesNotExist:
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
            result = Targeted_Keyword.insert(
                keyword_author_user_id=data['keyword_author_user_id'],
                keyword_title=data.get('keyword_title', None),
                keyword_created_at=date.strftime("%Y-%m-%d %H:%M:%S"),
                keyword_updated_at=date.strftime("%Y-%m-%d %H:%M:%S")
            ).execute()
            response = {"status": "ok", "body": result}
        except Exception:
            response = {"status": "nok", "body": traceback.format_exc(sys.exc_info())}
        finally:
            return Response(json.dumps(response, sort_keys=False),
                            mimetype='application/json')

    def delete(self, id):
        response = {}
        result = Targeted_Keyword.delete().where(Targeted_Keyword.id == id).execute()
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
            keyword = Targeted_Keyword.get(Targeted_Keyword.id == id)
            result = Targeted_Keyword.update(
                keyword_updated_user_id=data['keyword_updated_user_id'],
                keyword_title=data.get('keyword_title', keyword.keyword_title),
                keyword_updated_at=date.strftime("%Y-%m-%d %H:%M:%S")
            ).where(Targeted_Keyword.id == id).execute()
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
    admin.add_url_rule(url, defaults={pk: None},
                       view_func=view_func, methods=['GET', 'DELETE'])
    admin.add_url_rule(url, view_func=view_func, methods=['POST', ])
    admin.add_url_rule('%s/<%s:%s>' % (url, pk_type, pk),
                       view_func=view_func,
                       methods=['GET', 'PUT', 'DELETE'])


register_api(AdCampaignTypeRests, 'AdCampaignTypeRests', '/campaign/type', pk='id')
register_api(AdPackageRests, 'AdPackageRests', '/package', pk='id')
register_api(AdBannerSizeRests, 'AdBannerSizeRests', '/banner/size', pk='id')
register_api(AdTypeRests, 'AdTypeRests', '/advertising/type', pk='id')
register_api(TargetedOperatingSystemRests, 'TargetedOperatingSystemRests', '/target/os', pk='id')
register_api(TargetedSubjectRests, 'TargetedSubjectRests', '/target/subject', pk='id')
register_api(TargetedGeographyRests, 'TargetedGeographyRests', '/target/geography', pk='id')
register_api(TargetedKeywordRests, 'TargetedKeywordRests', '/target/keyword', pk='id')




@admin.before_request
def _db_connect():
    if not db.is_closed():
        db.close()
    db.connect()


# This hook ensures that the connection is closed when we've finished
# processing the request.
@admin.teardown_request
def _db_close(exc):
    if not db.is_closed():
        db.close()
