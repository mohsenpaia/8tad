from peewee import *
from flask_security import UserMixin, RoleMixin
from playhouse.pool import PooledMySQLDatabase

# db = PooledMySQLDatabase(
#     'security',
#     host='localhost',
#     port=3306,
#     max_connections=32,
#     stale_timeout=300,  # 5 minutes.
#     user='root',
#     password='A<~*8u7-')


db = PooledMySQLDatabase('security', host='localhost', user='root',
                               passwd='A<~*8u7-', max_connections=100, stale_timeout=110)

# db = MySQLDatabase('security', host='localhost', user='root',
#                    password='A<~*8u7-', threadlocals=True)


class Role(Model, RoleMixin):
    name = CharField(unique=True)
    description = TextField(null=True)

    class Meta:
        database = db


if not Role.table_exists():
    Role.create_table()


class User(Model, UserMixin):
    email = CharField(null=True, default=None)
    password = CharField(null=True, default=None)
    phone = CharField(null=True, default=None)
    fullname = CharField(null=True, default=None)
    account_type = CharField(null=True, default=None)
    telegram_unique_code = CharField(null=True, default=None)
    telegram_chat_id = CharField(null=True, default=None)
    active = BooleanField(default=True)
    confirmed_at = DateTimeField(null=True)
    last_login_at = DateTimeField(null=True)
    current_login_at = DateTimeField(null=True)
    last_login_ip = CharField(null=True, default=None)
    current_login_ip = CharField(null=True, default=None)
    login_count = IntegerField(null=True, default=0)

    class Meta:
        database = db


if not User.table_exists():
    User.create_table()


class UserRoles(Model):
    user = ForeignKeyField(User, related_name='roles', on_delete='CASCADE')
    role = ForeignKeyField(Role, related_name='users', on_delete='CASCADE')
    name = property(lambda self: self.role.name)
    description = property(lambda self: self.role.description)

    class Meta:
        database = db


if not UserRoles.table_exists():
    UserRoles.create_table()



class User_Bank_Account(Model):
    user = ForeignKeyField(User, related_name='accounts', on_delete='CASCADE')
    shaba_code = CharField(null=True, default=None)
    bank_name = CharField(null=True, default=None)
    bank_account_number = CharField(null=True, default=None)
    bank_card_number = CharField(null=True, default=None)
    bank_account_created_at = DateTimeField()
    bank_account_updated_at = DateTimeField()

    class Meta:
        database = db


if not User_Bank_Account.table_exists():
    User_Bank_Account.create_table()
