from ..advertiser.models import *
from ..publisher.models import *


class Ad_Show_Counter(Model):
    ad_show_publisher = ForeignKeyField(Publisher_Website, related_name='counters')
    ad_show_campaign = ForeignKeyField(Ad_Campaign, related_name='counters')
    ad_show_banner_size = CharField(null=True, default=None)
    ad_show_date_hour = SmallIntegerField()
    ad_show_date_day = SmallIntegerField()
    ad_show_date_month = SmallIntegerField()
    ad_show_date_year = SmallIntegerField()
    ad_show_date = DateTimeField()
    ad_show_counter = IntegerField()
    class Meta:
        database = db


if not Ad_Show_Counter.table_exists():
    Ad_Show_Counter.create_table()




class Ad_Click_Counter(Model):
    ad_click_publisher = ForeignKeyField(Publisher_Website, related_name='click_counters')
    ad_click_campaign = ForeignKeyField(Ad_Campaign, related_name='click_counters')
    ad_click_banner_size = CharField(null=True, default=None)
    ad_click_date_hour = SmallIntegerField()
    ad_click_date_day = SmallIntegerField()
    ad_click_date_month = SmallIntegerField()
    ad_click_date_year = SmallIntegerField()
    ad_click_date = DateTimeField()
    ad_click_counter = IntegerField()
    class Meta:
        database = db


if not Ad_Click_Counter.table_exists():
    Ad_Click_Counter.create_table()