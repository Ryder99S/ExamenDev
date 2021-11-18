from django.contrib import admin
from django.apps import apps
# Register your models here.

myapp = apps.get_app_config("ExamenApp")

for model_name, model in myapp.models.items():
	admin.site.register(model)