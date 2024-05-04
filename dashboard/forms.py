#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import sys

reload(sys)
sys.setdefaultencoding('utf-8')
from flask_security.forms import *
from flask_wtf import FlaskForm as BaseForm
from wtforms import TextField, IntegerField, TextAreaField, SubmitField, RadioField, SelectField, SelectMultipleField, \
    widgets, BooleanField, HiddenField, PasswordField

from wtforms import validators



class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class ContactForm(BaseForm):
    name = TextField("نام", [validators.Required("Please enter your name.")], description="test1",
                     render_kw={"placeholder": "test2"})
    Gender = RadioField('جنسیت', choices=[('M', 'مرد'), ('F', 'زن')])
    Address = TextAreaField("آدرس")
    email = TextField("پست الکترونیک", [validators.Required("Please enter your email address."),
                                        validators.Email("Please enter your email address.")])
    Age = IntegerField("سن")
    language = SelectField('زبان', choices=[('cpp', 'C++'),
                                            ('py', 'Python')])
    # submit = SubmitField("Send")


class TargetedOperatingSystemForm(BaseForm):
    name = TextField("نام سیستم عامل", [validators.Required("Please enter name.")], description="",
                     render_kw={"placeholder": ""})
    title = TextField("عنوان سیستم عامل", [validators.Required("Please enter title.")], description="",
                      render_kw={"placeholder": ""})
    type = RadioField('نوع دستگاه', coerce=str, default='desktop',
                      choices=[('desktop', 'رومیزی'), ('mobile', 'موبایل')])


class TargetedSubjectForm(BaseForm):
    name = TextField("نام", [validators.Required("Please enter name.")], description="",
                     render_kw={"placeholder": ""})
    title = TextField("عنوان", [validators.Required("Please enter title.")], description="",
                      render_kw={"placeholder": ""})
    type = RadioField('نوع رسانه', coerce=str, default='desktop',
                      choices=[('web', 'وب'), ('telegram', 'تلگرام')])


class AdvertisingTypeForm(BaseForm):
    name = TextField("نام", [validators.Required("Please enter name.")], description="",
                     render_kw={"placeholder": ""})
    title = TextField("عنوان", [validators.Required("Please enter title.")], description="",
                      render_kw={"placeholder": ""})
    type = RadioField('نوع رسانه', coerce=str, default='desktop',
                      choices=[('web', 'وب'), ('telegram', 'تلگرام')])


class TargetedGeographyForm(BaseForm):
    name = TextField("نام منطقه", [validators.Required("Please enter name.")], description="",
                     render_kw={"placeholder": ""})
    title = TextField("عنوان منطقه", [validators.Required("Please enter title.")], description="",
                      render_kw={"placeholder": ""})


class TargetedKeywordForm(BaseForm):
    title = TextField("کلمه کلیدی", [validators.Required("Please enter title.")], description="",
                      render_kw={"placeholder": ""})


class BlockedWebsiteForm(BaseForm):
    url = TextField("آدرس وب سایت", [validators.Required("Please enter url.")], description="",
                    render_kw={"placeholder": "http://www.example.com/", "dir": "ltr"})


class PublisherWebsiteForm(BaseForm):
    title = TextField("عنوان وب سایت", [validators.Required("Please enter title.")], description="",
                      render_kw={"placeholder": ""})

    url = TextField("آدرس وب سایت", [validators.Required("Please enter url.")], description="",
                    render_kw={"placeholder": "http://www.example.com/", "dir": "ltr"})

    type = RadioField('نوع تبلیغات درخواستی', coerce=str, default='both',
                      choices=[('banner', 'بنری'), ('search_engine', 'موتور جستجو'), ('both', 'هر دو')])

    subjects = MultiCheckboxField('موضوع وب سایت', coerce=int, choices=[])



