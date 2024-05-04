import datetime
import json
import sys
import traceback
from flask import request, Response
from flask.views import MethodView
from slugify import slugify_unicode
from elasticsearch import Elasticsearch
import time
from urlparse import urlparse
from models import *
from . import financial
from ..publisher.views import user_all_websites


@financial.route('/credit/request/count', methods=['GET'])
def publisher_credit_request_count():
    if request.method == 'GET':
        result = Credit_Request.select().where(Credit_Request.request_amount_paid == None).count()
        response = {"status": "ok", "body": result}
        return Response(json.dumps(response, sort_keys=True),
                        mimetype='application/json')


@financial.route('/user/<id>/transactions', methods=['GET'])
def publisher_credit_calculation(id):
    if request.method == 'GET':
        response = []
        transactions = User_Financial_Transaction.select().where(
            (User_Financial_Transaction.transaction_author_user_id == id) & (
                User_Financial_Transaction.transaction_status == 1))

        for query in transactions:
            record = {
                'transaction_id': query.id,
                'transaction_author_user_id': query.transaction_author_user_id,
                'transaction_updated_user_id': query.transaction_updated_user_id,
                'transaction_description': query.transaction_description,
                'transaction_deposit_amount': query.transaction_deposit_amount,
                'transaction_withdrawal_amount': query.transaction_withdrawal_amount,
                'transaction_first_status': query.transaction_first_status,
                'transaction_authority': query.transaction_authority,
                'transaction_second_status': query.transaction_second_status,
                'transaction_reference_id': query.transaction_reference_id,
                'transaction_status': query.transaction_status,
                'transaction_created_at': str(query.transaction_created_at),
                'transaction_updated_at': str(query.transaction_updated_at)
            }
            response.append(record)
        response = {"status": "ok", "body": response}
        return Response(json.dumps(response, sort_keys=True),
                        mimetype='application/json')


# @financial.route('/user/<id>/credit/calculation', methods=['GET'])
# def publisher_credit_calculation(id):
#     if request.method == 'GET':
#         es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
#
#         result = user_all_websites(id)
#         result = json.loads(result)
#         websites = result['body']
#
#         date = datetime.datetime.now()
#         lte = date.strftime("%Y-%m-%d%H:%M:%S")
#         credit = 0
#         for website in websites:
#             records = Website_Credit_Calculation.select().where(
#                 Website_Credit_Calculation.website == website["publisher_website_id"]).order_by(
#                 SQL("website_credit_calculation_created_at DESC"))
#
#             credit_amount = 0
#             for record in records:
#                 credit_amount += record.website_credit_amount
#
#             if len(list(records)) > 0:
#                 gte = (str(records[0].website_credit_calculation_created_at)).replace(' ', '')
#             else:
#                 gte = "1000-01-0100:00:00"
#
#             query = '{"size" : 10000, "query": {"bool": {"must": [{"wildcard" : {"SiteURL" : "*' + urlparse(website[
#                                                                                                                 "publisher_website_url"]).hostname + '*"}},{"range": {"Time": {"gte": "' + gte + '","lte": "' + lte + '","format": "yyyy-MM-ddHH:mm:ss"}}}]}}}'
#             query = json.loads(query)
#             logs = es.search(index='logs', doc_type='clickAdSenseLog', body=query)
#             credit_amount_from_log = 0
#             for log in logs["hits"]["hits"]:
#                 if log["_source"]["ClickStatus"] == 'Real':
#                     credit_amount_from_log = credit_amount_from_log + int(log["_source"]["ClickCost"])
#
#             credit_amount_from_log = credit_amount_from_log * (float(website["publisher_website_percentage"]) / 100)
#
#             if credit_amount_from_log > 0:
#                 result = Website_Credit_Calculation.insert(
#                     website=website["publisher_website_id"],
#                     website_percentage=website["publisher_website_percentage"],
#                     website_credit_amount=int(credit_amount_from_log),
#                     website_credit_calculation_created_at=date.strftime("%Y-%m-%d %H:%M:%S"),
#                     website_credit_calculation_updated_at=date.strftime("%Y-%m-%d %H:%M:%S")
#                 ).execute()
#
#             credit = credit + credit_amount + credit_amount_from_log
#
#         if credit > 0:
#             result = User_Credit.update(
#                 credit_updated_user_id=id,
#                 user_credit_amount=int(credit),
#                 user_credit_updated_at=date.strftime("%Y-%m-%d %H:%M:%S")
#             ).where(User_Credit.credit_author_user_id == id).execute()
#
#         return str(credit)


