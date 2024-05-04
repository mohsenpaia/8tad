import datetime
import json
import sys
import traceback
from flask import request, Response
from flask.views import MethodView
from models import *
from . import ticketing
from ..uploads.views import files


@ticketing.route('/ticket/count', methods=['GET'])
def ticketing_ticket_count():
    if request.method == 'GET':
        result = User_Ticket.select().where(User_Ticket.ticket_status == 'open').count()
        response = {"status": "ok", "body": result}
        return Response(json.dumps(response, sort_keys=True),
                        mimetype='application/json')


class TicketCategoryRests(MethodView):
    def get(self, id):
        if id is None:
            response = []
            limit = int(20 if request.args.get('limit') is None else request.args.get('limit'))
            page = int(1 if request.args.get('page') is None else request.args.get('page'))
            order = str('DESC' if request.args.get('order') is None else request.args.get('order'))
            websites = []
            websites = Ticket_Category.select().order_by(SQL("category_created_at " + order)).paginate(
                page, limit)
            for query in websites:
                record = {
                    'category_id': query.id,
                    'category_author_user_id': query.category_author_user_id,
                    'category_updated_user_id': query.category_updated_user_id,
                    'category_name': query.category_name,
                    'category_title': query.category_title,
                    'category_created_at': str(query.category_created_at),
                    'category_updated_at': str(query.category_updated_at)
                }
                response.append(record)
            response = {"status": "ok", "body": response}
            return Response(json.dumps(response, sort_keys=True),
                            mimetype='application/json')
        else:
            response = {}
            try:
                category = Ticket_Category.get(Ticket_Category.id == id)
                response = {
                    'category_id': category.id,
                    'category_author_user_id': category.category_author_user_id,
                    'category_updated_user_id': category.category_updated_user_id,
                    'category_name': category.category_name,
                    'category_title': category.category_title,
                    'category_created_at': str(category.category_created_at),
                    'category_updated_at': str(category.category_updated_at)
                }
                response = {"status": "ok", "body": response}
            except Ticket_Category.DoesNotExist:
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
            result = Ticket_Category.insert(
                category_author_user_id=data['category_author_user_id'],
                category_updated_user_id=data.get('category_updated_user_id', None),
                category_name=data.get('category_name', None),
                category_title=data.get('category_title', None),
                category_created_at=date.strftime("%Y-%m-%d %H:%M:%S"),
                category_updated_at=date.strftime("%Y-%m-%d %H:%M:%S")
            ).execute()
            response = {"status": "ok", "body": result}
        except Exception:
            response = {"status": "nok", "body": traceback.format_exc(sys.exc_info())}
        finally:
            return Response(json.dumps(response, sort_keys=False),
                            mimetype='application/json')

    def delete(self, id):
        response = {}
        result = Ticket_Category.delete().where(Ticket_Category.id == id).execute()
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
            category = Ticket_Category.get(Ticket_Category.id == id)
            result = Ticket_Category.update(
                category_updated_user_id=data['category_updated_user_id'],
                category_name=data.get('category_name', category.category_name),
                category_title=data.get('category_title', category.category_title),
                category_updated_at=date.strftime("%Y-%m-%d %H:%M:%S")
            ).where(Ticket_Category.id == id).execute()

            if result == 0:
                response = {"status": "nok", "body": "Record Does Not Exist"}
            else:
                response = {"status": "ok", "body": result}
        except Exception:
            response = {"status": "nok", "body": traceback.format_exc(sys.exc_info())}
        finally:
            return Response(json.dumps(response, sort_keys=False),
                            mimetype='application/json')


