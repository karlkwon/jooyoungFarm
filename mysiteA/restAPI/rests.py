from django.contrib.auth.models import User, Group
from rest_framework import viewsets

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView

from .dbConfig import dbConfig

import mysql.connector
import pandas as pd
import pandas.io.sql as sql
import datetime
import json

# http://www.django-rest-framework.org/

config = dbConfig

@api_view(['GET'])
def getData(request):
    if request.method == 'GET':
        date_ = request.GET.get('date', '20151103')
        
        ret = list()

        print(date_)
        ret.append({"data":date_})

        return Response(ret)

def getRoomIdSub(cnx, type1, order = 'asc'):
        cursor = cnx.cursor()
        
        if type1 == None:
          query = ('select * from roomId order by type2 ' + order)
          cursor.execute(query)
        else:
          query = ('select * from roomId where type1 = %s order by type2 ' + order)
          cursor.execute(query, (type1, ))

        ret = list()

        for (roomId, type1, type2) in cursor:
            ret.append({'id':roomId, 'type1':type1, 'type2':type2})

        cursor.close()

        return ret

def getLastDate2(cnx, date = None):
        cursor = cnx.cursor()
        
        if date == None:
            query = ('select distinct(jadonsa.date) from jadonsa order by jadonsa.date desc')
            cursor.execute(query)
        else:
            query = ('select distinct(jadonsa.date) from jadonsa where jadonsa.date < %s order by jadonsa.date desc')
            cursor.execute(query, (date, ))

        ret = list()

        for d in cursor:
            ret.append(d[0])

        cursor.close()

        return ret

def getJadonsaData(cnx, date_ = None):
        cursor = cnx.cursor()

        query = ('select * from jadonsa where date = %s')
        cursor.execute(query, (date_, ))
        

        ret = list()

        for (roomId, date, junip, junchul, panmea, dopeasa, birth, currentCount, description) in cursor:
            ret.append({'roomId': roomId, 'date': date, 'junip': junip, 'junchul': junchul, \
			'panmea': panmea, 'dopeasa': dopeasa, 'birth': birth, 'currentCount': currentCount, 'description': description})

        cursor.close()

        return ret

################################################################################################3

@api_view(['GET'])
def getRoomId(request):
    if request.method == 'GET':
        type1 = request.GET.get('type1')

        cnx = mysql.connector.connect(**config)
        
        ret = list()

        ret1 = getRoomIdSub(cnx, r'이유')
        ret2 = getRoomIdSub(cnx, r'자돈1')
        ret3 = getRoomIdSub(cnx, r'자돈2')
        ret4 = getRoomIdSub(cnx, r'기타', 'desc')
        ret5 = getRoomIdSub(cnx, r'total')

        ret1 = ret1 + ret2
        ret3 = ret3 + ret4
        ret1 = ret1 + ret3
        ret1 = ret1 + ret5

        cnx.close()

        return Response(ret1)

@api_view(['GET'])
def getJadonsa(request):
    if request.method == 'GET':
        cnx = mysql.connector.connect(**config)

        date_ = request.GET.get('date', '20160209')
        dateLast_ = getLastDate2(cnx, date_)
#        date_ = datetime.datetime.strptime(date_, '%Y%m%d').date()
#        dateLast = datetime.datetime.strptime(dateLast_[0], '%Y%m%d').date()

        print("date_: " + date_)
        print(dateLast_[0])

        current = getJadonsaData(cnx, date_)
#        print(current);

        past = getJadonsaData(cnx, dateLast_[0])

        for d in current:
            for d2 in past:
                if d['roomId'] == d2['roomId']:
                    d['pastCount'] = d2['currentCount']
        
        cnx.close()

        return Response(current)

@api_view(['GET'])
def getJadonsaPandas(request):
    if request.method == 'GET':
        cnx = mysql.connector.connect(**config)
        date_ = request.GET.get('date', '20160209')
        date_ = datetime.datetime.strptime(date_, '%Y%m%d').date()

        query = "select * from jadonsa where date = %(ddd)s"
        df = sql.read_sql(query, cnx, params={"ddd":date_})

        df['date'] = pd.to_datetime(df['date'])

#        query = ('select * from jadonsa')
#        df = sql.read_sql(query, cnx)
        print(df)

        cnx.close()

        return Response(df.to_json(orient='index'))


@api_view(['POST'])
def setJadonsa(request):
    if request.method == 'POST':
        data = request.data #.get("data", 'empty')
        print(data);

        return Response(data)

