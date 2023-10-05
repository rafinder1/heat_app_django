from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from heat.models import TypeLayer, Material, ThermalIsolation, Isolation, Wall, Plaster
from heat.calculator.temp_calculator import calculate, multi_variant_calculate
from heat.calculator.APAP_data import AmountPolystyreneData
from heat.calculator.amount_polystyrene_and_price import AmountPolystyreneAndPriceCalculator
import json
from django.core.serializers import serialize


# Create your views here.
@api_view(['GET'])
def get_routes(request):
    routes = [
        'api/materials',
        'api/type_layers',
        'api/thermal_isolation',
        'api/isolation',
        'api/wall',
        'api/plaster',

        # 'api/materials/filter',

    ]
    return Response(routes)


@api_view(['GET'])
def get_materials(*args, **kwargs):
    materials = Material.objects.all()
    materials_data = []

    for material in materials:
        material_data = {
            'id': material.id,
            'name_layer': material.name_layer,
            'type_layer': material.type_layer.type_layer
        }
        materials_data.append(material_data)

    return Response(materials_data)


@api_view(['GET'])
def filter_materials_by_type(request):
    selected_type = request.query_params.get('selected_type')

    type_layer_pk = TypeLayer.objects.values('pk').get(type_layer=selected_type)['pk']

    # Filter materials by the selected TypeLayer using the retrieved pk
    materials = Material.objects.filter(type_layer_id=type_layer_pk)

    materials_data = []
    for material in materials:
        material_data = {
            'id': material.id,
            'name_layer': material.name_layer,
            'type_layer': material.type_layer.type_layer
        }
        materials_data.append(material_data)

    return Response(materials_data)


@api_view(['GET'])
def filter_thickness_by_material(request):
    selected_material = request.query_params.get('selected_material')
    filtered_materials = Material.objects.get(name_layer=selected_material)

    type_layer = filtered_materials.type_layer
    if str(type_layer) == 'tynk':
        many_materials = filtered_materials.plaster_set.all()
    elif str(type_layer) == 'mur':
        many_materials = filtered_materials.wall_set.all()
    elif str(type_layer) == 'ocieplenie':
        many_materials = filtered_materials.thermalisolation_set.all()
    elif str(type_layer) == 'izolacja':
        many_materials = filtered_materials.isolation_set.all()

    materials_data = []
    for material in many_materials:
        material_data = {
            'thickness': material.thickness,
            'thermal_conductivity': material.thermal_conductivity,
            'cost': material.cost
        }
        materials_data.append(material_data)

    return Response(materials_data)


@api_view(['GET'])
def get_type_layers(*args, **kwargs):
    type_layers = TypeLayer.objects.all()
    type_layers_data = []

    for type_layer in type_layers:
        type_layer_data = {
            'id': type_layer.id,
            'type_layer': type_layer.type_layer
        }
        type_layers_data.append(type_layer_data)

    return Response(type_layers_data)


@api_view(['GET'])
def get_thermal_isolation(*args, **kwargs):
    thermal_isolations = ThermalIsolation.objects.all()
    thermal_isolations_data = []

    for ti in thermal_isolations:
        ti_data = {
            'id': ti.id,
            'name_layer': ti.name_layer.name_layer,
            'thickness': ti.thickness,
            'thermal_conductivity': ti.thermal_conductivity,
            'cost': ti.cost,
            'package_square_meters': ti.package_square_meters,
        }
        thermal_isolations_data.append(ti_data)

    return Response(thermal_isolations_data)


@api_view(['GET'])
def get_isolation(*args, **kwargs):
    isolations = Isolation.objects.all()
    isolations_data = []

    for isolation in isolations:
        i_data = {
            'id': isolation.id,
            'name_layer': isolation.name_layer.name_layer,
            'thickness': isolation.thickness,
            'thermal_conductivity': isolation.thermal_conductivity,
            'cost': isolation.cost,
        }
        isolations_data.append(i_data)

    return Response(isolations_data)


@api_view(['GET'])
def get_wall(*args, **kwargs):
    walls = Wall.objects.all()
    walls_data = []

    for wall in walls:
        w_data = {
            'id': wall.id,
            'name_layer': wall.name_layer.name_layer,
            'thickness': wall.thickness,
            'thermal_conductivity': wall.thermal_conductivity,
            'cost': wall.cost,
        }
        walls_data.append(w_data)

    return Response(walls_data)


@api_view(['GET'])
def get_plaster(*args, **kwargs):
    plasters = Plaster.objects.all()
    plasters_data = []

    for plaster in plasters:
        p_data = {
            'id': plaster.id,
            'name_layer': plaster.name_layer.name_layer,
            'thickness': plaster.thickness,
            'thermal_conductivity': plaster.thermal_conductivity,
            'cost': plaster.cost,
        }
        plasters_data.append(p_data)

    return Response(plasters_data)


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

        thermal_isolations_data = []

        for ti in thermal_isolation:
            ti_data = {
                'id': ti.id,
                'name_layer': ti.name_layer.name_layer,
                'thickness': ti.thickness,
                'thermal_conductivity': ti.thermal_conductivity,
                'cost': ti.cost,
                'package_square_meters': ti.package_square_meters,
            }
            thermal_isolations_data.append(ti_data)

        thermal_isolation_information = multi_variant_calculate(information_about_building, thermal_isolations_data)
        print(thermal_isolation_information)
        return Response(thermal_isolation_information)
    else:
        return Response({'error': 'Only POST requests are allowed for this endpoint.'}, status=400)


@api_view(['POST'])
def calculate_amount_polystyrene_and_price(request):
    information_about_polystyrene = request.data
    wall_surface = information_about_polystyrene['inputWallSurface']

    best_thermal_isolations = information_about_polystyrene['mvc']

    amount_and_price_thermal_isolations = []
    for ti in best_thermal_isolations:
        amount_polystyrene_data = AmountPolystyreneData(wall_surface=wall_surface,
                                                        price_square_meter=ti['cost'],
                                                        amount_package=ti['package_square_meters'])

        data = AmountPolystyreneAndPriceCalculator.calculate(amount_polystyrene_data=amount_polystyrene_data)
        data['name_layer'] = ti['name_layer']
        data['thickness'] = ti['thickness']

        amount_and_price_thermal_isolations.append(data)

    return Response(amount_and_price_thermal_isolations)
