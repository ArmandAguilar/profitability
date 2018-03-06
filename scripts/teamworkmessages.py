#!user/bin/python
# -*- coding: utf-8 -*-

#imports for jso and request
from tokensTeamWork import *
from urllib2 import urlopen,base64
import json
import requests
import unicodedata

#{
#  "post": {
#    "title": "Yet another task for tomorrow",
#    "category-id": "",
#    "notify": [""],
#    "private": "0",
#    "body": "Yet another message content goes here",
#    "attachments": "",
#    "pendingFileAttachments": "",
#    "tags": "tag1,tag2,tag3"
#  }
#}
#POST /projects/{project_id}/posts.json


def send_private_messaje(title,IdTeamWorkUsers,IdTeamWorkProject,message):
    val = 0
    data = {'post': {}}
    data['post']['title'] = title
    data['post']['category-id'] = ''
    data['post']['notify'] = ['1']
    data['post']['body'] = message
    data['post']['private'] = '1'
    data['post']['attachments'] = ''
    data['post']['pendingFileAttachments'] = ''
    data['post']['tags'] = ''
    data['post']['grant-access-to'] = IdTeamWorkUsers
    #data['post']['grant-access-to'] = '215992'
    dataJson = json.dumps(data)
    #r = requests.post(url + '/projects/418014/posts.json', auth=(key, ''), data=dataJson)
    r = requests.post(url + '/projects/'+ str(IdTeamWorkProject) + '/posts.json', auth=(key, ''), data=dataJson)
    return val


################################################################################
##                                                                            ##
##                                 Test                                       ##
##                                                                            ##
################################################################################


#send_private_messaje('say hello')

