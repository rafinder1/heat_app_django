from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_routes, name="routes"),
    path('materials', views.get_materials, name="materials"),
    path('materials/filter', views.filter_materials_by_type, name='filter_materials_by_type'),
    path('type_layers', views.get_type_layers, name="type_layers"),
    path('thermal_isolation', views.get_thermal_isolation, name="thermal_isolation"),
    path('calculate', views.calculate_param, name="calculate"),
    path('multi_variant_calc', views.multi_variant_calc, name="multi_variant_calc")
]