class UserTicketRests(MethodView):
    def get(self, id):
        if id is None:
            response = []
            limit = int(20 if request.args.get('limit') is None else request.args.get('limit'))
            page = int(1 if request.args.get('page') is None else request.args.get('page'))
            order = str('DESC' if request.args.get('order') is None else request.args.get('order'))

            tickets = []
            if request.args.get('user') is None:
                tickets = User_Ticket.select().order_by(SQL("ticket_created_at " + order)).paginate(
                    page, limit)
            else:
                tickets = User_Ticket.select().where(
                    (User_Ticket.ticket_author_user_id == request.args.get('user'))).order_by(
                    SQL("ticket_created_at " + order)).paginate(
                    page, limit)

            for query in tickets:
                record = {
                    'ticket_id': query.id,
                    'ticket_author_user_id': query.ticket_author_user_id,
                    'ticket_updated_user_id': query.ticket_updated_user_id,
                    'ticket_category': {
                        'ticket_category_title': query.ticket_category.category_title,
                        'ticket_category_name': query.ticket_category.category_name,
                    },
                    'ticket_priority': query.ticket_priority,
                    'ticket_title': query.ticket_title,
                    'ticket_status': query.ticket_status,
                    'ticket_viewed_by_admin': query.ticket_viewed_by_admin,
                    'ticket_viewed_by_user': query.ticket_viewed_by_user,
                    'ticket_created_at': str(query.ticket_created_at),
                    'ticket_updated_at': str(query.ticket_updated_at)
                }
                response.append(record)
            response = {"status": "ok", "body": response}
            return Response(json.dumps(response, sort_keys=True),
                            mimetype='application/json')
        else:
            response = {}
            try:
                ticket = User_Ticket.get(User_Ticket.id == id)
                response = {
                    'ticket_id': ticket.id,
                    'ticket_author_user_id': ticket.ticket_author_user_id,
                    'ticket_updated_user_id': ticket.ticket_updated_user_id,
                    'ticket_category': {
                        'ticket_category_id': ticket.ticket_category.id,
                        'ticket_category_title': ticket.ticket_category.category_title,
                        'ticket_category_name': ticket.ticket_category.category_name
                    },
                    'ticket_priority': ticket.ticket_priority,
                    'ticket_title': ticket.ticket_title,
                    'ticket_status': ticket.ticket_status,
                    'ticket_viewed_by_admin': ticket.ticket_viewed_by_admin,
                    'ticket_viewed_by_user': ticket.ticket_viewed_by_user,
                    'ticket_created_at': str(ticket.ticket_created_at),
                    'ticket_updated_at': str(ticket.ticket_updated_at)
                }
                response = {"status": "ok", "body": response}
            except User_Ticket.DoesNotExist:
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
            result = User_Ticket.insert(
                ticket_author_user_id=data['ticket_author_user_id'],
                ticket_updated_user_id=data.get('ticket_updated_user_id', None),
                ticket_category=data.get('ticket_category', None),
                ticket_priority=data.get('ticket_priority', None),
                ticket_title=data.get('ticket_title', None),
                ticket_status='open',
                ticket_viewed_by_admin=False,
                ticket_viewed_by_user=True,
                ticket_created_at=date.strftime("%Y-%m-%d %H:%M:%S"),
                ticket_updated_at=date.strftime("%Y-%m-%d %H:%M:%S")
            ).execute()
            response = {"status": "ok", "body": result}
        except Exception:
            response = {"status": "nok", "body": traceback.format_exc(sys.exc_info())}
        finally:
            return Response(json.dumps(response, sort_keys=False),
                            mimetype='application/json')

    def delete(self, id):
        response = {}
        result = User_Ticket.delete().where(User_Ticket.id == id).execute()
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
            ticket = User_Ticket.get(User_Ticket.id == id)
            result = User_Ticket.update(
                ticket_updated_user_id=data['ticket_updated_user_id'],
                ticket_category=data.get('ticket_category', ticket.ticket_category),
                ticket_priority=data.get('ticket_priority', ticket.ticket_priority),
                ticket_title=data.get('ticket_title', ticket.ticket_title),
                ticket_status=data.get('ticket_status', ticket.ticket_status),
                ticket_viewed_by_admin=data.get('ticket_viewed_by_admin', ticket.ticket_viewed_by_admin),
                ticket_viewed_by_user=data.get('ticket_viewed_by_user', ticket.ticket_viewed_by_user),
                ticket_updated_at=(date.strftime("%Y-%m-%d %H:%M:%S") if data.get('ticket_updated_at') is None else ticket.ticket_updated_at)
            ).where(User_Ticket.id == id).execute()

            if result == 0:
                response = {"status": "nok", "body": "Record Does Not Exist"}
            else:
                response = {"status": "ok", "body": result}
        except Exception:
            response = {"status": "nok", "body": traceback.format_exc(sys.exc_info())}
        finally:
            return Response(json.dumps(response, sort_keys=False),
                            mimetype='application/json')