class PublisherChannelForm(BaseForm):
    title = TextField("نام کانال", [validators.Required("Please enter title.")], description="",
                      render_kw={"placeholder": ""})

    admin_username = TextField("آیدی سازنده - (ادمین)", [validators.Required("Please enter admin username.")], description="",
                      render_kw={"placeholder": "", "dir": "ltr"})

    url = TextField("آدرس کانال", [validators.Required("Please enter url.")], description="",
                    render_kw={"placeholder": "http://www.t.me/example", "dir": "ltr"})

    description = TextAreaField("توضیحات کانال", description="", render_kw={"placeholder": ""})

    picture = HiddenField("عکس پروفایل",
                        description="",
                        render_kw={"placeholder": "", "dir": "ltr"})

    geography = SelectField('استان', choices=[])
    subjects = MultiCheckboxField('موضوع کانال', coerce=int, choices=[])

    ad_type = MultiCheckboxField('نوع تبلیغات درخواستی', coerce=int, choices=[])



class PublisherChannelAdminForm(BaseForm):
    title = TextField("عنوان کانال", [validators.Required("Please enter title.")], description="",
                      render_kw={"placeholder": ""})

    url = TextField("آدرس کانال", [validators.Required("Please enter url.")], description="",
                    render_kw={"placeholder": "http://www.t.me/example", "dir": "ltr"})

    type = RadioField('نوع تبلیغات درخواستی', coerce=str, default='both',
                      choices=[('viewing', 'نمایشی'), ('bidding', 'پیشنهاد قیمت'), ('both', 'هر دو')])

    grade = RadioField('رتبه کانال', coerce=str, default='class_c',
                       choices=[('class_a', 'کلاس A'), ('class_b', 'کلاس B'), ('class_c', 'کلاس C')])

    percentage = TextField("درصد سود", [validators.Required("Please enter percentage.")],
                           description="(%)",
                           render_kw={"placeholder": "", "dir": "ltr"})

    subjects = MultiCheckboxField('موضوع کانال', coerce=int, choices=[])



class PublisherWebsiteAdminForm(BaseForm):
    title = TextField("عنوان وب سایت", [validators.Required("Please enter title.")], description="",
                      render_kw={"placeholder": ""})

    url = TextField("آدرس وب سایت", [validators.Required("Please enter url.")], description="",
                    render_kw={"placeholder": "http://www.example.com/", "dir": "ltr"})

    type = RadioField('نوع تبلیغات درخواستی', coerce=str, default='both',
                      choices=[('banner', 'بنری'), ('search_engine', 'موتور جستجو'), ('both', 'هر دو')])

    grade = RadioField('نوع سایت', coerce=str, default='class_c',
                       choices=[('class_a', 'کلاس A'), ('class_b', 'کلاس B'), ('class_c', 'کلاس C')])

    percentage = TextField("درصد سود", [validators.Required("Please enter percentage.")],
                           description="(%)",
                           render_kw={"placeholder": "", "dir": "ltr"})

    subjects = MultiCheckboxField('موضوع وب سایت', coerce=int, choices=[])

    native_style = TextAreaField("استایل همسان", description="",
                                 render_kw={"placeholder": ""})


class CampaignTypeForm(BaseForm):
    name = TextField("نام", [validators.Required("Please enter name.")], description="",
                     render_kw={"placeholder": "", "dir": "ltr"})
    title = TextField("عنوان", [validators.Required("Please enter title.")], description="",
                      render_kw={"placeholder": ""})
    base_price = TextField("قیمت پایه", [validators.Required("Please enter base price.")], description="(ریال)",
                       render_kw={"placeholder": "", "dir": "ltr"})
    special_for = TextField("مخصوص", [validators.Required("Please enter special for.")], description="",
                            render_kw={"placeholder": "برای مثال وب"})
    description = TextAreaField("توضیحات", [validators.Required("Please enter description.")], description="",
                                render_kw={"placeholder": ""})
    icon = TextField("آیکن", [validators.Required("Please enter icon.")], description="",
                     render_kw={"placeholder": "", "dir": "ltr"})