class UserFinancialTransactionRests(MethodView):
    def get(self, id):
        if id is None:
            response = []
            limit = int(20 if request.args.get('limit') is None else request.args.get('limit'))
            page = int(1 if request.args.get('page') is None else request.args.get('page'))
            order = str('DESC' if request.args.get('order') is None else request.args.get('order'))

            transactions = []
            if request.args.get('user') is None:
                transactions = User_Financial_Transaction.select().order_by(
                    SQL("transaction_created_at " + order)).paginate(page, limit)
            else:
                transactions = User_Financial_Transaction.select().where((
                                                                             User_Financial_Transaction.transaction_author_user_id == request.args.get(
                                                                                 'user')) & (
                                                                             User_Financial_Transaction.transaction_status == 1)).order_by(
                    SQL("transaction_created_at " + order)).paginate(page, limit)

            for query in transactions:
                record = {
                    'transaction_id': query.id,
                    'transaction_author_user_id': query.transaction_author_user_id,
                    'transaction_updated_user_id': query.transaction_updated_user_id,
                    'transaction_description': query.transaction_description,
                    'transaction_deposit_amount': query.transaction_deposit_amount,
                    'transaction_withdrawal_amount': query.transaction_withdrawal_amount,
                    'transaction_first_status': query.transaction_first_status,
                    'transaction_authority': query.transaction_authority,
                    'transaction_second_status': query.transaction_second_status,
                    'transaction_reference_id': query.transaction_reference_id,
                    'transaction_status': query.transaction_status,
                    'transaction_created_at': str(query.transaction_created_at),
                    'transaction_updated_at': str(query.transaction_updated_at)
                }
                response.append(record)
            response = {"status": "ok", "body": response}
            return Response(json.dumps(response, sort_keys=True),
                            mimetype='application/json')
        else:
            response = {}
            try:
                transaction = User_Financial_Transaction.get(User_Financial_Transaction.transaction_authority == id)
                response = {
                    'transaction_id': transaction.id,
                    'transaction_author_user_id': transaction.transaction_author_user_id,
                    'transaction_updated_user_id': transaction.transaction_updated_user_id,
                    'transaction_description': transaction.transaction_description,
                    'transaction_deposit_amount': transaction.transaction_deposit_amount,
                    'transaction_withdrawal_amount': transaction.transaction_withdrawal_amount,
                    'transaction_first_status': transaction.transaction_first_status,
                    'transaction_authority': transaction.transaction_authority,
                    'transaction_second_status': transaction.transaction_second_status,
                    'transaction_reference_id': transaction.transaction_reference_id,
                    'transaction_status': transaction.transaction_status,
                    'transaction_created_at': str(transaction.transaction_created_at),
                    'transaction_updated_at': str(transaction.transaction_updated_at)
                }
                response = {"status": "ok", "body": response}
            except User_Financial_Transaction.DoesNotExist:
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
            result = User_Financial_Transaction.insert(
                transaction_author_user_id=data['transaction_author_user_id'],
                transaction_updated_user_id=data.get('transaction_updated_user_id', None),
                transaction_description=data.get('transaction_description', None),
                transaction_deposit_amount=data.get('transaction_deposit_amount', None),
                transaction_withdrawal_amount=data.get('transaction_withdrawal_amount', None),
                transaction_first_status=data.get('transaction_first_status', None),
                transaction_authority=data.get('transaction_authority', None),
                transaction_second_status=data.get('transaction_second_status', None),
                transaction_reference_id=data.get('transaction_reference_id', None),
                transaction_status=data.get('transaction_status', None),
                transaction_created_at=date.strftime("%Y-%m-%d %H:%M:%S"),
                transaction_updated_at=date.strftime("%Y-%m-%d %H:%M:%S")
            ).execute()
            response = {"status": "ok", "body": result}
        except Exception:
            response = {"status": "nok", "body": traceback.format_exc(sys.exc_info())}
        finally:
            return Response(json.dumps(response, sort_keys=False),
                            mimetype='application/json')

    def delete(self, id):
        response = {}
        result = User_Financial_Transaction.delete().where(User_Financial_Transaction.id == id).execute()
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
            transaction = User_Financial_Transaction.get(User_Financial_Transaction.transaction_authority == id)
            result = User_Financial_Transaction.update(
                transaction_updated_user_id=data['transaction_updated_user_id'],
                transaction_description=data.get('transaction_description', transaction.transaction_description),
                transaction_deposit_amount=data.get('transaction_deposit_amount',
                                                    transaction.transaction_deposit_amount),
                transaction_withdrawal_amount=data.get('transaction_withdrawal_amount',
                                                       transaction.transaction_withdrawal_amount),
                transaction_first_status=data.get('transaction_first_status', transaction.transaction_first_status),
                transaction_authority=data.get('transaction_authority', transaction.transaction_authority),
                transaction_second_status=data.get('transaction_second_status', transaction.transaction_second_status),
                transaction_reference_id=data.get('transaction_reference_id', transaction.transaction_reference_id),
                transaction_status=data.get('transaction_status', transaction.transaction_status),
                transaction_updated_at=date.strftime("%Y-%m-%d %H:%M:%S")
            ).where(User_Financial_Transaction.transaction_authority == id).execute()
            if result == 0:
                response = {"status": "nok", "body": "Record Does Not Exist"}
            else:
                response = {"status": "ok", "body": result}
        except Exception:
            response = {"status": "nok", "body": traceback.format_exc(sys.exc_info())}
        finally:
            return Response(json.dumps(response, sort_keys=False),
                            mimetype='application/json')


