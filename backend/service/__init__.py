from flask import Flask

app = Flask(__name__)
#app.config.from_object('settings')

from uploads import uploads
from admin import admin
from advertiser import advertiser
from publisher import publisher
from financial import financial
from reports import reports
from ticketing import ticketing
from api import api


app.register_blueprint(uploads, url_prefix="/uploads")
app.register_blueprint(admin, url_prefix="/admin")
app.register_blueprint(advertiser, url_prefix="/advertiser")
app.register_blueprint(publisher, url_prefix="/publisher")
app.register_blueprint(financial, url_prefix="/financial")
app.register_blueprint(reports, url_prefix="/reports")
app.register_blueprint(ticketing, url_prefix="/ticketing")
app.register_blueprint(api, url_prefix="/api")
