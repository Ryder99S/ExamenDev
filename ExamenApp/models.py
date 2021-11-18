from django.db import models

# Create your models here.

class Sitios(models.Model):
    descripcion = models.CharField(max_length=80,null = False,blank=False)
    longitud = models.FloatField(null=False, blank=False)
    latitud = models.FloatField(null=False, blank=False)
    fotografia =  models.BinaryField(blank = False, null = False, editable = True)

    def __str__(self):
        return "{}-{}-{}-{}".format(self.pk,self.descripcion,self.longitud,self.latitud,self.fotografia)