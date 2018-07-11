#!user/bin/python
# -*- coding: utf-8 -*-

#imports for jso and request
from tokensTeamWork import *
from urllib2 import urlopen,base64
import json
import requests
import unicodedata

def get_user_id(txtAcronimo,listaBusqueda):
    idUser = 0
    for VData in listaBusqueda['Person']:
        if txtAcronimo == VData['Acronimo']:
            idUser = VData['IdUserTeamwork']
    return idUser

def get_user_data(txtAcronimo,listaBusqueda):
    registers = 0
    leader_data_json = '{"leader":['
    for VData in listaBusqueda['Person']:
        if  txtAcronimo == VData['Acronimo']:
            leader_data_json += '{"IdUserTeamWork":' + str(VData['IdUserTeamwork']) + ',"Email":"' + str(VData['Email']) + '","Nombre":"' + str(VData['Nombre']) + '"}'
            registers = 1
    if registers == 0:
        leader_data_json += '{"IdUserTeamWork":0,"Email":"empty","Nombre":"empty"}'
    leader_data_json += ']}'
    dataLeader = json.loads(leader_data_json)
    return dataLeader

def status_user(IdTemworUser):
    IdUserActive = 0
    req = requests.get(url + '/people/' + str(IdTemworUser) + '.json', auth=(key, ''))
    req.encoding = 'ISO-8859-1'
    dataPeople = json.loads(req.text, strict=False)
    if dataPeople['STATUS'] == 'Error':
        IdUserActive = 0
    elif dataPeople['STATUS'] == 'OK':
        IdUserActive = 1
    return IdUserActive