class PackageForm(BaseForm):
    title = TextField("عنوان", [validators.Required("Please enter title.")], description="",
                      render_kw={"placeholder": ""})
    price = TextField("قیمت", [validators.Required("Please enter price.")], description="",
                      render_kw={"placeholder": ""})
    discount = TextField("تخفیف", [validators.Required("Please enter discount.")], description="",
                         render_kw={"placeholder": ""})
    click_count = TextField("تعداد کلیک", [validators.Required("Please enter click count.")], description="",
                            render_kw={"placeholder": ""})
    impression_count = TextField("تعداد نمایش", [validators.Required("Please enter impression count.")], description="",
                                 render_kw={"placeholder": ""})
    description = TextAreaField("توضیحات", [validators.Required("Please enter description.")], description="",
                                render_kw={"placeholder": ""})


class BannerSizeForm(BaseForm):
    width = TextField("عرض بنر", [validators.Required("Please enter width.")], description="",
                      render_kw={"placeholder": "", "dir": "ltr"})
    height = TextField("طول بنر", [validators.Required("Please enter height.")], description="",
                       render_kw={"placeholder": "", "dir": "ltr"})
    type = RadioField('نوع دستگاه', coerce=str, default='desktop',
                      choices=[('desktop', 'رومیزی'), ('mobile', 'موبایل'), ('native', 'همسان')])


class CampaignForm(BaseForm):
    name = TextField("نام کمپین تبلیغاتی", [validators.Required("Please enter name.")], description="",
                     render_kw={"placeholder": ""})
    # total_budget = TextField("بودجه کل تبلیغات", [validators.Required("Please enter total budget.")],
    #                          description="(ریال)",
    #                          render_kw={"placeholder": "", "dir": "ltr"})
    daily_budget = TextField("بودجه روزانه تبلیغات", [validators.Required("Please enter daily budget.")],
                             description="(ریال)",
                             render_kw={"placeholder": "", "dir": "ltr"})
    click_price = TextField("قیمت کلیک",
                             description="(ریال)",
                             render_kw={"placeholder": "", "dir": "ltr"})

    budget_management = BooleanField("مدیریت بودجه توسط هسته تبلیغات",
                                     [validators.Required("Please enter budget management.")],
                                     description="",
                                     render_kw={"placeholder": ""})
    landing_page_url = TextField("آدرس سایت هدف", [validators.Required("Please enter landing page url.")],
                                 description="",
                                 render_kw={"placeholder": "", "dir": "ltr"})
    coef = TextField("ضریب کمپین", [validators.Required("Please enter coef.")],
                     description="(بین 1 تا 20)",
                     render_kw={"placeholder": "", "dir": "ltr", "data-v-max": "20", "data-v-min": "1"})


class CampaignNameForm(BaseForm):
    name = TextField("نام کمپین تبلیغاتی", [validators.Required("Please enter name.")], description="",
                     render_kw={"placeholder": ""})


class CampaignBudgetForm(BaseForm):
    total_budget = TextField("بودجه کل تبلیغات", [validators.Required("Please enter total budget.")],
                             description="(ریال)",
                             render_kw={"placeholder": "", "dir": "ltr"})
    daily_budget = TextField("بودجه روزانه تبلیغات", [validators.Required("Please enter daily budget.")],
                             description="(ریال)",
                             render_kw={"placeholder": "", "dir": "ltr"})


class CampaignLandingPageForm(BaseForm):
    landing_page_url = TextField("آدرس سایت هدف", [validators.Required("Please enter landing page url.")],
                                 description="",
                                 render_kw={"placeholder": "", "dir": "ltr"})


