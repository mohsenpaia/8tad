from ..admin.models import *


class Library(Model):
    file_author_user_id = IntegerField()
    file_updated_user_id = IntegerField(null=True, default=None)
    file_name = CharField()
    file_path = CharField(null=True, default=None)
    file_title = CharField(null=True, default=None)
    file_description = TextField(null=True, default=None)
    file_created_at = DateTimeField()
    file_updated_at = DateTimeField()

    class Meta:
        database = db


if not Library.table_exists():
    Library.create_table()
