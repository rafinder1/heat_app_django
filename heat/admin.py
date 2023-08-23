from django.contrib import admin
from .models import TypeLayer, Material


@admin.register(TypeLayer)
class TypeLayerAdmin(admin.ModelAdmin):
    list_display = ('type_layer',)


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('name_layer', 'type_layer', 'thickness', 'thermal_conductivity', 'cost')
    list_filter = ('type_layer',)
    search_fields = ('name_layer',)
