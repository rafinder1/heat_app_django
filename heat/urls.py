from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_routes, name="routes"),
    path('materials', views.get_materials, name="materials"),
    path('type_layers', views.get_type_layers, name="type_layers"),
    path('calculate', views.calculate_param, name="calculate")
]
