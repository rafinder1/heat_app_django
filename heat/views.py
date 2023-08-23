from django.shortcuts import render
from django.core import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from heat.models import Material, TypeLayer


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
    return Response({'materials': serializers.serialize('json', materials)})