class TargetingForm(BaseForm):
    keyword = RadioField('هدفگذاری کلمات کلیدی', coerce=str, default='all',
                         choices=[('all', 'نمایش برای تمامی کلمات کلیدی'), ('special', 'انتخاب کلمات کلیدی')])
    keywords = SelectMultipleField('کلمات کلیدی', coerce=str, choices=[])

    geography = RadioField('هدفگذاری جغرافیایی', coerce=str, default='all',
                           choices=[('all', 'نمایش در تمامی نقاط'), ('iran', 'فقط در ایران'),
                                    ('not_iran', 'فقط خارج از ایران'), ('special', 'انتخاب استان ها')])

    states = MultiCheckboxField('استان یا استان های مورد نظر خود را انتخاب کنید.', coerce=int, choices=[])

    operating_system = RadioField('سیستم عامل', coerce=str, default='all',
                                  choices=[('all', 'نمایش در تمامی سیستم عامل‌ها'),
                                           ('special', 'انتخاب برخی از سیستم عامل‌ها')])

    operating_systems = MultiCheckboxField('سیستم عامل یا سیستم عامل های مورد نظر خود را انتخاب کنید.', coerce=int,
                                           choices=[])

    subject = RadioField('هدفگذاری موضوعی', coerce=str, default='all',
                         choices=[('all', 'نمایش در تمام موضوعات'), ('special', 'انتخاب موضوع')])

    subjects = MultiCheckboxField('موضوع یا موضوعات مورد نظر خود را انتخاب کنید.', coerce=int, choices=[])

    playtime = RadioField('زمان پخش', coerce=str, default='all',
                          choices=[('all', 'همه ساعات'), ('special', 'عدم پخش در برخی از ساعات')])
    playtime_special = MultiCheckboxField('بازه یا بازه های زمانی مورد نظر خود را انتخاب کنید.', coerce=str,
                                          choices=[('not_24_08', 'عدم پخش در ساعات 24 تا 8'),
                                                   ('not_08_16', 'عدم پخش در ساعات 8 تا 16'),
                                                   ('not_16_24', 'عدم پخش در ساعات 16 تا 24')])
    site_grade = RadioField('نوع سایت های پخش کننده', coerce=str, default='class_c',
                            choices=[('class_a', 'کلاس A'), ('class_b', 'کلاس B'), ('class_c', 'کلاس C')])

    retargeting = RadioField('هدفگیری مجدد', coerce=str, default='no',
                             choices=[('no', 'بدون هدفگیری مجدد'), ('yes', 'هدفگیری مجدد')])

    retargeting_code = TextAreaField("کد زیر را در تگ head وب سایت خود قرار دهید.",
                                     [validators.Required("Please enter description.")], description="",
                                     render_kw={"placeholder": "", "dir": "ltr", "rows": "4", "spellcheck": "false",
                                                "readonly": "true"})

    price = HiddenField("قیمت هر کلیک", [validators.Required("Please enter price.")],
                        description="",
                        render_kw={"placeholder": "", "dir": "ltr"})


class CampaignAdwordsDescriptionForm(BaseForm):
    title = TextField("عنوان", [validators.Required("Please enter title.")],
                      description="",
                      render_kw={"placeholder": ""})
    description = TextAreaField("توضیحات", [validators.Required("Please enter description.")], description="",
                                render_kw={"placeholder": ""})
    email = TextField("آدرس ایمیل", [validators.Required("Please enter email.")],
                      description="",
                      render_kw={"placeholder": "", "dir": "ltr"})
    phone = TextField("شماره تماس", [validators.Required("Please enter phone.")],
                      description="",
                      render_kw={"placeholder": "", "dir": "ltr"})
    address = TextField("آدرس", [validators.Required("Please enter address.")],
                        description="",
                        render_kw={"placeholder": ""})


class ExtendedSendConfirmationForm(SendConfirmationForm):
    email = TextField("آدرس ایمیل", [validators.Required("Please enter email.")],
                      description="",
                      render_kw={"placeholder": "Email Address", "dir": "ltr"})
    submit = SubmitField("ارسال", description="ارسال")


class ExtendedLoginForm(LoginForm):
    email = TextField("آدرس ایمیل", [validators.Required("Please enter email.")],
                      description="",
                      render_kw={"placeholder": "Email Address", "dir": "ltr"})
    password = PasswordField("کلمه عبور", [validators.Required("Please enter password.")],
                             description="",
                             render_kw={"placeholder": "Password", "dir": "ltr"})
    remember = BooleanField("مرا به خاطر بسپار")
    submit = SubmitField("ورود", description="ورود")


class ExtendedChangePasswordForm(ChangePasswordForm):
    password = PasswordField("کلمه عبور فعلی", validators=[password_required],
                      description="",
                      render_kw={"placeholder": "", "dir": "ltr"})
    new_password = PasswordField("کلمه عبور جدید", validators=[password_required, password_length],
                             description="",
                             render_kw={"placeholder": "", "dir": "ltr"})
    new_password_confirm = PasswordField("تکرار کلمه عبور جدید", validators=[EqualTo('new_password', message='RETYPE_PASSWORD_MISMATCH')],
                                 description="",
                                 render_kw={"placeholder": "", "dir": "ltr"})
    submit = SubmitField("ویرایش", description="ویرایش")



