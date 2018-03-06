#!user/bin/python
# -*- coding: utf-8 -*-
from tokensSQL import *
from tokensNotification import *
from teamworkmessages import *
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
    sql = 'SELECT [Id],[IdTemWork],[Email],[Acronimo] FROM [Northwind].[dbo].[Usuarios] Where [Departamento] <> \'Baja\''
    conn = pymssql.connect(host=hostMSSQL,user=userMSSQL,password=passMSSQL,database=dbMSSQLN)
    cur = conn.cursor()
    cur.execute(sql)
    for value in cur:
        Personal += '{"IdUser":' +  str(value[0])  + ',"IdUserTeamwork":' + str(value[1]) +   ',"Email":"' + str(value[2]) + '","Acronimo":"' + str(value[3]) + '"},'
    conn.commit()
    conn.close()
    temp = len(Personal)
    Personal = Personal[:temp - 1]
    Personal += ']}'
    data = json.loads(Personal)
    return data

def get_project_list():
    #
    constr = 'DRIVER={SQL Server};SERVER=INGENIERIA\MSSQLINGENIERIA;DATABASE=SAP;UID=Sistemas;PWD=masterMX9456'
    Proyects = ''
    Proyects = '{"Proyect":['
    sql = 'SELECT CONVERT(varchar,[NumProyecto])As NumP ,[NomProyecto] AS NomP,CONVERT(varchar,[Trabajo programado]) As TP ,CONVERT(varchar,[Flujo Neto]) AS FN,CONVERT(varchar,[Mgn Act]) AS MA,[LP] FROM [SAP].[dbo].[RV-ESTADOPROYECTOS-AA] Where ([LP] <> \'-\' and [EstadoCompra]=\'Activo\') and ([Flujo Neto]<0 or [Mgn Act] < 0 or [Trabajo programado] <= 0)'
    #conn = pymssql.connect(host=hostMSSQL,user=userMSSQL,password=passMSSQL,database=dbMSSQL)
    conn = pyodbc.connect(constr)
    cur = conn.cursor()
    cur.execute(sql)
    for value in cur:
        Proyects += '{"NumProyecto":' +  str(value[0])  + ',"TrabajoProgramado":' + str(value[2]) + ',"FlujoNeto":' + str(value[3]) + ',"MgnAct":' + str(value[4]) + ',"LP":"' + str(value[5]) + '"},'
    conn.commit()
    conn.close()
    temp = len(Proyects)
    Proyects = Proyects[:temp - 1]
    Proyects += ']}'
    dataProjects = json.loads(Proyects)
    return dataProjects

def get_user_id(txtAcronimo,listaBusqueda):
    idUser = 0
    for VData in listaBusqueda['Person']:
        if txtAcronimo == VData['Acronimo']:
            idUser = VData['IdUserTeamwork']
    return idUser

def rules(jsonProject,jsonUser):
    message = ''
    messageEmail = ''
    #here read all projects and apply us the rules
    #1 .-  FlujoNegativo < 0 (AD)
    #2 .-  Rentabilidad Negativa (AG)
    #3 .-  Tiempo Programado 0

    for datosP in jsonProject['Proyect']:
        iduser = get_user_id(datosP['LP'], jsonUser)
        if iduser == 0:
            iduser = 215992

        message += '--------------------------------------------------------------------------------------------\n'
        message +=  'El Proyecto: ' + str(datosP['NumProyecto']) + ' Lider de Projecto ' + str(datosP['LP']) + '\n'
        message += '--------------------------------------------------------------------------------------------\n'
        if datosP['FlujoNeto'] < 0:
            message += ' Presenta un flujo negativo (' + str(datosP['FlujoNeto']) + ') y necesita de tu atencion\n'

        if datosP['MgnAct'] <=  0:
            message += ' Cuenta con una rentabilidad (' + str(datosP['MgnAct']) + ') y necesita de tu atencion\n'

        if datosP['TrabajoProgramado'] <=  0:
            message += ' No cuenta con actividad porgramada (' + str(datosP['TrabajoProgramado']) + ') y necesita de tu atencion\n'
        message += '------------------------------------------------------------------------------------------\nNo es necesario responder este mensaje\n\n'
        messageEmail += message

        message = ''
    Title = 'Projectos con acividad peligrosa'
    send_private_messaje(Title,'215992','418014',messageEmail)
    return messageEmail
################################################################################
##                                                                            ##
##                                 Test                                       ##
##                                                                            ##
################################################################################


print (rules(get_project_list(),get_listPersonal()))


