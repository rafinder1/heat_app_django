from django.contrib import admin
from .models import TypeLayer, Material, ThermalIsolation


@admin.register(TypeLayer)
class TypeLayerAdmin(admin.ModelAdmin):
    list_display = ('type_layer',)


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('name_layer', 'type_layer', 'thickness', 'thermal_conductivity', 'cost')
    list_filter = ('type_layer',)
    search_fields = ('name_layer',)


@admin.register(ThermalIsolation)
class ThermalIsolationAdmin(admin.ModelAdmin):
    list_display = ('name_layer', 'thickness', 'thermal_conductivity', 'cost', 'package_square_meters')
    list_filter = ('name_layer',)
    search_fields = ('name_layer',)