class ExtendedResetPasswordForm(ResetPasswordForm):
    password = PasswordField("کلمه عبور", validators=[password_required, password_length],
                             description="",
                             render_kw={"placeholder": "", "dir": "ltr"})
    password_confirm = PasswordField("تکرار کلمه عبور", validators=[EqualTo('password', message='RETYPE_PASSWORD_MISMATCH')],
                                 description="",
                                 render_kw={"placeholder": "", "dir": "ltr"})



class ExtendedRegisterForm(RegisterForm):
    email = TextField("آدرس ایمیل", validators=[email_required, email_validator, unique_user_email],
                      description="",
                      render_kw={"placeholder": "Email Address", "dir": "ltr"})
    password = PasswordField("کلمه عبور", validators=[password_required, password_length],
                             description="",
                             render_kw={"placeholder": "Password", "dir": "ltr"})
    password_confirm = PasswordField("تکرار کلمه عبور",
                                     validators=[EqualTo('password', message='RETYPE_PASSWORD_MISMATCH')],
                                     description="",
                                     render_kw={"placeholder": "RePassword", "dir": "ltr"})
    phone = TextField("شماره موبایل", [validators.Required("Please enter phone.")],
                      description="",
                      render_kw={"placeholder": "Mobile Number", "dir": "ltr"})
    fullname = TextField("نام و نام خانوادگی", [validators.Required("Please enter fullname.")],
                         description="",
                         render_kw={"placeholder": "FullName"})
    account_type = RadioField('نوع حساب', coerce=str, default='both',
                              choices=[('publisher', 'نمایش دهنده'), ('advertiser', 'آگهی دهنده'), ('both', 'هر دو')])
    submit = SubmitField("ثبت نام", description="ثبت نام")


class ExtendedForgotPasswordForm(ForgotPasswordForm):
    email = TextField("آدرس ایمیل", validators=[email_required, email_validator, valid_user_email],
                      description="",
                      render_kw={"placeholder": "Email Address", "dir": "ltr"})


class EditRegisterForm(BaseForm):
    # email = TextField("آدرس ایمیل", validators=[email_required, email_validator],
    #                   description="",
    #                   render_kw={"placeholder": "", "dir": "ltr"})
    phone = TextField("شماره موبایل", [validators.Required("Please enter phone.")],
                      description="",
                      render_kw={"placeholder": "", "dir": "ltr"})
    fullname = TextField("نام و نام خانوادگی", [validators.Required("Please enter fullname.")],
                         description="",
                         render_kw={"placeholder": ""})
    account_type = RadioField('نوع حساب', coerce=str, default='both',
                              choices=[('publisher', 'تبلیغ گیرنده'), ('advertiser', 'تبلیغ دهنده'), ('both', 'هر دو')])

    active = BooleanField("حساب کاربر فعال باشد")


class EditProfileForm(BaseForm):
    phone = TextField("شماره موبایل", [validators.Required("Please enter phone.")],
                      description="",
                      render_kw={"placeholder": "", "dir": "ltr"})
    fullname = TextField("نام و نام خانوادگی", [validators.Required("Please enter fullname.")],
                         description="",
                         render_kw={"placeholder": ""})
    account_type = RadioField('نوع حساب', coerce=str, default='both',
                              choices=[('publisher', 'تبلیغ گیرنده'), ('advertiser', 'تبلیغ دهنده'), ('both', 'هر دو')])


class EditProfileEmailForm(BaseForm):
    email = TextField("آدرس ایمیل", validators=[email_required, email_validator, unique_user_email],
                      description="",
                      render_kw={"placeholder": "", "dir": "ltr"})




