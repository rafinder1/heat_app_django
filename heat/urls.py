from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_routes, name="routes"),
    path('materials', views.get_materials, name="materials"),
    path('type_layers', views.get_type_layers, name="type_layers"),
    path('thermal_isolation', views.get_thermal_isolation, name="thermal_isolation"),
    path('isolation', views.get_isolation, name="isolation"),
    path('wall', views.get_wall, name="wall"),
    path('plaster', views.get_plaster, name="plaster"),

    path('materials/filter', views.filter_materials_by_type, name='filter_materials_by_type'),
    path('thickness_material/filter', views.filter_thickness_by_material, name='filter_thickness_by_material'),
    path('calculate', views.calculate_param, name="calculate"),
    path('multi_variant_calc', views.multi_variant_calc, name="multi_variant_calc"),
    path('calculate_amount_polys_price', views.calculate_amount_polystyrene_and_price,
         name="calculate_amount_polystyrene_and_price")
]