class TicketReplyRests(MethodView):
    def get(self, id):
        if id is None:
            response = {}
            ids = []
            ticket_id = request.args.get('ticket')
            replies = Ticket_Reply.select(Ticket_Reply, Ticket_Reply_Reply_Attachment).join(
                Ticket_Reply_Reply_Attachment, JOIN_LEFT_OUTER,
                on=(Ticket_Reply.id == Ticket_Reply_Reply_Attachment.reply)).where(
                Ticket_Reply.ticket == ticket_id)

            for query in replies:
                try:
                    file_id = query.ticket_reply_reply_attachment.attachment.attachment_file
                    ids.append(file_id)
                except Exception:
                    # no attachment
                    pass

            result = files(ids)
            result = json.loads(result)
            result = result['body']

            for query in replies:
                if query.id not in response:
                    response[query.id] = {
                        'reply_author_user_id': query.reply_author_user_id,
                        'reply_updated_user_id': query.reply_updated_user_id,
                        'reply_description': query.reply_description,
                        'reply_attachments': [],
                        'reply_created_at': str(query.reply_created_at),
                        'reply_updated_at': str(query.reply_updated_at)
                    }
                try:
                    file_id = query.ticket_reply_reply_attachment.attachment.attachment_file
                    attachment = {'file_path': result[str(file_id)]["file_path"],
                                  'file_name': result[str(file_id)]["file_name"]},
                    response[query.id]['reply_attachments'].append(attachment)
                except Exception:
                    # no attachment
                    pass

            response = {"status": "ok", "body": response}
            return Response(json.dumps(response, sort_keys=True),
                            mimetype='application/json')
        else:
            response = {}
            try:
                reply = Ticket_Reply.get(Ticket_Reply.id == id)
                response = {
                    'reply_id': reply.id,
                    'reply_author_user_id': reply.reply_author_user_id,
                    'reply_updated_user_id': reply.reply_updated_user_id,
                    'ticket': {
                        'ticket_id': reply.ticket.id,
                        'ticket_title': reply.ticket.ticket_title,
                    },
                    'reply_description': reply.reply_description,
                    'reply_created_at': str(reply.reply_created_at),
                    'reply_updated_at': str(reply.reply_updated_at)
                }
                response = {"status": "ok", "body": response}
            except Ticket_Reply.DoesNotExist:
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
            result = Ticket_Reply.insert(
                reply_author_user_id=data['reply_author_user_id'],
                reply_updated_user_id=data.get('reply_updated_user_id', None),
                ticket=data.get('ticket', None),
                reply_description=data.get('reply_description', None),
                reply_created_at=date.strftime("%Y-%m-%d %H:%M:%S"),
                reply_updated_at=date.strftime("%Y-%m-%d %H:%M:%S")
            ).execute()

            if data.get('reply_attachment', None) is not None:
                for attachment in data['reply_attachment']:
                    Ticket_Reply_Reply_Attachment.create(
                        reply=result,
                        attachment=int(attachment)
                    )

            response = {"status": "ok", "body": result}
        except Exception:
            response = {"status": "nok", "body": traceback.format_exc(sys.exc_info())}
        finally:
            return Response(json.dumps(response, sort_keys=False),
                            mimetype='application/json')

    def delete(self, id):
        response = {}
        result = Ticket_Reply.delete().where(Ticket_Reply.id == id).execute()
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
            ticket = Ticket_Reply.get(Ticket_Reply.id == id)
            result = Ticket_Reply.update(
                reply_updated_user_id=data['reply_updated_user_id'],
                ticket=data.get('ticket', ticket.ticket),
                reply_description=data.get('reply_description', ticket.reply_description),
                reply_updated_at=date.strftime("%Y-%m-%d %H:%M:%S")
            ).where(Ticket_Reply.id == id).execute()

            if result == 0:
                response = {"status": "nok", "body": "Record Does Not Exist"}
            else:
                response = {"status": "ok", "body": result}
        except Exception:
            response = {"status": "nok", "body": traceback.format_exc(sys.exc_info())}
        finally:
            return Response(json.dumps(response, sort_keys=False),
                            mimetype='application/json')