class EditBankAccount(BaseForm):
    shaba_code = TextField("کد شبا", [validators.Required("Please enter shaba code.")],
                      description="",
                      render_kw={"placeholder": "", "dir": "ltr"})
    bank_name = TextField("نام بانک",
                         description="",
                         render_kw={"placeholder": ""})
    bank_account_number = TextField("شماره حساب",
                         description="",
                         render_kw={"placeholder": "", "dir": "ltr"})
    bank_card_number = TextField("شماره کارت",
                         description="",
                         render_kw={"placeholder": "", "dir": "ltr"})


class CreditForm(BaseForm):
    amount = TextField("میزان افزایش اعتبار", [validators.Required("Please enter credit.")],
                       description="(ریال)",
                       render_kw={"placeholder": "", "dir": "ltr"})
    # discount_code = TextField("کد تخفیف",
    #                           description="",
    #                           render_kw={"placeholder": "", "dir": "ltr"})


class CreditRequestForm(BaseForm):
    amount = TextField("مبلغ درخواستی", [validators.Required("Please enter credit.")],
                       description="(ریال)",
                       render_kw={"placeholder": "", "dir": "ltr"})


class CreditRequestAdminForm(BaseForm):
    amount = TextField("مبلغ درخواستی", [validators.Required("Please enter amount.")],
                       description="(ریال)",
                       render_kw={"placeholder": "", "dir": "ltr", "readonly": "true"})
    amount_paid = TextField("مبلغ واریز شده توسط بخش مالی",
                            description="(ریال)",
                            render_kw={"placeholder": "", "dir": "ltr"})
    status = SelectField('وضعیت درخواست', choices=[('requested', 'درخواست شده'), ('pending', 'در حال بررسی'),
                                                ('paid', 'پرداخت شده')])
    description = TextAreaField("توضیحات", description="",
                                render_kw={"placeholder": "", "rows": "2"})

class CreditAdminForm(BaseForm):
    amount = TextField("مبلغ", [validators.Required("Please enter credit.")],
                       description="(ریال)",
                       render_kw={"placeholder": "", "dir": "ltr"})

    amount_status = RadioField('واریز/برداشت', default='deposit', choices=[('deposit', 'واریز'), ('withdrawal', 'برداشت')])
    description = TextAreaField("توضیحات", [validators.Required("Please enter description.")], description="",
                                render_kw={"placeholder": ""})


class CampaignCreditForm(BaseForm):
    amount = TextField("مبلغ", [validators.Required("Please enter credit.")],
                       description="(ریال)",
                       render_kw={"placeholder": "", "dir": "ltr"})



class TicketCategoryForm(BaseForm):
    name = TextField("نام دسته", [validators.Required("Please enter name.")], description="",
                     render_kw={"placeholder": ""})
    title = TextField("عنوان دسته", [validators.Required("Please enter title.")], description="",
                      render_kw={"placeholder": ""})



class TicketForm(BaseForm):
    user = SelectField('کاربر', choices=[])
    category = SelectField('ارسال به بخش', choices=[])
    priority = SelectField('درجه اهمیت', choices=[('normal', 'عادی'),
                                            ('high', 'زیاد'), ('very_high', 'خیلی زیاد')])
    title = TextField("عنوان", [validators.Required("Please enter title.")], description="",
                      render_kw={"placeholder": ""})

    description = TextAreaField("متن تیکت", [validators.Required("Please enter description.")], description="",
                                render_kw={"placeholder": "", "rows": "7"})



class TicketAdminForm(BaseForm):
    status = SelectField('وضعیت تیکت', choices=[('open', 'در انتظار پاسخ'), ('pending', 'در حال بررسی'),
                                            ('respond', 'پاسخ داده شد'), ('close', 'بسته شده')])
    category = SelectField('ارسال به بخش', coerce=str, choices=[])
    priority = SelectField('درجه اهمیت', choices=[('normal', 'عادی'),
                                            ('high', 'زیاد'), ('very_high', 'خیلی زیاد')])
    title = TextField("عنوان", [validators.Required("Please enter title.")], description="",
                      render_kw={"placeholder": ""})



class TicketReplyForm(BaseForm):
    description = TextAreaField("پاسخ تیکت", [validators.Required("Please enter description.")], description="",
                                render_kw={"placeholder": "", "rows": "7"})