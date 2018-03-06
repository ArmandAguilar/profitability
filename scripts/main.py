#!user/bin/python
# -*- coding: utf-8 -*-
import pandas as pd
#other lib and toke to use
from tokensSQL import *
from tokensNotification import *
import pypyodbc as pyodbc
import pymssql
import urllib2, base64
import simplejson as json
import unicodedata
import sys
from see_profitability import *
reload(sys)


################################################################################
##                                                                            ##
##                              Main                                          ##
##                                                                            ##
################################################################################
# Flujo negativos (AD)
# Rentabilidad Negativa AG
#Timpo Programado 0

print(get_listPersonal())
