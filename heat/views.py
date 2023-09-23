from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from heat.models import Material, TypeLayer, ThermalIsolation
from heat.temp_calculator.temp_calculator import calculate, multi_variant_calculate
import json
from django.core.serializers import serialize


# Create your views here.
@api_view(['GET'])
def get_routes(request):
    routes = [
        'api/materials',
        'api/materials/filter',
        'api/type_layers',
        'api/thermal_isolation',
    ]
    return Response(routes)


@api_view(['GET'])
def get_materials(request):
    materials = Material.objects.all()
    materials = serialize("json", materials)
    materials = json.loads(materials)

    type_layers = TypeLayer.objects.all()
    type_layers_mapping = {layer.pk: layer.type_layer for layer in type_layers}

    for material in materials:
        material['fields']['type_layer'] = type_layers_mapping.get(material['fields']['type_layer'])

    return Response({'materials': materials})


@api_view(['GET'])
def filter_materials_by_type(request):
    selected_type = request.query_params.get('selected_type')

    type_layer_pk = TypeLayer.objects.values('pk').get(type_layer=selected_type)['pk']

    # Filter materials by the selected TypeLayer using the retrieved pk
    materials = Material.objects.filter(type_layer_id=type_layer_pk)

    materials = serialize("json", materials)
    materials = json.loads(materials)

    type_layers = TypeLayer.objects.all()
    type_layers_mapping = {layer.pk: layer.type_layer for layer in type_layers}

    for material in materials:
        material['fields']['type_layer'] = type_layers_mapping.get(material['fields']['type_layer'])

    return Response({'material': materials})


@api_view(['GET'])
def get_type_layers(request):
    type_layers = TypeLayer.objects.all()
    type_layers = serialize("json", type_layers)
    type_layers_json = json.loads(type_layers)

    return Response({'type_layers': type_layers_json})


@api_view(['GET'])
def get_thermal_isolation(request):
    thermal_isolation = ThermalIsolation.objects.all()
    thermal_isolation = serialize("json", thermal_isolation)
    thermal_isolation_json = json.loads(thermal_isolation)
    for item in thermal_isolation_json:
        item['fields']['type_layer'] = 'ocieplenie'

    return Response({'material': thermal_isolation_json})


@api_view(['POST'])
def calculate_param(request):
    if request.method == 'POST':

        information_about_building = request.data

        temperatures_and_thickness = calculate(information_about_building)

        return Response(temperatures_and_thickness)
    else:
        return Response({'error': 'Only POST requests are allowed for this endpoint.'}, status=400)


@api_view(['POST'])
def multi_variant_calc(request):
    if request.method == 'POST':

        information_about_building = request.data
        thermal_isolation = ThermalIsolation.objects.all()
        thermal_isolation = serialize("json", thermal_isolation)
        thermal_isolation_json = json.loads(thermal_isolation)

        thermal_isolation_information = multi_variant_calculate(information_about_building, thermal_isolation_json)
        return Response(thermal_isolation_information)
    else:
        return Response({'error': 'Only POST requests are allowed for this endpoint.'}, status=400)
