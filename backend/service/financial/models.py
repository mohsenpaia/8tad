from ..publisher.models import *


class User_Financial_Transaction(Model):
    transaction_author_user_id = IntegerField(null=True, default=None)
    transaction_updated_user_id = IntegerField(null=True, default=None)
    transaction_description = TextField(null=True, default=None)
    transaction_deposit_amount = IntegerField(null=True, default=None)
    transaction_withdrawal_amount = IntegerField(null=True, default=None)
    transaction_first_status = SmallIntegerField(null=True, default=None)
    transaction_authority = CharField(null=True, default=None)
    transaction_second_status = SmallIntegerField(null=True, default=None)
    transaction_reference_id = CharField(null=True, default=None)
    transaction_status = BooleanField(null=True, default=None)
    transaction_created_at = DateTimeField()
    transaction_updated_at = DateTimeField()

    class Meta:
        database = db


if not User_Financial_Transaction.table_exists():
    User_Financial_Transaction.create_table()



# class User_Credit(Model):
#     credit_author_user_id = IntegerField(null=True, default=None)
#     credit_updated_user_id = IntegerField(null=True, default=None)
#     user_credit_amount = IntegerField(default=0)
#     user_credit_created_at = DateTimeField()
#     user_credit_updated_at = DateTimeField()
#
#     class Meta:
#         database = db
#
# if not User_Credit.table_exists():
#     User_Credit.create_table()


class Credit_Request(Model):
    request_author_user_id = IntegerField(null=True, default=None)
    request_updated_user_id = IntegerField(null=True, default=None)
    request_amount = IntegerField(null=True, default=None)
    request_amount_paid = IntegerField(null=True, default=None)
    request_status = CharField(null=True, default=None)
    request_description = TextField(null=True, default=None)
    request_created_at = DateTimeField()
    request_updated_at = DateTimeField()

    class Meta:
        database = db

if not Credit_Request.table_exists():
    Credit_Request.create_table()


# class Website_Credit_Calculation(Model):
#     website = ForeignKeyField(Publisher_Website, related_name='credits', on_delete='CASCADE')
#     website_percentage = SmallIntegerField(null=True, default=None)
#     website_credit_amount = IntegerField(null=True, default=None)
#     website_credit_calculation_created_at = DateTimeField()
#     website_credit_calculation_updated_at = DateTimeField()
#     class Meta:
#         database = db
#
# if not Website_Credit_Calculation.table_exists():
#     Website_Credit_Calculation.create_table()