# class UserCreditRests(MethodView):
#     def get(self, id):
#         if id is None:
#             response = []
#             limit = int(20 if request.args.get('limit') is None else request.args.get('limit'))
#             page = int(1 if request.args.get('page') is None else request.args.get('page'))
#             order = str('DESC' if request.args.get('order') is None else request.args.get('order'))
#             for query in User_Credit.select().order_by(SQL("user_credit_created_at " + order)).paginate(page, limit):
#                 record = {
#                     'credit_id': query.id,
#                     'credit_author_user_id': query.credit_author_user_id,
#                     'credit_updated_user_id': query.credit_updated_user_id,
#                     'user_credit_amount': query.user_credit_amount,
#                     'user_credit_created_at': str(query.user_credit_created_at),
#                     'user_credit_updated_at': str(query.user_credit_updated_at)
#                 }
#                 response.append(record)
#             response = {"status": "ok", "body": response}
#             return Response(json.dumps(response, sort_keys=True),
#                             mimetype='application/json')
#         else:
#             response = {}
#             try:
#                 user_credit = User_Credit.get(User_Credit.credit_author_user_id == id)
#                 response = {
#                     'credit_id': user_credit.id,
#                     'credit_author_user_id': user_credit.credit_author_user_id,
#                     'credit_updated_user_id': user_credit.credit_updated_user_id,
#                     'user_credit_amount': user_credit.user_credit_amount,
#                     'user_credit_created_at': str(user_credit.user_credit_created_at),
#                     'user_credit_updated_at': str(user_credit.user_credit_updated_at)
#                 }
#                 response = {"status": "ok", "body": response}
#             except User_Credit.DoesNotExist:
#                 response = {"status": "nok", "body": "Record Does Not Exist"}
#             except Exception:
#                 response = {"status": "nok", "body": traceback.format_exc(sys.exc_info())}
#             finally:
#                 return Response(json.dumps(response, sort_keys=True),
#                                 mimetype='application/json')
#
#     def post(self):
#         response = {}
#         try:
#             data = json.loads(request.data)
#             date = datetime.datetime.now()
#             result = User_Credit.insert(
#                 credit_author_user_id=data['credit_author_user_id'],
#                 user_credit_amount=data.get('user_credit_amount', 0),
#                 user_credit_created_at=date.strftime("%Y-%m-%d %H:%M:%S"),
#                 user_credit_updated_at=date.strftime("%Y-%m-%d %H:%M:%S")
#             ).execute()
#             response = {"status": "ok", "body": result}
#         except Exception:
#             response = {"status": "nok", "body": traceback.format_exc(sys.exc_info())}
#         finally:
#             return Response(json.dumps(response, sort_keys=False),
#                             mimetype='application/json')
#
#     def delete(self, id):
#         pass
#
#     def put(self, id):
#         response = {}
#         try:
#             data = json.loads(request.data)
#             date = datetime.datetime.now()
#             user_credit = User_Credit.get(User_Credit.credit_author_user_id == id)
#             result = User_Credit.update(
#                 credit_updated_user_id=data['credit_updated_user_id'],
#                 user_credit_amount=data.get('user_credit_amount', user_credit.user_credit_amount),
#                 user_credit_updated_at=date.strftime("%Y-%m-%d %H:%M:%S")
#             ).where(User_Credit.credit_author_user_id == id).execute()
#             if result == 0:
#                 response = {"status": "nok", "body": "Record Does Not Exist"}
#             else:
#                 response = {"status": "ok", "body": result}
#         except Exception:
#             response = {"status": "nok", "body": traceback.format_exc(sys.exc_info())}
#         finally:
#             return Response(json.dumps(response, sort_keys=False),
#                             mimetype='application/json')


