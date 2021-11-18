from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth import login as auth_login,logout,authenticate
from django.db import transaction,connections #manejo de base de datos
import json, re, os
from ExamenApp.models import *
from django.contrib.auth.decorators import login_required, permission_required
from django.core import serializers

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth.hashers import make_password
import requests
import json
import base64
import binascii

from rest_framework import serializers
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser

from django.core.mail import EmailMessage, send_mail
from ProyectoExamen.settings import EMAIL_HOST_USER
from django.db.models import Sum,Q

# Create your views here.

def inicio(request):
    return render(request,'inicio.html')

class ApiSitios(APIView):
    ctx = {}

    def get(self, request, format=None):
        print(request.body)
        lista = []
        if request.body:#Suponiendo que se enviara el id en el Json
            Data = json.loads(request.body)
            id_tp = Data['ID'] #Id del tipo de producto a filtrar
            if Sitios.objects.filter(pk=id_tp).exists():
                s = Sitios.objects.get(pk=id_tp)
                lista.append({'pk':s.pk, 'descripcion':s.descripcion, 'longitud':s.longitud, 'latitud':s.latitud, 'fotografia':bytes(s.fotografia)})
            else:
                for s in Sitios.objects.all().order_by('pk'):
                    lista.append({'pk':s.pk, 'descripcion':s.descripcion, 'longitud':s.longitud, 'latitud':s.latitud, 'fotografia':bytes(s.fotografia)})
                ctx = {'Id':'No Encontrado','sitio':lista}
                return Response(ctx)
        else:
            #sitio = list(Sitios.objects.all().values('pk','descripcion','longitud','latitud','fotografia'))
            for p in Sitios.objects.all().order_by('pk'):
                lista.append({'pk':p.pk, 'descripcion':p.descripcion, 'longitud':p.longitud, 'latitud':p.latitud, 'fotografia':bytes(p.fotografia)})
        if lista:
            ctx = {'sitio':lista}
            return Response(ctx)
        else:
            ctx = {'error','No hay Registros'}
            return Response(ctx)
    def post(self, request, format=None):
        query_sitios,errores, ctx = {},{},{}
        if  request.method == 'POST':

            # print(request.body)
            Data = json.loads(request.body)
            descripcion = Data["descripcion"]
            longitud = Data["longitud"]
            latitud = Data["latitud"]
            fotografia = Data["fotografia"]

            #fotografia2 = base64.b64encode(fotografia.encode('utf-8'))

            # descripcion_producto
            if type(descripcion) != str:
                errores['descripcion'] = "La descripcion no es un string"
            else:
                query_sitios['descripcion'] = descripcion
            
            # Longitud
            if type(longitud) != float:
                errores['longitud'] = "La Longitud no es un float"
            else:
                query_sitios['longitud'] = longitud

            # Latitud
            if type(latitud) != float:
                errores['latitud'] = "La Latitud no es un float"
            else:
                query_sitios['latitud'] = latitud

            if type(fotografia) != str:
                errores['fotografia'] = "La Fotografia no viene en Base64"
            else:
                query_sitios['fotografia'] = bytes(fotografia,'utf-8')

            print(errores)

            if not errores:
                ctx = {'Sussces','Se almaceno con exito'}
                guardado = Sitios(**query_sitios)
                guardado.save()
            else:
                ctx = {'error': errores}
        return Response(ctx)
    def put(self, request):
        if  request.method == 'PUT':
            Data = json.loads(request.body)
            id_tp = Data['ID'] #Id del tipo de producto a filtrar
            if Sitios.objects.filter(pk=id_tp).exists():

                descripcion = Data["descripcion"]
                longitud = Data["longitud"]
                latitud = Data["latitud"]
                fotografia = bytes(Data["fotografia"],'utf-8')

                editar = Sitios.objects.filter(pk=id_tp).update(
                                                                descripcion = descripcion,
                                                                longitud = longitud,
                                                                latitud = latitud,
                                                                fotografia = fotografia
                                                                                    )
                ctx = {'Sussces','Datos modificados'}
                return Response(ctx)
            else:
                ctx = {'Error','ID no existente'}
                return Response(ctx)
    def delete(self, request):
        if request.method == 'DELETE':
            Data = json.loads(request.body)
            id_tp = Data['ID']
            if Sitios.objects.filter(pk=id_tp).exists():
                eliminar = Sitios.objects.filter(pk=id_tp).delete()
                ctx = {'Sussces','Registro Eliminado'}
                return Response(ctx)
            else:
                ctx = {'Error','ID no existente'}
                return Response(ctx)
