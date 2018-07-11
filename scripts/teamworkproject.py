#!user/bin/python
# -*- coding: utf-8 -*-

#imports for jso and request
from tokensTeamWork import *
from urllib2 import urlopen,base64
import json
import requests
import unicodedata


#{
#    "project": {
#        "company": {
#            "name": "Demo 1 Company",
#            "id": "999"
#        },
#        "starred": false,
#        "name": "demo",
#        "show-announcement": false,
#        "announcement": "",
#        "description": "A demo project",
#        "status": "active",
#        "created-on": "2014-03-28T15:24:22Z",
#        "category": {
#            "name": "",
#            "id": ""
#        },
#        "start-page": "projectoverview",
#        "logo": "http://demo1company.teamwork.com/images/logo.jpg",
#        "startDate": "",
#        "notifyeveryone": false,
#        "id": "999",
#        "last-changed-on": "2014-04-01T14:29:32Z",
#        "endDate": "",
#        "harvest-timers-enabled":"true"
#    },
#    "STATUS": "OK"
#}
# /projects/{project_id}.json
#active | archived
def projectStatus(idProjectTeamwork):
    status = 0
    r = requests.get(url + '/projects/' + str(idProjectTeamwork) + '.json', auth=(key, ''))
    data = json.loads(r.text, encoding='utf-8', cls=None, object_hook=None, parse_float=None, parse_int=None,
                      parse_constant=None, object_pairs_hook=None)
    print (data['project']['status'])
    return status

def projectIdTeamSap():
    # Here get a list with IdTeamWork
    req = requests.get(url + '/projects.json', auth=(key, ''))
    req.encoding = 'ISO-8859-1'
    dataProjects = json.loads(req.text, strict=False)
    ProjectsTemaWorks = '{"projecteam":['
    for valProjects in dataProjects['projects']:
        ProjectoArray = valProjects['name'].split(" ")
        ProjectsTemaWorks += '{"NumProyecto" : "' + str(ProjectoArray[0]) + '","IdTemWork" : "' + str(valProjects['id'] + '"},')
    temp = len(ProjectsTemaWorks)
    ProjectsTemaWorks = ProjectsTemaWorks[:temp - 1]
    ProjectsTemaWorks += ']}'
    dataProjects = json.loads(ProjectsTemaWorks)
    return dataProjects