class CreditRequestRests(MethodView):
    def get(self, id):
        if id is None:
            response = []
            limit = int(100 if request.args.get('limit') is None else request.args.get('limit'))
            page = int(1 if request.args.get('page') is None else request.args.get('page'))
            order = str('DESC' if request.args.get('order') is None else request.args.get('order'))

            credit_request = []
            if request.args.get('user') is None:
                credit_request = Credit_Request.select().order_by(SQL("request_created_at " + order)).paginate(page, limit)

            elif request.args.get('user') is not None:
                credit_request = Credit_Request.select().where(
                    Credit_Request.request_author_user_id == request.args.get('user')).order_by(
                    SQL("request_created_at " + order)).paginate(page, limit)


            for query in credit_request:
                record = {
                    'request_id': query.id,
                    'request_author_user_id': query.request_author_user_id,
                    'request_updated_user_id': query.request_updated_user_id,
                    'request_amount': query.request_amount,
                    'request_amount_paid': query.request_amount_paid,
                    'request_status': query.request_status,
                    'request_description': query.request_description,
                    'request_created_at': str(query.request_created_at),
                    'request_updated_at': str(query.request_updated_at)
                }
                response.append(record)
            response = {"status": "ok", "body": response}
            return Response(json.dumps(response, sort_keys=True),
                            mimetype='application/json')
        else:
            response = {}
            try:
                credit_request = Credit_Request.get(Credit_Request.id == id)
                response = {
                    'request_id': credit_request.id,
                    'request_author_user_id': credit_request.request_author_user_id,
                    'request_updated_user_id': credit_request.request_updated_user_id,
                    'request_amount': credit_request.request_amount,
                    'request_amount_paid': credit_request.request_amount_paid,
                    'request_status': credit_request.request_status,
                    'request_description': credit_request.request_description,
                    'request_created_at': str(credit_request.request_created_at),
                    'request_updated_at': str(credit_request.request_updated_at)
                }
                response = {"status": "ok", "body": response}
            except Credit_Request.DoesNotExist:
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
            result = Credit_Request.insert(
                request_author_user_id=data['request_author_user_id'],
                request_amount=data.get('request_amount', None),
                request_status=data.get('request_status', 'requested'),
                request_created_at=date.strftime("%Y-%m-%d %H:%M:%S"),
                request_updated_at=date.strftime("%Y-%m-%d %H:%M:%S")
            ).execute()
            response = {"status": "ok", "body": result}
        except Exception:
            response = {"status": "nok", "body": traceback.format_exc(sys.exc_info())}
        finally:
            return Response(json.dumps(response, sort_keys=False),
                            mimetype='application/json')

    def delete(self, id):
        response = {}
        result = Credit_Request.delete().where(Credit_Request.id == id).execute()
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
            credit_request = Credit_Request.get(Credit_Request.id == id)
            result = Credit_Request.update(
                request_updated_user_id=data['request_updated_user_id'],
                request_amount=data.get('request_amount', credit_request.request_amount),
                request_amount_paid=data.get('request_amount_paid', credit_request.request_amount_paid),
                request_status=data.get('request_status', credit_request.request_status),
                request_description=data.get('request_description', credit_request.request_description),
                request_updated_at=date.strftime("%Y-%m-%d %H:%M:%S")
            ).where(Credit_Request.id == id).execute()
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
    financial.add_url_rule(url, defaults={pk: None},
                           view_func=view_func, methods=['GET', 'DELETE'])
    financial.add_url_rule(url, view_func=view_func, methods=['POST', ])
    financial.add_url_rule('%s/<%s:%s>' % (url, pk_type, pk),
                           view_func=view_func,
                           methods=['GET', 'PUT', 'DELETE'])


register_api(UserFinancialTransactionRests, 'UserFinancialTransactionRests', '/transaction', pk='id', pk_type="string")
# register_api(UserCreditRests, 'UserCreditRests', '/user/credit', pk='id')
register_api(CreditRequestRests, 'CreditRequestRests', '/user/credit/request', pk='id')


@financial.before_request
def _db_connect():
    if not db.is_closed():
        db.close()
    db.connect()


# This hook ensures that the connection is closed when we've finished
# processing the request.
@financial.teardown_request
def _db_close(exc):
    if not db.is_closed():
        db.close()
