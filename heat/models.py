from django.db import models


# Create your models here.
class TypeLayer(models.Model):
    type_layer = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.type_layer


class Material(models.Model):
    type_layer = models.ForeignKey(TypeLayer, on_delete=models.CASCADE)
    name_layer = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name_layer


class ThermalIsolation(models.Model):
    name_layer = models.ForeignKey(Material, on_delete=models.CASCADE, null=True, blank=True)
    thickness = models.FloatField()
    thermal_conductivity = models.FloatField()
    cost = models.FloatField()
    package_square_meters = models.FloatField()


class Wall(models.Model):
    name_layer = models.ForeignKey(Material, on_delete=models.CASCADE, null=True, blank=True)
    thickness = models.FloatField()
    thermal_conductivity = models.FloatField()
    cost = models.FloatField()


class Plaster(models.Model):
    name_layer = models.ForeignKey(Material, on_delete=models.CASCADE, null=True, blank=True)
    thickness = models.FloatField()
    thermal_conductivity = models.FloatField()
    cost = models.FloatField()


class Isolation(models.Model):
    name_layer = models.ForeignKey(Material, on_delete=models.CASCADE, null=True, blank=True)
    thickness = models.FloatField()
    thermal_conductivity = models.FloatField()
    cost = models.FloatField()
