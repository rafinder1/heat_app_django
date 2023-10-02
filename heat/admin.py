from django.contrib import admin
from .models import TypeLayer, Material, ThermalIsolation, Wall, Plaster, Isolation


@admin.register(TypeLayer)
class TypeLayerAdmin(admin.ModelAdmin):
    list_display = ('type_layer',)


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('name_layer', 'type_layer')
    list_filter = ('type_layer',)
    search_fields = ('name_layer',)


@admin.register(ThermalIsolation)
class ThermalIsolationAdmin(admin.ModelAdmin):
    list_display = ('thickness', 'thermal_conductivity', 'cost', 'package_square_meters')


@admin.register(Wall)
class WallAdmin(admin.ModelAdmin):
    list_display = ('thickness', 'thermal_conductivity', 'cost')


@admin.register(Plaster)
class PlasterAdmin(admin.ModelAdmin):
    list_display = ('thickness', 'thermal_conductivity', 'cost')


@admin.register(Isolation)
class IsolationAdmin(admin.ModelAdmin):
    list_display = ('thickness', 'thermal_conductivity', 'cost')
