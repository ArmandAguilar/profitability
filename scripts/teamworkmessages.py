#!user/bin/python
# -*- coding: utf-8 -*-

#imports for jso and request
from tokensTeamWork import *
from urllib2 import urlopen,base64
import json
import requests
import unicodedata
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

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


def send_private_messaje(title,IdTeamWorkUsers,IdTeamWorkProject,message,notify):
    val = 0
    data = {'post': {}}
    data['post']['title'] = title
    data['post']['category-id'] = ''
    data['post']['notify'] = notify
    data['post']['body'] = message
    data['post']['private'] = '1'
    data['post']['attachments'] = ''
    data['post']['pendingFileAttachments'] = ''
    data['post']['tags'] = ''
    data['post']['grant-access-to'] = IdTeamWorkUsers
    dataJson = json.dumps(data)
    #r = requests.post(url + '/projects/418014/posts.json', auth=(key, ''), data=dataJson)
    r = requests.post(url + '/projects/'+ str(IdTeamWorkProject) + '/posts.json', auth=(keyBot, ''), data=dataJson)
    return dataJson



################################################################################
##                                                                            ##
##                                 Test                                       ##
##                                                                            ##
################################################################################

#txt = 'Es una prueba de privacidad'
#IdTeamWorkUsersList = '216004,270823'
#print (send_private_messaje(title='Test de Privacidad',IdTeamWorkUsers=IdTeamWorkUsersList,IdTeamWorkProject='418014',message=txt))

