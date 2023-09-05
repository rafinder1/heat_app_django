from django.db import models


# Create your models here.
class TypeLayer(models.Model):
    type_layer = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.type_layer


class Material(models.Model):
    type_layer = models.ForeignKey(TypeLayer, on_delete=models.CASCADE)
    name_layer = models.CharField(max_length=100)
    thickness = models.FloatField()
    thermal_conductivity = models.FloatField()
    cost = models.FloatField()

    def __str__(self):
        return self.name_layer


class Polystyrene(models.Model):
    name_polystyrene = models.CharField(max_length=100)
    thickness = models.FloatField()
    thermal_conductivity = models.FloatField()
    cost = models.FloatField()

    def __str__(self):
        return self.name_polystyrene
