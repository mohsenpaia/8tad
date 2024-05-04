import json
import datetime
from flask import request, Response
from flask.views import MethodView
import traceback
import sys
from models import *


def users(ids):
    response = {}
    for query in User.select().where(User.id << ids):
        response[query.id] = {
            'email': query.email,
            'phone': query.phone,
            'fullname': query.fullname
        }
    response = {"status": "ok", "body": response}
    return json.dumps(response, sort_keys=True)


class UserRests(MethodView):
    def get(self, id=None, limit=None, page=None, order=None):
        if id is None:
            response = []
            mylimit = int(100 if limit is None else limit)
            mypage = int(1 if page is None else page)
            myorder = str('DESC' if page is order else order)
            for query in User.select(User, User_Bank_Account).join(User_Bank_Account, JOIN_LEFT_OUTER, on=(User.id == User_Bank_Account.user)).order_by(User.id.desc()).paginate(mypage, mylimit):
                record = {
                    'user_id': query.id,
                    'user_bank_account': {
                        'shaba_code': query.user_bank_account.shaba_code,
                        'bank_name': query.user_bank_account.bank_name,
                        'bank_account_number': query.user_bank_account.bank_account_number,
                        'bank_card_number': query.user_bank_account.bank_card_number,
                    },
                    'user_email': query.email,
                    'user_phone': query.phone,
                    'user_fullname': query.fullname,
                    'user_account_type': query.account_type,
                    'user_telegram_unique_code': query.telegram_unique_code,
                    'user_telegram_chat_id': query.telegram_chat_id,
                    'user_active': query.active,
                    'user_confirmed_at': str(query.confirmed_at),
                    'user_last_login_at': str(query.last_login_at),
                    'user_current_login_at': str(query.current_login_at),
                    'user_last_login_ip': query.last_login_ip,
                    'user_current_login_ip': query.current_login_ip,
                    'user_login_count': query.login_count
                }
                response.append(record)
            response = {"status": "ok", "body": response}
            return json.dumps(response, sort_keys=True)
        else:
            response = {}
            try:
                user = User.select(User, User_Bank_Account).join(User_Bank_Account, JOIN_LEFT_OUTER, on=(User.id == User_Bank_Account.user)).where(User.id == id).get()
                response = {
                    'user_id': user.id,
                    'user_bank_account': {
                        'shaba_code': user.user_bank_account.shaba_code,
                        'bank_name': user.user_bank_account.bank_name,
                        'bank_account_number': user.user_bank_account.bank_account_number,
                        'bank_card_number': user.user_bank_account.bank_card_number,
                    },
                    'user_email': user.email,
                    'user_phone': user.phone,
                    'user_fullname': user.fullname,
                    'user_account_type': user.account_type,
                    'user_telegram_unique_code': user.telegram_unique_code,
                    'user_telegram_chat_id': user.telegram_chat_id,
                    'user_active': user.active,
                    'user_confirmed_at': str(user.confirmed_at),
                    'user_last_login_at': str(user.last_login_at),
                    'user_current_login_at': str(user.current_login_at),
                    'user_last_login_ip': user.last_login_ip,
                    'user_current_login_ip': user.current_login_ip,
                    'user_login_count': user.login_count
                }
                response = {"status": "ok", "body": response}
            except User.DoesNotExist:
                response = {"status": "nok", "body": "Record Does Not Exist"}
            except Exception:
                response = {"status": "nok", "body": traceback.format_exc(sys.exc_info())}
            finally:
                return json.dumps(response, sort_keys=True)

    def post(self):
        pass

    def delete(self, id):
        pass

    def put(self, id, data):
        response = {}
        try:
            data = json.loads(data)
            user = User.get(User.id == id)
            result = User.update(
                email=data.get('user_email', user.email),
                phone=data.get('user_phone', user.phone),
                fullname=data.get('user_fullname', user.fullname),
                account_type=data.get('user_account_type', user.account_type),
                telegram_unique_code=data.get('user_telegram_unique_code', user.telegram_unique_code),
                telegram_chat_id=data.get('user_telegram_chat_id', user.telegram_chat_id),
                active=data.get('user_active', user.active)
            ).where(User.id == id).execute()

            if result == 0:
                response = {"status": "nok", "body": "Record Does Not Exist"}
            else:
                response = {"status": "ok", "body": result}
        except Exception:
            response = {"status": "nok", "body": traceback.format_exc(sys.exc_info())}
        finally:
            return json.dumps(response, sort_keys=False)


class RoleRests(MethodView):
    def get(self, id=None, limit=None, page=None, order=None):
        if id is None:
            response = []
            mylimit = int(20 if limit is None else limit)
            mypage = int(1 if page is None else page)
            myorder = str('DESC' if page is order else order)
            for query in Role.select().order_by(SQL("id " + myorder)).paginate(mypage, mylimit):
                record = {
                    'role_id': query.id,
                    'role_name': query.name,
                    'role_description': query.description
                }
                response.append(record)
            response = {"status": "ok", "body": response}
            return json.dumps(response, sort_keys=True)
        else:
            response = {}
            try:
                role = Role.get(Role.id == id)
                response = {
                    'role_id': role.id,
                    'role_name': role.name,
                    'role_description': role.description
                }
                response = {"status": "ok", "body": response}
            except Role.DoesNotExist:
                response = {"status": "nok", "body": "Record Does Not Exist"}
            except Exception:
                response = {"status": "nok", "body": traceback.format_exc(sys.exc_info())}
            finally:
                return json.dumps(response, sort_keys=True)

    def post(self):
        pass

    def delete(self, id):
        pass

    def put(self, id):
        pass


