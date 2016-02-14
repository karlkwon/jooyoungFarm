from django.contrib.auth.models import User, Group
from rest_framework import viewsets

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView

from .dbConfig import dbConfig

import mysql.connector
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

@api_view(['GET'])
def getRoomId(request):
    if request.method == 'GET':
        cnx = mysql.connector.connect(**config)
        
        cursor = cnx.cursor()
        
        query = ('select * from roomId')
        cursor.execute(query)

        ret = list()

        for (roomId, type1, type2) in cursor:
            ret.append({'id':roomId, 'type1':type1, 'type2':type2})

        cursor.close()
        cnx.close()

        return Response(ret)

@api_view(['GET'])
def getJadonsa(request):
    if request.method == 'GET':
        cnx = mysql.connector.connect(**config)
        date_ = request.GET.get('date', '20160209')
        date_ = datetime.datetime.strptime(date_, '%Y%m%d').date()

        cursor = cnx.cursor()
        
        query = ('select * from jadonsa where date = %s')
        cursor.execute(query, (date_, ))

        ret = list()

        for (roomId, date, junip, junchul, panmea, dopeasa, birth, currentCount, description) in cursor:
            ret.append({'roomId': roomId, 'date': date, 'junip': junip, 'junchul': junchul, \
			'panmea': panmea, 'dopeasa': dopeasa, 'birth': birth, 'currentCount': currentCount, 'description': description})

        cursor.close()
        cnx.close()

        return Response(ret)

@api_view(['GET'])
def getJadonsaPandas(request):
    if request.method == 'GET':
        cnx = mysql.connector.connect(**config)
        date_ = request.GET.get('date', '20160209')
        date_ = datetime.datetime.strptime(date_, '%Y%m%d').date()

        query = "select * from jadonsa where date = %(ddd)s"
        df = sql.read_sql(query, cnx, params={"ddd":date_})
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
