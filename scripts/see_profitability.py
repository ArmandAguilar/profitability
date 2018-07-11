#!user/bin/python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from tokensSQL import *
from tokensNotification import *
from teamworkmessages import *
from teamworkproject import *
from teamworkusers import *
from tokensUserNotificationList import *
from emailnotification import *
import pypyodbc as pyodbc
import pymssql
import urllib2, base64
import simplejson as json
import unicodedata
import sys
reload(sys)

def get_listPersonal():
    Personal = ''
    Personal = '{"Person":['
    sql = 'SELECT [Id],[IdTemWork],[Email],[Acronimo],[Nombre] FROM [Northwind].[dbo].[Usuarios] Where [Departamento] <> \'Baja\''
    conn = pymssql.connect(host=hostMSSQL,user=userMSSQL,password=passMSSQL,database=dbMSSQLN)
    cur = conn.cursor()
    cur.execute(sql)
    for value in cur:
        Personal += '{"IdUser":' +  str(value[0])  + ',"IdUserTeamwork":' + str(value[1]) +   ',"Email":"' + str(unicode(value[2], errors='replace')) + '","Acronimo":"' + str(value[3]) + '","Nombre":"' + str(unicode(value[4], errors='replace')) + '"},'
    conn.commit()
    conn.close()
    temp = len(Personal)
    Personal = Personal[:temp - 1]
    Personal += ']}'
    data = json.loads(Personal)
    return data

def get_project_list():
    listP = projectIdTeamSap()
    IdTeamWorkProyecto = 0
    #Here created a Json con ID's in SAP and Teamwork
    Proyects = ''
    Proyects = '{"Proyect":['
    sql = 'SELECT CONVERT(varchar,[NumProyecto])As NumP ,[NomProyecto] AS NomP,CONVERT(varchar,[Trabajo programado]) As TP ,CONVERT(varchar,[Flujo Neto]) AS FN,CONVERT(varchar,[Mgn Act]) AS MA,[LP] FROM [SAP].[dbo].[RV-ESTADOPROYECTOS-AA] Where ( [Fecha Maduracion] >= \'2018-01-01\' and [LP] <> \'-\' and [EstadoCompra]=\'Activo\') and ([Flujo Neto]<0 or [Mgn Act] < 0 or [Trabajo programado] <= 0)'
    #conn = pymssql.connect(host=hostMSSQL,user=userMSSQL,password=passMSSQL,database=dbMSSQL)
    conn = pyodbc.connect(constr)
    cur = conn.cursor()
    cur.execute(sql)
    for value in cur:
        for valProject in listP['projecteam']:
            if str(value[0]) == str(valProject['NumProyecto']):
                IdTeamWorkProyecto = valProject['IdTemWork']
        Proyects += '{"NumProyecto":' +  str(value[0])  + ',"TrabajoProgramado":' + str(value[2]) + ',"FlujoNeto":' + str(value[3]) + ',"MgnAct":' + str(value[4]) + ',"LP":"' + str(value[5]) + '","IdTeamWork":' + str(IdTeamWorkProyecto) + '},\n'
        IdTeamWorkProyecto = 0
    conn.commit()
    conn.close()
    temp = len(Proyects)
    Proyects = Proyects[:temp - 2]
    Proyects += ']}'
    dataProjects = json.loads(Proyects)
    return dataProjects

#Here make a function for messages
def message_sendUser(lider,typeSend,typeMessage,valInt,NoProyecto,IdLpTeamWork,IdTeamWorkProjecto,Email):
    idlider = 0
    ListAdmins = str(UserEfren) + ',' + str(UserRV) + ',' + str(UserJV) + ',' + str(UserAngelica)
    message = ''
    if typeMessage == 'FlujoNeto':
        message += 'Hola  ' + str(lider) + '\n'
        message += 'Detectamos que el proyecto ' + str(NoProyecto) + ' que estás coordinando tiene '
        message += ' un flujo negativo (' + str(valInt) + ') \n'
        message += 'Por favor responde a este mensaje ccp el gerente del área, Efren y Angélica de administración, Jorge Vera de NN y Ricardo Villasana, el plan de acción que vas a seguir para corregir la situación.\n'
        message += 'Gracias y saludos.\n'
    elif typeMessage == 'MgnAct':
        message += 'Hola  ' + str(lider) + '\n'
        message += 'Detectamos que el proyecto ' + str(NoProyecto) + ' que estás coordinando tiene '
        message += ' una rentabilidad negativa (' + str(valInt) + ') \n'
        message += 'Por favor responde a este mensaje ccp el gerente del área, Efren y Angélica de administración, Jorge Vera de NN y Ricardo Villasana, el plan de acción que vas a seguir para corregir la situación.\n'
        message += 'Gracias y saludos.\n'
    elif typeMessage == 'TrabajoProgramado':
        message += 'Hola  ' + str(lider) + '\n'
        message += 'Detectamos que el proyecto ' + str(NoProyecto) + ' que estás coordinando no tiene días programados\n'
        message += 'Es necesario que revises la información del proyecto y corrijas los días programados entrando al siguiente link: 187.162.64.252:82/costoprogramado\n'
        message += 'Gracias y saludos.\n'
    if typeSend == 'Teamwork':
        idlider = status_user(IdLpTeamWork)
        if idlider == 0:
            #LP don't active and we need send message to administrative area
            message_error(str(NoProyecto))
        else:
            #Send Nogiciation
            title = 'Hola detectamos que el proyecto :' + str(NoProyecto) + ' tiene un problema'
            if typeMessage == 'FlujoNeto':
                IdTeamWorkUsersList = str(IdLpTeamWork)  + ',' + str(ListAdmins)
            elif typeMessage == 'MgnAct':
                IdTeamWorkUsersList = str(IdLpTeamWork) + ',' + str(ListAdmins)
            elif typeMessage == 'TrabajoProgramado':
                IdTeamWorkUsersList = IdLpTeamWork
            else:
                IdTeamWorkUsersList = UserTestA
            #IdTeamWorkUsersList = UserTestA
            send_private_messaje(title=title, IdTeamWorkUsers=IdTeamWorkUsersList, IdTeamWorkProject=IdTeamWorkProjecto,message=message,notify=IdTeamWorkUsersList)
    else:
       #Email
       title = 'Hola detectamos que el proyecto :' + str(NoProyecto) + ' tiene un problema'
       send_notification_email(title,'a.aguilar@fortaingenieria.com',message)
    #return message

