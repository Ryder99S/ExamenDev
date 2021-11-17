from django.urls import path

from . import views

app_name = 'ExamenApp'

urlpatterns = [
 path('',views.inicio,name="inicio"),
 ]