class UserRolesRests(MethodView):
    def get(self, id):
        if id is not None:
            response = []
            for query in UserRoles.select().where(
                            UserRoles.user == id):
                record = {
                    'user_roles_id': query.id,
                    'user': query.user.id,
                    'role': {
                        'role_id': query.role.id,
                        'role_name': query.role.name,
                        'role_description': query.role.description
                    }
                }
                response.append(record)
            response = {"status": "ok", "body": response}
            return json.dumps(response, sort_keys=True)
        else:
            pass

    def post(self, data):
        response = {}
        try:
            data = json.loads(data)
            result = UserRoles.delete().where(
                UserRoles.user == data["user"]).execute()
            for role in data["roles"]:
                result = UserRoles.insert(
                    role=role,
                    user=data["user"],
                ).execute()
            response = {"status": "ok", "body": result}
        except Exception:
            response = {"status": "nok", "body": traceback.format_exc(sys.exc_info())}
        finally:
            return json.dumps(response, sort_keys=False)

    def delete(self, id):
        response = {}
        if id is None:
            user_id = request.args.get('user')
            result = UserRoles.delete().where(
                UserRoles.user == user_id).execute()
        else:
            result = UserRoles.delete().where(UserRoles.id == id).execute()
        if result == 0:
            response = {"status": "nok", "body": "Record Does Not Exist"}
        else:
            response = {"status": "ok", "body": result}
        return json.dumps(response, sort_keys=False)

    def put(self, id):
        pass


class UserBankAccountRests(MethodView):
    def get(self, id):
        if id is None:
            response = []
            limit = int(20 if request.args.get('limit') is None else request.args.get('limit'))
            page = int(1 if request.args.get('page') is None else request.args.get('page'))
            order = str('DESC' if request.args.get('order') is None else request.args.get('order'))
            for query in User_Bank_Account.select().order_by(SQL("bank_account_created_at " + order)).paginate(page,
                                                                                                             limit):
                record = {
                    'bank_account_id': query.id,
                    'user_id': query.user.id,
                    'shaba_code': query.shaba_code,
                    'bank_name': query.bank_name,
                    'bank_account_number': query.bank_account_number,
                    'bank_card_number': query.bank_card_number,
                    'bank_account_created_at': str(query.bank_account_created_at),
                    'bank_account_updated_at': str(query.bank_account_updated_at)
                }
                response.append(record)
            response = {"status": "ok", "body": response}
            return json.dumps(response, sort_keys=True)
        else:
            response = {}
            try:
                bank_account = User_Bank_Account.get(User_Bank_Account.user == id)
                response = {
                    'bank_account_id': bank_account.id,
                    'user_id': bank_account.user.id,
                    'shaba_code': bank_account.shaba_code,
                    'bank_name': bank_account.bank_name,
                    'bank_account_number': bank_account.bank_account_number,
                    'bank_card_number': bank_account.bank_card_number,
                    'bank_account_created_at': str(bank_account.bank_account_created_at),
                    'bank_account_updated_at': str(bank_account.bank_account_updated_at)
                }
                response = {"status": "ok", "body": response}
            except User_Bank_Account.DoesNotExist:
                response = {"status": "nok", "body": "Record Does Not Exist"}
            except Exception:
                response = {"status": "nok", "body": traceback.format_exc(sys.exc_info())}
            finally:
                return json.dumps(response, sort_keys=True)

    def post(self, id, data):
        response = {}
        try:
            data = json.loads(data)
            date = datetime.datetime.now()
            result = User_Bank_Account.insert(
                user=id,
                shaba_code=data.get('shaba_code', None),
                bank_name=data.get('bank_name', None),
                bank_account_number=data.get('bank_account_number', None),
                bank_card_number=data.get('bank_card_number', None),
                bank_account_created_at=date.strftime("%Y-%m-%d %H:%M:%S"),
                bank_account_updated_at=date.strftime("%Y-%m-%d %H:%M:%S")
            ).execute()
            response = {"status": "ok", "body": result}
        except Exception:
            response = {"status": "nok", "body": traceback.format_exc(sys.exc_info())}
        finally:
            return json.dumps(response, sort_keys=False)

    def delete(self, id):
        response = {}
        result = User_Bank_Account.delete().where(User_Bank_Account.user == id).execute()
        if result == 0:
            response = {"status": "nok", "body": "Record Does Not Exist"}
        else:
            response = {"status": "ok", "body": result}
        return json.dumps(response, sort_keys=False)

    def put(self, id, data):
        response = {}
        try:
            data = json.loads(data)
            date = datetime.datetime.now()
            bank_account = User_Bank_Account.get(User_Bank_Account.user == id)
            result = User_Bank_Account.update(
                shaba_code=data.get('shaba_code', bank_account.shaba_code),
                bank_name=data.get('bank_name', bank_account.bank_name),
                bank_account_number=data.get('bank_account_number', bank_account.bank_account_number),
                bank_card_number=data.get('bank_card_number', bank_account.bank_card_number),
                bank_account_updated_at=date.strftime("%Y-%m-%d %H:%M:%S")
            ).where(User_Bank_Account.user == id).execute()
            if result == 0:
                response = {"status": "nok", "body": "Record Does Not Exist"}
            else:
                response = {"status": "ok", "body": result}
        except Exception:
            response = {"status": "nok", "body": traceback.format_exc(sys.exc_info())}
        finally:
            return json.dumps(response, sort_keys=False)
