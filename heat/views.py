from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from heat.models import Material, TypeLayer
from heat.temp_calculator.temp_calculator import calculate
import json
from django.core.serializers import serialize


# Create your views here.
@api_view(['GET'])
def get_routes(request):
    routes = [
        'api/materials',
        'api/type_layers'
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


@api_view(['POST'])
def calculate_param(request):
    if request.method == 'POST':

        information_about_building = request.data

        temperatures_and_thickness = calculate(information_about_building)

        return Response(temperatures_and_thickness)
    else:
        return Response({'error': 'Only POST requests are allowed for this endpoint.'}, status=400)
