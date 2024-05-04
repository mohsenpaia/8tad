import json
import datetime
from flask import request, Response
from flask.views import MethodView
import traceback
import sys
from models import *
from . import uploads


def files(ids):
    response = {}
    for query in Library.select().where(Library.id << ids):
        response[query.id] = {
            'file_author_user_id': query.file_author_user_id,
            'file_updated_user_id': query.file_updated_user_id,
            'file_name': query.file_name,
            'file_path': query.file_path,
            'file_title': query.file_title,
            'file_description': query.file_description,
            'file_created_at': str(query.file_created_at),
            'file_updated_at': str(query.file_updated_at)
        }
    response = {"status": "ok", "body": response}
    return json.dumps(response, sort_keys=True)


class LibraryRests(MethodView):
    def get(self, id):
        if id is None:
            response = []
            limit = int(20 if request.args.get('limit') is None else request.args.get('limit'))
            page = int(1 if request.args.get('page') is None else request.args.get('page'))
            order = str('DESC' if request.args.get('order') is None else request.args.get('order'))
            for query in Library.select().order_by(SQL("file_created_at " + order)).paginate(page, limit):
                record = {
                    'file_id': query.id,
                    'file_author_user_id': query.file_author_user_id,
                    'file_updated_user_id': query.file_updated_user_id,
                    'file_name': query.file_name,
                    'file_path': query.file_path,
                    'file_title': query.file_title,
                    'file_description': query.file_description,
                    'file_created_at': str(query.file_created_at),
                    'file_updated_at': str(query.file_updated_at)
                }
                response.append(record)
            response = {"status": "ok", "body": response}
            return Response(json.dumps(response, sort_keys=True),
                            mimetype='application/json')
        else:
            response = {}
            try:
                file = Library.get(Library.id == id)
                response = {
                    'file_id': file.id,
                    'file_author_user_id': file.file_author_user_id,
                    'file_updated_user_id': file.file_updated_user_id,
                    'file_name': file.file_name,
                    'file_path': file.file_path,
                    'file_title': file.file_title,
                    'file_description': file.file_description,
                    'file_created_at': str(file.file_created_at),
                    'file_updated_at': str(file.file_updated_at)
                }
                response = {"status": "ok", "body": response}
            except Library.DoesNotExist:
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
            result = Library.insert(
                file_author_user_id=data['file_author_user_id'],
                file_name=data['file_name'],
                file_path=data.get('file_path', None),
                file_title=data.get('file_title', None),
                file_description=data.get('file_description', None),
                file_created_at=date.strftime("%Y-%m-%d %H:%M:%S"),
                file_updated_at=date.strftime("%Y-%m-%d %H:%M:%S")
            ).execute()
            response = {"status": "ok", "body": result}
        except Exception:
            response = {"status": "nok", "body": traceback.format_exc(sys.exc_info())}
        finally:
            return Response(json.dumps(response, sort_keys=False),
                            mimetype='application/json')

    def delete(self, id):
        response = {}
        result = Library.delete().where(Library.id == id).execute()
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
            file = Library.get(Library.id == id)
            result = Library.update(
                file_updated_user_id=data['file_updated_user_id'],
                file_name=data.get('file_name', file.file_name),
                file_path=data.get('file_path', file.file_path),
                file_title=data.get('file_title', file.file_title),
                file_description=data.get('file_description', file.file_description),
                file_updated_at=date.strftime("%Y-%m-%d %H:%M:%S")
            ).where(Library.id == id).execute()
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
    uploads.add_url_rule(url, defaults={pk: None},
                         view_func=view_func, methods=['GET', ])
    uploads.add_url_rule(url, view_func=view_func, methods=['POST', ])
    uploads.add_url_rule('%s/<%s:%s>' % (url, pk_type, pk),
                         view_func=view_func,
                         methods=['GET', 'PUT', 'DELETE'])


register_api(LibraryRests, 'library_rests', '/library', pk='id')


@uploads.before_request
def _db_connect():
    if not db.is_closed():
        db.close()
    db.connect()


# This hook ensures that the connection is closed when we've finished
# processing the request.
@uploads.teardown_request
def _db_close(exc):
    if not db.is_closed():
        db.close()
