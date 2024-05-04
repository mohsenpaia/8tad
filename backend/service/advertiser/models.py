from ..admin.models import *


class Ad_Campaign(Model):
    campaign_author_user_id = IntegerField()
    campaign_updated_user_id = IntegerField(null=True, default=None)
    campaign_name = CharField(null=True, default=None)
    campaign_type = ForeignKeyField(Ad_Campaign_Type, related_name='campaigns')
    campaign_package = ForeignKeyField(Ad_Package, related_name='campaigns', null=True, default=None)
    campaign_total_budget_main = IntegerField(null=True, default=None)
    campaign_total_budget = IntegerField(null=True, default=None)
    campaign_daily_budget = IntegerField(null=True, default=None)
    campaign_budget_management = BooleanField(null=True, default=None)
    campaign_native_title = CharField(null=True, default=None)
    campaign_adwords_title = CharField(null=True, default=None)
    campaign_adwords_description = TextField(null=True, default=None)
    campaign_adwords_email = CharField(null=True, default=None)
    campaign_adwords_phone = CharField(null=True, default=None)
    campaign_adwords_address = CharField(null=True, default=None)
    campaign_landing_page_url = CharField(null=True, default=None)
    campaign_targeted_geography_all = BooleanField(null=True, default=None)
    campaign_targeted_geography_iran = BooleanField(null=True, default=None)
    campaign_targeted_geography_not_iran = BooleanField(null=True, default=None)
    campaign_targeted_geography_special = BooleanField(null=True, default=None)
    campaign_targeted_operating_system_all = BooleanField(null=True, default=None)
    campaign_targeted_operating_system_special = BooleanField(null=True, default=None)
    campaign_targeted_subject_all = BooleanField(null=True, default=None)
    campaign_targeted_subject_special = BooleanField(null=True, default=None)
    campaign_playtime_all = BooleanField(null=True, default=None)
    campaign_playtime_special = BooleanField(null=True, default=None)
    campaign_playtime_not_24_08 = BooleanField(null=True, default=None)
    campaign_playtime_not_08_16 = BooleanField(null=True, default=None)
    campaign_playtime_not_16_24 = BooleanField(null=True, default=None)
    campaign_network_class_a = BooleanField(null=True, default=None)
    campaign_network_class_b = BooleanField(null=True, default=None)
    campaign_network_class_c = BooleanField(null=True, default=None)
    campaign_retargeting = BooleanField(null=True, default=None)
    campaign_targeted_keyword_all = BooleanField(null=True, default=None)
    campaign_targeted_keyword_special = BooleanField(null=True, default=None)
    campaign_click_price = IntegerField(null=True, default=None)
    campaign_coef = SmallIntegerField(null=True, default=None)
    campaign_active_by_user = BooleanField(null=True, default=None)
    campaign_active_by_admin = BooleanField(null=True, default=None)
    campaign_default = BooleanField(null=True, default=None)
    campaign_is_deleted = BooleanField(null=True, default=None)
    campaign_created_at = DateTimeField()
    campaign_updated_at = DateTimeField()

    class Meta:
        database = db

if not Ad_Campaign.table_exists():
    Ad_Campaign.create_table()




class Ad_Banner(Model):
    banner_author_user_id = IntegerField()
    banner_updated_user_id = IntegerField(null=True, default=None)
    banner_size = ForeignKeyField(Ad_Banner_Size, related_name='banners')
    banner_file = IntegerField(null=True, default=None)
    banner_description = TextField(null=True, default=None)
    banner_created_at = DateTimeField()
    banner_updated_at = DateTimeField()

    class Meta:
        database = db

if not Ad_Banner.table_exists():
    Ad_Banner.create_table()



class Ad_Campaign_Ad_Banner(Model):
    campaign = ForeignKeyField(Ad_Campaign, related_name='banners', on_delete='CASCADE')
    banner = ForeignKeyField(Ad_Banner, related_name='campaigns', on_delete='CASCADE')

    class Meta:
        database = db

if not Ad_Campaign_Ad_Banner.table_exists():
    Ad_Campaign_Ad_Banner.create_table()



class Advertiser_Blocked_Website(Model):
    blocked_website_author_user_id = IntegerField(null=True, default=None)
    blocked_website_updated_user_id = IntegerField(null=True, default=None)
    blocked_website_url = CharField()
    blocked_website_created_at = DateTimeField()
    blocked_website_updated_at = DateTimeField()

    class Meta:
        database = db


if not Advertiser_Blocked_Website.table_exists():
    Advertiser_Blocked_Website.create_table()



class Ad_Campaign_Targeted_Operating_System(Model):
    campaign = ForeignKeyField(Ad_Campaign, related_name='osystems', on_delete='CASCADE')
    os = ForeignKeyField(Targeted_Operating_System, related_name='campaigns', on_delete='CASCADE')

    class Meta:
        database = db

if not Ad_Campaign_Targeted_Operating_System.table_exists():
    Ad_Campaign_Targeted_Operating_System.create_table()


class Ad_Campaign_Targeted_Subject(Model):
    campaign = ForeignKeyField(Ad_Campaign, related_name='subjects', on_delete='CASCADE')
    subject = ForeignKeyField(Targeted_Subject, related_name='campaigns', on_delete='CASCADE')

    class Meta:
        database = db

if not Ad_Campaign_Targeted_Subject.table_exists():
    Ad_Campaign_Targeted_Subject.create_table()



class Ad_Campaign_Targeted_Geography(Model):
    campaign = ForeignKeyField(Ad_Campaign, related_name='geographies', on_delete='CASCADE')
    geography = ForeignKeyField(Targeted_Geography, related_name='campaigns', on_delete='CASCADE')

    class Meta:
        database = db

if not Ad_Campaign_Targeted_Geography.table_exists():
    Ad_Campaign_Targeted_Geography.create_table()


class Ad_Campaign_Targeted_Keyword(Model):
    campaign = ForeignKeyField(Ad_Campaign, related_name='keywords', on_delete='CASCADE')
    keyword = ForeignKeyField(Targeted_Keyword, related_name='campaigns', on_delete='CASCADE')

    class Meta:
        database = db

if not Ad_Campaign_Targeted_Keyword.table_exists():
    Ad_Campaign_Targeted_Keyword.create_table()