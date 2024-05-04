from ..admin.models import *


class Publisher_Channel(Model):
    publisher_channel_author_user_id = IntegerField(null=True, default=None)
    publisher_channel_updated_user_id = IntegerField(null=True, default=None)
    publisher_channel_title = CharField()
    publisher_channel_admin_username = CharField()
    publisher_channel_url = CharField()
    publisher_channel_description = TextField(null=True, default=None)
    publisher_channel_picture = IntegerField(null=True, default=None)
    publisher_channel_geography = ForeignKeyField(Targeted_Geography, related_name='publisher_channel', null=True, default=None)
    publisher_channel_member_count = IntegerField(null=True, default=None)
    publisher_channel_grade = SmallIntegerField(null=True, default=None)
    publisher_channel_active_by_admin = BooleanField(null=True, default=None)
    publisher_channel_percentage = SmallIntegerField(null=True, default=None)
    publisher_channel_is_deleted = BooleanField(null=True, default=None)
    publisher_channel_created_at = DateTimeField()
    publisher_channel_updated_at = DateTimeField()

    class Meta:
        database = db


if not Publisher_Channel.table_exists():
    Publisher_Channel.create_table()



class Publisher_Channel_Ad_Type(Model):
    channel = ForeignKeyField(Publisher_Channel, related_name='types', on_delete='CASCADE')
    type = ForeignKeyField(Ad_Type, related_name='channels', on_delete='CASCADE')

    class Meta:
        database = db

if not Publisher_Channel_Ad_Type.table_exists():
    Publisher_Channel_Ad_Type.create_table()




class Publisher_Channel_Targeted_Subject(Model):
    channel = ForeignKeyField(Publisher_Channel, related_name='subjects', on_delete='CASCADE')
    subject = ForeignKeyField(Targeted_Subject, related_name='channels', on_delete='CASCADE')

    class Meta:
        database = db

if not Publisher_Channel_Targeted_Subject.table_exists():
    Publisher_Channel_Targeted_Subject.create_table()



class Publisher_Website(Model):
    publisher_website_author_user_id = IntegerField(null=True, default=None)
    publisher_website_updated_user_id = IntegerField(null=True, default=None)
    publisher_website_title = CharField()
    publisher_website_type = CharField(null=True, default=None)
    publisher_website_url = CharField()
    publisher_website_grade = CharField(null=True, default=None)
    publisher_website_active_by_admin = BooleanField(null=True, default=None)
    publisher_website_percentage = SmallIntegerField(null=True, default=None)
    publisher_website_native_style = TextField(null=True, default=None)
    publisher_website_is_deleted = BooleanField(null=True, default=None)
    publisher_website_created_at = DateTimeField()
    publisher_website_updated_at = DateTimeField()

    class Meta:
        database = db


if not Publisher_Website.table_exists():
    Publisher_Website.create_table()



class Publisher_Website_Targeted_Subject(Model):
    website = ForeignKeyField(Publisher_Website, related_name='subjects', on_delete='CASCADE')
    subject = ForeignKeyField(Targeted_Subject, related_name='publishers', on_delete='CASCADE')

    class Meta:
        database = db

if not Publisher_Website_Targeted_Subject.table_exists():
    Publisher_Website_Targeted_Subject.create_table()
