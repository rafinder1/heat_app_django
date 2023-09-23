from django.core.management.base import BaseCommand
from heat.models import ThermalIsolation
import csv


# run import data: python manage.py import_data

class Command(BaseCommand):
    help = 'Import data into the database'

    def handle(self, *args, **options):
        with open('./heat/management/data/data_polystyrene.csv', 'r', encoding='iso-8859-2') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                name_layer, thermal_conductivity, thickness, cost, package_square_meters = [
                    cell.encode('iso-8859-2').decode('utf-8') for cell in row]
                ThermalIsolation.objects.create(name_layer=name_layer, thickness=thickness,
                                                thermal_conductivity=thermal_conductivity, cost=cost,
                                                package_square_meters=package_square_meters)