def message_error(NoProjecto):
    message = ''
    message += 'Hola Efren\n'
    message += 'Detectamos que el proyecto ' + str(NoProjecto) + ' no tiene un lider de proyecto activo \n'
    title = 'El proyecto ' + str(NoProjecto) + ' no tiene un lider de proyecto activo'
    IdTeamWorkUsersList = str(UserTestA)  + ',' + str(UserEfren)
    send_private_messaje(title=title,IdTeamWorkUsers=IdTeamWorkUsersList,IdTeamWorkProject='418014',message=message,notify=IdTeamWorkUsersList)
    return message

def message_error_comunication(NoProjecto):
    message = ''
    message += 'Hola Efren\n'
    message += 'no puedo comunicarme con el lider de este proyecto ' + str(NoProjecto) + ' probablemente ya no este trabajando en FortaIngenieria o esten mal sus datos. \n'
    title = 'Problema de comunicación con el proyecto ' + str(NoProjecto)
    IdTeamWorkUsersList = str(UserTestA) + ',' + str(UserEfren)
    send_private_messaje(title=title,IdTeamWorkUsers=IdTeamWorkUsersList,IdTeamWorkProject='418014',message=message,notify=IdTeamWorkUsersList)
    return message

def rules(jsonProject,jsonUser):

    #here read all projects and apply us the rules
    #1 .-  FlujoNegativo < 0 (AD)
    #2 .-  Rentabilidad Negativa (AG)
    #3 .-  Tiempo Programado 0

    for datosP in jsonProject['Proyect']:

        # Here seek the data for each Leader
        user_data = get_user_data(datosP['LP'], jsonUser)

        # Here seek type of message that i need send
        if datosP['IdTeamWork'] > 0:
            typeMessege = 'Teamwork'
            #Here i verificate if exit IdUserTeamwork
            if user_data['leader'][0]['IdUserTeamWork'] == 0:
                typeMessege = 'Error'
        elif datosP['IdTeamWork'] == 0:
            typeMessege = 'Email'
            if user_data['leader'][0]['Email'] == 'empty':
                typeMessege = 'Error'

        if typeMessege == 'Error':
            msj = message_error_comunication(datosP['NumProyecto'])
        else:
            if datosP['FlujoNeto'] < 0:
                msj = message_sendUser(lider=user_data['leader'][0]['Nombre'], typeSend=typeMessege,typeMessage='FlujoNeto', valInt=datosP['FlujoNeto'],NoProyecto=datosP['NumProyecto'],IdLpTeamWork=user_data['leader'][0]['IdUserTeamWork'],IdTeamWorkProjecto=datosP['IdTeamWork'],Email=user_data['leader'][0]['Email'])
            if datosP['MgnAct'] <= 0:
                msj = message_sendUser(lider=user_data['leader'][0]['Nombre'], typeSend=typeMessege, typeMessage='MgnAct',valInt=datosP['MgnAct'],NoProyecto=datosP['NumProyecto'],IdLpTeamWork=user_data['leader'][0]['IdUserTeamWork'],IdTeamWorkProjecto=datosP['IdTeamWork'],Email=user_data['leader'][0]['Email'])
            if datosP['TrabajoProgramado'] <= 0:
                msj = message_sendUser(lider=user_data['leader'][0]['Nombre'], typeSend=typeMessege, typeMessage='TrabajoProgramado',valInt=datosP['TrabajoProgramado'],NoProyecto=datosP['NumProyecto'],IdLpTeamWork=user_data['leader'][0]['IdUserTeamWork'],IdTeamWorkProjecto=datosP['IdTeamWork'],Email=user_data['leader'][0]['Email'])
        #print (msj)

    return msj
################################################################################
##                                                                            ##
##                                 Test                                       ##
##                                                                            ##
################################################################################


print (rules(get_project_list(),get_listPersonal()))
#print (get_project_list())
#print (get_listPersonal())