class ReplyAttachmentRests(MethodView):
    def get(self, id):
        if id is None:
            response = []
            limit = int(20 if request.args.get('limit') is None else request.args.get('limit'))
            page = int(1 if request.args.get('page') is None else request.args.get('page'))
            order = str('DESC' if request.args.get('order') is None else request.args.get('order'))
            attachments = []
            attachments = Reply_Attachment.select().order_by(SQL("attachment_created_at " + order)).paginate(
                page, limit)
            for query in attachments:
                record = {
                    'attachment_id': query.id,
                    'attachment_author_user_id': query.attachment_author_user_id,
                    'attachment_updated_user_id': query.attachment_updated_user_id,
                    'attachment_file': query.attachment_file,
                    'attachment_title': query.attachment_title,
                    'attachment_description': query.attachment_description,
                    'attachment_created_at': str(query.attachment_created_at),
                    'attachment_updated_at': str(query.attachment_updated_at)
                }
                response.append(record)
            response = {"status": "ok", "body": response}
            return Response(json.dumps(response, sort_keys=True),
                            mimetype='application/json')
        else:
            response = {}
            try:
                attachment = Reply_Attachment.get(Reply_Attachment.id == id)
                response = {
                    'attachment_id': attachment.id,
                    'attachment_author_user_id': attachment.attachment_author_user_id,
                    'attachment_updated_user_id': attachment.attachment_updated_user_id,
                    'attachment_file': attachment.attachment_file,
                    'attachment_title': attachment.attachment_title,
                    'attachment_description': attachment.attachment_description,
                    'attachment_created_at': str(attachment.attachment_created_at),
                    'attachment_updated_at': str(attachment.attachment_updated_at)
                }
                response = {"status": "ok", "body": response}
            except Reply_Attachment.DoesNotExist:
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
            result = Reply_Attachment.insert(
                attachment_author_user_id=data['attachment_author_user_id'],
                attachment_updated_user_id=data.get('attachment_updated_user_id', None),
                attachment_file=data.get('attachment_file', None),
                attachment_title=data.get('attachment_title', None),
                attachment_description=data.get('attachment_description', None),
                attachment_created_at=date.strftime("%Y-%m-%d %H:%M:%S"),
                attachment_updated_at=date.strftime("%Y-%m-%d %H:%M:%S")
            ).execute()
            response = {"status": "ok", "body": result}
        except Exception:
            response = {"status": "nok", "body": traceback.format_exc(sys.exc_info())}
        finally:
            return Response(json.dumps(response, sort_keys=False),
                            mimetype='application/json')

    def delete(self, id):
        response = {}
        result = Reply_Attachment.delete().where(Reply_Attachment.id == id).execute()
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
            ticket = Reply_Attachment.get(Reply_Attachment.id == id)
            result = Reply_Attachment.update(
                attachment_updated_user_id=data['attachment_updated_user_id'],
                attachment_file=data.get('attachment_file', ticket.attachment_file),
                attachment_title=data.get('attachment_title', ticket.attachment_title),
                attachment_description=data.get('attachment_description', ticket.attachment_description),
                attachment_updated_at=date.strftime("%Y-%m-%d %H:%M:%S")
            ).where(Reply_Attachment.id == id).execute()

            if result == 0:
                response = {"status": "nok", "body": "Record Does Not Exist"}
            else:
                response = {"status": "ok", "body": result}
        except Exception:
            response = {"status": "nok", "body": traceback.format_exc(sys.exc_info())}
        finally:
            return Response(json.dumps(response, sort_keys=False),
                            mimetype='application/json')


class TicketReplyReplyAttachmentRests(MethodView):
    def get(self, id):
        if id is None:
            response = []
            reply_id = request.args.get('reply')
            for query in Ticket_Reply_Reply_Attachment.select().where(
                            Ticket_Reply_Reply_Attachment.reply == reply_id):
                record = {
                    'ticket_reply_reply_attachment_id': query.id,
                    'reply': query.reply.id,
                    'attachment': {
                        'attachment_id': query.attachment.id,
                        'attachment_author_user_id': query.attachment.attachment_author_user_id,
                        'attachment_updated_user_id': query.attachment.attachment_updated_user_id,
                        'attachment_file': query.attachment.attachment_file,
                        'attachment_title': query.attachment.attachment_title,
                        'attachment_description': query.attachment.attachment_description,
                        'attachment_created_at': str(query.attachment.attachment_created_at),
                        'attachment_updated_at': str(query.attachment.attachment_updated_at)
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
            result = Ticket_Reply_Reply_Attachment.insert(
                reply=data.get('reply', None),
                attachment=data.get('attachment', None),
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
            reply_id = request.args.get('reply')
            result = Ticket_Reply_Reply_Attachment.delete().where(
                Ticket_Reply_Reply_Attachment.reply == reply_id).execute()
        else:
            result = Ticket_Reply_Reply_Attachment.delete().where(Ticket_Reply_Reply_Attachment.id == id).execute()
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
    ticketing.add_url_rule(url, defaults={pk: None},
                           view_func=view_func, methods=['GET', 'DELETE'])
    ticketing.add_url_rule(url, view_func=view_func, methods=['POST', ])
    ticketing.add_url_rule('%s/<%s:%s>' % (url, pk_type, pk),
                           view_func=view_func,
                           methods=['GET', 'PUT', 'DELETE'])


register_api(TicketCategoryRests, 'TicketCategoryRests', '/ticket/category', pk='id')
register_api(UserTicketRests, 'UserTicketRests', '/ticket', pk='id')
register_api(TicketReplyRests, 'TicketReplyRests', '/ticket/reply', pk='id')
register_api(ReplyAttachmentRests, 'ReplyAttachmentRests', '/ticket/attachment', pk='id')
register_api(TicketReplyReplyAttachmentRests, 'TicketReplyReplyAttachmentRests', '/ticket/reply/attachment', pk='id')


@ticketing.before_request
def _db_connect():
    if not db.is_closed():
        db.close()
    db.connect()


# This hook ensures that the connection is closed when we've finished
# processing the request.
@ticketing.teardown_request
def _db_close(exc):
    if not db.is_closed():
        db.close()
