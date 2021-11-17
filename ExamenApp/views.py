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

# class ApiTipo_producto(APIView):
#     ctx = {}

#     def get(self, request, format=None):
#         print(request.body)
#         if request.body:#Suponiendo que se enviara el id en el Json
#             Data = json.loads(request.body)
#             id_tp = Data['ID'] #Id del tipo de producto a filtrar
#             if Tipo_producto.objects.filter(pk=id_tp).exists():
#                 T_producto = list(Tipo_producto.objects.filter(pk=id_tp).values('pk','descripcion_producto'))
#             else:
#                 T_producto = list(Tipo_producto.objects.all().values('pk','descripcion_producto'))
#                 ctx = {'Id':'No Encontrado','T_producto':T_producto}
#                 return Response(ctx)
#         else:
#             T_producto = list(Tipo_producto.objects.all().values('pk','descripcion_producto'))



#         if T_producto:
#             ctx = {'T_producto':T_producto}
#             return Response(ctx)
#         else:
#             ctx = {'error','No hay Registros'}
#             return Response(ctx)
#     def post(self, request, format=None):
#         query_Tproducto,errores, ctx = {},{},{}
#         if  request.method == 'POST':

#             # print(request.body)
#             Data = json.loads(request.body)
#             D_producto = Data['descripcion_producto']


#             if Tipo_producto.objects.filter(descripcion_producto = D_producto).exists():
#                 ctx = {'Sussces','existe ya este tipo de producto'}

#             else:


#                 # descripcion_producto
#                 if type(D_producto) != str:
#                     errores['descripcion_producto'] = "La descripcion del producto no es un string"
#                 else:
#                     query_Tproducto['descripcion_producto'] = D_producto

#                 print(errores)

#                 if not errores:
#                     ctx = {'Sussces','Se almaceno con exito'}
#                     T_producto = Tipo_producto(**query_Tproducto)
#                     T_producto.save()
#                 else:
#                     ctx = {'error': errores}
#             return Response(ctx)
#     def put(self, request):
#         if  request.method == 'PUT':
#             Data = json.loads(request.body)
#             id_tp = Data['ID'] #Id del tipo de producto a filtrar
#             if Tipo_producto.objects.filter(pk=id_tp).exists():

#                 D_producto = Data['descripcion_producto']

#                 T_producto = Tipo_producto.objects.filter(pk=id_tp).update(
#                                                                                     descripcion_producto = D_producto,

#                                                                                     )
#                 ctx = {'Sussces','Datos modificados'}
#                 return Response(ctx)
#             else:
#                 ctx = {'Error','ID no existente'}
#                 return Response(ctx)
#     def delete(self, request):
#         if request.method == 'DELETE':
#             Data = json.loads(request.body)
#             id_tp = Data['ID']
#             if Tipo_producto.objects.filter(pk=id_tp).exists():
#                 eliminar = Tipo_producto.objects.filter(pk=id_tp).delete()
#                 ctx = {'Sussces','Registro Eliminado'}
#                 return Response(ctx)
#             else:
#                 ctx = {'Error','ID no existente'}
#                 return Response(ctx)
