from ..admin.models import *


class Ticket_Category(Model):
    category_author_user_id = IntegerField()
    category_updated_user_id = IntegerField(null=True, default=None)
    category_name = CharField(null=True, default=None)
    category_title = CharField(null=True, default=None)
    category_created_at = DateTimeField()
    category_updated_at = DateTimeField()

    class Meta:
        database = db

if not Ticket_Category.table_exists():
    Ticket_Category.create_table()



class User_Ticket(Model):
    ticket_author_user_id = IntegerField()
    ticket_updated_user_id = IntegerField(null=True, default=None)
    ticket_category = ForeignKeyField(Ticket_Category, related_name='tickets', on_delete='CASCADE')
    ticket_priority = CharField(null=True, default=None)
    ticket_title = CharField(null=True, default=None)
    ticket_status = CharField(null=True, default=None)
    ticket_viewed_by_admin = BooleanField(null=True, default=None)
    ticket_viewed_by_user = BooleanField(null=True, default=None)
    ticket_created_at = DateTimeField()
    ticket_updated_at = DateTimeField()

    class Meta:
        database = db

if not User_Ticket.table_exists():
    User_Ticket.create_table()



class Ticket_Reply(Model):
    reply_author_user_id = IntegerField()
    reply_updated_user_id = IntegerField(null=True, default=None)
    ticket = ForeignKeyField(User_Ticket, related_name='replies', on_delete='CASCADE')
    reply_description = TextField(null=True, default=None)
    reply_created_at = DateTimeField()
    reply_updated_at = DateTimeField()

    class Meta:
        database = db

if not Ticket_Reply.table_exists():
    Ticket_Reply.create_table()



class Reply_Attachment(Model):
    attachment_author_user_id = IntegerField()
    attachment_updated_user_id = IntegerField(null=True, default=None)
    attachment_file = IntegerField(null=True, default=None)
    attachment_title = CharField(null=True, default=None)
    attachment_description = TextField(null=True, default=None)
    attachment_created_at = DateTimeField()
    attachment_updated_at = DateTimeField()

    class Meta:
        database = db

if not Reply_Attachment.table_exists():
    Reply_Attachment.create_table()



class Ticket_Reply_Reply_Attachment(Model):
    reply = ForeignKeyField(Ticket_Reply, related_name='attachments', on_delete='CASCADE')
    attachment = ForeignKeyField(Reply_Attachment, related_name='replies', on_delete='CASCADE')

    class Meta:
        database = db

if not Ticket_Reply_Reply_Attachment.table_exists():
    Ticket_Reply_Reply_Attachment.create_table()