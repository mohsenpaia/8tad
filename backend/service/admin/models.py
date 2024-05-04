from peewee import *
from playhouse.pool import PooledMySQLDatabase

# db = PooledMySQLDatabase(
#     'advertiser',
#     host='localhost',
#     port=3306,
#     max_connections=32,
#     stale_timeout=300,  # 5 minutes.
#     user='root',
#     password='A<~*8u7-')


db = PooledMySQLDatabase('advertiser', host='localhost', user='root',
                               passwd='A<~*8u7-', max_connections=100, stale_timeout=110)


# db = MySQLDatabase('advertiser', host='localhost', user='root',
#                    password='A<~*8u7-',
#                                threadlocals=True)


class Ad_Campaign_Type(Model):
    campaign_type_author_user_id = IntegerField()
    campaign_type_updated_user_id = IntegerField(null=True, default=None)
    campaign_type_name = CharField(null=True, default=None)
    campaign_type_title = CharField()
    campaign_type_base_price = SmallIntegerField(null=True, default=None)
    campaign_type_special_for = CharField()
    campaign_type_description = TextField(null=True, default=None)
    campaign_type_icon = CharField()
    campaign_type_created_at = DateTimeField()
    campaign_type_updated_at = DateTimeField()

    class Meta:
        database = db

if not Ad_Campaign_Type.table_exists():
    Ad_Campaign_Type.create_table()



class Ad_Package(Model):
    package_author_user_id = IntegerField()
    package_updated_user_id = IntegerField(null=True, default=None)
    package_title = CharField()
    package_price = IntegerField()
    package_discount = CharField(null=True, default=None)
    package_click_count = CharField()
    package_impression_count = CharField()
    package_description = TextField(null=True, default=None)
    package_created_at = DateTimeField()
    package_updated_at = DateTimeField()

    class Meta:
        database = db

if not Ad_Package.table_exists():
    Ad_Package.create_table()


class Ad_Banner_Size(Model):
    banner_size_author_user_id = IntegerField()
    banner_size_updated_user_id = IntegerField(null=True, default=None)
    banner_size_width = SmallIntegerField()
    banner_size_height = SmallIntegerField()
    banner_size_type = CharField()
    banner_size_created_at = DateTimeField()
    banner_size_updated_at = DateTimeField()

    class Meta:
        database = db

if not Ad_Banner_Size.table_exists():
    Ad_Banner_Size.create_table()


class Ad_Type(Model):
    type_author_user_id = IntegerField()
    type_updated_user_id = IntegerField(null=True, default=None)
    type_name = CharField()
    type_title = CharField()
    type_media = CharField()
    type_created_at = DateTimeField()
    type_updated_at = DateTimeField()

    class Meta:
        database = db

if not Ad_Type.table_exists():
    Ad_Type.create_table()


class Targeted_Operating_System(Model):
    os_author_user_id = IntegerField()
    os_updated_user_id = IntegerField(null=True, default=None)
    os_name = CharField()
    os_title = CharField()
    os_type = CharField()
    os_created_at = DateTimeField()
    os_updated_at = DateTimeField()

    class Meta:
        database = db

if not Targeted_Operating_System.table_exists():
    Targeted_Operating_System.create_table()


class Targeted_Subject(Model):
    subject_author_user_id = IntegerField()
    subject_updated_user_id = IntegerField(null=True, default=None)
    subject_name = CharField()
    subject_title = CharField()
    subject_type = CharField()
    subject_created_at = DateTimeField()
    subject_updated_at = DateTimeField()

    class Meta:
        database = db

if not Targeted_Subject.table_exists():
    Targeted_Subject.create_table()



class Targeted_Geography(Model):
    geography_author_user_id = IntegerField()
    geography_updated_user_id = IntegerField(null=True, default=None)
    geography_name = CharField()
    geography_title = CharField()
    geography_created_at = DateTimeField()
    geography_updated_at = DateTimeField()

    class Meta:
        database = db

if not Targeted_Geography.table_exists():
    Targeted_Geography.create_table()



class Targeted_Keyword(Model):
    keyword_author_user_id = IntegerField(null=True, default=None)
    keyword_updated_user_id = IntegerField(null=True, default=None)
    keyword_title = CharField()
    keyword_created_at = DateTimeField()
    keyword_updated_at = DateTimeField()

    class Meta:
        database = db

if not Targeted_Keyword.table_exists():
    Targeted_Keyword.create_table()


class Audit_Trail(Model):
    user_id = IntegerField()
    event_date = DateTimeField()
    table_name = CharField(50)
    record_id = CharField(20)
    field_name = CharField(50)
    new_value = CharField(5000)

    class Meta:
        database = db


if not Audit_Trail.table_exists():
    Audit_Trail.create_table()
