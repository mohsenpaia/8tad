#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import threading
import subprocess
import requests,codecs
from flask import Flask, render_template, request, flash, json, redirect, url_for, g, session, Response, Request

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


result = requests.get("http://127.0.0.1:5555/advertiser/campaigns/itrc").content
result = json.loads(result)
result = result['body']

i = 0
file = codecs.open("/home/ubuntu/campaigns.txt", "w", "utf-8")
for value in result:
    data = {
        'from_date': "2017-01-01 00:00:00",
        'to_date': "2018-03-07 23:59:59",
        'campaign_id': value["campaign_id"]
    }

    result = requests.post("http://127.0.0.1:5555/reports/admin/one/campaign/ctr",
                           data=json.dumps(data)).content
    result = json.loads(result)
    campaign = result['body']

    if campaign:
        for key, value in campaign.items():
            print key
            file.write(key+ '\n')
            if key=='ad_show_campaign_author_user_id':
                result = requests.get("http://127.0.0.1/dashboard/one/admin/user/"+str(value)).content
                result = json.loads(result)
                user = result['body']
                print user["user_fullname"]
                file.write(user["user_fullname"]+ '\n')
            else:
                file.write(str(value)+ '\n')
                print value

        print "##############################################################"
        file.write("##############################################################"+ '\n')

file.close()



